"""Every chat.tool_call row a turn persists is linked to its tool-result message.

A call rejected before dispatch (invalid_arguments, admin_only, not_allowed…)
is written by ``ToolExecutionLogger.log_rejected``, not ``log_started``. It used
to skip the ``(conversation_id, call_id) -> row_id`` registration, so when the
tool-result message persisted, ``backfill_message_id`` fell to a DB read that
lost the race with the row's own still-deferred INSERT and dropped the link.
The row landed with ``message_id`` NULL; ``get_cx_conversation_bundle`` loads
tool calls only by message_id, so on reload the card was rebuilt from the
message stub and showed a completed call where the live turn had shown an error
(conversation 8cccb224…, call toolu_01TN3JXq…, 2026-09-27).

Two layers:
  1. behavioural — a rejected call, then its result message, links by pk with
     the DB read finding nothing (the deferred-INSERT race);
  2. structural — every logger method that INSERTs a tool_call row registers
     it, so a future INSERT path cannot reopen the class.
"""

from __future__ import annotations

import ast
import inspect
import textwrap
from types import SimpleNamespace

import pytest

import matrx_ai.tools.logger as logger_mod
from matrx_ai.tools.logger import (
    _TOOL_CALL_ROW_BY_CALL_ID,
    ToolExecutionLogger,
    _call_row_key,
)
from matrx_ai.tools.models import ToolError, ToolResult


class _FakeCoord:
    def __init__(self) -> None:
        self.queued: list[tuple] = []

    def queue(self, table, payload, *, op_type, primary_key):
        self.queued.append((table, payload, op_type, primary_key))
        return "op-1"


class _EmptyToolCallMgr:
    """The committed DB: the rejected row's INSERT is still deferred, so a
    read finds nothing."""

    def __init__(self) -> None:
        self.filter_calls = 0

    async def filter_items(self, **kw):
        self.filter_calls += 1
        return []


def _rejected_result(call_id: str) -> ToolResult:
    return ToolResult(
        success=False,
        call_id=call_id,
        tool_name="memory",
        error=ToolError(
            error_type="invalid_arguments",
            message="Invalid arguments for 'memory': recall.limit: Input should be less than or equal to 20",
        ),
    )


@pytest.mark.asyncio
async def test_rejected_call_links_to_its_result_message_before_insert_commits(monkeypatch):
    conv, call_id, msg_id = "conv-rejected", "toolu_rejected", "msg-tool-result"
    _TOOL_CALL_ROW_BY_CALL_ID.remove(_call_row_key(conv, call_id) or "")

    coord = _FakeCoord()
    inserts: list[dict] = []
    mgr = _EmptyToolCallMgr()

    async def _no_parents(**kw):
        return None

    monkeypatch.setattr(logger_mod, "_should_persist_tool_call", lambda: True)
    monkeypatch.setattr(logger_mod, "_ensure_tool_call_parents", _no_parents)
    monkeypatch.setattr(logger_mod, "_get_coordinator", lambda: coord)
    monkeypatch.setattr(logger_mod, "_queue_tool_call_create", lambda **kw: inserts.append(kw))
    monkeypatch.setattr(logger_mod, "_cxm", lambda: SimpleNamespace(tool_call=mgr))
    monkeypatch.setattr(logger_mod, "stamp_row_owner", lambda data, user_id: None)

    ctx = SimpleNamespace(
        conversation_id=conv,
        request_id="req-1",
        call_id=call_id,
        iteration=1,
        message_id=None,
        user_id="user-1",
    )
    tool_logger = ToolExecutionLogger()
    row_id = await tool_logger.log_rejected(
        ctx,
        tool_name="memory",
        arguments={"action": "recall", "limit": 50},
        result=_rejected_result(call_id),
    )

    assert row_id, "log_rejected must persist a terminal row"
    assert [d["id"] for d in inserts] == [row_id]
    assert inserts[0]["status"] == "error"

    # The tool-result message persists while the INSERT is still deferred.
    await tool_logger.backfill_message_id(call_id, conv, msg_id)

    assert coord.queued == [
        ("chat.tool_call", {"id": row_id, "message_id": msg_id}, "update", ("id", row_id))
    ], "a rejected call's row must be linked to its result message, never left NULL"
    assert mgr.filter_calls == 0, "the link must resolve from the registry, not race the DB"


_INSERT_CALLS = {"_queue_tool_call_create", "log_tool_call_start"}


def _called_names(fn_node: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(fn_node):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name):
                names.add(f.id)
            elif isinstance(f, ast.Attribute):
                names.add(f.attr)
    return names


def test_every_tool_call_insert_path_registers_its_row():
    tree = ast.parse(textwrap.dedent(inspect.getsource(ToolExecutionLogger)))
    inserting: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        called = _called_names(node)
        if called & _INSERT_CALLS:
            inserting.append(node.name)
            assert "_register_call_row" in called, (
                f"ToolExecutionLogger.{node.name} INSERTs a chat.tool_call row but "
                f"never calls _register_call_row — its message_id link will be "
                f"dropped whenever the result message persists before the INSERT "
                f"commits."
            )
    assert {"log_started", "log_rejected"} <= set(inserting), inserting
