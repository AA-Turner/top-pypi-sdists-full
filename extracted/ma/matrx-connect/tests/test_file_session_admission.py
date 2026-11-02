"""Byte admission must check the exact signed source freshly, without fallback."""

import asyncio
import time

import httpx
import jwt
import pytest
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from matrx_connect.middleware.auth import AuthMiddleware
from matrx_connect.middleware.file_session import (
    FileSessionCredential,
    mint_bound_file_session_value,
)
from matrx_connect.middleware.session_cookie import SESSION_COOKIE_NAME, mint_session_cookie_value

SECRET = "synthetic-file-admission-secret-not-a-deployment-secret"
USER = "00000000-0000-4000-8000-000000000001"
SOURCE = "00000000-0000-4000-8000-000000000002"
OTHER = "00000000-0000-4000-8000-000000000003"


def bound(kind="login", source=SOURCE):
    return FileSessionCredential(USER, kind, source, int(time.time()) + 3600)


def cookie(credential=None):
    return mint_bound_file_session_value(credential or bound(), SECRET.encode())


def host(**kwargs):
    async def handler(request):
        ctx = request.state.context
        if not ctx.is_authenticated:
            return JSONResponse({"code": "unauthenticated"}, status_code=401)
        return JSONResponse({"user": ctx.user_id, "auth_type": ctx.auth_type})

    app = Starlette(
        routes=[
            Route("/files/{id}/download", handler, methods=["GET", "POST", "HEAD"]),
            Route("/media/{id}/v/{variant}", handler),
            Route("/admin", handler),
            Route("/files/session", handler, methods=["POST"]),
        ]
    )
    return AuthMiddleware(
        app,
        jwt_secret=SECRET,
        guest_fingerprint_secret=SECRET,
        organization_exempt_paths=("/",),
        log_requests=False,
        **kwargs,
    )


def client(app):
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="https://test")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "kind,source", [("login", SOURCE), ("api_key", "publicKey"), ("guest", SOURCE)]
)
async def test_each_signed_family_is_checked_freshly_and_ended_source_is_refused(kind, source):
    active = True
    calls = []
    credential = bound(kind, source)

    async def authority(value):
        calls.append(value)
        return active

    async with client(host(resolve_file_session=authority)) as c:
        c.cookies.set(SESSION_COOKIE_NAME, cookie(credential))
        for path in ("/files/test/download", "/media/test/v/original"):
            response = await c.get(path)
            assert response.status_code == 200
            assert response.json() == {"user": USER, "auth_type": "cookie"}
        active = False
        assert (await c.get("/files/test/download")).status_code == 401
    assert calls == [credential] * 3


@pytest.mark.asyncio
async def test_exact_source_not_sibling_authorizes_same_subject():
    async def authority(value):
        return value.source_id == OTHER

    async with client(host(resolve_file_session=authority)) as c:
        c.cookies.set(SESSION_COOKIE_NAME, cookie())
        assert (await c.get("/files/test/download")).status_code == 401
        c.cookies.set(SESSION_COOKIE_NAME, cookie(bound(source=OTHER)))
        assert (await c.get("/files/test/download")).status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("required", [False, True])
async def test_valid_v2_without_callback_is_retryably_unavailable(required):
    async with client(host(require_file_session_source=required)) as c:
        c.cookies.set(SESSION_COOKIE_NAME, cookie())
        response = await c.get("/files/test/download")
    assert response.status_code == 503
    assert response.headers["retry-after"] == "1"


@pytest.mark.asyncio
@pytest.mark.parametrize("configured", [False, True])
async def test_source_enabled_host_refuses_legacy_v1(configured):
    calls = []

    async def authority(value):
        calls.append(value)
        return True

    kwargs = (
        {"resolve_file_session": authority} if configured else {"require_file_session_source": True}
    )
    async with client(host(**kwargs)) as c:
        c.cookies.set(SESSION_COOKIE_NAME, mint_session_cookie_value(USER, SECRET.encode()))
        assert (await c.get("/files/test/download")).status_code == 401
    assert calls == []


@pytest.mark.asyncio
async def test_unconfigured_generic_host_retains_legacy_lane():
    async with client(host()) as c:
        c.cookies.set(SESSION_COOKIE_NAME, mint_session_cookie_value(USER, SECRET.encode()))
        assert (await c.get("/files/test/download")).status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,path",
    [
        ("POST", "/files/test/download"),
        ("HEAD", "/files/test/download"),
        ("GET", "/admin"),
        ("POST", "/files/session"),
    ],
)
async def test_cookie_never_authorizes_nonbyte_or_nonget_routes(method, path):
    calls = []

    async def authority(value):
        calls.append(value)
        return True

    async with client(host(resolve_file_session=authority)) as c:
        c.cookies.set(SESSION_COOKIE_NAME, cookie())
        assert (await c.request(method, path)).status_code == 401
    assert calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["exception", "timeout", "truthy"])
