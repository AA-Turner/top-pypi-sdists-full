"""Hosted MCP transport: stateless sessions and edge token validation.

The hosted service runs multiple replicas behind a load balancer with no session
affinity, so anything held in one pod's memory is unreachable from the next request.
"""

from __future__ import annotations

import asyncio
import hashlib
import time

import httpx
import pytest
from mcp.server.transport_security import TransportSecuritySettings

from probe.mcp.server import create_server, with_auth_and_health


@pytest.fixture(autouse=True)
def _reset_verify_caches():
    """THREE pieces of module state on this path: both token-verdict caches and the
    per-loop httpx client. Leaking a cache makes a later test's /v1/me probe silently
    never fire; leaking the client hands the next test a stale mock the moment anything
    reuses a loop. Reset before AND after so an ordering change cannot resurrect it."""
    import probe.mcp.server as server

    server._verify_cache.clear()
    server._accept_cache.clear()
    server._verify_clients.clear()
    yield
    server._verify_cache.clear()
    server._accept_cache.clear()
    server._verify_clients.clear()

_INIT = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "0"},
    },
}
_LIST = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
_HEADERS = {
    "Authorization": "Bearer probe_pat_test",
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}
_OPEN = TransportSecuritySettings(
    enable_dns_rebinding_protection=False, allowed_hosts=["*"], allowed_origins=["*"]
)


def test_hosted_server_is_stateless() -> None:
    """A session would live in one pod's memory and 404 from every other replica."""
    assert create_server(transport_security=_OPEN).settings.stateless_http is True


def test_tools_list_works_without_a_session_id(service) -> None:
    """The multi-replica path: a follow-up request carries no session the pod knows.

    Statefully this is `400 Bad Request: Missing session ID` (and `Session not found`
    when the id came from a sibling pod) — the live failure this guards against.
    """

    async def run() -> tuple[int, str]:
        mcp = create_server(service, transport_security=_OPEN)
        mcp.settings.streamable_http_path = "/mcp"
        inner = mcp.streamable_http_app()
        async with inner.router.lifespan_context(inner):
            transport = httpx.ASGITransport(app=inner)
            async with httpx.AsyncClient(transport=transport, base_url="http://mcp.test") as c:
                first = await c.post("/mcp", json=_INIT, headers=_HEADERS)
                assert first.status_code == 200
                # Stateless issues no session id at all; there is nothing to lose.
                assert first.headers.get("mcp-session-id") is None
                second = await c.post("/mcp", json=_LIST, headers=_HEADERS)
                return second.status_code, second.text

    status, body = asyncio.run(run())
    assert status == 200
    assert '"tools"' in body
    assert "Missing session ID" not in body


@pytest.fixture
def service(client):
    from probe.mcp.service import ResearchReadService
    from probe.mcp.source import ResearchOSSource

    return ResearchReadService(ResearchOSSource(client))


# -- edge token verification -------------------------------------------------
async def _inner_ok(scope, receive, send) -> None:
    """Stands in for the MCP app: reaching it means the token passed the wrapper."""
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b'{"reached":true}'})


def _call(app, headers: list | None = None) -> dict:
    out: dict = {}

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(msg):
        if msg["type"] == "http.response.start":
            out["status"] = msg["status"]
            out["headers"] = {k.decode(): v.decode() for k, v in msg["headers"]}
        elif msg["type"] == "http.response.body":
            out["body"] = msg.get("body", b"")

    scope = {"type": "http", "method": "POST", "path": "/mcp", "headers": headers or []}
    asyncio.run(app(scope, receive, send))
    return out


@pytest.fixture
def hosted_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PROBE_MCP_OAUTH", "1")
    monkeypatch.setenv("PROBE_MCP_RESOURCE_URL", "https://mcp.test")
    monkeypatch.setenv("PROBE_MCP_AUTH_SERVER", "https://api.test")


def _bearer(token: str) -> list:
    return [(b"authorization", f"Bearer {token}".encode())]


