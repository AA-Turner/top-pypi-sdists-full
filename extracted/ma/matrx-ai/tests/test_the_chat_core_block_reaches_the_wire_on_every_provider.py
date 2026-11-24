"""FORCING GUARD — a converted conversation's core block (slot ``chat_core``) reaches EVERY provider's wire.

chat-agent-skills, finding 1 of the vision check: a converted Google conversation looked like it carried the
skill tools but not the standing line. The class is "a translator that drops a per-turn slot". Each translator
family must carry the slot's text in its request body, on a turn that already has history."""

from __future__ import annotations

import importlib
import json

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.testing.profile_factory import make_profile

BLOCK = "<platform_core>\nBefore you tell the person you cannot do something, search for a skill.\n</platform_core>"
FAMILIES = [
    ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat"),
    ("matrx_ai.providers.openai.translator", "OpenAITranslator", "openai_chat"),
    ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat"),
    ("matrx_ai.providers.xai.translator", "XAITranslator", "xai_chat"),
    ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
    ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator", "cerebras_chat"),
    ("matrx_ai.providers.together.translator", "TogetherTranslator", "together_chat"),
    ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat"),
]


def _msg(role: str, text: str) -> UnifiedMessage:
    return UnifiedMessage(role=role, content=[TextContent(text=text)])


@pytest.mark.parametrize("module,cls,wire_format", FAMILIES, ids=[f[1] for f in FAMILIES])
def test_the_core_block_slot_is_on_the_wire(module: str, cls: str, wire_format: str) -> None:
    history = [_msg("user", "What is the latest news?"), _msg("assistant", "Here is the news."), _msg("user", "Book me a flight.")]
    config = UnifiedConfig(model="m", messages=MessageList(_messages=history))
    config.system_instruction = "You are a careful assistant. " * 10
    config.messages.attach_turn_context(BLOCK, slot="chat_core")
    profile = make_profile(model_name="m", wire_format=wire_format)
    prep = order_for_wire(config, profile)
    translator = getattr(importlib.import_module(module), cls)()
    request = translator.build_request(prep.wire_config if prep.wire_config is not None else config, profile)
    assert "search for a skill" in json.dumps(request, default=str), f"{cls} dropped the chat_core slot"


def test_a_cleared_slot_is_not_on_the_wire() -> None:
    config = UnifiedConfig(model="m", messages=MessageList(_messages=[_msg("user", "Hi")]))
    config.system_instruction = "You are a careful assistant."
    config.messages.attach_turn_context(BLOCK, slot="chat_core")
    config.messages.attach_turn_context("", slot="chat_core")
    profile = make_profile(model_name="m", wire_format="google_chat")
    prep = order_for_wire(config, profile)
    from matrx_ai.providers.google.translator import GoogleTranslator

    request = GoogleTranslator().build_request(prep.wire_config if prep.wire_config is not None else config, profile)
    assert "search for a skill" not in json.dumps(request, default=str)
