"""Actual ASGI mint adapter/transport/codec; authority responses are synthetic."""
from __future__ import annotations

import asyncio
from dataclasses import asdict
import time

import httpx
import pytest

from matrx_connect.middleware.file_session import FileSessionCredential, mint_bound_file_session_value
from matrx_connect.middleware.session_cookie import session_cookie_headers
from matrx_files.standalone import remote_mint as module

ORIGINAL_CLIENT = httpx.AsyncClient
USER = "00000000-0000-4000-8000-000000000001"
SOURCE = "00000000-0000-4000-8000-000000000002"
SECRET = b"synthetic-remote-mint-shared-secret-not-deployment-secret"
MINT = "https://authority.example/files/session"
STATUS = "https://authority.example/auth/file-session/status"


@pytest.fixture
def network(monkeypatch):
    now = int(time.time())
    monkeypatch.setattr(module.time, "time", lambda: now)
    state = {"now": now, "kind": "login", "mint_status": 200, "source_status": 200,
             "body": None, "cookies": None, "cache": "no-store", "encoding": None,
             "calls": [], "delay": 0, "source_delay": 0, "error": None}

    def binding():
        return FileSessionCredential(USER, state["kind"], "publicKey" if state["kind"] == "api_key" else SOURCE, now + 120)

    state["binding"] = binding

    async def handler(request):
        state["calls"].append(request)
        if state["error"]:
            raise httpx.ConnectError("synthetic-private-transport-detail", request=request)
        if request.method == "POST":
            await asyncio.sleep(state["delay"])
            value = mint_bound_file_session_value(binding(), SECRET)
            headers = [("Cache-Control", state["cache"])]
            headers += [("Set-Cookie", c) for c in (state["cookies"] if state["cookies"] is not None else session_cookie_headers(value, ttl_seconds=120))]
            headers += [("X-Private-Upstream", "must-not-forward")]
            if state["encoding"]:
                headers.append(("Content-Encoding", state["encoding"]))
            body = state["body"] if state["body"] is not None else b'{"ok":true,"expires_in":120}'
            return httpx.Response(state["mint_status"], content=body, headers=headers)
        await asyncio.sleep(state["source_delay"])
        assert request.url == STATUS
        assert request.headers["authorization"] == "FileSession " + mint_bound_file_session_value(binding(), SECRET)
        return httpx.Response(state["source_status"], json=asdict(binding()))

    def client(**kwargs):
        assert kwargs["follow_redirects"] is False and kwargs["trust_env"] is False
        return ORIGINAL_CLIENT(transport=httpx.MockTransport(handler), **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", client)
    return state


class OrdinaryApp:
    def __init__(self):
        self.calls = []

    async def __call__(self, scope, receive, send):
        self.calls.append((scope["type"], scope.get("method"), scope.get("path")))
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ordinary"})


def application(timeout=5.0):
    sink = OrdinaryApp()
    mint = module.RemoteFileSessionMint(MINT, STATUS, SECRET, timeout_seconds=timeout)
    return module.RemoteFileSessionMintMiddleware(sink, mint=mint), sink


async def post(app, headers=None, path="/files/session", data=b""):
    async with ORIGINAL_CLIENT(transport=httpx.ASGITransport(app=app), base_url="https://files.example") as client:
        return await client.post(path, headers=headers, content=data)


@pytest.mark.asyncio
@pytest.mark.parametrize("kind,headers", [
    ("login", {"Authorization": "Bearer synthetic-jwt"}),
    ("api_key", {"Authorization": "Bearer mx_live_publicKey_secret"}),
    ("guest", {"X-Fingerprint-ID": "synthetic-fingerprint"}),
    ("guest", {"X-Guest-Fingerprint": "synthetic-fingerprint"}),
])
async def test_each_family_uses_only_presented_credential_and_fresh_exact_authority(network, kind, headers):
    network["kind"] = kind
    app, sink = application()
    response = await post(app, {**headers, "Cookie": "ambient=must-not-forward", "X-Organization-Id": "caller-selector",
                                "X-Forwarded-For": "192.0.2.10", "User-Agent": "caller-agent"}, data=b'{"user_id":"caller-selector"}')
    assert response.status_code == 200
    assert response.json() == {"ok": True, "expires_in": 120}
    assert response.headers["cache-control"] == "no-store"
    assert not response.headers.get("x-private-upstream")
    cookies = response.headers.get_list("set-cookie")
    value = mint_bound_file_session_value(network["binding"](), SECRET)
    assert cookies == session_cookie_headers(value, ttl_seconds=120)
    assert value not in response.text
    assert sink.calls == []
    first, second = network["calls"]
    assert str(first.url) == MINT and first.method == "POST" and first.content == b""
    assert "cookie" not in first.headers and "x-organization-id" not in first.headers and "x-forwarded-for" not in first.headers
    assert first.headers["user-agent"] != "caller-agent"
    assert first.headers["accept-encoding"] == "identity"
    assert "cookie" not in second.headers and second.content == b""
    assert first.headers.get("authorization") == headers.get("Authorization")
    if kind == "guest":
        assert first.headers["x-fingerprint-id"] == "synthetic-fingerprint"
        assert "x-guest-fingerprint" not in first.headers
    network["source_status"] = 401
    ended = await post(app, headers)
    assert ended.status_code == 401 and ended.headers["cache-control"] == "no-store"
    assert not ended.headers.get_list("set-cookie")
    assert len(network["calls"]) == 4


@pytest.mark.asyncio
@pytest.mark.parametrize("headers", [
    {}, {"Cookie": "mx_files_session=ambient"}, {"Authorization": "Basic invalid"}, {"Authorization": "Bearer "},
    [("Authorization", "Bearer one"), ("authorization", "Bearer one")],
    [("X-Fingerprint-ID", "one"), ("x-fingerprint-id", "one")],
    {"X-Fingerprint-ID": "one", "X-Guest-Fingerprint": "one"},
    {"Authorization": "Bearer one", "X-Fingerprint-ID": "one"},
    {"Authorization": "Bearer one", "X-Guest-Fingerprint": ""},
    {"Authorization": "Bearer  one"}, {"X-Fingerprint-ID": ""}, {"X-Fingerprint-ID": "with space"},
    [(b"authorization", b"Bearer \xff")], [(b"x-fingerprint-id", b"\xff")],
    [(b"authorization", b"Bearer \x00hidden")], [(b"x-fingerprint-id", b"\x7f")],
])
async def test_ambiguous_missing_or_malformed_credentials_never_reach_authority(network, headers):
    app, sink = application()
    response = await post(app, headers)
    assert response.status_code == 401 and response.headers["cache-control"] == "no-store"
    assert not response.headers.get_list("set-cookie")
    assert network["calls"] == [] and sink.calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize("kind,name,prefix,limit", [
    ("login", "Authorization", "Bearer ", module.MAX_AUTHORIZATION_BYTES),
    ("guest", "X-Fingerprint-ID", "", module.MAX_FINGERPRINT_BYTES),
])
async def test_exact_credential_byte_caps_and_cap_plus_one(network, kind, name, prefix, limit):
    network["kind"] = kind
    app, _ = application()
    assert (await post(app, {name: prefix + "a" * (limit - len(prefix))})).status_code == 200
    network["calls"].clear()
    assert (await post(app, {name: prefix + "a" * (limit - len(prefix) + 1)})).status_code == 401
    assert network["calls"] == []


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [301, 302, 307, 403, 429, 500, 503])
async def test_non_decision_statuses_are_retryable_not_forwarded_or_fallback(network, status):
    network["mint_status"] = status
    app, _ = application()
    response = await post(app, {"Authorization": "Bearer one"})
    assert response.status_code == 503 and response.headers["retry-after"] == "1"
    assert response.headers["cache-control"] == "no-store" and not response.headers.get_list("set-cookie")
    assert len(network["calls"]) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("body", [
    b'null', b'[]', b'{', b'{"ok":true,"expires_in":true}', b'{"ok":true,"expires_in":120.0}',
    b'{"ok":false,"expires_in":120}', b'{"ok":true,"expires_in":0}', b'{"ok":true,"expires_in":604801}',
    b'{"ok":true,"expires_in":120,"value":"must-not-forward"}',
    b'{"ok":true,"expires_in":119,"expires_in":120}', b' ' * 4097,
])
async def test_inexact_duplicate_or_oversized_body_is_unavailable(network, body):
    network["body"] = body
    app, _ = application()
    response = await post(app, {"Authorization": "Bearer one"})
    assert response.status_code == 503 and not response.headers.get_list("set-cookie")
    assert len(network["calls"]) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("case", ["missing", "extra", "mismatch", "domain", "no_http_only", "oversized", "wrong_signature", "wrong_family"])
