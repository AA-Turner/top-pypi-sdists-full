"""THE prompt estimator measures what the model is SENT — never a debug repr, never tool names.

Live 2026-10-23/24 (AI Matrx organization, condensing switched on, trigger 120,000): not one
condense was ever queued. The ONE estimator (``context_preflight.estimate_prompt_tokens``) fed the
turn-end condense decision, the pre-flight refusal, the trim payback gate and input-fit, and it
measured each ``UnifiedMessage`` through ``json.dumps(default=str)`` — the dataclass REPR, whose
``TextContent.__repr__`` cuts every text block to 70 characters — and ``config.tools`` as the
list of tool NAMES the registry expands at the wire. Against the provider's own count:

* a text-heavy Haiku chat: estimate 18,518 vs provider 67,576 (27%);
* another: 22,489 vs 88,264;
* a tool-heavy Opus chat: 89,153 vs 123,000 — 41 declarations (73,345 wire chars) counted as names.

Locked here: text counts in full, registered tool names count as their declarations, inline
tools and the context channel count, while a hidden message and opaque provider bytes (a thinking
signature, inline base64) do not — and a conversation past the trigger is SEEN past it.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config.context_preflight import estimate_prompt_tokens
from matrx_ai.config.context_trim import CHARS_PER_TOKEN_MEASURED, CondensePolicy, decide_condense
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.unified_content import TextContent, ThinkingContent

PROSE = CHARS_PER_TOKEN_MEASURED["prose"]
STRUCTURED = CHARS_PER_TOKEN_MEASURED["structured"]


def _config(messages: list, *, tools: list | None = None, custom_tools: list | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        model="m",
        matrx_model_name="m",
        system_instruction=None,
        messages=messages,
        tools=tools or [],
        custom_tools=custom_tools or [],
    )


def _text_message(role: str, chars: int, *, visible: bool = True) -> UnifiedMessage:
    return UnifiedMessage(role=role, content=[TextContent(text="w" * chars)], is_visible_to_model=visible)


def test_a_text_block_counts_in_full_not_its_repr() -> None:
    chars = 290_000  # 100,000 tokens of prose
    estimate = estimate_prompt_tokens(_config([_text_message("user", chars)]))
    assert estimate >= int(chars / PROSE), (
        f"a {chars:,}-char text block was estimated at {estimate:,} tokens — it was measured "
        "through a truncating repr, not the text the model reads"
    )


def test_a_message_hidden_from_the_model_is_not_counted() -> None:
    estimate = estimate_prompt_tokens(_config([_text_message("assistant", 290_000, visible=False)]))
    assert estimate < 100


def test_a_thinking_signature_is_opaque_bytes_not_prompt() -> None:
    block = ThinkingContent(text="short thought", signature="s" * 200_000, provider="anthropic")
    estimate = estimate_prompt_tokens(_config([UnifiedMessage(role="assistant", content=[block])]))
    assert estimate < 1_000, f"a thinking signature was counted as prompt ({estimate:,} tokens)"


def test_the_context_channel_is_counted() -> None:
    messages = MessageList([_text_message("user", 10)])
    messages.attach_tail_context("t" * 29_000, slot="probe")
    assert estimate_prompt_tokens(_config(messages)) >= int(29_000 / PROSE)


@pytest.fixture
def registered_probe_tool():
    from matrx_ai.tools.models import ToolDefinition
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    tool = ToolDefinition(name="estimate_probe_tool", description="d" * 24_000)
    registry.register(tool)
    try:
        yield tool
    finally:
        registry.unregister(tool.name)


def test_a_registered_tool_name_counts_as_its_declaration(registered_probe_tool) -> None:
    estimate = estimate_prompt_tokens(_config([], tools=[registered_probe_tool.name]))
    assert estimate >= int(24_000 / STRUCTURED), (
        f"a registered tool with a 24,000-char declaration was estimated at {estimate:,} tokens "
        "— its NAME was measured, not what the provider is sent"
    )


def test_an_inline_tool_is_counted() -> None:
    inline = SimpleNamespace(get_provider_format=lambda provider: {"name": "x", "description": "d" * 24_000})
    estimate = estimate_prompt_tokens(_config([], custom_tools=[inline]))
    assert estimate >= int(24_000 / STRUCTURED)


def test_a_conversation_past_the_trigger_is_seen_past_it() -> None:
    """The live failure end to end: 190,000 tokens of chat must reach the decision as ~190,000
    (past the 200,000 cap less the next-turn reserve)."""
    policy = CondensePolicy()
    history = [_text_message("user" if i % 2 == 0 else "assistant", int(19_000 * PROSE)) for i in range(10)]
    decision = decide_condense(
        estimated_prompt_tokens=estimate_prompt_tokens(_config(history)),
        policy=policy,
        model_window_tokens=1_000_000,
        window_ceiling_tokens=200_000,
    )
    assert decision.condense, decision.to_snapshot()
    assert decision.rule == "at_cap"


# ── Review fixes (2026-10-24): the wire's own name rule, the wire's format, a loud fallback ──


@pytest.fixture
def fresh_announcements():
    from matrx_ai.config import context_preflight

    announced = getattr(context_preflight, "_TOOL_MEASURE_ANNOUNCED", set())
    announced.clear()
    yield
    announced.clear()


def test_a_tool_in_both_buckets_counts_once_like_the_wire(registered_probe_tool) -> None:
    """``build_provider_tools`` keeps the FIRST declaration per name across registered + inline
    (a browser-dom tool arrives in both); counting both tripped the pre-flight early."""
    twin = SimpleNamespace(
        get_provider_format=lambda provider: {"name": registered_probe_tool.name, "description": "d" * 24_000}
    )
    once = estimate_prompt_tokens(_config([], tools=[registered_probe_tool.name]))
    both = estimate_prompt_tokens(_config([], tools=[registered_probe_tool.name], custom_tools=[twin]))
    assert both == once, f"the same tool name counted twice: {once:,} alone vs {both:,} in both buckets"


def test_tools_are_measured_in_the_format_this_requests_wire_sends(
    registered_probe_tool, monkeypatch, fresh_announcements
) -> None:
    from matrx_ai.catalog.manager import ai_catalog_manager
    from matrx_ai.tools.models import ToolDefinition

    asked: list[str] = []
    real = ToolDefinition.get_provider_format

    def spy(self, provider: str):
        asked.append(provider)
        return real(self, provider)

    monkeypatch.setattr(ToolDefinition, "get_provider_format", spy)
    monkeypatch.setattr(
        ai_catalog_manager, "wire_format_for", lambda model, offering=None: "openai_chat", raising=True
    )
    estimate_prompt_tokens(_config([], tools=[registered_probe_tool.name]))
    assert asked == ["openai"], asked


def test_an_unknown_wire_is_announced_and_still_measured(
    registered_probe_tool, monkeypatch, caplog, fresh_announcements
) -> None:
    import logging

    from matrx_ai.catalog.manager import ai_catalog_manager

    monkeypatch.setattr(ai_catalog_manager, "wire_format_for", lambda model, offering=None: None)
    with caplog.at_level(logging.WARNING, logger="matrx_ai.config.context_preflight"):
        estimate = estimate_prompt_tokens(_config([], tools=[registered_probe_tool.name]))
    assert estimate >= int(24_000 / STRUCTURED)
    assert any("names no tool-declaration format" in r.getMessage() for r in caplog.records), caplog.text


def test_names_the_registry_cannot_render_are_announced(caplog, fresh_announcements) -> None:
    import logging

    with caplog.at_level(logging.WARNING, logger="matrx_ai.config.context_preflight"):
        estimate_prompt_tokens(_config([], tools=["not_a_registered_tool_xyz"]))
    assert any("measured as their NAMES" in r.getMessage() for r in caplog.records), caplog.text


def test_every_tool_capable_wire_format_has_its_translators_format() -> None:
    """The map is the estimator's copy of which format each wire sends: every chat client the
    client dispatches has an entry, and every value is a format a translator really sends."""
    import re
    from pathlib import Path

    from matrx_ai.providers import base_translator
    from matrx_ai.providers.unified_client import UnifiedAIClient

    no_tools_path = {"mock_chat", "elevenlabs_chat"}
    chat_wires = {k for k in UnifiedAIClient._PROVIDER_FACTORIES if k.endswith("_chat")} - no_tools_path
    chat_wires.add(UnifiedAIClient._GENERIC_OPENAI_CLIENT_ATTR)
    assert chat_wires <= set(base_translator.TOOL_FORMAT_BY_WIRE_FORMAT), (
        chat_wires - set(base_translator.TOOL_FORMAT_BY_WIRE_FORMAT)
    )
    sent: set[str] = set()
    for path in Path(base_translator.__file__).parent.glob("*/translator.py"):
        sent |= set(re.findall(r'build_provider_tools\(config, "([a-z_]+)"\)', path.read_text()))
    assert set(base_translator.TOOL_FORMAT_BY_WIRE_FORMAT.values()) <= sent, sent