def test_invalid_token_gets_401_not_a_200_tool_error(hosted_env) -> None:
    """A stale token must fail at the edge.

    Otherwise its tools load and every call fails inside an HTTP 200 — and the 401
    is what makes a client re-run its credential helper and retry.
    """

    async def rejects(token: str) -> bool:
        return True

    app = with_auth_and_health(_inner_ok, mcp_path="/mcp", token_rejected=rejects)
    res = _call(app, _bearer("probe_pat_revoked"))
    assert res["status"] == 401
    assert res["headers"]["www-authenticate"].startswith("Bearer ")
    assert b"reached" not in res["body"]


def test_valid_token_reaches_the_mcp_app(hosted_env) -> None:
    async def accepts(token: str) -> bool:
        return False

    app = with_auth_and_health(_inner_ok, mcp_path="/mcp", token_rejected=accepts)
    assert _call(app, _bearer("probe_pat_good"))["status"] == 200


def test_both_token_prefixes_are_accepted(hosted_env) -> None:
    """The prefix only discriminates; auth is a sha256 lookup. Legacy ros_pat_ lives."""
    seen: list[str] = []

    async def accepts(token: str) -> bool:
        seen.append(token)
        return False

    app = with_auth_and_health(_inner_ok, mcp_path="/mcp", token_rejected=accepts)
    for token in ("ros_pat_legacy", "probe_pat_current"):
        assert _call(app, _bearer(token))["status"] == 200
    assert seen == ["ros_pat_legacy", "probe_pat_current"]


# -- the real verifier ------------------------------------------------------
def _verifier_against(monkeypatch, *, status: int | None = None, exc: Exception | None = None):
    """Point _upstream_rejects at a mock transport instead of the live API."""
    import probe.mcp.server as server

    server._verify_cache.clear()

    def handle(request: httpx.Request) -> httpx.Response:
        if exc is not None:
            raise exc
        return httpx.Response(status, json={})

    real = httpx.AsyncClient

    class Mocked(real):
        def __init__(self, **kwargs):
            kwargs.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(handle), base_url="http://api.test", **kwargs
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)
    return server


@pytest.mark.parametrize(
    ("status", "exc", "rejected", "why"),
    [
        (200, None, False, "valid"),
        (401, None, True, "revoked"),
        (403, None, True, "forbidden"),
        (500, None, False, "server error must not disconnect everyone"),
        (None, httpx.ConnectError("down"), False, "API down must not disconnect everyone"),
        (None, httpx.ReadTimeout("slow"), False, "timeout must not disconnect everyone"),
    ],
)
def test_upstream_rejects_only_on_a_definitive_refusal(
    monkeypatch, status, exc, rejected, why
) -> None:
    """Fail closed on 401/403; fail open on everything else. `why` documents each case."""
    server = _verifier_against(monkeypatch, status=status, exc=exc)
    assert asyncio.run(server._upstream_rejects("probe_pat_x")) is rejected, why


def test_both_verdicts_are_cached_on_asymmetric_clocks(monkeypatch) -> None:
    """Rejections cache for a minute, acceptances for seconds. The asymmetry is the point.

    This REPLACES test_a_rejection_is_cached_but_an_acceptance_is_not, which pinned the
    old "never cache an accept" rule. That rule taxed every healthy user with a /v1/me
    round trip in front of every tool call. What caching an accept costs is bounded by
    _ACCEPT_TTL_SECONDS and is NOT data access -- the API authenticates every backend
    call behind this check -- it is a delayed 401, and with it a delayed client heal.
    See test_a_revoked_token_stops_working_once_the_accept_expires.
    """
    import probe.mcp.server as server

    calls: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        # 401 for the dead token, 200 for the live one.
        bad = request.headers["Authorization"].endswith("dead")
        return httpx.Response(401 if bad else 200, json={})

    real = httpx.AsyncClient

    class Mocked(real):
        def __init__(self, **kwargs):
            kwargs.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(handle), base_url="http://api.test", **kwargs
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)

    assert asyncio.run(server._upstream_rejects("probe_pat_dead")) is True
    assert asyncio.run(server._upstream_rejects("probe_pat_dead")) is True
    assert len(calls) == 1  # second rejection served from cache

    calls.clear()
    assert asyncio.run(server._upstream_rejects("probe_pat_live")) is False
    assert asyncio.run(server._upstream_rejects("probe_pat_live")) is False
    assert len(calls) == 1  # second acceptance served from cache too, now


