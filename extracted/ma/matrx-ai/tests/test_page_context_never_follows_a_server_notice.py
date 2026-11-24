"""FORCING GUARD — the page block never rides after a tool result, even after a server notice.

``typed_text_last.resumed_person_turn_index`` returned the newest user message that was not a
tool result. Server-written notices (``host_authored_user_turn``: loop guard, iteration ceiling,
answer check, text tool call, required-member gate, injections, recovery) are user messages the
executor appends mid-loop right after a tool result. Once one sat in the loop, every later send
put the page block before the NOTICE, i.e. right after a tool result — the placement owner ruling
PB-05 forbids (2026-10-18: the model told the person about "the platform block in that last
turn"). Wave-1 review item 1b, repro ``notice.py`` (2026-11-02).

The block stays before HER words on every send (``typed_text_last.turn_person_index`` skips
server-written turns), including the send whose newest message is the notice itself.
"""

from __future__ import annotations

import pytest

from matrx_ai.config import (
    MessageList,
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
)
from matrx_ai.config.message_config import host_authored_user_turn
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.testing.profile_factory import make_profile

PAGE = "<page>PAGEVAL</page>"


def _loop(*, notice_is_newest: bool) -> list[UnifiedMessage]:
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="HER WORDS")]),
        UnifiedMessage(role="assistant", content=[ToolCallContent(id="c0", name="t", arguments={})]),
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="c0", name="t", content="R0")]),
        host_authored_user_turn("NOTICE: 3 tool rounds left", reason="iteration_ceiling_approaching"),
    ]
    if not notice_is_newest:
        messages += [
            UnifiedMessage(role="assistant", content=[ToolCallContent(id="c1", name="t", arguments={})]),
            UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="c1", name="t", content="R1")]),
        ]
    return messages


def _wire(messages: list[UnifiedMessage], wire_format: str) -> list[UnifiedMessage]:
    config = UnifiedConfig(model="m", messages=MessageList(_messages=messages))
    config.system_instruction = "S" * 100
    config.messages.attach_turn_context(PAGE, slot="context_manifest")
    prep = order_for_wire(config, make_profile(model_name="m", wire_format=wire_format), iteration=3)
    return list((prep.wire_config or config).messages)


def _texts(message: UnifiedMessage) -> str:
    return "".join(getattr(c, "text", "") or "" for c in message.content)


@pytest.mark.parametrize("wire_format", ["openai_chat", "anthropic_chat", "openai_responses"])
@pytest.mark.parametrize("notice_is_newest", [False, True])
def test_the_block_stays_before_her_words_after_a_server_notice(wire_format: str, notice_is_newest: bool) -> None:
    wire = _wire(_loop(notice_is_newest=notice_is_newest), wire_format)
    carrying = [i for i, m in enumerate(wire) if "PAGEVAL" in _texts(m)]
    assert len(carrying) == 1, f"the page block must ride exactly once on this send, found {carrying}"
    at = carrying[0]
    assert at + 1 < len(wire) and "HER WORDS" in _texts(wire[at + 1]), (
        f"the page block rides at {at}, before {_texts(wire[at + 1])[:30]!r}: it must sit right before her words"
    )
    before = wire[at - 1] if at else None
    assert before is None or before.role != "tool", "the page block rides right after a tool result (PB-05)"
