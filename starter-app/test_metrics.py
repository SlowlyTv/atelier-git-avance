from prometheus_client import REGISTRY

from app import app


def _sample_value(metric_name, labels):
    return REGISTRY.get_sample_value(metric_name, labels) or 0


def test_metrics_counts_requests_and_excludes_scrapes():
    client = app.test_client()
    labels = {"method": "GET", "endpoint": "/", "status": "200"}
    before = _sample_value("http_requests_total", labels)

    assert client.get("/").status_code == 200
    assert _sample_value("http_requests_total", labels) == before + 1

    metrics_before = _sample_value(
        "http_requests_total",
        {"method": "GET", "endpoint": "/metrics", "status": "200"},
    )
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.get_data(as_text=True)
    assert _sample_value(
        "http_requests_total",
        {"method": "GET", "endpoint": "/metrics", "status": "200"},
    ) == metrics_before


def test_latency_histogram_and_simulated_error():
    client = app.test_client()
    response = client.get("/simulate-error")
    assert response.status_code == 500

    metrics = client.get("/metrics").get_data(as_text=True)
    assert "http_request_duration_seconds_bucket" in metrics
    assert 'endpoint="/simulate-error"' in metrics
    assert 'status="500"' in metrics