def test_a_revoked_token_stops_working_once_the_accept_expires(monkeypatch) -> None:
    """The bound on caching an accept: revocation lands, it just lands a little later.

    Without this the accept cache would be indistinguishable from "revocation is
    ignored", which is the objection it has to answer.
    """
    import probe.mcp.server as server

    alive = {"ok": True}
    calls: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        return httpx.Response(200 if alive["ok"] else 401, json={})

    real = httpx.AsyncClient

    class Mocked(real):
        def __init__(self, **kwargs):
            kwargs.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(handle), base_url="http://api.test", **kwargs
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)

    assert asyncio.run(server._upstream_rejects("probe_pat_x")) is False
    alive["ok"] = False
    # Still accepted inside the window — this is the cost, stated as a test.
    assert asyncio.run(server._upstream_rejects("probe_pat_x")) is False
    assert len(calls) == 1

    # Expire the entry the way time would, and the revocation lands.
    key = hashlib.sha256(b"probe_pat_x").hexdigest()
    expires, identity = server._accept_cache[key]
    server._accept_cache[key] = (time.monotonic() - 1, identity)
    assert asyncio.run(server._upstream_rejects("probe_pat_x")) is True
    assert len(calls) == 2


def test_the_accept_cache_carries_the_caller_identity(monkeypatch) -> None:
    """/v1/me is called anyway; its body is what labels an accounting event."""
    import probe.mcp.server as server

    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json={"user_id": "u-1", "customer_id": "acme", "email": "a@b.c"}
        )

    real = httpx.AsyncClient

    class Mocked(real):
        def __init__(self, **kwargs):
            kwargs.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(handle), base_url="http://api.test", **kwargs
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)

    assert asyncio.run(server._upstream_rejects("probe_pat_x")) is False
    identity = server.identity_for_token("probe_pat_x")
    assert identity == {
        "distinct_id": "u-1",
        "customer_id": "acme",
        "workspace_id": None,
        "authenticated": True,
    }


def test_an_unparseable_200_is_still_a_valid_token(monkeypatch) -> None:
    """A body we cannot read must not turn a live token into a rejection."""
    import probe.mcp.server as server

    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"not json")

    real = httpx.AsyncClient

    class Mocked(real):
        def __init__(self, **kwargs):
            kwargs.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(handle), base_url="http://api.test", **kwargs
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)

    assert asyncio.run(server._upstream_rejects("probe_pat_x")) is False
    assert server.identity_for_token("probe_pat_x") is None


def test_a_transient_failure_caches_no_verdict(monkeypatch) -> None:
    """A blip must not be remembered as either answer."""
    import probe.mcp.server as server

    def handle(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("down")

    real = httpx.AsyncClient

    class Mocked(real):
        def __init__(self, **kwargs):
            kwargs.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(handle), base_url="http://api.test", **kwargs
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)

    assert asyncio.run(server._upstream_rejects("probe_pat_x")) is False
    assert server._accept_cache == {}
    assert server._verify_cache == {}


def test_rotating_past_a_cached_rejection_is_not_delayed(monkeypatch) -> None:
    """A cached rejection must not bleed onto the replacement token.

    Rotation is the moment this matters: the revoked token is cached as dead, and the
    new one has to be believed immediately or the heal stalls for the whole TTL.
    """
    import probe.mcp.server as server

    def handle(request: httpx.Request) -> httpx.Response:
        revoked = request.headers["Authorization"].endswith("old")
        return httpx.Response(401 if revoked else 200, json={})

    real = httpx.AsyncClient

    class Mocked(real):
        def __init__(self, **kwargs):
            kwargs.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(handle), base_url="http://api.test", **kwargs
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)
    server._verify_cache.clear()

    assert asyncio.run(server._upstream_rejects("probe_pat_old")) is True
    assert len(server._verify_cache) == 1  # the dead one is remembered
    assert asyncio.run(server._upstream_rejects("probe_pat_new")) is False  # and not inherited


