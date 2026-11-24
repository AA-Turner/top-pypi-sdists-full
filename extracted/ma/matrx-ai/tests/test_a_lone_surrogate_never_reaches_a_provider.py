"""A lone UTF-16 surrogate in what a person typed never reaches a provider (L12b, 2026-11-03).

Live on chat.aimatrx.com (adversarial sweep P2-2): `Reply ok. lone:\\uD800x\\uDC00 end` failed with "Failed after 3
attempts. An unexpected Groq error occurred." — a provider error for plain input. A lone surrogate half is not valid
Unicode: it cannot be encoded as UTF-8, so every provider SDK refuses the request body. The persistence layer already
replaced it before a write; the provider call had no such step. Now the ONE send boundary replaces lone halves with
U+FFFD on whatever goes on the wire, for every provider; a proper pair (an emoji) is left alone. Red proof: before
this, `sanitize_wire_text` did not exist and the text kept its lone halves.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.config import ToolResultContent, UnifiedMessage
from matrx_ai.config.message_config import MessageList
from matrx_ai.config.send_boundary import sanitize_wire_text
from matrx_ai.config.unified_content import TextContent

TYPED = "Reply ok. lone:\ud800x\udc00 end 😀"


def _config(text: str, system: str = "be brief") -> SimpleNamespace:
    msgs = MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text=text)])])
    return SimpleNamespace(messages=msgs, system_instruction=system)


def test_a_lone_half_is_replaced_and_the_body_encodes() -> None:
    cfg = _config(TYPED)
    replaced = sanitize_wire_text(cfg)
    text = cfg.messages[0].content[0].text
    assert replaced == 2
    assert text == "Reply ok. lone:�x� end 😀"
    text.encode("utf-8")  # a lone half raises UnicodeEncodeError here


def test_a_proper_pair_and_clean_text_are_untouched() -> None:
    cfg = _config("plain 😀 text")
    assert sanitize_wire_text(cfg) == 0
    assert cfg.messages[0].content[0].text == "plain 😀 text"


def test_the_system_text_and_a_tool_result_are_covered_too() -> None:
    cfg = _config("ok", system="sys \udc80")
    cfg.messages.append(
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="t1", name="x", content=[{"page": "a\ud83d b"}])])
    )
    assert sanitize_wire_text(cfg) == 2
    assert cfg.system_instruction == "sys �"
    assert cfg.messages[1].content[0].content == [{"page": "a\ufffd b"}]
