"""A model that ends a turn with no visible output is asked ONCE for its answer.

Live 2026-10-17: the Studio Assistant on Gemini Pro ended turns after tool
results with nothing the person could see ("The model ended without producing
a visible answer"). The loop failed the run immediately. Now it spends one
continuation turn (announced as a warning in Watch AI) and only then fails.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source
from types import SimpleNamespace

from matrx_ai.config import (
    TextContent,
    ThinkingContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedMessage,
)
from matrx_ai.config.message_config import MessageList
from matrx_ai.orchestrator import executor
from matrx_ai.orchestrator.execution_state import ExecutionState


def _request(*messages: UnifiedMessage) -> SimpleNamespace:
    return SimpleNamespace(config=SimpleNamespace(messages=MessageList(_messages=list(messages)), model="m"))


def _after_tools(blank: UnifiedMessage) -> SimpleNamespace:
    return _request(
        UnifiedMessage(role="user", content=[TextContent(text="do it")]),
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="c1", name="t", arguments={})],
        ),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="c1", name="t")],
        ),
        blank,
    )


def test_blank_turn_after_tool_results_gets_one_continuation_then_fails() -> None:
    state = ExecutionState()
    req = _after_tools(UnifiedMessage(role="assistant", content=[ThinkingContent(text="hmm")]))

    assert executor._drop_blank_turn_for_continuation(req, state) is True
    roles = [m.role for m in req.config.messages]
    assert roles == ["user", "assistant", "tool", "user"]  # blank turn removed
    assert "without writing any visible reply" in req.config.messages[-1].content[0].text
    assert state.empty_reply_continuations == 1

    # the second blank turn is the honest failure, nothing further is touched
    req.config.messages.append(UnifiedMessage(role="assistant", content=[]))
    assert executor._drop_blank_turn_for_continuation(req, state) is False
    assert [m.role for m in req.config.messages][-1] == "assistant"


def test_loop_tries_the_continuation_before_the_failed_branch() -> None:
    src = stable_source(executor)
    assert src.index("_drop_blank_turn_for_continuation(current_request, state)") < src.index(
        "Provider reported a terminal"
    )
