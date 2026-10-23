"""THE AGENT SPEAKS FIRST — an opening the person never typed is stored host-authored.

Live 2026-10-22: a design-system board starts its job by itself (no Send, no
``user_input``, no host turn). The agent's seeded user message — its template
filled from page values — was persisted with ``user_content`` NULL, which every
reader treats as "no authorship recorded" and falls back to ``content``. The web
chat showed the template and a dump of the board's items as the person's bubble
(chat.conversation 8cc40245-a443-4951-a6f3-64a04ec4c4da, position 0).
"""

from __future__ import annotations

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.message_config import human_authored_text


def _config(*messages: UnifiedMessage) -> UnifiedConfig:
    return UnifiedConfig(model="claude-sonnet-4-5", messages=MessageList(_messages=list(messages)))


def test_a_template_only_opening_is_recorded_as_the_hosts() -> None:
    opening = UnifiedMessage(role="user", content=[TextContent(text="Build this board's design system now.")])
    config = _config(opening)

    assert config.mark_unspoken_opening_turn() is True

    last = config.messages[-1]
    assert last.user_content == []
    assert last.metadata["authored_by"] == "host"
    assert last.metadata["authored_reason"] == "agent_opening"
    # The model still reads the template; no reader can quote it as hers.
    assert last.content[0].text == "Build this board's design system now."
    assert human_authored_text("user", last.content, last.user_content) == ""


def test_a_turn_with_recorded_authorship_or_history_is_untouched() -> None:
    typed = UnifiedMessage(
        role="user", content=[TextContent(text="hi")], user_content=[TextContent(text="hi")]
    )
    assert _config(typed).mark_unspoken_opening_turn() is False

    answered = _config(
        UnifiedMessage(role="user", content=[TextContent(text="seed")]),
        UnifiedMessage(role="assistant", content=[TextContent(text="ok")]),
        UnifiedMessage(role="user", content=[TextContent(text="again")]),
    )
    assert answered.mark_unspoken_opening_turn() is False
    assert answered.messages[-1].user_content is None
