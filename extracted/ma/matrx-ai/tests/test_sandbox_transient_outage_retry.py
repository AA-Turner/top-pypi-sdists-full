"""A sandbox ROUTE outage must cost ONE waited call, never eight wasted turns.

The break each test names is a production change in
``matrx_ai.tools._sandbox_proxy._request``:

1. Stop retrying a non-migrating 503 → the first test fails (the call errors
   instead of returning the daemon's payload).
2. Let an exhausted budget raise the old bare ``upstream_error`` (or keep
   retrying past the budget) → the second test fails.
3. Widen the transient class to any 4xx/5xx → the third test fails (a 400 gets
   replayed, and a bad request is replayed against the box).

The SUT owns: classifying the response, the backoff schedule, the budget
deadline, the retry count it reports, and the exact error it produces. The only
stubbed dependency is the network (``httpx.MockTransport``) and the clock —
``_now``/``_sleep`` are seams, so a 45s budget is proven in milliseconds.
"""

from __future__ import annotations

import httpx
import pytest

from matrx_ai.tools import _sandbox_proxy as proxy

pytestmark = pytest.mark.asyncio

BINDING = proxy.SandboxBinding(
    sandbox_id="sbx-5515667942bd",
    base_url="https://orchestrator.invalid/sandboxes/sbx-5515667942bd",
    access_token="token",
    root_path="/home/agent",
)

# Verbatim Traefik body from the 2026-09-13 06:40:45Z ledger (the value comes
# from outside the code: it is what the live edge proxy actually returned).
TRAEFIK_503 = "no available server"


class _Clock:
    """Fake monotonic clock: only a slept second passes."""

    def __init__(self) -> None:
        self.t = 1_000.0
        self.slept: list[float] = []

    def now(self) -> float:
        return self.t

    async def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.t += seconds


@pytest.fixture
def clock(monkeypatch: pytest.MonkeyPatch) -> _Clock:
    c = _Clock()
    monkeypatch.setattr(proxy, "_now", c.now)
    monkeypatch.setattr(proxy, "_sleep", c.sleep)
    return c


@pytest.fixture
def budget(monkeypatch: pytest.MonkeyPatch):
    original = proxy.get_transient_retry_budget_seconds()

    def _set(seconds: float) -> None:
        proxy.configure_sandbox_transient_retry(budget_seconds=seconds)

    yield _set
    proxy.configure_sandbox_transient_retry(budget_seconds=original)


