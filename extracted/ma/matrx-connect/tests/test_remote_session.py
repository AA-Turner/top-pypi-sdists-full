"""Remote authority responses cannot keep ended sessions admitted or hide outages."""

import asyncio
import time

import httpx
import pytest
from matrx_connect.middleware.auth import VerifiedToken
from matrx_connect.middleware.session_authority import SessionAuthorityUnavailable

from matrx_connect.middleware.remote_session import RemoteSessionResolver

URL = "https://authority.example/auth/session/status"
SUBJECT = "00000000-0000-4000-8000-000000000001"
SESSION = "00000000-0000-4000-8000-000000000002"


def verified():
    return VerifiedToken(
        user_id=SUBJECT,
        is_admin=False,
        email=None,
        claims={"session_id": SESSION},
        token="synthetic-bearer",
        expires_at=int(time.time()) + 3600,
    )


def transport(monkeypatch, handler):
    original = httpx.AsyncClient
    clients = []

    def client(**kwargs):
        assert kwargs["follow_redirects"] is False
        assert kwargs["trust_env"] is False
        clients.append(kwargs)
        return original(**kwargs, transport=httpx.MockTransport(handler))

    monkeypatch.setattr(httpx, "AsyncClient", client)
    return clients


@pytest.mark.asyncio
async def test_each_check_sends_only_presented_bearer_to_exact_authority(monkeypatch):
    value = verified()
    requests = []

    def handler(request):
        requests.append(request)
        if len(requests) == 2:
            return httpx.Response(401)
        return httpx.Response(
            200,
            json={"user_id": SUBJECT, "session_id": SESSION, "expires_at": value.expires_at},
            headers={"Set-Cookie": "secret=synthetic"},
        )

    transport(monkeypatch, handler)
    resolver = RemoteSessionResolver(URL)
    assert await resolver(value) is True
    assert await resolver(value) is False
    assert len(requests) == 2
    for request in requests:
        assert str(request.url) == URL
        assert request.headers["authorization"] == "Bearer synthetic-bearer"
        assert request.headers["accept-encoding"] == "identity"
        assert "cookie" not in request.headers
        assert request.content == b""


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,body,headers",
    [
        (302, b"", {"Location": "https://other.example/steal"}),
        (403, b"", {}),
        (429, b"", {}),
        (500, b"private", {}),
        (200, b"bad json", {}),
        (200, b"[]", {}),
        (200, b"x" * 4097, {}),
        (200, b"compressed", {"Content-Encoding": "gzip"}),
    ],
)
async def test_bad_authority_is_unavailable_not_logout_or_acceptance(
    monkeypatch, status, body, headers
):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(status, content=body, headers=headers)

    transport(monkeypatch, handler)
    with pytest.raises(SessionAuthorityUnavailable) as error:
        await RemoteSessionResolver(URL)(verified())
    assert len(calls) == 1
    assert "private" not in str(error.value)
    assert "synthetic-bearer" not in str(error.value)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ("user_id", SESSION),
        ("session_id", SUBJECT),
        ("expires_at", None),
        ("expires_at", True),
        ("expires_at", "9999999999"),
        ("expires_at", 9999999999),
        ("expires_at", 0),
    ],
)
async def test_positive_response_must_match_exact_verified_credential(monkeypatch, field, value):
    token = verified()
    body = {"user_id": SUBJECT, "session_id": SESSION, "expires_at": token.expires_at}
    body[field] = value
    transport(monkeypatch, lambda request: httpx.Response(200, json=body))
    with pytest.raises(SessionAuthorityUnavailable):
        await RemoteSessionResolver(URL)(token)


@pytest.mark.asyncio
async def test_total_timeout_and_cancellation(monkeypatch):
    async def handler(request):
        await asyncio.sleep(10)
        return httpx.Response(200)

    transport(monkeypatch, handler)
    with pytest.raises(SessionAuthorityUnavailable):
        await RemoteSessionResolver(URL, timeout_seconds=0.01)(verified())
    task = asyncio.create_task(RemoteSessionResolver(URL)(verified()))
    await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


