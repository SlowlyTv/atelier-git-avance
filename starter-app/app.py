import os
import time

import redis
from flask import Flask, Response, g, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Nombre total de requetes HTTP",
    ["method", "endpoint", "status"],
)
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "Duree de traitement des requetes HTTP",
    ["method", "endpoint"],
)


@app.before_request
def start_request_timer():
    g.request_started_at = time.perf_counter()


@app.after_request
def record_request_metrics(response):
    if request.path == "/metrics":
        return response

    endpoint = request.url_rule.rule if request.url_rule else request.path
    HTTP_REQUESTS_TOTAL.labels(
        method=request.method, endpoint=endpoint, status=str(response.status_code)
    ).inc()
    started_at = getattr(g, "request_started_at", time.perf_counter())
    HTTP_REQUEST_DURATION_SECONDS.labels(
        method=request.method, endpoint=endpoint
    ).observe(time.perf_counter() - started_at)
    return response


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/simulate-error")
def simulate_error():
    return jsonify(error="simulated error"), 500


ALERT_THRESHOLD = 25


def alert_threshold():
    """Seuil d'alerte au-dessus duquel une notification est declenchee."""
    return ALERT_THRESHOLD


def sanitize_input(value):
    """Echappe les caracteres dangereux d'une entree utilisateur."""
    return value.replace("<", "&lt;").replace(">", "&gt;")


def get_redis_client():
    """Construit le client Redis a partir de la configuration du conteneur."""
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,
    )


@app.route("/")
def index():
    return """<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Atelier Git avance</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      max-width: 760px;
      margin: 64px auto;
      padding: 0 24px;
      background: #10162f;
      color: #f4f6ff;
    }
    main {
      background: #1a2347;
      padding: 32px;
      border-radius: 16px;
      box-shadow: 0 16px 50px #070b1c;
    }
    h1 { margin-top: 0; color: #91a7ff; }
    a { color: #8ce99a; }
    code { background: #0b1025; padding: 3px 7px; border-radius: 6px; }
  </style>
</head>
<body>
  <main>
    <h1>Atelier Git avance</h1>
    <p>L'application Flask fonctionne dans Docker avec Redis.</p>
    <ul>
      <li><a href="/health">Verifier la sante de Redis</a></li>
      <li><a href="/status">Afficher le statut</a></li>
      <li><a href="/visits">Tester le compteur de visites</a></li>
    </ul>
    <p>Service expose par le port <code>8080</code> du Codespace.</p>
  </main>
</body>
</html>"""


@app.route("/health")
def health():
    try:
        get_redis_client().ping()
    except redis.RedisError:
        return jsonify(status="error", dependency="redis"), 503
    return jsonify(status="ok", redis="ok"), 200


@app.route("/status")
def status():
    return jsonify(
        service="projet-devops-groupe-demo",
        version="1.0",
        deploy_color=os.getenv("DEPLOY_COLOR", "unknown"),
        commit_sha=os.getenv("COMMIT_SHA", "development"),
        release_message=os.getenv("RELEASE_MESSAGE", "atelier4-ready"),
    ), 200


@app.route("/visits")
def visits():
    try:
        count = get_redis_client().incr("visits")
    except redis.RedisError:
        return jsonify(error="redis unavailable"), 503
    return jsonify(visits=count), 200


if __name__ == "__main__":
    app.run(debug=True)
