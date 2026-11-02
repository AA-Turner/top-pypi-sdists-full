"""A warm crypto cache must never turn a logged-out session into admission."""
import asyncio
import time

import httpx
import jwt
import pytest
from matrx_connect.middleware.auth import AuthMiddleware
from matrx_connect.middleware.session_authority import SessionAuthorityUnavailable
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

SECRET = "synthetic-test-key-not-a-deployment-secret"
SUBJECT = "00000000-0000-4000-8000-000000000001"
SESSION = "00000000-0000-4000-8000-000000000002"


def token():
    return jwt.encode({"sub": SUBJECT, "session_id": SESSION, "aud": "authenticated",
        "exp": int(time.time()) + 3600}, SECRET, algorithm="HS256")


@pytest.mark.asyncio
async def test_warm_crypto_cache_cannot_keep_revoked_session_alive():
    active = True
    calls = []
    async def current(verified):
        calls.append((verified.user_id, verified.claims["session_id"]))
        return active
    mw = AuthMiddleware(lambda *args: None, jwt_secret=SECRET, resolve_current_session=current,
                        log_requests=False)
    bearer = token()
    assert await mw.verify_token_raw(bearer) is not None
    assert mw._token_cache
    active = False
    assert await mw.verify_token_raw(bearer) is None
    assert calls == [(SUBJECT, SESSION), (SUBJECT, SESSION)]


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["timeout", "exception"])
async def test_authority_outage_is_503_without_handler_or_guest_fallback(failure):
    called = []
    async def current(verified):
        if failure == "timeout":
            await asyncio.sleep(1)
        raise RuntimeError("synthetic-private-database-detail")
    async def handler(request):
        called.append("handler")
        return JSONResponse({"wrong": True})
    async def guest(*args):
        called.append("guest")
    app = AuthMiddleware(Starlette(routes=[Route("/health", handler)]), jwt_secret=SECRET,
        resolve_current_session=current, session_resolve_timeout=0.01,
        resolve_guest=guest, log_requests=False)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health", headers={"Authorization": f"Bearer {token()}",
                                                        "X-Fingerprint-ID": "synthetic"})
    assert response.status_code == 503
    assert response.json()["code"] == "session_authority_unavailable"
    assert response.headers["Retry-After"] == "1"
    assert "private" not in response.text
    assert called == []


@pytest.mark.asyncio
async def test_raw_verifier_preserves_typed_unavailable_after_warmed_cache():
    active = True
    async def current(verified):
        if active:
            return True
        raise RuntimeError("private")
    mw = AuthMiddleware(lambda *args: None, jwt_secret=SECRET, resolve_current_session=current,
                        log_requests=False)
    bearer = token()
    assert await mw.verify_token_raw(bearer)
    active = False
    with pytest.raises(SessionAuthorityUnavailable):
        await mw.verify_token_raw(bearer)


@pytest.mark.asyncio
async def test_websocket_authority_outage_refuses_handshake_retryably():
    messages = []
    async def current(verified):
        raise RuntimeError("private")
    async def handler(*args):
        pytest.fail("unavailable session reached handler")
    async def receive():
        return {"type": "websocket.connect"}
    async def send(message):
        messages.append(message)
    app = AuthMiddleware(handler, jwt_secret=SECRET, resolve_current_session=current,
                         log_requests=False)
    await app({"type": "websocket", "path": "/health", "query_string": b"",
        "headers": [(b"authorization", f"Bearer {token()}".encode())],
        "client": ("127.0.0.1", 1234), "state": {}}, receive, send)
    assert messages == [{"type": "websocket.close", "code": 1013,
                         "reason": "session_authority_unavailable"}]
