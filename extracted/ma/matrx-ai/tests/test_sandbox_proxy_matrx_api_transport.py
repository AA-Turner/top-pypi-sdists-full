"""The sandbox proxy's HTTP transport is the matrx-api client; the policy around it is unchanged.

Breaks each test names (production change in ``matrx_ai.tools._sandbox_proxy``):

1. Drop ``RawPath`` around the in-box path (slashes become ``%2F``), lose a header,
   the query or the JSON body -> the first test fails.
2. Stop passing ``raw_errors=True`` (the client raises before the module sees the
   answer) or stop mapping the client's wrapped transport error back to the original
   ``httpx`` error -> the second and third tests fail.

Only the network is faked (``httpx.MockTransport``); the SUT owns URL building,
headers, status classification and every message asserted here.
"""

from __future__ import annotations

import httpx
import pytest

from matrx_ai.tools import _sandbox_proxy as proxy

pytestmark = pytest.mark.asyncio

BINDING = proxy.SandboxBinding(
    sandbox_id="sbx-abc123",
    base_url="https://orchestrator.invalid/sandboxes/sbx-abc123",
    access_token="tok-1",
)


_REAL_CLIENT = httpx.AsyncClient


def _install(monkeypatch: pytest.MonkeyPatch, handler) -> list[httpx.Request]:
    seen: list[httpx.Request] = []

    def wrapped(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return handler(request)

    def factory(*args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(wrapped)
        return _REAL_CLIENT(*args, **kwargs)

    monkeypatch.setattr(proxy.httpx, "AsyncClient", factory)
    return seen


@pytest.fixture
def no_wait(monkeypatch: pytest.MonkeyPatch):
    original = proxy.get_transient_retry_budget_seconds()
    proxy.configure_sandbox_transient_retry(budget_seconds=0)

    async def no_sleep(_s: float) -> None:
        return None

    monkeypatch.setattr(proxy, "_sleep", no_sleep)
    yield
    proxy.configure_sandbox_transient_retry(budget_seconds=original)


async def test_the_real_request_keeps_slashes_headers_query_and_body(monkeypatch) -> None:
    seen = _install(monkeypatch, lambda _r: httpx.Response(200, json={"ok": True}))

    await proxy._request(
        BINDING,
        "GET",
        "/fs/dir/sub/list",
        params={"path": "/home/agent/a b", "limit": 5, "all": True},
        extra_headers={"X-Extra": "yes"},
    )
    await proxy._request(BINDING, "PUT", "/fs/write", json={"path": "/x", "content": "hi"})
    await proxy._request(BINDING, "POST", "/exec", json={"command": "ls"})

    listing, write, run = seen
    assert listing.url.raw_path.decode().startswith("/sandboxes/sbx-abc123/fs/dir/sub/list?")
    assert "%2F" not in listing.url.path
    assert dict(listing.url.params) == {"path": "/home/agent/a b", "limit": "5", "all": "true"}
    assert listing.headers["X-Sandbox-Access-Token"] == "tok-1"
    assert listing.headers["Content-Type"] == "application/json"
    assert listing.headers["X-Extra"] == "yes"
    assert write.method == "PUT"
    assert write.url.path == "/sandboxes/sbx-abc123/fs/write"
    assert write.read() == b'{"path":"/x","content":"hi"}'
    # /exec has no generated operation: it keeps the raw call to the same URL.
    assert run.url == httpx.URL("https://orchestrator.invalid/sandboxes/sbx-abc123/exec")
    assert run.headers["X-Sandbox-Access-Token"] == "tok-1"


async def test_a_503_body_and_a_404_reach_the_existing_error_mapping(monkeypatch, no_wait) -> None:
    _install(monkeypatch, lambda _r: httpx.Response(503, text="no available server"))
    with pytest.raises(proxy.SandboxProxyError) as outage:
        await proxy._request(BINDING, "GET", "/fs/stat", params={"path": "/a"})
    assert outage.value.error_type == "sandbox_unavailable"
    assert "HTTP 503: no available server" in str(outage.value)

    _install(monkeypatch, lambda _r: httpx.Response(404, json={"detail": "nope"}))
    with pytest.raises(proxy.SandboxProxyError) as missing:
        await proxy._request(BINDING, "GET", "/fs/stat", params={"path": "/home/agent/gone.txt"})
    assert missing.value.status == 404
    assert str(missing.value) == "Not found: /home/agent/gone.txt"

    _install(monkeypatch, lambda _r: httpx.Response(500, text="boom"))
    with pytest.raises(proxy.SandboxProxyError) as failed:
        await proxy._request(BINDING, "POST", "/search/content", json={"q": "x"})
    assert failed.value.error_type == "upstream_error"
    assert "Sandbox call failed (500): boom" in str(failed.value)


async def test_transport_failures_keep_their_original_classification(monkeypatch, no_wait) -> None:
    def read_timeout(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow", request=request)

    _install(monkeypatch, read_timeout)
    # A read timeout on a POST is never replayed: the plain timeout message.
    with pytest.raises(proxy.SandboxProxyError) as timed_out:
        await proxy._request(BINDING, "POST", "/search/paths", json={}, timeout=7.0)
    assert timed_out.value.error_type == "timeout"
    assert str(timed_out.value) == "Sandbox call timed out after 7.0s"

    def broken(request: httpx.Request) -> httpx.Response:
        raise httpx.DecodingError("garbled", request=request)

    _install(monkeypatch, broken)
    with pytest.raises(proxy.SandboxProxyError) as unreachable:
        await proxy._request(BINDING, "GET", "/fs/list")
    assert unreachable.value.error_type == "unreachable"
    assert "Sandbox unreachable" in str(unreachable.value)

    def refused(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    _install(monkeypatch, refused)
    # A connect failure is the transient class even for a POST (nothing was delivered).
    with pytest.raises(proxy.SandboxProxyError) as down:
        await proxy._request(BINDING, "POST", "/fs/mkdir", json={"path": "/d"})
    assert down.value.error_type == "sandbox_unavailable"
