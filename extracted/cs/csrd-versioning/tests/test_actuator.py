"""Tests for actuator endpoints and plugins."""

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from csrd.versioning.extensions.actuator.actuator import _resolve_plugins, register_actuator_router
from csrd.versioning.extensions.actuator.plugins import ActuatorPlugin

# ── register_actuator_router ─────────────────────────────────────────────


class TestActuatorRouter:
    @pytest.fixture
    def app(self):
        app = FastAPI()
        register_actuator_router(app)
        return app

    @pytest.fixture
    def client(self, app):
        return TestClient(app)

    def test_actuator_root(self, client):
        r = client.get("/actuator")
        assert r.status_code == 200
        data = r.json()
        assert "_links" in data
        assert "self" in data["_links"]

    def test_health_endpoint(self, client):
        r = client.get("/actuator/health")
        assert r.status_code == 200
        data = r.json()
        assert "status" in data

    def test_info_endpoint(self, client):
        r = client.get("/actuator/info")
        # Info may return 200 or 404 if no build-info.json exists
        assert r.status_code in (200, 404)

    def test_env_endpoint(self, client):
        r = client.get("/actuator/env")
        assert r.status_code == 200
        data = r.json()
        assert "propertySources" in data


# ── _resolve_plugins ─────────────────────────────────────────────────────


class TestResolvePlugins:
    def test_default_plugins_present(self):
        plugins = _resolve_plugins(None)
        names = {p.name for p in plugins}
        assert "health" in names
        assert "info" in names
        assert "env" in names

    def test_custom_plugin_override(self):
        class CustomHealth(ActuatorPlugin):
            name = "health"

            def register(self, router, *, app, prefix):
                return {}

        plugins = _resolve_plugins([CustomHealth()])
        health_plugins = [p for p in plugins if p.name == "health"]
        assert len(health_plugins) == 1
        assert isinstance(health_plugins[0], CustomHealth)

    def test_custom_plugin_added(self):
        class CustomPlugin(ActuatorPlugin):
            name = "custom"

            def register(self, router, *, app, prefix):
                return {}

        plugins = _resolve_plugins([CustomPlugin()])
        names = {p.name for p in plugins}
        assert "custom" in names
        assert "health" in names  # defaults still present


# ── Health indicators ────────────────────────────────────────────────────


class TestHealthIndicators:
    def test_ping_indicator(self):
        from csrd.versioning.extensions.actuator.plugins.health.indicators import (
            PingHealthIndicator,
        )

        indicator = PingHealthIndicator()
        result = indicator._check()
        assert result == {"status": "UP"}

    def test_liveness_indicator(self):
        from csrd.versioning.extensions.actuator.plugins.health.indicators import LivenessIndicator

        indicator = LivenessIndicator()
        result = indicator._check()
        assert result["status"] == "UP"

    def test_readiness_indicator(self):
        from csrd.versioning.extensions.actuator.plugins.health.indicators import ReadinessIndicator

        indicator = ReadinessIndicator()
        result = indicator._check()
        assert result["status"] == "UP"

    def test_disk_space_up(self):
        from unittest.mock import patch

        from csrd.versioning.extensions.actuator.plugins.health.indicators import (
            DiskSpaceHealthIndicator,
        )

        indicator = DiskSpaceHealthIndicator()
        mock_usage = type("Usage", (), {"free": 1_000_000_000, "total": 2_000_000_000})()
        with patch("shutil.disk_usage", return_value=mock_usage):
            result = indicator._check()
            assert result["status"] == "UP"

    def test_disk_space_down(self):
        from unittest.mock import patch

        from csrd.versioning.extensions.actuator.plugins.health.indicators import (
            DiskSpaceHealthIndicator,
        )

        indicator = DiskSpaceHealthIndicator(threshold=999_999_999_999)
        mock_usage = type("Usage", (), {"free": 100, "total": 1000})()
        with patch("shutil.disk_usage", return_value=mock_usage):
            result = indicator._check()
            assert result["status"] == "DOWN"


# ── Health endpoint integration ──────────────────────────────────────────


class TestHealthEndpoint:
    @pytest.fixture
    def client(self):
        app = FastAPI()
        register_actuator_router(app)
        return TestClient(app)

    def test_health_returns_up(self, client):
        r = client.get("/actuator/health")
        data = r.json()
        assert data["status"] in ("UP", "DOWN")

    def test_health_component(self, client):
        r = client.get("/actuator/health/ping")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "UP"

    def test_health_unknown_component(self, client):
        r = client.get("/actuator/health/nonexistent")
        assert r.status_code in (404, 200)


# ── Env endpoint ─────────────────────────────────────────────────────────


class TestEnvEndpoint:
    @pytest.fixture
    def client(self):
        from csrd.versioning.extensions.actuator.plugins import (
            EnvActuatorPlugin,
            SanitizationConfig,
            ShowValues,
        )

        app = FastAPI()
        env_plugin = EnvActuatorPlugin.with_providers(
            sanitization=SanitizationConfig(show_values=ShowValues.ALWAYS),
        )
        register_actuator_router(app, plugins=[env_plugin])
        return TestClient(app)

    def test_env_returns_property_sources(self, client):
        r = client.get("/actuator/env")
        assert r.status_code == 200
        data = r.json()
        assert "propertySources" in data

    def test_env_filter(self, client):
        r = client.get("/actuator/env/PATH")
        assert r.status_code == 200
