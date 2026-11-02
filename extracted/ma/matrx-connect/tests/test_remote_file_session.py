"""Current-source decisions must match the exact signed binding on every read."""

import asyncio
from dataclasses import asdict
import time

import httpx
import pytest
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from matrx_connect.middleware.auth import AuthMiddleware
from matrx_connect.middleware.file_session import FileSessionCredential, mint_bound_file_session_value
from matrx_connect.middleware.remote_file_session import RemoteFileSessionResolver
from matrx_connect.middleware.session_authority import SessionAuthorityUnavailable
from matrx_connect.middleware.session_cookie import SESSION_COOKIE_NAME

SECRET = b"synthetic-remote-file-key-not-a-deployment-secret"
URL = "https://authority.example/auth/file-session/status"
USER = "00000000-0000-4000-8000-000000000001"
SOURCE = "00000000-0000-4000-8000-000000000002"


def binding(kind="login"):
    return FileSessionCredential(USER, kind, "publicKey" if kind == "api_key" else SOURCE, int(time.time()) + 3600)


def mock_client(monkeypatch, handler):
    original = httpx.AsyncClient
    clients = []

    def client(**kwargs):
        assert kwargs["follow_redirects"] is False and kwargs["trust_env"] is False
        clients.append(kwargs)
        return original(**kwargs, transport=httpx.MockTransport(handler))

    monkeypatch.setattr(httpx, "AsyncClient", client)
    return clients, original


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["login", "api_key", "guest"])
async def test_exact_signed_family_is_forwarded_fresh_without_cookie_reuse(monkeypatch, kind):
    credential = binding(kind)
    expected = mint_bound_file_session_value(credential, SECRET)
    requests = []

    def authority(request):
        requests.append(request)
        return httpx.Response(200, json=asdict(credential), headers={"Set-Cookie": "untrusted=synthetic"}) if len(requests) == 1 else httpx.Response(401)

    clients, _ = mock_client(monkeypatch, authority)
    resolver = RemoteFileSessionResolver(URL, SECRET)
    assert await resolver(credential) is True
    assert await resolver(credential) is False
    assert len(clients) == 2
    for request in requests:
        assert str(request.url) == URL
        assert request.headers["Authorization"] == f"FileSession {expected}"
        assert request.headers["Accept-Encoding"] == "identity"
        assert "Cookie" not in request.headers
        assert request.content == b""


@pytest.mark.asyncio
@pytest.mark.parametrize("field,value", [
    ("user_id", SOURCE), ("source_id", USER), ("source_kind", "guest"),
    ("expires_at", 0), ("expires_at", True), ("expires_at", 9999999999),
    ("extra", "untrusted"),
])
async def test_mismatch_is_unavailable_not_admission_or_logout(monkeypatch, field, value):
    credential = binding()
    body = asdict(credential)
    body[field] = value
    mock_client(monkeypatch, lambda r: httpx.Response(200, json=body))
    with pytest.raises(SessionAuthorityUnavailable):
        await RemoteFileSessionResolver(URL, SECRET)(credential)


@pytest.mark.asyncio
@pytest.mark.parametrize("case", ["float_expiry", "null", "list", "duplicate", "invalid_json", "oversize", "compression", "redirect", "403", "503"])
async def test_invalid_authority_wire_is_bounded_unavailable(monkeypatch, case):
    credential = binding()
    body = asdict(credential)
    if case == "float_expiry":
        body["expires_at"] = float(credential.expires_at)
    responses = {
        "float_expiry": lambda: httpx.Response(200, json=body),
        "null": lambda: httpx.Response(200, content=b"null"),
        "list": lambda: httpx.Response(200, content=b"[]"),
        "duplicate": lambda: httpx.Response(200, content=b'{"user_id":"wrong","user_id":"duplicate"}'),
        "invalid_json": lambda: httpx.Response(200, content=b"synthetic-private-detail"),
        "oversize": lambda: httpx.Response(200, content=b" " * 4097),
        "compression": lambda: httpx.Response(200, content=b"fake", headers={"Content-Encoding": "gzip"}),
        "redirect": lambda: httpx.Response(302, headers={"Location": "https://other.example"}),
        "403": lambda: httpx.Response(403),
        "503": lambda: httpx.Response(503),
    }
    requests = []

    def authority(request):
        requests.append(request)
        return responses[case]()

    mock_client(monkeypatch, authority)
    with pytest.raises(SessionAuthorityUnavailable) as error:
        await RemoteFileSessionResolver(URL, SECRET)(credential)
    assert len(requests) == 1
    assert "private-detail" not in str(error.value) and "v2." not in str(error.value)