async def test_only_exact_paired_signed_cookies_are_accepted(network, case):
    value = mint_bound_file_session_value(network["binding"](), SECRET)
    cookies = session_cookie_headers(value, ttl_seconds=120)
    if case == "missing":
        cookies.pop()
    elif case == "extra":
        cookies.append("other=value")
    elif case == "mismatch":
        cookies[1] = cookies[1].replace(value, value + "x")
    elif case == "domain":
        cookies[0] += "; Domain=authority.example"
    elif case == "no_http_only":
        cookies[0] = cookies[0].replace("; HttpOnly", "")
    elif case == "oversized":
        cookies[0] += "; " + "a" * 1024
    elif case == "wrong_signature":
        cookies = session_cookie_headers(value[:-1] + ("0" if value[-1] != "0" else "1"), ttl_seconds=120)
    else:
        network["kind"] = "guest"
    network["cookies"] = cookies
    app, _ = application()
    response = await post(app, {"X-Fingerprint-ID": "fingerprint"} if case == "wrong_family" else {"Authorization": "Bearer one"})
    assert response.status_code == 503 and not response.headers.get_list("set-cookie")
    assert len(network["calls"]) == 1


@pytest.mark.asyncio
async def test_upstream_refusal_query_cookie_compression_cache_and_transport_failures(network):
    app, _ = application()
    headers = {"Authorization": "Bearer one"}
    network["mint_status"] = 401
    assert (await post(app, headers)).status_code == 401
    network["mint_status"] = 200
    assert (await post(app, headers, path="/files/session?user_id=selector")).status_code == 401
    assert len(network["calls"]) == 1
    network["cache"] = "public"
    assert (await post(app, headers)).status_code == 503
    network["cache"] = "no-store"
    network["encoding"] = "br"
    assert (await post(app, headers)).status_code == 503
    network["encoding"] = None
    network["error"] = True
    response = await post(app, headers)
    assert response.status_code == 503 and "synthetic-private-transport-detail" not in response.text