def test_valid_plugin_version_headers_reach_the_backend_auth_probe(monkeypatch, hosted_env) -> None:
    """The MCP edge preserves only bounded telemetry alongside the bearer."""
    import probe.mcp.server as server

    seen: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={})

    real = httpx.AsyncClient

    class Mocked(real):
        def __init__(self, **kwargs):
            kwargs.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(handle),
                base_url="http://api.test",
                **kwargs,
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)
    server._verify_cache.clear()
    app = with_auth_and_health(
        _inner_ok,
        mcp_path="/mcp",
        token_rejected=server._upstream_rejects,
    )

    response = _call(
        app,
        _bearer("probe_pat_good")
        + [
            (b"x-probe-client", b"plugin"),
            (b"x-probe-client-version", b"0.7.0"),
        ],
    )

    assert response["status"] == 200
    assert seen[0].headers["X-Probe-Client"] == "plugin"
    assert seen[0].headers["X-Probe-Client-Version"] == "0.7.0"


@pytest.mark.parametrize(
    "metadata",
    [
        [(b"x-probe-client", b"plugin")],
        [
            (b"x-probe-client", b"unknown"),
            (b"x-probe-client-version", b"0.7.0"),
        ],
        [
            (b"x-probe-client", b"plugin"),
            (b"x-probe-client-version", b"latest"),
        ],
        [
            (b"x-probe-client", b"plugin"),
            (b"x-probe-client-version", b"0.7.0\nx-evil: yes"),
        ],
        [
            (b"x-probe-client", b"plugin"),
            (b"x-probe-client-version", b"\xff"),
        ],
    ],
)
def test_bad_mcp_client_metadata_is_ignored(monkeypatch, hosted_env, metadata) -> None:
    """Malformed telemetry never rejects a valid MCP bearer and is not forwarded."""
    import probe.mcp.server as server

    seen: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={})

    real = httpx.AsyncClient

    class Mocked(real):
        def __init__(self, **kwargs):
            kwargs.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(handle),
                base_url="http://api.test",
                **kwargs,
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)
    server._verify_cache.clear()
    app = with_auth_and_health(
        _inner_ok,
        mcp_path="/mcp",
        token_rejected=server._upstream_rejects,
    )

    assert _call(app, _bearer("probe_pat_good") + metadata)["status"] == 200
    assert "X-Probe-Client" not in seen[0].headers
    assert "X-Probe-Client-Version" not in seen[0].headers


def test_verification_disabled_wires_no_verifier(hosted_env) -> None:
    """PROBE_MCP_VERIFY_TOKEN=0 (set for the whole suite in conftest) skips the check.

    Nothing is injected here, so reaching the inner app proves no upstream call was
    attempted — the escape hatch self-hosters use to avoid the extra round-trip.
    """
    app = with_auth_and_health(_inner_ok, mcp_path="/mcp")
    assert _call(app, _bearer("probe_pat_unchecked"))["status"] == 200


# -- response accounting, end to end through the wrapper ---------------------
#
# The unit tests in test_mcp_accounting.py prove each piece. These prove the WIRING:
# that the wrapper actually counts the body it serves, that only tool-serving requests
# produce an event, and that measurement never becomes a failure mode of the request.


@pytest.fixture
def emitted(monkeypatch):
    from probe.mcp import accounting as accounting_mod

    # Opt IN to emission. `_telemetry_off` pins PROBE_TELEMETRY=off suite-wide and
    # `_telemetry_permitted()` fails closed on it, so without this every assertion
    # below would pass against an empty list -- the shape of green test that proves
    # nothing. Base URL must also satisfy the self-host egress gate.
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.setenv(accounting_mod.ANALYTICS_ENV, "1")
    """Capture what the accounting sender would have shipped."""
    from probe.mcp import accounting

    out: list[dict] = []
    sender = accounting._Sender()
    sender.put = out.append  # type: ignore[method-assign]
    monkeypatch.setattr(accounting, "_ensure_sender", lambda: sender)
    return out


def _inner_serving(tool: str, body: bytes):
    """An inner app that behaves like a tool call: names its tool, returns a payload."""
    from probe.mcp import accounting

    async def inner(scope, receive, send) -> None:
        accounting.note_tool(tool)
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": body})

    return inner


async def _accepts(token: str) -> bool:
    return False


