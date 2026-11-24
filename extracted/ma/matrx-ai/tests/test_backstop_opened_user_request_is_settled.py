"""Forcing-function: a chat.user_request the ToolLogger backstop OPENS, it also CLOSES.

Live class (LifecycleWatchdogAlarm ``chat.user_request: N stuck row(s), predicate
status='pending'``, 406 alarms by 2026-11-04): a direct tool call with no chat/agent
boundary — an operator script under ``system_app_context("script.render_incidents")``,
a harness, an MCP tool door — reaches ``ToolExecutionLogger.log_started``, whose FK
backstop ``_ensure_tool_call_parents`` creates the parent ``chat.user_request`` as
'pending'. Nothing ever settled it: 53 render_incidents rows (each with its tool_call,
iterations=0, no chat.request) sat pending until the watchdog abandoned them.

Gut check: drop the settle calls from ``log_completed`` / ``log_error`` /
``log_rejected`` (or have ``ensure_user_request_exists`` stop reporting a birth) and
the first three tests fail; settle a request a boundary opened and the last one fails.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate
from matrx_ai.tools import logger as logger_mod
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolError, ToolResult, ToolType


@pytest.fixture
def harness(monkeypatch):
    gate._ensured_request_ids.clear()
    logger_mod._BACKSTOP_OPENED_REQUESTS.clear()
    logger_mod._BACKSTOP_REQUEST_BY_ROW.clear()

    on_disk: set[str] = set()
    settled: list[tuple[str, str, str | None]] = []

    async def _no_store(request_id, user_id):
        return False

    class _FakeUR:
        async def filter_user_requests(self, id):  # noqa: A002 - mirrors real kwarg
            return [SimpleNamespace(id=id)] if id in on_disk else []

    async def _create(*, request_id, user_id):
        on_disk.add(request_id)
        return True

    async def _ensure_conversation(*, conversation_id, user_id):
        return None

    async def _update_status(request_id, status, error=None):
        settled.append((request_id, status, error))

    monkeypatch.setattr(gate, "_store_pending_user_request", _no_store)
    monkeypatch.setattr(gate, "_cxm", lambda: type("M", (), {"user_request": _FakeUR()})())
    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    monkeypatch.setattr(gate, "_get_coordinator", lambda: None)
    monkeypatch.setattr(gate, "_create_user_request", _create)
    monkeypatch.setattr(gate, "ensure_conversation_exists", _ensure_conversation)
    monkeypatch.setattr(gate, "update_user_request_status", _update_status)
    monkeypatch.setattr("matrx_ai.providers.usage_gate.precheck_usage", lambda config=None: None)

    queued: list[dict] = []
    monkeypatch.setattr(logger_mod, "_should_persist_tool_call", lambda: True)
    coord = SimpleNamespace(_request_id=None, set_correlation=lambda **kw: None)
    monkeypatch.setattr(logger_mod, "_get_coordinator", lambda: coord)
    monkeypatch.setattr(logger_mod, "_queue_tool_call_create", lambda **kw: queued.append(kw) or "op")

    async def _write_ahead(*args, **kwargs):
        return None

    async def _update_row(self, row_id, data, *, coordinator=None):
        return None

    monkeypatch.setattr(logger_mod, "_write_ahead", _write_ahead)
    monkeypatch.setattr(ToolExecutionLogger, "_update_row", _update_row)
    monkeypatch.setattr(ToolExecutionLogger, "_stamp_run_link", lambda self, data: None)
    monkeypatch.setattr(logger_mod, "_cx_tool_call_supports_as_called", lambda: False)
    monkeypatch.setattr(logger_mod, "stamp_row_owner", lambda data, _uid: data)
    monkeypatch.setattr(logger_mod, "try_get_tracker", lambda: None)

    request_id, user_id = str(uuid4()), str(uuid4())
    app_ctx = SimpleNamespace(
        user_id=user_id, conversation_id=None, request_id=request_id, store=True, metadata={}, emitter=None
    )
    monkeypatch.setattr("matrx_ai.context.app_context.get_app_context", lambda: app_ctx)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: app_ctx)

    yield SimpleNamespace(
        request_id=request_id, user_id=user_id, on_disk=on_disk, settled=settled, queued=queued
    )
    gate._ensured_request_ids.clear()
    logger_mod._BACKSTOP_OPENED_REQUESTS.clear()
    logger_mod._BACKSTOP_REQUEST_BY_ROW.clear()


_TOOL = ToolDefinition(
    name="kindcomp_get_context",
    description="test",
    parameters={"type": "object", "properties": {}},
    tool_type=ToolType.LOCAL,
)


def _ctx() -> ToolContext:
    return ToolContext(call_id=f"call_{uuid4().hex[:12]}", tool_name=_TOOL.name)


def _result(ctx: ToolContext, *, success: bool) -> ToolResult:
    return ToolResult(
        success=success,
        output={"ok": success},
        error=None if success else ToolError(error_type="execution", message="boom"),
        call_id=ctx.call_id,
        tool_name=_TOOL.name,
    )


@pytest.mark.asyncio
async def test_direct_tool_call_settles_the_request_it_opened(harness):
    logger = ToolExecutionLogger()
    ctx = _ctx()
    row_id = await logger.log_started(ctx, _TOOL, {})
    assert row_id and harness.request_id in harness.on_disk, "backstop must open the parent"
    assert harness.settled == [], "a running call must not settle its request early"

    await logger.log_completed(row_id, _result(ctx, success=True))

    assert harness.settled == [(harness.request_id, "completed", None)], (
        "the chat.user_request the backstop opened was left 'pending' — the lifecycle "
        f"watchdog abandons it 30 minutes later. settled={harness.settled!r}"
    )


@pytest.mark.asyncio
async def test_direct_tool_error_settles_the_request_failed_and_failure_sticks(harness):
    logger = ToolExecutionLogger()
    first = _ctx()
    row_a = await logger.log_started(first, _TOOL, {})
    await logger.log_error(row_a, _result(first, success=False))
    # A second call under the SAME request (row already exists) still settles it,
    # and its success never hides the earlier failure.
    second = _ctx()
    row_b = await logger.log_started(second, _TOOL, {})
    await logger.log_completed(row_b, _result(second, success=True))

    assert [s[1] for s in harness.settled] == ["failed", "failed"], harness.settled
    assert harness.settled[0][2] == "boom"


@pytest.mark.asyncio
async def test_rejected_direct_call_settles_the_request_failed(harness):
    ctx = _ctx()
    rejected = ToolResult(
        success=False,
        output=None,
        error=ToolError(error_type="invalid_arguments", message="bad args"),
        call_id=ctx.call_id,
        tool_name=_TOOL.name,
    )
    await ToolExecutionLogger().log_rejected(ctx, tool_name=_TOOL.name, arguments={}, result=rejected)

    assert harness.settled == [(harness.request_id, "failed", "bad args")], harness.settled


@pytest.mark.asyncio
async def test_a_request_a_boundary_opened_is_never_settled_by_the_logger(harness):
    # The chat/agent boundary ensured the request first — it owns the settle.
    await gate.ensure_user_request_exists(harness.request_id, harness.user_id)
    logger = ToolExecutionLogger()
    ctx = _ctx()
    row_id = await logger.log_started(ctx, _TOOL, {})
    await logger.log_completed(row_id, _result(ctx, success=True))

    assert harness.settled == [], (
        f"the logger settled a request the turn boundary owns: {harness.settled!r}"
    )
