"""A run bound to a PARKED computer wakes it at the first call that needs it, never at arm time.

The host arms a run on a parked machine with a binding that names the machine but carries no
endpoint (``wake_on_first_use``). Nothing wakes while the run is armed or while the agent only
talks; the first proxied call (shell, file, git) asks the host-injected waker for the live
endpoint, concurrent first calls share that one wake, a failed wake is a clear tool error, and a
binding that already carries an endpoint never calls the waker.

The waker is the only external dependency (the host's machine control plane); the HTTP transport
is replaced at ``_send_raw`` so the test reads which endpoint and token each call really used.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from matrx_connect import AppContext
from matrx_connect.context.app_context import set_app_context

from matrx_ai import _ext
from matrx_ai.tools import _sandbox_proxy as proxy
from matrx_ai.tools.streaming import CURRENT_TOOL_STREAM

PARKED = {
    "sandbox_id": "cc-parked",
    "root_path": "/home/browser-worker",
    "target_kind": "sandbox",
    "working_dir": "/home/browser-worker/chats/c1",
    "wake_on_first_use": True,
}


class _Waker:
    """Wakes the machine (slowly, so concurrent first calls overlap) and answers its endpoint."""

    def __init__(self, *, fail: bool = False, delay: float = 0.05) -> None:
        self.calls: list[dict[str, object]] = []
        self.fail = fail
        self.delay = delay

    async def __call__(self, **kwargs: object) -> dict[str, str]:
        self.calls.append(kwargs)
        await asyncio.sleep(self.delay)
        if self.fail:
            raise RuntimeError("too_many_running: 3 machines already run")
        return {
            "sandbox_id": "cc-parked",
            "base_url": "http://10.0.0.5:8002/agent",
            "access_token": "machine-token",
            "root_path": "/home/browser-worker",
            "working_dir": "/home/browser-worker/chats/c1",
        }


@pytest.fixture
def sent(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, str]]:
    seen: list[tuple[str, str]] = []

    async def send_raw(method, url, *, params, json, call_timeout, headers):
        seen.append((url, headers["X-Sandbox-Access-Token"]))
        return SimpleNamespace(
            status_code=200,
            json=lambda: {"exit_code": 0, "stdout": "ok", "stderr": "", "cwd": "/"},
            headers={},
            text="",
        )

    monkeypatch.setattr(proxy, "_send_raw", send_raw)
    return seen


def _arm(waker: _Waker | None, monkeypatch: pytest.MonkeyPatch, *, request_id: str = "run-1") -> AppContext:
    monkeypatch.setattr(_ext, "get_sandbox_binding_waker", lambda: waker)
    proxy._WAKES.clear()
    ctx = AppContext(
        emitter=AsyncMock(),
        user_id="person",
        organization_id="org",
        conversation_id="c1",
        request_id=request_id,
        metadata={"active_sandbox": dict(PARKED)},
    )
    set_app_context(ctx)
    return ctx


def test_arming_and_reading_the_binding_wakes_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    # Breaks caught: a parked binding read as "no binding" (the tools would fall to the
    # emulated filesystem), or reading it waking the machine.
    waker = _Waker()
    _arm(waker, monkeypatch)
    binding = proxy.get_active_sandbox()
    assert binding is not None and binding.wake_on_first_use
    assert binding.sandbox_id == "cc-parked" and binding.default_dir == PARKED["working_dir"]
    assert waker.calls == []


async def test_the_first_call_wakes_once_and_reaches_the_woken_machine(
    monkeypatch: pytest.MonkeyPatch, sent: list[tuple[str, str]]
) -> None:
    waker = _Waker()
    _arm(waker, monkeypatch)
    binding = proxy.get_active_sandbox()
    assert binding is not None
    await proxy.exec_command(binding, "ls")
    await proxy.exec_command(binding, "pwd")
    assert len(waker.calls) == 1
    assert waker.calls[0]["sandbox_id"] == "cc-parked"
    assert waker.calls[0]["user_id"] == "person" and waker.calls[0]["conversation_id"] == "c1"
    assert sent == [
        ("http://10.0.0.5:8002/agent/exec", "machine-token"),
        ("http://10.0.0.5:8002/agent/exec", "machine-token"),
    ]


async def test_concurrent_first_calls_share_one_wake(
    monkeypatch: pytest.MonkeyPatch, sent: list[tuple[str, str]]
) -> None:
    waker = _Waker(delay=0.1)
    _arm(waker, monkeypatch)
    binding = proxy.get_active_sandbox()
    assert binding is not None
    await asyncio.gather(*(proxy.exec_command(binding, f"echo {i}") for i in range(3)))
    assert len(waker.calls) == 1
    assert len(sent) == 3 and {url for url, _ in sent} == {"http://10.0.0.5:8002/agent/exec"}


async def test_a_failed_wake_is_a_clear_tool_error_and_the_next_call_tries_again(
    monkeypatch: pytest.MonkeyPatch, sent: list[tuple[str, str]]
) -> None:
    waker = _Waker(fail=True)
    _arm(waker, monkeypatch)
    binding = proxy.get_active_sandbox()
    assert binding is not None
    with pytest.raises(proxy.SandboxProxyError) as failed:
        await proxy.exec_command(binding, "ls")
    assert failed.value.error_type == "sandbox_unavailable"
    assert "could not be woken" in str(failed.value) and "too_many_running" in str(failed.value)
    assert sent == []  # never sent anywhere
    with pytest.raises(proxy.SandboxProxyError):
        await proxy.exec_command(binding, "ls")
    assert len(waker.calls) == 2  # a failure is never cached as the run's answer


async def test_without_a_host_waker_the_call_says_so(
    monkeypatch: pytest.MonkeyPatch, sent: list[tuple[str, str]]
) -> None:
    _arm(None, monkeypatch)
    binding = proxy.get_active_sandbox()
    assert binding is not None
    with pytest.raises(proxy.SandboxProxyError) as failed:
        await proxy.exec_command(binding, "ls")
    assert failed.value.error_type == "sandbox_unavailable" and sent == []


async def test_the_wake_is_announced_on_the_calls_own_stream(
    monkeypatch: pytest.MonkeyPatch, sent: list[tuple[str, str]]
) -> None:
    waker = _Waker()
    _arm(waker, monkeypatch)
    stream = SimpleNamespace(progress=AsyncMock())
    token = CURRENT_TOOL_STREAM.set(stream)  # type: ignore[arg-type]
    try:
        binding = proxy.get_active_sandbox()
        assert binding is not None
        await proxy.exec_command(binding, "ls")
    finally:
        CURRENT_TOOL_STREAM.reset(token)
    messages = [c.args[0] for c in stream.progress.await_args_list]
    assert any("Waking your Cloud Computer" in m for m in messages)


async def test_another_run_wakes_for_itself(
    monkeypatch: pytest.MonkeyPatch, sent: list[tuple[str, str]]
) -> None:
    # The woken endpoint belongs to ONE actor and ONE run, never the process.
    waker = _Waker()
    _arm(waker, monkeypatch, request_id="run-1")
    await proxy.exec_command(proxy.get_active_sandbox(), "ls")  # type: ignore[arg-type]
    set_app_context(
        AppContext(
            emitter=AsyncMock(), user_id="person", conversation_id="c1", request_id="run-2",
            metadata={"active_sandbox": dict(PARKED)},
        )
    )
    await proxy.exec_command(proxy.get_active_sandbox(), "ls")  # type: ignore[arg-type]
    assert len(waker.calls) == 2


async def test_a_live_binding_never_calls_the_waker(
    monkeypatch: pytest.MonkeyPatch, sent: list[tuple[str, str]]
) -> None:
    waker = _Waker()
    ctx = _arm(waker, monkeypatch)
    live = {**PARKED, "wake_on_first_use": False, "base_url": "https://live/agent", "access_token": "t"}
    set_app_context(ctx.with_overrides(metadata={"active_sandbox": live}))
    binding = proxy.get_active_sandbox()
    assert binding is not None and not binding.wake_on_first_use
    await proxy.exec_command(binding, "ls")
    assert waker.calls == [] and sent == [("https://live/agent/exec", "t")]


async def test_a_call_with_no_run_identity_never_reuses_a_settled_wake(
    monkeypatch: pytest.MonkeyPatch, sent: list[tuple[str, str]]
) -> None:
    # Break caught: with neither request_id nor execution_id the key fell back to
    # (person, "", machine), so a woken endpoint served EVERY run-less call for 30 minutes —
    # after the machine slept meanwhile, calls went to a dead address. With no run identity a
    # call shares only a wake still in flight; the next call asks the host again (which answers
    # the live endpoint, or wakes the machine if it slept).
    waker = _Waker(delay=0.1)
    _arm(waker, monkeypatch, request_id="")
    binding = proxy.get_active_sandbox()
    assert binding is not None
    await asyncio.gather(*(proxy.exec_command(binding, f"echo {i}") for i in range(3)))
    assert len(waker.calls) == 1  # concurrent calls still share one wake
    await proxy.exec_command(binding, "ls")
    assert len(waker.calls) == 2  # a settled wake is never handed to a later run-less call
    assert proxy._WAKES == {}