def test_a_served_tool_call_is_counted_end_to_end(hosted_env, emitted, monkeypatch) -> None:
    import probe.mcp.server as server

    monkeypatch.setattr(server, "identity_for_token", lambda token: _IDENT)
    app = with_auth_and_health(
        _inner_serving("browse", b"x" * 1234),
        mcp_path="/mcp",
        token_rejected=_accepts,
    )
    res = _call(
        app,
        _bearer("probe_pat_good")
        + [
            (b"x-probe-agent", b"claude_code"),
            (b"x-probe-agent-session", b"385cbaab-3a35-4e8f-91d7-cc57826261e4"),
        ],
    )
    assert res["status"] == 200
    assert len(emitted) == 1
    props = emitted[0]["properties"]
    assert props["tool"] == "browse"
    assert props["response_bytes"] == 1234
    assert props["agent"] == "claude_code"
    assert props["agent_session_id"] == "385cbaab-3a35-4e8f-91d7-cc57826261e4"


_IDENT = {
    "distinct_id": "u-1",
    "customer_id": "acme",
    "workspace_id": None,
    "authenticated": True,
}


def test_a_request_that_serves_no_tool_is_not_counted(hosted_env, emitted) -> None:
    """initialize and tools/list ride this same path and are out of scope."""
    app = with_auth_and_health(_inner_ok, mcp_path="/mcp", token_rejected=_accepts)
    assert _call(app, _bearer("probe_pat_good"))["status"] == 200
    assert emitted == []


def test_healthz_is_never_counted(hosted_env, emitted) -> None:
    """Two kubelet probes every 10s across replicas. Counting them would bury real
    traffic under a noise floor nobody asked for."""
    app = with_auth_and_health(_inner_ok, mcp_path="/mcp", token_rejected=_accepts)

    out: dict = {}

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(msg):
        if msg["type"] == "http.response.start":
            out["status"] = msg["status"]

    asyncio.run(app({"type": "http", "method": "GET", "path": "/healthz", "headers": []}, receive, send))
    assert out["status"] == 200
    assert emitted == []


def test_an_unauthorized_request_is_not_counted(hosted_env, emitted) -> None:
    async def rejects(token: str) -> bool:
        return True

    app = with_auth_and_health(_inner_ok, mcp_path="/mcp", token_rejected=rejects)
    assert _call(app, _bearer("probe_pat_revoked"))["status"] == 401
    assert emitted == []


def test_a_missing_session_header_still_counts_the_bytes(hosted_env, emitted) -> None:
    """Old installed plugin copies never send the pair. Absent means no transcript
    link, not a dropped measurement — and that stays true indefinitely."""
    app = with_auth_and_health(
        _inner_serving("search_knowledge", b"y" * 10),
        mcp_path="/mcp",
        token_rejected=_accepts,
    )
    assert _call(app, _bearer("probe_pat_good"))["status"] == 200
    assert len(emitted) == 1
    props = emitted[0]["properties"]
    assert props["response_bytes"] == 10
    assert "agent_session_id" not in props


def test_a_broken_emitter_cannot_break_a_tool_call(hosted_env, monkeypatch) -> None:
    """Emission runs in the wrapper's finally. If it can raise, a measurement outage
    becomes an outage."""
    from probe.mcp import accounting

    def boom(*_a, **_k):
        raise RuntimeError("sender exploded")

    monkeypatch.setattr(accounting, "_ensure_sender", boom)
    app = with_auth_and_health(
        _inner_serving("browse", b"z" * 8),
        mcp_path="/mcp",
        token_rejected=_accepts,
    )
    res = _call(app, _bearer("probe_pat_good"))
    assert res["status"] == 200
    assert res["body"] == b"z" * 8


def test_the_verify_client_is_built_once_per_loop(monkeypatch) -> None:
    """The whole point of the shared client: one handshake, not one per tool call."""
    import probe.mcp.server as server

    built: list[int] = []

    class Mocked(httpx.AsyncClient):
        def __init__(self, **kw):
            built.append(1)
            kw.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(lambda r: httpx.Response(200, json={})),
                base_url="http://api.test",
                **kw,
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)

    async def two_calls():
        await server._upstream_rejects("probe_pat_a")
        await server._upstream_rejects("probe_pat_b")

    asyncio.run(two_calls())
    assert built == [1], "a handshake per tool call is exactly what this change removed"


def test_a_200_that_names_no_user_is_accepted_but_unattributed(monkeypatch) -> None:
    import probe.mcp.server as server

    class Mocked(httpx.AsyncClient):
        def __init__(self, **kw):
            kw.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(lambda r: httpx.Response(200, json={})),
                base_url="http://api.test",
                **kw,
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)
    assert asyncio.run(server._upstream_rejects("probe_pat_x")) is False
    assert server.identity_for_token("probe_pat_x") is None


