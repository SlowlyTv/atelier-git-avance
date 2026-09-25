import os

import redis
from flask import Flask, jsonify

app = Flask(__name__)

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
        release_message=os.getenv("RELEASE_MESSAGE", "atelier4-problematic"),
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
