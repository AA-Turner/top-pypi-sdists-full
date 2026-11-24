"""FORCING GUARD — a resumed turn's first send carries the context block its run rebuilt.

A turn that parks on a client-delegated tool (an approval card, a browser tool) and is
resumed (``POST /conversations/{id}/resume``, the headless resume, the deferred-result
inbox) starts a NEW run whose newest message is the tool result. Its resume prep rebuilds
this turn's page values (``apply_context_objects`` → ``attach_turn_context``), but the send
boundary placed the block only when the newest message was the person's own, so the
resumed run's first send went out with NO page values at all. The Data Table Assistant
then told the person "No table details reached me this turn" after they pressed Apply
(lane RESUME-CONTEXT, 2026-11-02, conversations db810092 and 686a4d44: the resumed
``chat.request_snapshot`` had no ``<turn_context`` anywhere).

The fix keeps owner ruling PB-05 (2026-10-18): the block never rides AFTER a tool result
and never moves into the system channel. On the first send of a run (``iteration == 1``)
whose newest message is a tool result, the block is placed exactly where a fresh turn
places it — its own host turn right before the person's typed text. Later sends of a live
tool loop carry it in the same place (``tests/test_a_tool_loop_keeps_its_page_values.py``).
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
PAGE_VALUE = "<page_value>column_list: item, qty, status</page_value>"

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


def _resumed_turn() -> UnifiedConfig:
    history = [
        UnifiedMessage(role="user", content=[TextContent(text="HER WORDS describe this table")]),
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="c1", name="apply_surface_write", arguments={"target": "d"})],
        ),
        UnifiedMessage(
            role="tool",
            content=[
                ToolResultContent(
                    tool_use_id="c1", name="apply_surface_write", content="TOOL_RESULT_APPLIED"
                )
            ],
        ),
    ]
    config = UnifiedConfig(model="m", messages=MessageList(_messages=history))
    config.system_instruction = SYSTEM
    config.messages.attach_turn_context(PAGE_VALUE, slot="context_manifest")
    return config


def _build(module: str, cls: str, wire_format: str, iteration: int) -> str:
    config = _resumed_turn()
    profile = make_profile(model_name="m", wire_format=wire_format)
    prep = order_for_wire(config, profile, iteration=iteration)
    translator = getattr(importlib.import_module(module), cls)()
    request: Any = translator.build_request(
        prep.wire_config if prep.wire_config is not None else config, profile
    )
    # The canonical ledger is never touched: the person's stored message stays her words.
    assert [type(c) for c in config.messages[0].content] == [TextContent]
    return str(request)


@pytest.mark.parametrize(("module", "cls", "wire_format"), TRANSLATORS)
def test_the_first_send_of_a_resumed_run_carries_the_page_values(
    module: str, cls: str, wire_format: str
) -> None:
    wire = _build(module, cls, wire_format, iteration=1)
    assert "column_list: item, qty, status" in wire, (
        f"{cls}: the resumed run's first send dropped this turn's page values"
    )
    block_at = wire.index("column_list: item, qty, status")
    assert block_at < wire.index("HER WORDS"), f"{cls}: the block must ride before her words"
    assert block_at < wire.index("TOOL_RESULT_APPLIED"), (
        f"{cls}: the block rode after the tool result (PB-05)"
    )


@pytest.mark.parametrize(("module", "cls", "wire_format"), TRANSLATORS)
def test_a_live_tool_loop_carries_it_in_the_same_place(module: str, cls: str, wire_format: str) -> None:
    """A later tool-loop send keeps the block where the first send put it (W1c, 2026-11-02:
    dropping it erased the page values after the first tool call). Never after the tool result."""
    wire = _build(module, cls, wire_format, iteration=2)
    assert "column_list: item, qty, status" in wire, f"{cls}: a tool-loop send dropped the page values"
    block_at = wire.index("column_list: item, qty, status")
    assert block_at < wire.index("HER WORDS")
    assert block_at < wire.index("TOOL_RESULT_APPLIED"), f"{cls}: the block rode after the tool result (PB-05)"
