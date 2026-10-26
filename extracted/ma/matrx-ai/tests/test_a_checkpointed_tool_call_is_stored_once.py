"""A response checkpointed before tool dispatch is stored as ONE row, never two.

With a live client the executor checkpoints the assistant row before running any
tool, folding every message of the provider response into that one row. OpenAI
returns text and tool calls as SEPARATE assistant messages, and the checkpoint
used to mark only the first one committed — so the turn barrier wrote the
tool-call message again as a second row and the chat drew the same tool card
(and its image) twice (conversation 6fd1c446, 2026-10-24).
"""

from types import SimpleNamespace

from matrx_utils.source_guard import stable_source

from matrx_ai.config import UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.config.unified_content import TextContent
from matrx_ai.orchestrator import executor
from matrx_ai.orchestrator.executor import _checkpointed_response_last_position


def _request_with(history_len: int):
    history = [UnifiedMessage(role="user", content=[TextContent(text="hi")])] * history_len
    return SimpleNamespace(config=SimpleNamespace(messages=SimpleNamespace(to_list=lambda: history)))


def _text_then_tool_call_response() -> UnifiedResponse:
    return UnifiedResponse(
        messages=[
            UnifiedMessage(role="assistant", content=[TextContent(text="Optimized prompt…")]),
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id="call_1", name="agent", arguments={"agent_id": "x"})],
            ),
        ]
    )


def test_every_message_of_a_split_response_is_marked_committed():
    # History holds positions 0..1; the response adds positions 2 (text) and 3 (tool call).
    last = _checkpointed_response_last_position(_request_with(2), _text_then_tool_call_response())
    assert last == 3
    # The barrier writes only positions > committed_position: neither message is rewritten.
    assert [p for p in (2, 3) if p > last] == []


def test_a_single_message_response_keeps_its_own_position():
    response = UnifiedResponse(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id="call_1", name="agent", arguments={})],
            )
        ]
    )
    assert _checkpointed_response_last_position(_request_with(2), response) == 2


def test_the_checkpoint_commits_through_the_helper():
    source = stable_source(executor)
    assert "_assistant_pos = _checkpointed_response_last_position(current_request, response)" in source