@pytest.mark.asyncio
async def test_whole_mint_and_status_deadline_and_cancellation(network):
    app, _ = application(timeout=0.03)
    network["source_delay"] = 0.05
    assert (await post(app, {"Authorization": "Bearer one"})).status_code == 503
    network["delay"] = 0.05
    assert (await post(app, {"Authorization": "Bearer one"})).status_code == 503
    task = asyncio.create_task(post(app, {"Authorization": "Bearer one"}))
    await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


@pytest.mark.asyncio
@pytest.mark.parametrize("method,path", [("GET", "/files/session"), ("HEAD", "/files/session"), ("POST", "/files/session/"),
                                          ("POST", "/files/session-other"), ("POST", "/files/upload"), ("GET", "/files/id/download")])
async def test_neighbor_operations_keep_their_existing_handler(network, method, path):
    app, sink = application()
    async with ORIGINAL_CLIENT(transport=httpx.ASGITransport(app=app), base_url="https://files.example") as client:
        response = await client.request(method, path)
    assert response.status_code == 200
    assert sink.calls == [("http", method, path)] and network["calls"] == []


@pytest.mark.asyncio
async def test_missing_authority_and_key_cannot_mint(network):
    sink = OrdinaryApp()
    for mint_url, status_url in [(None, STATUS), (MINT, None)]:
        app = module.RemoteFileSessionMintMiddleware(sink, mint=module.RemoteFileSessionMint(mint_url, status_url, SECRET))
        assert (await post(app, {"Authorization": "Bearer one"})).status_code == 503
    for key in [b"", "not-bytes", None]:
        with pytest.raises(ValueError):
            module.RemoteFileSessionMint(MINT, STATUS, key)


@pytest.mark.asyncio
async def test_expiry_during_source_check_refuses_and_roundtrip_ttl_is_clamped(network, monkeypatch):
    app, _ = application()
    # The source callback completes before cookie generation, so elapsed time
    # must reduce the host's Max-Age even when upstream returned its original TTL.
    original = module.RemoteFileSessionResolver.__call__
    async def advance(self, credential):
        admitted = await original(self, credential)
        monkeypatch.setattr(module.time, "time", lambda: network["now"] + 7)
        return admitted
    monkeypatch.setattr(module.RemoteFileSessionResolver, "__call__", advance)
    response = await post(app, {"Authorization": "Bearer one"})
    assert response.status_code == 200 and response.json()["expires_in"] == 113
    assert response.headers.get_list("set-cookie") == session_cookie_headers(
        mint_bound_file_session_value(network["binding"](), SECRET), ttl_seconds=113)
    monkeypatch.setattr(module.time, "time", lambda: network["now"])
    async def expire(self, credential):
        admitted = await original(self, credential)
        monkeypatch.setattr(module.time, "time", lambda: credential.expires_at)
        return admitted
    monkeypatch.setattr(module.RemoteFileSessionResolver, "__call__", expire)
    response = await post(app, {"Authorization": "Bearer one"})
    assert response.status_code == 401 and not response.headers.get_list("set-cookie")


@pytest.mark.asyncio
async def test_source_outage_and_exact_body_size_limit(network):
    app, _ = application()
    base = b'{"ok":true,"expires_in":120}'
    network["body"] = base + b" " * (4096 - len(base))
    assert (await post(app, {"Authorization": "Bearer one"})).status_code == 200
    network["source_status"] = 503
    response = await post(app, {"Authorization": "Bearer one"})
    assert response.status_code == 503 and not response.headers.get_list("set-cookie")
    network["body"] += b" "
    network["calls"].clear()
    assert (await post(app, {"Authorization": "Bearer one"})).status_code == 503
    assert len(network["calls"]) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("scope_type", ["websocket", "lifespan"])
async def test_non_http_scopes_pass_through_without_authority(network, scope_type):
    calls = []
    async def sink(scope, receive, send):
        calls.append(scope)
    mint = module.RemoteFileSessionMint(MINT, STATUS, SECRET)
    app = module.RemoteFileSessionMintMiddleware(sink, mint=mint)
    scope = {"type": scope_type, "path": "/files/session", "method": "POST"}
    async def receive():
        return {}
    async def send(message):
        raise AssertionError("mint adapter must not produce a response")
    await app(scope, receive, send)
    assert calls == [scope] and network["calls"] == []
