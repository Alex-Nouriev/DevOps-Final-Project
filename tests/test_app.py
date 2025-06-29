import pytest
import threading
import time

from app.main import app, services, services_lock, _monitor_loop


@pytest.fixture(autouse=True)
def clear_services():
    """
    Clear the global `services` dict after each test to avoid state leakage.
    """
    yield
    with services_lock:
        services.clear()


def test_add_and_get_service():
    client = app.test_client()
    data = {"name": "svc1", "url": "http://example.com", "interval": 1}
    resp = client.post('/service', json=data)
    assert resp.status_code == 201

    status = client.get('/service/svc1')
    assert status.status_code == 200
    json_data = status.get_json()
    assert json_data['name'] == 'svc1'
    assert json_data['url'] == data['url']
    assert isinstance(json_data['is_up'], bool)


def test_add_duplicate_service():
    client = app.test_client()
    data = {"name": "svc2", "url": "http://example.com", "interval": 1}
    resp1 = client.post('/service', json=data)
    assert resp1.status_code == 201

    resp2 = client.post('/service', json=data)
    assert resp2.status_code == 400
    assert "already exists" in resp2.get_json().get('error', '')


def test_get_unknown_service():
    client = app.test_client()
    resp = client.get('/service/doesnotexist')
    assert resp.status_code == 404
    assert "Service not found" in resp.get_json().get('error', '')


def test_missing_fields():
    client = app.test_client()
    resp = client.post('/service', json={"name": ""})
    assert resp.status_code == 400
    assert "Missing 'name' or 'url'" in resp.get_json().get('error', '')


def test_metrics_after_add(monkeypatch):
    """
    After adding a service, start the monitor loop once and then
    scrape /metrics to verify the custom Prometheus metrics appear.
    """
    # Simulate a healthy response for every check
    class DummyResponse:
        status_code = 200

    monkeypatch.setattr('app.main.requests.get', lambda url,
                        timeout: DummyResponse())

    client = app.test_client()
    client.post('/service', json={"name": "svc3", "url": "http://example.com",
                "interval": 1})

    # Run one iteration of the monitor loop in the background
    t = threading.Thread(target=_monitor_loop, daemon=True)
    t.start()
    time.sleep(1.1)

    resp = client.get('/metrics')
    text = resp.get_data(as_text=True)
    # Verify the service count gauge
    assert "service_tracker_total_services 1.0" in text