def _install_transport(monkeypatch: pytest.MonkeyPatch, handler) -> list[httpx.Request]:
    """Route every proxy call through a fake transport; record the requests."""
    seen: list[httpx.Request] = []
    real_client = httpx.AsyncClient

    def _wrapped(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return handler(request)

    def factory(*args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(_wrapped)
        return real_client(*args, **kwargs)

    monkeypatch.setattr(proxy.httpx, "AsyncClient", factory)
    return seen


async def test_route_outage_is_waited_out_and_the_call_succeeds(
    monkeypatch: pytest.MonkeyPatch, clock: _Clock, budget
) -> None:
    """Two Traefik 503s then a real payload → the agent sees only the payload."""
    budget(45.0)
    responses = [
        httpx.Response(503, text=TRAEFIK_503),
        httpx.Response(503, text=TRAEFIK_503),
        httpx.Response(
            200, json={"exit_code": 0, "stdout": "hi\n", "stderr": "", "cwd": "/home/agent"}
        ),
    ]
    seen = _install_transport(monkeypatch, lambda request: responses.pop(0))

    result = await proxy.exec_command(BINDING, "echo hi")

    assert result["exit_code"] == 0
    assert result["stdout"] == "hi\n"
    assert result["transient_retries"] == 2
    assert proxy.last_transient_retries() == 2
    assert len(seen) == 3
    # Capped exponential backoff, starting at 1s and doubling.
    assert clock.slept == [1.0, 2.0]


async def test_a_clean_call_reports_zero_retries_and_no_stamp(
    monkeypatch: pytest.MonkeyPatch, clock: _Clock, budget
) -> None:
    """Second forcing input: no outage → no waiting, no stamp, zero retries."""
    budget(45.0)
    _install_transport(
        monkeypatch,
        lambda request: httpx.Response(
            200, json={"exit_code": 7, "stdout": "", "stderr": "boom", "cwd": "/home/agent"}
        ),
    )

    result = await proxy.exec_command(BINDING, "false")

    assert result["exit_code"] == 7
    assert "transient_retries" not in result
    assert proxy.last_transient_retries() == 0
    assert clock.slept == []


async def test_exhausted_budget_raises_one_honest_sandbox_unavailable(
    monkeypatch: pytest.MonkeyPatch, clock: _Clock, budget
) -> None:
    """A 503 that never clears → ONE retryable error carrying the wait-once rule."""
    budget(3.0)
    seen = _install_transport(monkeypatch, lambda request: httpx.Response(503, text=TRAEFIK_503))

    with pytest.raises(proxy.SandboxProxyError) as caught:
        await proxy.exec_command(BINDING, "echo hi")

    exc = caught.value
    assert exc.error_type == "sandbox_unavailable"
    assert exc.is_retryable is True
    message = str(exc)
    assert (
        "wait about a minute, then retry this exact command ONCE; if it fails "
        "again, stop and tell the user the sandbox is unreachable" in message
    )
    assert "files are intact" in message
    assert "orchestrator restart or deploy" in message
    assert exc.suggested_action and "ONCE" in exc.suggested_action
    # The budget really bounds the wait: 1s + 2s, then stop.
    assert clock.slept == [1.0, 2.0]
    assert len(seen) == 3
    assert proxy.last_transient_retries() == 2


async def test_a_connect_error_is_the_same_class(
    monkeypatch: pytest.MonkeyPatch, clock: _Clock, budget
) -> None:
    """A dead route also shows up as a refused connection — same one class."""
    budget(45.0)
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            raise httpx.ConnectError("All connection attempts failed", request=request)
        return httpx.Response(200, json={"entries": []})

    _install_transport(monkeypatch, handler)

    out = await proxy.fs_list(BINDING, "/home/agent")

    assert out == {"entries": []}
    assert proxy.last_transient_retries() == 1
    assert clock.slept == [1.0]


async def test_a_4xx_is_never_retried(
    monkeypatch: pytest.MonkeyPatch, clock: _Clock, budget
) -> None:
    """A bad request is the agent's fault, not the route's — surface it at once."""
    budget(45.0)
    seen = _install_transport(monkeypatch, lambda request: httpx.Response(400, text="bad command"))

    with pytest.raises(proxy.SandboxProxyError) as caught:
        await proxy.exec_command(BINDING, "echo hi")

    assert caught.value.error_type == "upstream_error"
    assert caught.value.is_retryable is False
    assert len(seen) == 1
    assert clock.slept == []


async def test_a_migrating_503_keeps_its_own_long_retry(
    monkeypatch: pytest.MonkeyPatch, clock: _Clock, budget
) -> None:
    """The image-swap path is untouched: it waits minutes, not the short budget."""
    budget(3.0)
    responses = [
        httpx.Response(503, json={"detail": {"status": "migrating"}}, headers={"Retry-After": "4"}),
        httpx.Response(503, json={"detail": {"status": "migrating"}}, headers={"Retry-After": "4"}),
        httpx.Response(200, json={"ok": True}),
    ]
    _install_transport(monkeypatch, lambda request: responses.pop(0))

    out = await proxy.fs_stat(BINDING, "/home/agent")

    assert out == {"ok": True}
    # Migration backoff is Retry-After capped at 5s, and it outlasts the short
    # transient budget by design.
    assert clock.slept == [4.0, 4.0]
    assert proxy.last_transient_retries() == 0