async def test_outage_timeout_and_nonboolean_do_not_admit(failure):
    async def authority(value):
        if failure == "truthy":
            return 1
        if failure == "timeout":
            await asyncio.sleep(1)
        raise RuntimeError("synthetic-private-source-detail")

    async with client(host(resolve_file_session=authority, session_resolve_timeout=0.01)) as c:
        c.cookies.set(SESSION_COOKIE_NAME, cookie())
        response = await c.get("/files/test/download")
    assert response.status_code == (401 if failure == "truthy" else 503)
    assert "private" not in response.text


@pytest.mark.asyncio
async def test_cancel_propagates():
    async def authority(value):
        raise asyncio.CancelledError

    async with client(host(resolve_file_session=authority)) as c:
        c.cookies.set(SESSION_COOKIE_NAME, cookie())
        with pytest.raises(asyncio.CancelledError):
            await c.get("/files/test/download")


@pytest.mark.asyncio
@pytest.mark.parametrize("value", ["v2.malformed", "", "v1.malformed"])
async def test_invalid_value_never_calls_authority(value):
    calls = []

    async def authority(binding):
        calls.append(binding)
        return True

    async with client(host(resolve_file_session=authority)) as c:
        c.cookies.set(SESSION_COOKIE_NAME, value)
        assert (await c.get("/files/test/download")).status_code == 401
    assert calls == []


@pytest.mark.asyncio
async def test_bad_signature_never_calls_authority():
    async def authority(value):
        pytest.fail("tampered value reached current-source authority")

    async with client(host(resolve_file_session=authority)) as c:
        c.cookies.set(SESSION_COOKIE_NAME, cookie()[:-1] + "X")
        assert (await c.get("/files/test/download")).status_code == 401


@pytest.mark.asyncio
async def test_refused_bearer_cannot_fall_back_to_valid_file_cookie():
    calls = []

    async def file_authority(value):
        calls.append(value)
        return True

    async def login_authority(value):
        return False

    token = jwt.encode(
        {"sub": USER, "session_id": SOURCE, "aud": "authenticated", "exp": int(time.time()) + 3600},
        SECRET,
        algorithm="HS256",
    )
    async with client(
        host(resolve_file_session=file_authority, resolve_current_session=login_authority)
    ) as c:
        c.cookies.set(SESSION_COOKIE_NAME, cookie())
        response = await c.get("/files/test/download", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert calls == []


@pytest.mark.asyncio
async def test_websocket_cookie_is_not_identity_and_never_checks_source():
    observed = []

    async def authority(value):
        pytest.fail("WebSocket entered byte-cookie authority")

    async def handler(scope, receive, send):
        observed.append(scope["state"]["context"].is_authenticated)
        await receive()
        await send({"type": "websocket.close", "code": 1000})

    async def receive():
        return {"type": "websocket.connect"}

    async def send(message):
        assert message["type"] == "websocket.close"

    app = AuthMiddleware(
        handler,
        jwt_secret=SECRET,
        guest_fingerprint_secret=SECRET,
        resolve_file_session=authority,
        organization_exempt_paths=("/",),
        log_requests=False,
    )
    scope = {
        "type": "websocket",
        "scheme": "wss",
        "path": "/files/test/download",
        "query_string": b"",
        "headers": [(b"cookie", f"{SESSION_COOKIE_NAME}={cookie()}".encode())],
        "server": ("test", 443),
        "client": ("127.0.0.1", 1000),
    }
    await app(scope, receive, send)
    assert observed == [False]


@pytest.mark.asyncio
async def test_expired_signed_source_never_calls_authority():
    async def authority(value):
        pytest.fail("Expired source entered byte-cookie authority")

    now = int(time.time())
    expired = FileSessionCredential(USER, "login", SOURCE, now - 10)
    value = mint_bound_file_session_value(expired, SECRET.encode(), now=now - 60)
    async with client(host(resolve_file_session=authority)) as c:
        c.cookies.set(SESSION_COOKIE_NAME, value)
        assert (await c.get("/files/test/download")).status_code == 401
