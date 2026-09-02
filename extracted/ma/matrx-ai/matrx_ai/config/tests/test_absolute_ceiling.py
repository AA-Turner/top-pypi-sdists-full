"""Phase 3 — Layer-2 absolute size ceiling enforced in MessageList.sanitize.

The source-agnostic backstop: even a tool_result that bypassed the executor's
Layer 1 (client-posted, rebuilt-from-DB) is hard-capped before any provider call.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.tools_config import ToolResultContent
from matrx_ai.tools.output_caps import TOOL_RESULT_ABSOLUTE_CEILING_CHARS
from matrx_ai.tools.result_gate import _SINKS, register_tool_result_gate_sink


@pytest.fixture
def captured_events():
    events = []
    register_tool_result_gate_sink(events.append)
    yield events
    if events.append in _SINKS:
        _SINKS.remove(events.append)


def _ml_with_block(block: ToolResultContent) -> MessageList:
    msg = UnifiedMessage(role="tool", content=[block])
    return MessageList(_messages=[msg])


def test_over_ceiling_is_hard_truncated_and_alarms(captured_events):
    huge = "Q" * (TOOL_RESULT_ABSOLUTE_CEILING_CHARS + 250_000)
    block = ToolResultContent(tool_use_id="tu-1", name="some_external_tool", content=huge)
    ml = _ml_with_block(block)

    ml._enforce_absolute_tool_result_ceiling()

    assert len(block.content) < len(huge)
    assert block.content.startswith("Q" * TOOL_RESULT_ABSOLUTE_CEILING_CHARS)
    assert "ABSOLUTE SIZE CEILING" in block.content
    assert len(captured_events) == 1
    assert captured_events[0].tier == "ceiling_fired"
    assert captured_events[0].output_chars == len(huge)


def test_approved_max_chars_raises_the_ceiling(captured_events):
    # A self-managed tool authorized a larger result — honor it, do not truncate.
    size = TOOL_RESULT_ABSOLUTE_CEILING_CHARS + 100_000
    body = "R" * size
    block = ToolResultContent(
        tool_use_id="tu-2",
        name="data",
        content=body,
        approved_max_chars=size + 10,  # authorized above the absolute ceiling
    )
    ml = _ml_with_block(block)

    ml._enforce_absolute_tool_result_ceiling()

    assert block.content == body  # untouched
    assert captured_events == []


def test_under_ceiling_untouched(captured_events):
    body = "S" * 1000
    block = ToolResultContent(tool_use_id="tu-3", name="data", content=body)
    ml = _ml_with_block(block)
    ml._enforce_absolute_tool_result_ceiling()
    assert block.content == body
    assert captured_events == []


def test_media_block_list_never_truncated(captured_events):
    # Typed image blocks (each carrying to_anthropic/to_openai/to_google) must pass
    # through untouched even if huge — they are references the model needs intact.
    class _TypedBlock:
        def to_anthropic(self):
            return {}

    blocks = [_TypedBlock() for _ in range(10)]
    block = ToolResultContent(tool_use_id="tu-4", name="screenshot", content=blocks)
    ml = _ml_with_block(block)
    ml._enforce_absolute_tool_result_ceiling()
    assert block.content is blocks
    assert captured_events == []


def test_dict_content_over_ceiling_is_truncated_to_string(captured_events):
    # The real bypass: a tool_result whose content is a raw dict (client-posted /chat
    # message). The provider would json.dumps it huge — Layer 2 must measure it the
    # same way and truncate it to a bounded string.
    huge_dict = {"rows": ["W" * 1000 for _ in range(800)]}  # ~800K serialized
    block = ToolResultContent(tool_use_id="tu-5", name="some_tool", content=huge_dict)
    ml = _ml_with_block(block)

    ml._enforce_absolute_tool_result_ceiling()

    assert isinstance(block.content, str)  # converted to a bounded string
    assert len(block.content) < TOOL_RESULT_ABSOLUTE_CEILING_CHARS + 500
    assert "ABSOLUTE SIZE CEILING" in block.content
    assert len(captured_events) == 1
    assert captured_events[0].tier == "ceiling_fired"


def test_idempotent_no_double_truncate_or_double_alarm(captured_events):
    huge = "Q" * (TOOL_RESULT_ABSOLUTE_CEILING_CHARS + 250_000)
    block = ToolResultContent(tool_use_id="tu-6", name="some_tool", content=huge)
    ml = _ml_with_block(block)

    ml._enforce_absolute_tool_result_ceiling()
    first_len = len(block.content)
    ml._enforce_absolute_tool_result_ceiling()  # second pass — must be a no-op
    ml._enforce_absolute_tool_result_ceiling()  # third pass

    assert len(block.content) == first_len  # not re-truncated
    assert len(captured_events) == 1  # alarm fired exactly once
