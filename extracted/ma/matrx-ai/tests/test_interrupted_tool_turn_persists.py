"""A turn cut off while its tool calls run still persists its tool calls.

The loop appends the assistant tool_use turn to ``current_request`` only AFTER
``handle_tool_calls`` returns. A cancel (client disconnect, server shutdown) or
an iteration error during dispatch therefore persisted only an empty assistant
placeholder and no tool-result message. Every chat.tool_call row of that turn
kept ``message_id`` NULL, ``get_cx_conversation_bundle`` (which loads tool calls
by message_id) returned none of them, and a reload showed nothing where the live
turn had shown the calls and their errors (live: conversation f0e79c3b…,
2026-09-22, three git_ingest calls on a cancelled request).

The fix keeps the in-flight response on ``ExecutionState.tool_dispatch_response``
and attaches it on interrupt with ONE honest result per call, read from the
turn's tool-call ledger: a call that finished is not reported as a failure, and
a call still running is never reported as a success. The normal finalize then
writes the assistant + tool messages and links every row by call_id.

Two layers:
  1. behavioural — the cancel path persists the tool_use turn and an honest
     tool-result message for every call;
  2. structural — every handler that finalizes a failed tool-dispatch try
     (and the cancel handler) attaches the in-flight turn first.
"""

from __future__ import annotations

import ast
import asyncio
import inspect
import textwrap

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import (
    MessageList,
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.tools.turn_ledger import record_tool_outcome, record_tool_started


class _StubAppContext:
    conversation_id = "conv-interrupt"
    user_id = "user-1"
    parent_conversation_id = None
    request_id = "req-interrupt"
    store = True

    class _Emitter:
        async def send_info(self, *a, **k):
            return None

        def get_turn_text(self):
            return "Ingesting the three repositories now."

    emitter = _Emitter()


def _role(msg) -> str:
    role = getattr(msg, "role", None)
    return role.value if hasattr(role, "value") else str(role)


@pytest.mark.asyncio
async def test_cancel_during_tool_dispatch_persists_tool_use_and_honest_results(monkeypatch):
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _StubAppContext())

    cfg = UnifiedConfig(
        model="m",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="ingest both repos")])]
        ),
    )
    req = AIMatrixRequest(conversation_id="conv-interrupt", config=cfg)
    dispatch_response = UnifiedResponse(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[
                    TextContent(text="Ingesting the three repositories now."),
                    ToolCallContent(id="toolu_done", name="git_ingest", arguments={"repo": "a"}),
                    ToolCallContent(id="toolu_running", name="git_ingest", arguments={"repo": "b"}),
                    ToolCallContent(id="toolu_failed", name="git_ingest", arguments={"repo": "c"}),
                ],
                metadata={"provider_iteration": 1},
            )
        ]
    )

    async def fake_inner(*, state: ExecutionState, **kwargs):
        state.current_request = req
        state.iteration = 1
        state.trigger_position = 0
        state.pre_execution_message_count = 1
        # The loop is inside handle_tool_calls for this response.
        state.tool_dispatch_response = dispatch_response
        for call_id in ("toolu_done", "toolu_running", "toolu_failed"):
            record_tool_started(key=call_id, tool_name="git_ingest")
        record_tool_outcome(key="toolu_done", tool_name="git_ingest", status="completed")
        record_tool_outcome(
            key="toolu_failed",
            tool_name="git_ingest",
            status="error",
            error_text="clone refused: repository not found",
        )
        raise asyncio.CancelledError()

    monkeypatch.setattr(executor_mod, "_execute_until_complete_inner", fake_inner)

    captured: dict = {}

    async def fake_finalize(*, current_request, iteration, final_response, metadata,
                            trigger_position, pre_execution_message_count, debug, state):
        captured["current_request"] = current_request
        captured["final_response"] = final_response
        captured["metadata"] = metadata
        if state is not None:
            state.persisted = True
        return object()

    monkeypatch.setattr(executor_mod, "_finalize_and_persist", fake_finalize)

    with pytest.raises(asyncio.CancelledError):
        await executor_mod.execute_until_complete(initial_request=object(), client=object())

    assert captured, "the cancel path did not persist"
    msgs = captured["current_request"].config.messages.to_list()
    roles = [_role(m) for m in msgs]
    assert roles == ["user", "assistant", "tool"], (
        f"the interrupted tool turn was not persisted (roles={roles}); its "
        f"chat.tool_call rows would keep message_id NULL"
    )

    tool_uses = [c.id for c in msgs[1].content if isinstance(c, ToolCallContent)]
    assert tool_uses == ["toolu_done", "toolu_running", "toolu_failed"]

    results = {
        c.call_id: c for c in msgs[2].content if isinstance(c, ToolResultContent)
    }
    assert set(results) == {"toolu_done", "toolu_running", "toolu_failed"}, (
        "every tool_use needs its tool_result (Anthropic rejects an orphan "
        "tool_use on the next turn, and the row links through this message)"
    )
    assert results["toolu_done"].is_error is False
    assert results["toolu_running"].is_error is True, "a running call must never read as a success"
    assert results["toolu_failed"].is_error is True
    assert "repository not found" in str(results["toolu_failed"].content)
    assert "interrupted" in str(results["toolu_running"].content).lower()

    # The assistant text is not duplicated as a separate partial turn.
    assert captured["final_response"] is dispatch_response
    assert captured["metadata"]["status"] == "cancelled"


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


def test_every_interrupt_handler_attaches_the_in_flight_tool_turn():
    """Structural layer: a new exit path cannot finalize a failed tool
    dispatch without first attaching the in-flight tool_use turn."""
    checked: list[str] = []

    inner = ast.parse(textwrap.dedent(inspect.getsource(executor_mod._execute_until_complete_inner)))
    for node in ast.walk(inner):
        if not isinstance(node, ast.Try):
            continue
        body_calls: set[str] = set()
        for stmt in node.body:
            body_calls |= _called(stmt)
        if "handle_tool_calls" not in body_calls:
            continue
        for handler in node.handlers:
            if "_finalize_and_persist" in _called(handler):
                checked.append(f"inner:{handler.lineno}")
                assert "_attach_interrupted_tool_turn" in _called(handler), (
                    "a handler finalizes a failed tool dispatch without attaching "
                    "the in-flight tool turn — its tool_call rows will be unlinked"
                )

    outer = ast.parse(textwrap.dedent(inspect.getsource(executor_mod.execute_until_complete)))
    for node in ast.walk(outer):
        if isinstance(node, ast.ExceptHandler) and "CancelledError" in ast.unparse(node.type or ast.Name("")):
            checked.append(f"cancel:{node.lineno}")
            assert "_attach_interrupted_tool_turn" in _called(node), (
                "the cancel handler must attach the in-flight tool turn"
            )

    assert any(c.startswith("inner:") for c in checked), checked
    assert any(c.startswith("cancel:") for c in checked), checked