@pytest.mark.parametrize("status", [404, 429, 500, 503])
def test_a_transient_upstream_fault_is_not_remembered_as_an_acceptance(
    monkeypatch, status
) -> None:
    """Fail open, yes -- a blip must not disconnect everyone. But do NOT cache it:
    that would turn one bad response into 15 seconds of 'everybody is authenticated'."""
    import probe.mcp.server as server

    class Mocked(httpx.AsyncClient):
        def __init__(self, **kw):
            kw.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(lambda r: httpx.Response(status, json={})),
                base_url="http://api.test",
                **kw,
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)
    assert asyncio.run(server._upstream_rejects("probe_pat_x")) is False
    assert server._accept_cache == {}


def test_the_accept_cache_evicts_the_oldest_instead_of_wiping(monkeypatch) -> None:
    """Clear-all eviction would collapse the hit rate to zero above the ceiling and
    release a synchronised herd of /v1/me calls -- the exact traffic the TTL removes."""
    import probe.mcp.server as server

    class Mocked(httpx.AsyncClient):
        def __init__(self, **kw):
            kw.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(
                    lambda r: httpx.Response(200, json={"user_id": "u", "customer_id": "c"})
                ),
                base_url="http://api.test",
                **kw,
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)

    async def fill():
        for i in range(server._VERIFY_CACHE_MAX + 5):
            await server._upstream_rejects(f"probe_pat_{i}")

    asyncio.run(fill())
    assert len(server._accept_cache) == server._VERIFY_CACHE_MAX
    # The most recent survives; the oldest was evicted one at a time, not en masse.
    newest = f"probe_pat_{server._VERIFY_CACHE_MAX + 4}"
    assert server.identity_for_token(newest) is not None
    assert server.identity_for_token("probe_pat_0") is None


def test_an_empty_bearer_takes_the_401_path(hosted_env) -> None:
    """`Authorization: Bearer ` parsed to "" rather than None, which is falsy -- so it
    skipped verification entirely and fell through to the server's own credential."""
    seen: list[str] = []

    async def rejects(token: str) -> bool:
        seen.append(token)
        return True

    app = with_auth_and_health(_inner_ok, mcp_path="/mcp", token_rejected=rejects)
    res = _call(app, [(b"authorization", b"Bearer ")])
    assert res["status"] == 401
    assert seen == [], "an empty bearer must never reach the verifier as a real token"


def test_a_tool_call_is_attributed_through_the_REAL_verifier(hosted_env, emitted, monkeypatch) -> None:
    """The seam that makes the whole feature work, end to end, with nothing stubbed
    between the /v1/me body and the emitted event.

    Every other test here either stubs `identity_for_token` or inherits conftest's
    `PROBE_MCP_VERIFY_TOKEN=0`, which sets `token_rejected` to None -- so the accept
    cache is never populated and `identity_for_token` returns None forever. If the
    wrapper ever passed a differently-shaped token than the one the verifier hashed,
    every event would silently emit `distinct_id: "unknown"` and the feature would be
    a false-green. Only this test would notice.
    """
    import probe.mcp.server as server

    monkeypatch.setenv("PROBE_MCP_VERIFY_TOKEN", "1")

    class Mocked(httpx.AsyncClient):
        def __init__(self, **kw):
            kw.pop("base_url", None)
            super().__init__(
                transport=httpx.MockTransport(
                    lambda r: httpx.Response(
                        200, json={"user_id": "u-42", "customer_id": "acme"}
                    )
                ),
                base_url="http://api.test",
                **kw,
            )

    monkeypatch.setattr(server.httpx, "AsyncClient", Mocked)

    app = with_auth_and_health(
        _inner_serving("browse", b"x" * 77), mcp_path="/mcp"
    )
    assert _call(app, _bearer("probe_pat_live"))["status"] == 200

    assert len(emitted) == 1
    entry = emitted[0]
    assert entry["distinct_id"] == "u-42", (
        "identity_for_token did not see the token the verifier hashed"
    )
    assert entry["properties"]["team"] == "acme"
    assert entry["properties"]["response_bytes"] == 77
