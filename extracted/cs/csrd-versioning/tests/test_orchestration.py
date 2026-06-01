"""Tests for orchestration: compose_versioned_apps, configure_versioned_api."""

from enum import Enum
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from csrd.versioning._config import VersionedApiConfig, VersionedAppComposeConfig
from csrd.versioning._orchestration import (
    _make_version_scoped_handler,
    _propagate_state_to_versioned_apps,
    _register_middleware,
    _resolve_exception_handlers,
    compose_versioned_apps,
    configure_versioned_api,
)


class Versions(Enum):
    Unversioned = "Unversioned"
    V1 = "2025-06-20"


def _dummy_apps():
    unv = FastAPI()

    @unv.get("/api/ping")
    async def ping():
        return {"ping": "pong"}

    v1 = FastAPI()

    @v1.get("/api/ping")
    async def ping_v1():
        return {"ping": "pong-v1"}

    return {Versions.Unversioned: unv, Versions.V1: v1}


# ── compose_versioned_apps ────────────────────────────────────────────────


class TestComposeVersionedApps:
    def test_returns_fastapi_instance(self):
        app = compose_versioned_apps(
            _dummy_apps(),
            config=VersionedAppComposeConfig(
                api=VersionedApiConfig(prefix="api", include_actuator_endpoints=False)
            ),
        )
        assert isinstance(app, FastAPI)

    def test_custom_title(self):
        app = compose_versioned_apps(
            _dummy_apps(),
            config=VersionedAppComposeConfig(
                title="My API",
                api=VersionedApiConfig(prefix="api", include_actuator_endpoints=False),
            ),
        )
        assert app.title == "My API"

    def test_builtin_docs_disabled(self):
        app = compose_versioned_apps(
            _dummy_apps(),
            config=VersionedAppComposeConfig(
                api=VersionedApiConfig(prefix="api", include_actuator_endpoints=False)
            ),
        )
        assert app.docs_url is None

    def test_app_state_propagated(self):
        app = compose_versioned_apps(
            _dummy_apps(),
            config=VersionedAppComposeConfig(
                app_state={"my_key": "my_value"},
                api=VersionedApiConfig(prefix="api", include_actuator_endpoints=False),
            ),
        )
        assert app.state.my_key == "my_value"

    def test_configure_app_callback(self):
        callback = MagicMock()
        compose_versioned_apps(
            _dummy_apps(),
            config=VersionedAppComposeConfig(
                configure_app=callback,
                api=VersionedApiConfig(prefix="api", include_actuator_endpoints=False),
            ),
        )
        callback.assert_called_once()

    def test_versioned_endpoint_reachable(self):
        app = compose_versioned_apps(
            _dummy_apps(),
            config=VersionedAppComposeConfig(
                api=VersionedApiConfig(prefix="api", include_actuator_endpoints=False)
            ),
        )
        client = TestClient(app, raise_server_exceptions=False)
        r = client.get("/api/ping")
        assert r.status_code == 200

    def test_root_prefix_unversioned_dispatch(self):
        app = compose_versioned_apps(
            {Versions.Unversioned: _dummy_apps()[Versions.Unversioned]},
            config=VersionedAppComposeConfig(
                api=VersionedApiConfig(prefix="/", include_actuator_endpoints=False)
            ),
        )
        client = TestClient(app, raise_server_exceptions=False)
        r = client.get("/api/ping", headers={"x-api-version": "unversioned"})
        assert r.status_code == 200
        assert r.json() == {"ping": "pong"}


# ── configure_versioned_api ─────────────────────────────────────────────


class TestConfigureVersionedApi:
    def test_empty_version_mapping_raises(self):
        app = FastAPI()
        with pytest.raises(ValueError, match="cannot be empty"):
            configure_versioned_api(app, {})

    def test_idempotent(self):
        app = FastAPI()
        mapping = _dummy_apps()
        config = VersionedApiConfig(prefix="api", include_actuator_endpoints=False)
        configure_versioned_api(app, mapping, config=config)
        # Second call should be a no-op
        configure_versioned_api(app, mapping, config=config)


# ── _register_middleware ────────────────────────────────────────────────


class TestRegisterMiddleware:
    def test_none_is_noop(self):
        app = FastAPI()
        _register_middleware(app, None)

    def test_invalid_type_raises(self):
        app = FastAPI()
        with pytest.raises(TypeError, match=r"class or .* tuple"):
            _register_middleware(app, ["not_a_middleware"])


# ── _propagate_state_to_versioned_apps ──────────────────────────────────


class TestPropagateState:
    def test_state_flows_to_sub_apps(self):
        app = FastAPI()
        app.state.shared = "value"
        mapping = _dummy_apps()
        _propagate_state_to_versioned_apps(app, mapping)
        for sub_app in mapping.values():
            assert sub_app.state.shared == "value"

    def test_does_not_overwrite_existing(self):
        app = FastAPI()
        app.state.key = "root"
        mapping = _dummy_apps()
        sub = next(iter(mapping.values()))
        sub.state.key = "sub_original"
        _propagate_state_to_versioned_apps(app, mapping)
        assert sub.state.key == "sub_original"


# ── _resolve_exception_handlers ─────────────────────────────────────────


class TestResolveExceptionHandlers:
    def test_provider_handlers_included(self):
        def provider():
            return {ValueError: lambda r, e: None}

        result = _resolve_exception_handlers(
            exception_handler_provider=provider,
            version_mapping={},
            exception_handlers=None,
        )
        assert ValueError in result

    def test_explicit_handlers_override(self):
        handler = lambda r, e: None  # noqa: E731

        def provider():
            return {ValueError: lambda r, e: None}

        result = _resolve_exception_handlers(
            exception_handler_provider=provider,
            version_mapping={},
            exception_handlers=[(ValueError, handler)],
        )
        assert result[ValueError] is handler


# ── _make_version_scoped_handler ────────────────────────────────────────


class TestMakeVersionScopedHandler:
    @pytest.mark.asyncio
    async def test_fallback_when_no_version(self):
        fallback = MagicMock(return_value="fallback_result")
        handler = _make_version_scoped_handler({}, fallback)
        result = await handler(None, Exception("test"))
        fallback.assert_called_once()
        assert result == "fallback_result"

    @pytest.mark.asyncio
    async def test_raises_when_no_handler_and_no_fallback(self):
        handler = _make_version_scoped_handler({}, None)
        with pytest.raises(Exception, match="test"):
            await handler(None, Exception("test"))
