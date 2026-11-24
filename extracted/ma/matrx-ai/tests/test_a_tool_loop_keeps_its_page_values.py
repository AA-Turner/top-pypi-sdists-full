"""FORCING GUARD — every send of a tool loop carries the turn's page values.

The per-turn block (``MessageList.attach_turn_context``: page values, the open document, the
selection, the live date) is never persisted; the send boundary re-renders it into the wire on
each send. It was placed only on the send whose newest message was the person's own (and, since
lane RESUME-CONTEXT, the first send of a resumed run). From the second send of a live tool loop
on, it was simply absent: the model's view of the turn lost the document it had just used.

Live evidence (2026-11-02, Office benchmark W1c): conversation d8bf9416 (Docs agent, "Turn this
doc into a 6-slide deck"). ``chat.request_snapshot`` iteration 1 carried a 14 KB
``<turn_context>`` user block holding the document; the agent built correct slides from it.
Iteration 2 (newest message = the deck tool result) had no ``<turn_context`` anywhere, and the
agent told the person "No document context reached me this turn ... The slide content is
invented". P11 (conversation 4733f21f): the PDF agent asked for an upload of the PDF it was
working on, after one tool round.

The fix keeps owner ruling PB-05 (2026-10-18): the block never rides AFTER a tool result and
never moves into the system channel. On every send whose newest message is a tool result, it is
placed exactly where the turn's first send placed it — its own host turn right before the
person's typed text — so the prefix the first send cached is byte-identical on the second.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from matrx_ai.config import (
    MessageList,
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
)
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.testing.profile_factory import make_profile

SYSTEM = "You are a careful assistant. " * 40
PAGE_VALUE = "<page_value>document: Website Corrections Brief. Why: R2 audit flags.</page_value>"

TRANSLATORS = [
    ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat"),
    ("matrx_ai.providers.openai.translator", "OpenAITranslator", "openai_responses"),
    ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
    ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator", "cerebras_chat"),
    ("matrx_ai.providers.together.translator", "TogetherTranslator", "together_chat"),
    ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat"),
    ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat"),
    ("matrx_ai.providers.xai.translator", "XAITranslator", "xai_chat"),
]
CHAT_COMPLETIONS = TRANSLATORS[2:6]
STRICT = {
    "input": ["text"],
    "output": ["text"],
    "features": ["function_calling", "strict_role_alternation"],
    "interaction": "turn",
}


def _loop(rounds: int) -> UnifiedConfig:
    """The person's turn followed by ``rounds`` tool round trips (the ledger the executor holds)."""
    history: list[UnifiedMessage] = [
        UnifiedMessage(role="user", content=[TextContent(text="HER WORDS turn this doc into a deck")])
    ]
    for n in range(rounds):
        history.append(
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id=f"c{n}", name="deck", arguments={"action": "create"})],
            )
        )
        history.append(
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id=f"c{n}", name="deck", content=f"TOOL_RESULT_{n}")],
            )
        )
    config = UnifiedConfig(model="m", messages=MessageList(_messages=history))
    config.system_instruction = SYSTEM
    config.messages.attach_turn_context(PAGE_VALUE, slot="context_manifest")
    return config


def _wire(module: str, cls: str, wire_format: str, rounds: int, capabilities: Any = None) -> str:
    config = _loop(rounds)
    profile = make_profile(model_name="m", wire_format=wire_format, capabilities=capabilities)
    prep = order_for_wire(config, profile, iteration=rounds + 1)
    translator = getattr(importlib.import_module(module), cls)()
    request = translator.build_request(
        prep.wire_config if prep.wire_config is not None else config, profile
    )
    # The canonical ledger is never touched: her stored message stays her words.
    assert [type(c) for c in config.messages[0].content] == [TextContent]
    return str(request)


@pytest.mark.parametrize(("module", "cls", "wire_format"), TRANSLATORS)
@pytest.mark.parametrize("rounds", [1, 3])
def test_every_tool_loop_send_carries_the_page_values_before_her_words(
    module: str, cls: str, wire_format: str, rounds: int
) -> None:
    wire = _wire(module, cls, wire_format, rounds)
    assert "Website Corrections Brief" in wire, (
        f"{cls}: send {rounds + 1} of the tool loop dropped this turn's page values"
    )
    at = wire.index("Website Corrections Brief")
    assert at < wire.index("HER WORDS"), f"{cls}: the block must ride before her words"
    assert at < wire.index("TOOL_RESULT_0"), f"{cls}: the block rode after a tool result (PB-05)"
    assert wire.count("Website Corrections Brief") == 1, f"{cls}: the block was sent twice"


@pytest.mark.parametrize(("module", "cls", "wire_format"), TRANSLATORS)
def test_the_second_send_keeps_the_first_sends_prefix(module: str, cls: str, wire_format: str) -> None:
    """Cache line law: the second send's text up to her words is the first send's, byte for byte."""
    first = _wire(module, cls, wire_format, 0)
    second = _wire(module, cls, wire_format, 1)
    cut = "HER WORDS"
    assert first[: first.index(cut)] == second[: second.index(cut)], (
        f"{cls}: the tool-loop send changed the prefix the first send cached"
    )


@pytest.mark.parametrize(("module", "cls", "wire_format"), CHAT_COMPLETIONS)
def test_a_strict_alternation_model_keeps_the_fallback_through_the_loop(
    module: str, cls: str, wire_format: str
) -> None:
    wire = _wire(module, cls, wire_format, 2, capabilities=STRICT)
    assert "Website Corrections Brief" in wire, f"{cls}: the strict-model loop send dropped the block"
    assert wire.index("Website Corrections Brief") < wire.index("HER WORDS")
