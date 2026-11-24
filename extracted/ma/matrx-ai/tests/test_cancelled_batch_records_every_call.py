"""A cancelled tool batch records a terminal outcome for EVERY call in it.

Release shift, 2026-11-07: ``execute_batch`` cancelled an archestra tool batch
and nothing recorded a failure — no FAIL trace row, no ledger row, no captured
error. In-flight calls closed their own row inside ``execute``; the calls still
queued behind a write chain (and any call cancelled before it reached
dispatch) simply vanished. Nothing fails silently: each unfinished call gets a
FAIL trace and a born-terminal ``cancelled`` row, the batch is captured once,
and the CancelledError still propagates.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai.tools import executor as executor_mod
from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult
from matrx_ai.tools.registry import ToolRegistry


def _executor() -> ToolExecutor:
    registry = ToolRegistry()
    registry.register(ToolDefinition(name="rulebook", side_effect_class="db_write"))
    registry.register(ToolDefinition(name="web_search", side_effect_class="read_only"))
    return ToolExecutor(registry=registry, lifecycle=object())  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_every_unfinished_call_in_a_cancelled_batch_is_recorded(monkeypatch):
    executor = _executor()
    traces: list[tuple[str, dict[str, Any]]] = []
    rejected: list[tuple[str, str, str]] = []
    captured: list[dict[str, Any]] = []
    started = asyncio.Event()

    async def fake_execute(name, arguments, ctx, client_tools=None, allowed_tools=None):
        if arguments.get("fast"):
            return {"id": ctx.call_id}, ToolResult(success=True, output={})
        started.set()
        await asyncio.sleep(10)  # in flight when the batch is cancelled
        return {}, ToolResult(success=True, output={})

    async def fake_log_rejected(ctx, *, tool_name, arguments, result, **_):
        rejected.append((ctx.call_id, tool_name, result.error.error_type))
        return "row"

    async def fake_capture(exc, *, kind, **fields):
        captured.append({"kind": kind, "exc": exc, **fields})

    def fake_db_log(event, **kwargs):
        traces.append((event, kwargs))

        async def _noop():
            return None

        return _noop()

    monkeypatch.setattr(executor, "execute", fake_execute)
    monkeypatch.setattr(executor.execution_logger, "log_rejected", fake_log_rejected)
    monkeypatch.setattr(executor_mod, "_db_log", fake_db_log)
    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error", fake_capture
    )

    calls = [
        {"name": "rulebook", "arguments": {"action": "a"}, "call_id": "c0"},  # in flight
        {"name": "rulebook", "arguments": {"action": "b"}, "call_id": "c1"},  # queued behind c0
        {"name": "web_search", "arguments": {"fast": True}, "call_id": "c2"},  # finished
    ]
    ctx = ToolContext(call_id="", tool_name="", user_id="u", request_id="r", conversation_id="conv")
    task = asyncio.create_task(executor.execute_batch(calls, ctx))
    await started.wait()
    await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    fails = {kw["call_id"]: kw for ev, kw in traces if ev == "FAIL"}
    assert set(fails) == {"c0", "c1"}, traces
    assert all(kw["err_type"] == "cancelled" for kw in fails.values())
    # The queued call never reached execute, so it had no row: it gets a terminal one.
    assert ("c1", "rulebook", "cancelled") in rejected
    assert len(captured) == 1 and captured[0]["kind"] == "tool_batch_cancelled"
    assert captured[0]["context"]["unfinished_call_ids"] == ["c0", "c1"]


@pytest.mark.asyncio
async def test_a_batch_cut_by_a_deploy_drain_records_its_calls_but_files_no_error(monkeypatch):
    """2026-11-16 / 2026-11-19: both ``tool_batch_cancelled`` rows were deploy drains, each
    already judged by its stream or the run reaper. The calls still get their FAIL traces."""
    from matrx_connect.streaming import run_tracking

    executor = _executor()
    traces: list[tuple[str, dict[str, Any]]] = []
    captured: list[dict[str, Any]] = []
    started = asyncio.Event()

    async def fake_execute(name, arguments, ctx, client_tools=None, allowed_tools=None):
        started.set()
        await asyncio.sleep(10)
        return {}, ToolResult(success=True, output={})

    async def fake_log_rejected(ctx, *, tool_name, arguments, result, **_):
        return "row"

    async def fake_capture(exc, *, kind, **fields):
        captured.append({"kind": kind})

    def fake_db_log(event, **kwargs):
        traces.append((event, kwargs))

        async def _noop():
            return None

        return _noop()

    monkeypatch.setattr(executor, "execute", fake_execute)
    monkeypatch.setattr(executor.execution_logger, "log_rejected", fake_log_rejected)
    monkeypatch.setattr(executor_mod, "_db_log", fake_db_log)
    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", fake_capture)
    monkeypatch.setattr(run_tracking, "_shutdown_probe", lambda: True)

    calls = [{"name": "rulebook", "arguments": {"action": "a"}, "call_id": "c0"}]
    ctx = ToolContext(call_id="", tool_name="", user_id="u", request_id="r", conversation_id="conv")
    task = asyncio.create_task(executor.execute_batch(calls, ctx))
    await started.wait()
    await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert [kw["call_id"] for ev, kw in traces if ev == "FAIL"] == ["c0"]
    assert captured == []
