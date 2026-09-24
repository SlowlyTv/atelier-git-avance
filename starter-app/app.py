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


@app.route("/health")
def health():
    try:
        get_redis_client().ping()
    except redis.RedisError:
        return jsonify(status="error", dependency="redis"), 503
    return jsonify(status="ok", redis="ok"), 200


@app.route("/status")
def status():
    return jsonify(service="projet-devops-groupe-demo", version="1.0"), 200


@app.route("/visits")
def visits():
    try:
        count = get_redis_client().incr("visits")
    except redis.RedisError:
        return jsonify(error="redis unavailable"), 503
    return jsonify(visits=count), 200


if __name__ == "__main__":
    app.run(debug=True)
