"""Eureka registration tests: py_eureka_client is mocked, no Eureka server is needed."""
import py_eureka_client.eureka_client as eureka_client
from fastapi.testclient import TestClient

from app.main import app


def test_registers_at_startup_and_stops_at_shutdown(monkeypatch):
    calls = {}

    async def fake_init_async(**kwargs):
        calls["init"] = kwargs

    async def fake_stop_async():
        calls["stop"] = True

    monkeypatch.setenv("EUREKA_ENABLED", "true")
    monkeypatch.setenv("PORT", "8094")
    monkeypatch.setenv("EUREKA_SERVER", "http://localhost:8761/eureka")
    monkeypatch.setattr(eureka_client, "init_async", fake_init_async)
    monkeypatch.setattr(eureka_client, "stop_async", fake_stop_async)

    with TestClient(app) as client:  # entering the context runs the lifespan startup
        assert "init" in calls
        assert calls["init"]["app_name"] == "NOTIFICATION"
        assert calls["init"]["instance_port"] == 8094
        assert calls["init"]["eureka_server"] == "http://localhost:8761/eureka"
        # the service keeps answering on its hello endpoint
        assert client.get("/api/notifications/hello").status_code == 200
        assert "stop" not in calls

    assert calls.get("stop") is True  # lifespan shutdown stopped the Eureka client


def test_service_still_starts_if_eureka_is_down(monkeypatch):
    async def failing_init_async(**kwargs):
        raise ConnectionError("Eureka is not reachable")

    monkeypatch.setenv("EUREKA_ENABLED", "true")
    monkeypatch.setattr(eureka_client, "init_async", failing_init_async)

    with TestClient(app) as client:
        assert client.get("/api/notifications/hello").status_code == 200


def test_registration_can_be_disabled(monkeypatch):
    called = []

    async def fake_init_async(**kwargs):
        called.append(kwargs)

    monkeypatch.setenv("EUREKA_ENABLED", "false")
    monkeypatch.setattr(eureka_client, "init_async", fake_init_async)

    with TestClient(app):
        pass
    assert called == []