@pytest.mark.asyncio
async def test_timeout_cancellation_and_transport_failure(monkeypatch):
    async def authority(request):
        await asyncio.sleep(10)
        return httpx.Response(200)

    mock_client(monkeypatch, authority)
    resolver = RemoteFileSessionResolver(URL, SECRET, timeout_seconds=.02)
    with pytest.raises(SessionAuthorityUnavailable):
        await resolver(binding())
    task = asyncio.create_task(RemoteFileSessionResolver(URL, SECRET)(binding()))
    await asyncio.sleep(.005)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


@pytest.mark.asyncio
async def test_expired_or_over_ceiling_binding_never_reaches_network(monkeypatch):
    calls = []
    mock_client(monkeypatch, lambda request: calls.append(request))
    resolver = RemoteFileSessionResolver(URL, SECRET)
    for expiry in (int(time.time()) - 1, int(time.time()) + 604802):
        assert await resolver(FileSessionCredential(USER, "login", SOURCE, expiry)) is False
    assert not calls


@pytest.mark.asyncio
async def test_absent_authority_is_unavailable():
    with pytest.raises(SessionAuthorityUnavailable):
        await RemoteFileSessionResolver(None, SECRET)(binding())


@pytest.mark.parametrize("secret", [b"", "secret", None])
def test_missing_or_wrong_type_shared_key_refuses_construction(secret):
    with pytest.raises(ValueError):
        RemoteFileSessionResolver(URL, secret)


@pytest.mark.parametrize("url", ["http://authority.example", "https://user:secret@authority.example", "https://authority.example?token=secret", "https://authority.example#secret", "https://authority.example:99999", "https://authority.example\\evil", " https://authority.example"])
def test_invalid_configured_destination_refuses_construction(url):
    with pytest.raises(ValueError):
        RemoteFileSessionResolver(url, SECRET)


@pytest.mark.asyncio
@pytest.mark.parametrize("reply,expected", [("current", 200), ("ended", 401), ("outage", 503)])
async def test_actual_byte_admission_uses_remote_source_decision(monkeypatch, reply, expected):
    credential = binding()
    clients, original = mock_client(monkeypatch, lambda r: httpx.Response(200, json=asdict(credential)) if reply == "current" else httpx.Response(401 if reply == "ended" else 503))

    async def bytes_route(request):
        return JSONResponse({"ok": True}, status_code=200 if request.state.context.user_id else 401)

    app = AuthMiddleware(Starlette(routes=[Route("/files/test/download", bytes_route)]),
        jwt_secret=SECRET.decode(), guest_fingerprint_secret=SECRET.decode(),
        resolve_file_session=RemoteFileSessionResolver(URL, SECRET), log_requests=False)
    async with original(transport=httpx.ASGITransport(app=app), base_url="https://consumer.example") as c:
        response = await c.get("/files/test/download", headers={"Cookie": f"{SESSION_COOKIE_NAME}={mint_bound_file_session_value(credential, SECRET)}"})
    # an outage is retried within the bounded budget (authority_retry); a decision is asked once
    assert response.status_code == expected and len(clients) == (3 if reply == "outage" else 1)
    if expected == 503:
        assert response.headers["Retry-After"] == "1"
        assert response.headers["Cache-Control"] == "no-store"


@pytest.mark.asyncio
async def test_expiry_during_authority_round_trip_refuses_admission(monkeypatch):
    now = time.time()
    clock = [now]
    credential = FileSessionCredential(USER, "login", SOURCE, int(now) + 2)
    monkeypatch.setattr(time, "time", lambda: clock[0])

    def authority(request):
        clock[0] += 3
        return httpx.Response(200, json=asdict(credential))

    mock_client(monkeypatch, authority)
    assert await RemoteFileSessionResolver(URL, SECRET)(credential) is False


@pytest.mark.asyncio
async def test_duplicate_field_with_matching_last_value_cannot_admit(monkeypatch):
    import json
    credential = binding()
    body = '{"user_id":"wrong",' + json.dumps(asdict(credential))[1:]
    mock_client(monkeypatch, lambda request: httpx.Response(200, content=body))
    with pytest.raises(SessionAuthorityUnavailable):
        await RemoteFileSessionResolver(URL, SECRET)(credential)
