"""Forcing-function: ToolLogger must ensure both parents before tool_call INSERT.

The 2026-07-09 orphan class: direct tool paths (``/tools/test``, realtime
bridge, local harnesses) reached ``log_started`` without a parent
``chat.user_request`` row. The INSERT then failed
``cx_tool_call_user_request_id_fkey`` and landed permanently in
``system_write_failure``.

Gut check: if ``_ensure_tool_call_parents`` is a no-op, this test fails —
the queue helper must see the ensure call before the INSERT is queued.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.tools import logger as logger_mod
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType


@pytest.mark.asyncio
async def test_log_started_ensures_parents_before_queue(monkeypatch):
    ensure_calls: list[tuple[str, str, str]] = []
    queued: list[dict] = []

    async def _spy_ensure(*, conversation_id, user_request_id, user_id):
        ensure_calls.append((conversation_id, user_request_id, user_id))

    monkeypatch.setattr(logger_mod, "_ensure_tool_call_parents", _spy_ensure)
    monkeypatch.setattr(logger_mod, "_should_persist_tool_call", lambda: True)
    monkeypatch.setattr(logger_mod, "_get_coordinator", lambda: object())
    monkeypatch.setattr(
        logger_mod,
        "_queue_tool_call_create",
        lambda **kwargs: queued.append(kwargs) or "op",
    )
    monkeypatch.setattr(logger_mod, "_cx_tool_call_supports_as_called", lambda: False)
    monkeypatch.setattr(logger_mod, "stamp_row_owner", lambda data, _uid: data)
    monkeypatch.setattr(logger_mod, "try_get_tracker", lambda: None)

    request_id = str(uuid4())
    user_id = str(uuid4())
    conversation_id = str(uuid4())

    app_ctx = SimpleNamespace(
        user_id=user_id,
        conversation_id=conversation_id,
        request_id=request_id,
        store=True,
        metadata={},
        emitter=None,
    )
    monkeypatch.setattr(
        "matrx_ai.context.app_context.get_app_context",
        lambda: app_ctx,
    )
    monkeypatch.setattr(
        "matrx_ai.context.app_context.try_get_app_context",
        lambda: app_ctx,
    )

    tool_def = ToolDefinition(
        name="sql",
        description="test",
        parameters={"type": "object", "properties": {}},
        tool_type=ToolType.LOCAL,
    )
    tctx = ToolContext(call_id=f"call_{uuid4().hex[:12]}", tool_name="sql")

    row_id = await ToolExecutionLogger().log_started(
        tctx, tool_def, {"action": "query", "table": "public.example"}
    )

    assert row_id, "log_started must return a row id"
    assert ensure_calls == [(conversation_id, request_id, user_id)], (
        f"both FK parents must be ensured BEFORE the tool_call INSERT — got {ensure_calls!r}"
    )
    assert len(queued) == 1
    assert queued[0]["user_request_id"] == request_id
    assert queued[0]["conversation_id"] == conversation_id


@pytest.mark.asyncio
async def test_log_started_skips_when_store_false(monkeypatch):
    ensure_calls: list[tuple[str, str, str]] = []
    queued: list[dict] = []

    async def _spy_ensure(*, conversation_id, user_request_id, user_id):
        ensure_calls.append((conversation_id, user_request_id, user_id))

    monkeypatch.setattr(logger_mod, "_ensure_tool_call_parents", _spy_ensure)
    monkeypatch.setattr(logger_mod, "_should_persist_tool_call", lambda: False)
    monkeypatch.setattr(
        logger_mod,
        "_queue_tool_call_create",
        lambda **kwargs: queued.append(kwargs) or "op",
    )
    monkeypatch.setattr(logger_mod, "stamp_row_owner", lambda data, _uid: data)

    app_ctx = SimpleNamespace(
        user_id=str(uuid4()),
        conversation_id=str(uuid4()),
        request_id=str(uuid4()),
        store=False,
        metadata={},
        emitter=None,
    )
    monkeypatch.setattr(
        "matrx_ai.context.app_context.get_app_context",
        lambda: app_ctx,
    )

    tool_def = ToolDefinition(
        name="sql",
        description="test",
        parameters={"type": "object", "properties": {}},
        tool_type=ToolType.LOCAL,
    )
    tctx = ToolContext(call_id=f"call_{uuid4().hex[:12]}", tool_name="sql")

    row_id = await ToolExecutionLogger().log_started(tctx, tool_def, {})

    assert row_id == ""
    assert ensure_calls == []
    assert queued == []


@pytest.mark.asyncio
async def test_tool_call_parent_gate_ensures_conversation_then_user_request(monkeypatch):
    calls: list[tuple[str, str]] = []

    async def _ensure_conversation_exists(*, conversation_id, user_id):
        calls.append(("conversation", conversation_id))

    async def _ensure_user_request_exists(*, request_id, user_id):
        calls.append(("user_request", request_id))

    monkeypatch.setattr(
        "matrx_ai.db.conversation_gate.ensure_conversation_exists",
        _ensure_conversation_exists,
    )
    monkeypatch.setattr(
        "matrx_ai.db.conversation_gate.ensure_user_request_exists",
        _ensure_user_request_exists,
    )
    monkeypatch.setattr(logger_mod, "_get_coordinator", lambda: None)

    conversation_id = str(uuid4())
    request_id = str(uuid4())
    await logger_mod._ensure_tool_call_parents(
        conversation_id=conversation_id,
        user_request_id=request_id,
        user_id=str(uuid4()),
    )

    assert calls == [
        ("conversation", conversation_id),
        ("user_request", request_id),
    ]


@pytest.mark.asyncio
async def test_queue_tool_call_create_declares_user_request_dep(monkeypatch):
    from matrx_ai.persistence import queue_helpers as qh

    captured: dict = {}

    def _capture(table, payload, *, op_type, primary_key=None, depends_on=()):
        captured["table"] = table
        captured["payload"] = payload
        captured["depends_on"] = depends_on
        return "op"

    monkeypatch.setattr(qh, "_queue_or_drop", _capture)

    ur_id = str(uuid4())
    conv_id = str(uuid4())
    qh.queue_tool_call_create(
        id=str(uuid4()),
        conversation_id=conv_id,
        user_request_id=ur_id,
        tool_name="sql",
    )

    assert captured["table"] == "chat.tool_call"
    assert ("chat.conversation", conv_id) in captured["depends_on"]
    assert ("chat.user_request", ur_id) in captured["depends_on"], (
        "tool_call INSERT must declare the user_request FK dep so a same-Session "
        "parent INSERT lands first"
    )
