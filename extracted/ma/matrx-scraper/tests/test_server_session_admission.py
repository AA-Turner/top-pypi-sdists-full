"""Actual factory must refuse ended user sessions without stranding service callers."""

from __future__ import annotations

import importlib
import time
from uuid import uuid4

import httpx
import jwt
import pytest
from fastapi.testclient import TestClient
from matrx_scraper.server.app import create_app
from matrx_scraper.server.config import ServerConfig

URL = "https://authority.example/auth/session/status"
KEY = "synthetic-jwt-test-key-at-least-32-bytes-long"
SERVICE = "synthetic-server-credential"
USER = str(uuid4())
ORG = str(uuid4())


@pytest.fixture
def boundary(monkeypatch):
    replies = {}
    calls = []
    original = httpx.AsyncClient

    def upstream(request):
        assert str(request.url) == URL
        assert request.method == "GET"
        assert "cookie" not in request.headers
        token = request.headers["authorization"][7:]
        calls.append(token)
        status, body, headers = replies[token]
        if isinstance(body, Exception):
            raise body
        return httpx.Response(status, json=body, headers=headers)

    class AuthorityClient(original):
        def __init__(self, **kwargs):
            assert kwargs["trust_env"] is False
            assert kwargs["follow_redirects"] is False
            super().__init__(**kwargs, transport=httpx.MockTransport(upstream))

    monkeypatch.setattr(httpx, "AsyncClient", AuthorityClient)
    module = importlib.import_module("matrx_scraper.server.app")
    monkeypatch.setattr(
        module,
        "_readiness_snapshot",
        lambda: ({"status": "ok", "failed_components": [], "database": True}, 200),
    )
    preview = importlib.import_module("matrx_scraper.api.preview_router")

    async def render(url):
        from matrx_connect import get_app_context

        ctx = get_app_context()
        return {"actor": ctx.user_id, "org": ctx.organization_id, "auth_type": ctx.auth_type}

    monkeypatch.setattr(preview, "quick_preview", render)

    def build(authority=URL):
        return create_app(
            ServerConfig(
                supabase_jwt_secret=KEY, admin_api_token=SERVICE, session_authority_url=authority
            )
        )

    def token():
        claims = {
            "sub": USER,
            "session_id": str(uuid4()),
            "exp": int(time.time()) + 600,
            "aud": "authenticated",
        }
        value = jwt.encode(claims, KEY, algorithm="HS256")
        replies[value] = (
            200,
            {"user_id": USER, "session_id": claims["session_id"], "expires_at": claims["exp"]},
            {"Cache-Control": "no-store"},
        )
        return value

    def post(client, value, **headers):
        return client.post(
            "/api/scraper/preview",
            json={"url": "https://example.com/"},
            headers={"Authorization": f"Bearer {value}", "X-Organization-Id": ORG, **headers},
        )

    return build, token, post, replies, calls


def test_warm_session_logout_and_sibling(boundary):
    build, token, post, replies, calls = boundary
    first, sibling = token(), token()
    client = TestClient(build())
    assert post(client, first).status_code == 200
    assert post(client, sibling).status_code == 200
    replies[first] = (401, {}, {"Cache-Control": "no-store", "WWW-Authenticate": "Bearer"})
    assert post(client, first).status_code == 401
    assert post(client, sibling).status_code == 200
    assert calls.count(first) == 2


@pytest.mark.parametrize(
    "authority", ["", "http://authority.example/status", "https://authority.example/status?key=bad"]
)
def test_missing_or_invalid_policy_refuses_user_but_service_survives(boundary, authority):
    build, token, post, replies, calls = boundary
    client = TestClient(build(authority))
    result = post(client, token(), Origin="https://www.aimatrx.com")
    assert result.status_code == 503
    assert result.headers["cache-control"] == "no-store"
    assert result.headers["retry-after"]
    assert result.headers["access-control-allow-origin"] == "https://www.aimatrx.com"
    assert post(client, SERVICE, **{"X-Matrx-User-Id": USER}).json()["actor"] == USER
    assert client.get("/health").status_code == 200
    assert not calls


