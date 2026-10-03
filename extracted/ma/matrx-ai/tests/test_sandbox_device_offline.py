"""A desktop that is not connected to the relay is ONE honest, retryable error — never a 45 s
route-outage wait, and never a bare ``upstream_error``.

Break ``_is_device_offline`` (or drop its check from ``_request``) and the 503 falls into the
transient-outage loop: the first test then sees sleeps and a ``sandbox_unavailable`` error naming
an orchestrator restart, and fails.
"""

from __future__ import annotations

import httpx
import pytest

from matrx_ai.tools import _sandbox_proxy as proxy

pytestmark = pytest.mark.asyncio

DESKTOP = proxy.SandboxBinding(
    sandbox_id="mac-1",
    base_url="https://aidream.invalid/api/local-proxy/5b0c3a9e-8a51-4c2c-9d0e-1f2a3b4c5d6e",
    access_token="user-jwt",
    root_path="/Users/person",
    target_kind="local_machine",
)

OFFLINE = {
    "detail": {
        "code": "DEVICE_OFFLINE",
        "message": "the device is not connected",
        "retryable": True,
        "status": "device_offline",
    }
}


def _transport(monkeypatch: pytest.MonkeyPatch, handler) -> list[httpx.Request]:
    seen: list[httpx.Request] = []
    real = httpx.AsyncClient

    def wrapped(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return handler(request)

    monkeypatch.setattr(
        proxy.httpx, "AsyncClient", lambda **kw: real(transport=httpx.MockTransport(wrapped), **kw)
    )
    return seen


async def test_device_offline_is_one_retryable_error_without_waiting(monkeypatch) -> None:
    slept: list[float] = []

    async def no_sleep(seconds: float) -> None:
        slept.append(seconds)

    monkeypatch.setattr(proxy, "_sleep", no_sleep)
    seen = _transport(monkeypatch, lambda _r: httpx.Response(503, json=OFFLINE))

    with pytest.raises(proxy.SandboxProxyError) as raised:
        await proxy.exec_command(DESKTOP, "pwd")

    err = raised.value
    assert err.error_type == "device_offline"
    assert err.is_retryable is True
    assert err.status == 503
    assert err.suggested_action and "Matrx 2" in err.suggested_action
    assert len(seen) == 1 and slept == []


async def test_a_plain_503_is_still_a_route_outage(monkeypatch) -> None:
    """The offline check is narrow: an edge 503 keeps its transient retry."""
    calls = {"n": 0}

    def handler(_r: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(503, text="no available server")
        return httpx.Response(200, json={"exit_code": 0, "stdout": "", "stderr": "", "cwd": "/"})

    async def no_sleep(_s: float) -> None:
        return None

    monkeypatch.setattr(proxy, "_sleep", no_sleep)
    _transport(monkeypatch, handler)
    data = await proxy.exec_command(DESKTOP, "pwd")
    assert data["exit_code"] == 0 and calls["n"] == 2
