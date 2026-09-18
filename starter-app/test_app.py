from unittest.mock import Mock, patch

import redis

from app import alert_threshold, sanitize_input, app


def test_alert_threshold():
    assert alert_threshold() == 25


def test_sanitize_input_escapes_html():
    assert sanitize_input("<script>") == "&lt;script&gt;"


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_status_endpoint():
    client = app.test_client()
    response = client.get("/status")
    assert response.status_code == 200
    assert response.get_json() == {
        "service": "projet-devops-groupe-demo",
        "version": "1.0",
    }


def test_visits_endpoint_increments_counter():
    redis_client = Mock()
    redis_client.incr.return_value = 7
    with patch("app.get_redis_client", return_value=redis_client):
        response = app.test_client().get("/visits")
    assert response.status_code == 200
    assert response.get_json() == {"visits": 7}
    redis_client.incr.assert_called_once_with("visits")


def test_visits_endpoint_reports_redis_failure():
    redis_client = Mock()
    redis_client.incr.side_effect = redis.RedisError("unavailable")
    with patch("app.get_redis_client", return_value=redis_client):
        response = app.test_client().get("/visits")
    assert response.status_code == 503
    assert response.get_json() == {"error": "redis unavailable"}
