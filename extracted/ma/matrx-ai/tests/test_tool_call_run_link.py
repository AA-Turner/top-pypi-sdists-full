"""Every chat.tool_call row names the run that made it, from the INSERT on.

A tool call always belongs to its run: in chat that is its message, otherwise
the run record (Chair ruling, 2026-09-27: never an invented conversation). Only
``log_delegated`` used to stamp ``runtime_execution_id``, so a row that never
got a chat message — a job or workflow-node call, a turn cut off mid-dispatch,
a pre-dispatch rejection — carried no run link at all.

Two layers:
  1. behavioural — both INSERT paths (``log_started``, ``log_rejected``) queue
     the row WITH the ambient root execution id; with no run in scope the row
     is written unlinked and that is announced;
  2. structural — every logger method that INSERTs a row stamps the link.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source

import ast
import textwrap
from types import SimpleNamespace

import pytest

import matrx_ai.tools.logger as logger_mod
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolError, ToolResult

ROOT_EXECUTION = "5b0f2a7e-3c1d-4e6f-9a8b-1c2d3e4f5a6b"
NESTING_EXECUTION = "9e8d7c6b-5a4f-4e3d-8c2b-1a0f9e8d7c6b"


def _ctx(call_id: str) -> SimpleNamespace:
    return SimpleNamespace(
        conversation_id="conv-run-link",
        request_id="",
        call_id=call_id,
        iteration=0,
        message_id=None,
        user_id="user-1",
    )


@pytest.fixture
def inserts(monkeypatch):
    queued: list[dict] = []

    async def _no_parents(**kw):
        return None

    monkeypatch.setattr(logger_mod, "_should_persist_tool_call", lambda: True)
    monkeypatch.setattr(logger_mod, "_ensure_tool_call_parents", _no_parents)
    monkeypatch.setattr(logger_mod, "_get_coordinator", lambda: object())
    monkeypatch.setattr(logger_mod, "_queue_tool_call_create", lambda **kw: queued.append(kw))
    monkeypatch.setattr(logger_mod, "stamp_row_owner", lambda data, user_id: None)
    return queued


def _ambient(monkeypatch, metadata: dict | None) -> None:
    import matrx_ai.context.app_context as app_context_mod

    ctx = None if metadata is None else SimpleNamespace(metadata=metadata)
    monkeypatch.setattr(app_context_mod, "try_get_app_context", lambda: ctx)


def _tool_def():
    return SimpleNamespace(name="ask_person", tool_type=SimpleNamespace(value="local"))


@pytest.mark.asyncio
async def test_log_started_row_carries_its_root_run(monkeypatch, inserts):
    _ambient(
        monkeypatch,
        {"runtime_root_execution_id": ROOT_EXECUTION, "runtime_execution_id": NESTING_EXECUTION},
    )
    row_id = await ToolExecutionLogger().log_started(
        _ctx("toolu_started"), _tool_def(), {"question": "Which invoice template?"}
    )
    assert row_id
    assert inserts[0]["runtime_execution_id"] == ROOT_EXECUTION, (
        "the INSERT must name the ROOT run (the id log_delegated pins), never "
        "the re-stampable nesting key and never nothing"
    )


@pytest.mark.asyncio
async def test_log_rejected_row_carries_its_root_run(monkeypatch, inserts):
    _ambient(monkeypatch, {"runtime_root_execution_id": ROOT_EXECUTION})
    row_id = await ToolExecutionLogger().log_rejected(
        _ctx("toolu_rejected"),
        tool_name="ask_person",
        arguments={"question": ""},
        result=ToolResult(
            success=False,
            call_id="toolu_rejected",
            tool_name="ask_person",
            error=ToolError(error_type="invalid_arguments", message="question: must not be empty"),
        ),
    )
    assert row_id
    assert inserts[0]["runtime_execution_id"] == ROOT_EXECUTION


@pytest.mark.asyncio
async def test_no_run_in_scope_is_announced_not_guessed(monkeypatch, inserts, caplog):
    _ambient(monkeypatch, None)
    await ToolExecutionLogger().log_started(_ctx("toolu_unscoped"), _tool_def(), {})
    assert "runtime_execution_id" not in inserts[0]
    assert "NO run link" in caplog.text


def _called(node: ast.AST) -> set[str]:
    out: set[str] = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                out.add(f.id)
            elif isinstance(f, ast.Attribute):
                out.add(f.attr)
    return out


def test_every_tool_call_insert_path_stamps_the_run_link():
    tree = ast.parse(textwrap.dedent(stable_source(ToolExecutionLogger)))
    inserting = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            called = _called(node)
            if "_queue_tool_call_create" in called:
                inserting.append(node.name)
                assert "_stamp_run_link" in called, (
                    f"ToolExecutionLogger.{node.name} INSERTs a chat.tool_call row "
                    f"without _stamp_run_link — a row with no message would name no run"
                )
    assert {"log_started", "log_rejected"} <= set(inserting), inserting