@pytest.mark.parametrize(
    "url",
    [
        "http://authority.example/status",
        "https://user:pass@authority.example/",
        "https://authority.example/?token=x",
        "https://authority.example/#fragment",
        "https://authority.example/status?",
        "https://authority.example/status#",
        "https://authority.example/path\x00tail",
        "\x00https://authority.example/status",
        "https://authority.example/path\x7ftail",
        "https://authority.example%40evil.com/path",
        "/status",
        "https://authority.example/\\else",
        "https://authority.example/\nstatus",
    ],
)
def test_refuse_untrusted_transport_configuration(url):
    with pytest.raises(ValueError):
        RemoteSessionResolver(url)


@pytest.mark.asyncio
@pytest.mark.parametrize("url", [None, "", "   "])
async def test_missing_authority_is_unavailable_without_network(monkeypatch, url):
    def forbidden(**kwargs):
        pytest.fail("missing configuration reached network")

    monkeypatch.setattr(httpx, "AsyncClient", forbidden)
    with pytest.raises(SessionAuthorityUnavailable):
        await RemoteSessionResolver(url)(verified())


@pytest.mark.parametrize("timeout", [True, 0, -1, float("inf"), float("nan")])
def test_invalid_timeout_refused(timeout):
    with pytest.raises(ValueError):
        RemoteSessionResolver(URL, timeout_seconds=timeout)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [{}, {"user_id": SUBJECT, "session_id": SESSION, "expires_at": 9999999999, "extra": True}],
)
async def test_inexact_response_shape_refused(monkeypatch, body):
    transport(monkeypatch, lambda request: httpx.Response(200, json=body))
    with pytest.raises(SessionAuthorityUnavailable):
        await RemoteSessionResolver(URL)(verified())


@pytest.mark.asyncio
async def test_streaming_body_timeout_and_size_abort_close_response(monkeypatch):
    class Stream(httpx.AsyncByteStream):
        slow = True
        closed = False
        chunks = 0

        async def __aiter__(self):
            for _ in range(3):
                self.chunks += 1
                if self.slow:
                    await asyncio.sleep(10)
                yield b"x" * 4096

        async def aclose(self):
            self.closed = True

    stream = Stream()
    transport(monkeypatch, lambda request: httpx.Response(200, stream=stream))
    with pytest.raises(SessionAuthorityUnavailable):
        await RemoteSessionResolver(URL, timeout_seconds=0.01)(verified())
    assert stream.closed
    stream.closed = False
    stream.chunks = 0
    stream.slow = False
    with pytest.raises(SessionAuthorityUnavailable):
        await RemoteSessionResolver(URL)(verified())
    assert stream.closed
    assert stream.chunks == 2


@pytest.mark.asyncio
async def test_real_middleware_warm_cache_cannot_bypass_remote_revocation(monkeypatch):
    import jwt
    from matrx_connect.middleware.auth import AuthMiddleware

    state = "active"
    value = verified()
    count = 0

    def handler(request):
        nonlocal count
        count += 1
        if state == "outage":
            raise httpx.ConnectError("private-transport-detail", request=request)
        if state == "ended":
            return httpx.Response(401)
        return httpx.Response(
            200, json={"user_id": SUBJECT, "session_id": SESSION, "expires_at": value.expires_at}
        )

    transport(monkeypatch, handler)
    secret = "synthetic-remote-session-signing-secret"
    bearer = jwt.encode(
        {"sub": SUBJECT, "session_id": SESSION, "exp": value.expires_at, "aud": "authenticated"},
        secret,
        algorithm="HS256",
    )
    middleware = AuthMiddleware(
        lambda *args: None,
        jwt_secret=secret,
        guest_fingerprint_secret=secret,
        resolve_current_session=RemoteSessionResolver(URL),
        log_requests=False,
    )
    assert await middleware.verify_token_raw(bearer)
    assert middleware._token_cache
    state = "ended"
    assert await middleware.verify_token_raw(bearer) is None
    state = "outage"
    with pytest.raises(SessionAuthorityUnavailable):
        await middleware.verify_token_raw(bearer)
    assert count == 5  # current + ended once each; the outage is retried 3 times (authority_retry)
