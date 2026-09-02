"""Regression for the tool-completion persistence contract (2026-06-20).

``ToolExecutor._persist_tool_outcome`` is the single funnel for the
``log_completed`` / ``log_error`` write fired after a tool returns. The
contract it enforces is the fix for the ``agent_call`` lost-completion bug:

* WITH a request coordinator (the in-request path) the write is a purely
  IN-MEMORY ``coordinator.queue()`` (no DB I/O), so it runs INLINE and
  synchronously — the UPDATE is in the coordinator's Session BEFORE the tool
  returns, coalescing/flushing deterministically at the barrier. Fire-and-forget
  here is what lost ``agent_call``'s completion: its ``child_agent_context``
  force-finalizes the parent coordinator (pre_fan_out), splitting the row's
  INSERT off from the UPDATE, and the detached UPDATE then raced the request's
  drain+seal and was dropped → row stuck 'running' → watchdog 'error' → 400.

* WITHOUT a coordinator (a true out-of-request background dispatch) the write
  IS a real DB UPDATE that runs in a fresh contextvars Context so it does not
  dispatch onto a parent transaction connection. The isolated task is awaited
  so short-lived CLIs cannot exit before the terminal ledger write lands.

These tests pin exactly that branch behavior, so a revert to unconditional
``detached_task`` (reintroducing the race) fails loudly.
"""

from __future__ import annotations

import contextvars
import types

import pytest

from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.logger import ToolExecutionLogger


@pytest.mark.asyncio
async def test_completion_write_runs_inline_when_coordinator_present():
    """With a coordinator, the completion coroutine must run synchronously
    (inline) — it is in the coordinator's Session by the time the call returns."""
    ran: list[str] = []

    async def _write():
        ran.append("done")

    # _persist_tool_outcome doesn't touch self; an empty stand-in is enough.
    self_stub = types.SimpleNamespace()

    await ToolExecutor._persist_tool_outcome(
        self_stub, _write(), coordinator=object(), name="tool_log_completed"
    )

    # Ran INLINE — the in-memory coord.queue() happened before we got control
    # back, so the UPDATE is guaranteed present for the next barrier flush.
    assert ran == ["done"]


@pytest.mark.asyncio
async def test_completion_write_is_isolated_and_awaited_when_no_coordinator():
    """The DB write gets a fresh Context and is terminal before return."""
    marker = contextvars.ContextVar("tool_completion_marker", default="fresh")
    marker.set("parent")
    ran: list[str] = []

    async def _write():
        ran.append(marker.get())

    self_stub = types.SimpleNamespace()

    await ToolExecutor._persist_tool_outcome(
        self_stub, _write(), coordinator=None, name="tool_log_completed"
    )

    assert ran == ["fresh"]


@pytest.mark.asyncio
async def test_inline_completion_failure_never_breaks_dispatch():
    """A failing completion write (inline path) must be swallowed — telemetry
    can never propagate an exception into the tool dispatch return path."""

    async def _boom():
        raise RuntimeError("simulated completion-write failure")

    self_stub = types.SimpleNamespace()

    # Must not raise.
    await ToolExecutor._persist_tool_outcome(
        self_stub, _boom(), coordinator=object(), name="tool_log_completed"
    )


@pytest.mark.asyncio
async def test_cancel_terminal_update_carries_captured_coordinator(monkeypatch):
    """Cancellation cleanup must not depend on ambient ContextVars surviving."""
    captured: dict[str, object] = {}
    coordinator = object()

    async def _capture_update(row_id, data, *, coordinator=None):
        captured.update(row_id=row_id, data=data, coordinator=coordinator)

    logger = ToolExecutionLogger()
    monkeypatch.setattr(logger, "_update_row", _capture_update)

    await logger.log_abandoned("tool-row", coordinator=coordinator)

    assert captured["row_id"] == "tool-row"
    assert captured["coordinator"] is coordinator
    assert captured["data"]["status"] == "error"
