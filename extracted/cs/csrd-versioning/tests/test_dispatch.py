"""Tests for version dispatch middleware."""

from enum import Enum
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI, WebSocket
from starlette.requests import Request
from starlette.testclient import TestClient

from csrd.versioning._dispatch import (
    VersionDispatchMiddleware,
    _ensure_request_scope,
    _send_json_error,
    _should_dispatch_request,
)


class Versions(Enum):
    Unversioned = "Unversioned"
    V1 = "2025-06-20"


def _make_request(path: str = "/api/test", headers: dict | None = None) -> Request:
    """Create a minimal Request from a synthetic ASGI scope."""
    scope = {
        "type": "http",
        "method": "GET",
        "path": path,
        "query_string": b"",
        "root_path": "",
        "headers": [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()],
    }
    return Request(scope)


# ── _should_dispatch_request ────────────────────────────────────────────


class TestShouldDispatchRequest:
    def test_root_path_skipped(self):
        assert _should_dispatch_request(_make_request("/"), "api") is False

    def test_docs_prefixes_skipped(self):
        for path in [
            "/swagger-ui",
            "/swagger-ui/index.html",
            "/openapi/v1.json",
            "/_info",
            "/_info/health",
            "/actuator",
            "/actuator/health",
            "/docs",
            "/redoc",
        ]:
            assert _should_dispatch_request(_make_request(path), "api") is False, path

    def test_api_path_dispatched(self):
        assert _should_dispatch_request(_make_request("/api/test"), "api") is True

    def test_api_prefix_exact_dispatched(self):
        assert _should_dispatch_request(_make_request("/api"), "api") is True

    def test_non_api_path_skipped(self):
        assert _should_dispatch_request(_make_request("/other/test"), "api") is False

    def test_root_prefix_dispatches_non_docs(self):
        assert _should_dispatch_request(_make_request("/anything"), "/") is True

    def test_root_prefix_skips_docs(self):
        assert _should_dispatch_request(_make_request("/swagger-ui"), "/") is False


# ── _ensure_request_scope ───────────────────────────────────────────────


class TestEnsureRequestScope:
    def test_creates_scope_when_missing(self):
        from csrd.context.middleware import REQUEST_SCOPE_KEY

        request = _make_request(headers={"x-client-hit-id": "abc", "x-client-app-id": "myapp"})
        _ensure_request_scope(request)
        scope = request.scope[REQUEST_SCOPE_KEY]
        assert scope["hit_id"] == "abc"
        assert scope["app_id"] == "myapp"

    def test_does_not_overwrite_existing(self):
        from csrd.context.middleware import REQUEST_SCOPE_KEY

        request = _make_request(headers={"x-client-hit-id": "new"})
        request.scope[REQUEST_SCOPE_KEY] = {"hit_id": "old"}
        _ensure_request_scope(request)
        assert request.scope[REQUEST_SCOPE_KEY]["hit_id"] == "old"

    def test_no_headers_generates_uuid(self):
        from csrd.context.middleware import REQUEST_SCOPE_KEY

        request = _make_request()
        _ensure_request_scope(request)
        scope = request.scope[REQUEST_SCOPE_KEY]
        # hit_id should be a UUID when header is absent
        assert len(scope["hit_id"]) == 36  # UUID format
        assert "app_id" not in scope


# ── _send_json_error ────────────────────────────────────────────────────


class TestSendJsonError:
    @pytest.mark.asyncio
    async def test_sends_json_with_status(self):
        messages = []
        send = AsyncMock(side_effect=lambda msg: messages.append(msg))
        scope = {"headers": []}
        await _send_json_error(send, scope, status_code=400, detail="bad version")

        assert len(messages) == 2
        assert messages[0]["status"] == 400
        assert messages[0]["type"] == "http.response.start"
        assert b"bad version" in messages[1]["body"]

    @pytest.mark.asyncio
    async def test_includes_cors_header_when_origin_present(self):
        messages = []
        send = AsyncMock(side_effect=lambda msg: messages.append(msg))
        scope = {"headers": [(b"origin", b"https://example.com")]}
        await _send_json_error(send, scope, status_code=400, detail="err")

        start = messages[0]
        header_names = [h[0] for h in start["headers"]]
        assert b"access-control-allow-origin" in header_names

    @pytest.mark.asyncio
    async def test_no_cors_header_without_origin(self):
        messages = []
        send = AsyncMock(side_effect=lambda msg: messages.append(msg))
        scope = {"headers": []}
        await _send_json_error(send, scope, status_code=400, detail="err")

        start = messages[0]
        header_names = [h[0] for h in start["headers"]]
        assert b"access-control-allow-origin" not in header_names


# ── VersionDispatchMiddleware integration ───────────────────────────────


def _build_versioned_app() -> FastAPI:
    """Build a minimal versioned app for dispatch testing."""
    unversioned = FastAPI()
    v1 = FastAPI()

    @unversioned.get("/api/hello")
    async def hello_unv():
        return {"version": "unversioned"}

    @v1.get("/api/hello")
    async def hello_v1():
        return {"version": "v1"}

    @unversioned.websocket("/api/ws")
    async def ws_unv(websocket: WebSocket):
        await websocket.accept()
        await websocket.send_json({"version": "unversioned"})
        await websocket.close()

    @v1.websocket("/api/ws")
    async def ws_v1(websocket: WebSocket):
        await websocket.accept()
        await websocket.send_json({"version": "v1"})
        await websocket.close()

    from csrd.versioning import compose_versioned_apps
    from csrd.versioning._config import VersionedApiConfig, VersionedAppComposeConfig

    return compose_versioned_apps(
        version_mapping={
            Versions.Unversioned: unversioned,
            Versions.V1: v1,
        },
        config=VersionedAppComposeConfig(
            api=VersionedApiConfig(prefix="api", include_actuator_endpoints=False)
        ),
    )


class TestVersionDispatchMiddleware:
    @pytest.fixture
    def app(self):
        return _build_versioned_app()

    @pytest.fixture
    def client(self, app):
        return TestClient(app, raise_server_exceptions=False)

    def test_default_version_dispatched(self, client):
        r = client.get("/api/hello")
        assert r.status_code == 200
        assert r.json()["version"] == "unversioned"

    def test_explicit_version_header(self, client):
        r = client.get("/api/hello", headers={"x-api-version": "2025-06-20"})
        assert r.status_code == 200
        assert r.json()["version"] == "v1"

    def test_docs_path_not_dispatched(self, client):
        r = client.get("/swagger-ui/index.html")
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]

    def test_root_redirects_to_docs(self, client):
        r = client.get("/", follow_redirects=False)
        assert r.status_code == 307
        assert "/swagger-ui/index.html" in r.headers["location"]

    def test_websocket_middleware_initializes(self, app):
        """Middleware constructs cleanly for websocket-capable app."""
        mw = VersionDispatchMiddleware(
            app=app,
            prefix="api",
            version_mapping={Versions.Unversioned: FastAPI()},
        )
        assert mw.prefix == "/api"

    def test_websocket_default_version_dispatched(self, client):
        with client.websocket_connect("/api/ws") as ws:
            data = ws.receive_json()
            assert data["version"] == "unversioned"

    def test_websocket_explicit_version_header_dispatched(self, client):
        with client.websocket_connect("/api/ws", headers={"x-api-version": "2025-06-20"}) as ws:
            data = ws.receive_json()
            assert data["version"] == "v1"