@pytest.mark.parametrize(
    "status,body,headers",
    [
        (503, {}, {"Cache-Control": "no-store"}),
        (200, {}, {"Cache-Control": "no-store"}),
        (200, httpx.ConnectError("synthetic outage"), {}),
    ],
)
def test_authority_fault_is_retryable_without_service_regression(boundary, status, body, headers):
    build, token, post, replies, calls = boundary
    value = token()
    replies[value] = (status, body, headers)
    client = TestClient(build())
    result = post(client, value)
    assert result.status_code == 503
    assert result.headers["cache-control"] == "no-store"
    assert post(client, SERVICE).status_code == 200
    assert client.get("/health/version").status_code == 200
    assert post(client, "bad-token").status_code == 401
    assert calls == [value]


@pytest.mark.parametrize(
    "status,headers,expected",
    [
        (401, {"Cache-Control": "no-store", "WWW-Authenticate": "Bearer"}, 200),
        (401, {}, 503),
        (200, {"Cache-Control": "no-store"}, 503),
    ],
)
def test_readiness_checks_fresh_contract_and_retains_other_checks(
    boundary, status, headers, expected
):
    build, token, post, replies, calls = boundary
    app = build()
    replies["scraper-readiness-invalid"] = (status, {}, headers)
    result = TestClient(app).get("/health/ready")
    assert result.status_code == expected
    assert result.headers["cache-control"] == "no-store"
    assert result.json()["database"] is True
    assert result.json()["session_authority"] is (expected == 200)
    assert calls == ["scraper-readiness-invalid"]


def test_missing_callback_is_not_ready(boundary):
    build, token, post, replies, calls = boundary
    app = build()
    from matrx_connect.middleware import AuthMiddleware

    for middleware in app.user_middleware:
        if middleware.cls is AuthMiddleware:
            middleware.kwargs.pop("resolve_current_session", None)
    result = TestClient(app).get("/health/ready")
    assert result.status_code == 503
    assert result.json()["session_authority"] is False
    assert not calls


def test_preflight_and_invalid_credentials_do_not_check_authority(boundary):
    build, token, post, replies, calls = boundary
    client = TestClient(build())
    preflight = client.options(
        "/api/scraper/preview",
        headers={
            "Origin": "https://www.aimatrx.com",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,x-organization-id",
        },
    )
    assert preflight.status_code == 200
    assert preflight.headers["access-control-allow-origin"] == "https://www.aimatrx.com"
    assert post(client, "malformed-jwt").status_code == 401
    assert post(client, SERVICE).status_code == 200
    assert not calls


def test_readiness_preserves_existing_failures(boundary, monkeypatch):
    build, token, post, replies, calls = boundary
    module = importlib.import_module("matrx_scraper.server.app")
    monkeypatch.setattr(
        module,
        "_readiness_snapshot",
        lambda: ({"status": "not_ready", "failed_components": ["cache"], "cache": False}, 503),
    )
    replies["scraper-readiness-invalid"] = (
        401,
        {},
        {"Cache-Control": "no-store", "WWW-Authenticate": "Bearer"},
    )
    result = TestClient(build()).get("/health/ready")
    assert result.status_code == 503
    assert result.json()["session_authority"] is True
    assert result.json()["failed_components"] == ["cache"]
    assert result.json()["cache"] is False


def test_explicit_scraper_environment_is_independent(monkeypatch):
    monkeypatch.setenv("MATRX_SCRAPER_SESSION_AUTHORITY_URL", URL)
    monkeypatch.setenv("MATRX_SESSION_AUTHORITY_URL", "https://wrong.example/status")
    assert ServerConfig.from_env().session_authority_url == URL


def test_websocket_authority_outage_closes_retryably(boundary):
    from fastapi import WebSocket
    from starlette.websockets import WebSocketDisconnect

    build, token, post, replies, calls = boundary
    value = token()
    replies[value] = (503, {}, {"Cache-Control": "no-store"})
    app = build()

    @app.websocket("/casa-disposable-probe")
    async def probe(socket: WebSocket):
        await socket.accept()
        await socket.send_text("admitted")

    with pytest.raises(WebSocketDisconnect) as result:
        with TestClient(app).websocket_connect(
            "/casa-disposable-probe",
            headers={"Authorization": f"Bearer {value}", "X-Organization-Id": ORG},
        ):
            pytest.fail("Unavailable authority must refuse before handler")
    assert result.value.code == 1013
    assert calls == [value]
