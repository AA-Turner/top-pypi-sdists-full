"""Every agent names AI Matrx and the lab of the model answering (Arman, 2026-10-26).

"All agents should identify as being a 'collaboration between AI Matrx and whatever lab
they're from" (``common-docs/systems/agents/agent-design/VISION.md``). The General Voice
Assistant (Grok Voice) answered "who built you?" with its lab alone.

The part (``matrx_ai/config/agent_identity.py``) rides the per-turn context channel, so:
the lab is the CATALOG maker of the model on this send (a switch names the new lab); a
frozen or held prompt never changes and never alarms; a non-chat model never carries it;
the Builder's Model view finds it as a registered platform part.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage, agent_identity
from matrx_ai.config.agent_identity import IDENTITY_SLOT, compose_identity
from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.platform_parts import (
    PLATFORM_PARTS,
    platform_parts_in_request,
    without_platform_parts,
)
from matrx_ai.config.send_boundary import (
    STAGE_LOOP,
    STAGE_RESOLVE,
    prepare_for_send,
    reset_loop_state,
)
from matrx_ai.instructions.core import SystemInstruction
from matrx_ai.testing.profile_factory import make_profile

KNOBS = {
    "statement": "You were built through a collaboration between AI Matrx and {lab}.",
    "statement_own_model": "You were built by AI Matrx.",
    "statement_unknown_lab": "You were built by AI Matrx together with the lab behind your model.",
}
MAKERS = {"claude-sonnet-4-6": "Anthropic", "grok-4": "xAI", "matrx-1": "AI Matrx"}


@pytest.fixture
def bound(monkeypatch):
    seen: list[str | None] = []

    async def resolver(org: str | None) -> dict[str, str]:
        seen.append(org)
        return dict(KNOBS)

    agent_identity.set_identity_statement_resolver(resolver)
    monkeypatch.setattr(agent_identity, "model_lab", lambda ref: MAKERS.get(str(ref)))
    reset_loop_state()
    yield seen
    agent_identity.set_identity_statement_resolver(None)
    reset_loop_state()


def _config(model: str = "claude-sonnet-4-6", system: Any = "You are the receiving desk.") -> UnifiedConfig:
    config = UnifiedConfig(
        model=model,
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="Who made you?")])]),
    )
    config.system_instruction = SystemInstruction.from_value(system) if isinstance(system, str) else system
    return config


def _identity(config: UnifiedConfig) -> str:
    return config.messages.turn_context_blocks().get(IDENTITY_SLOT, "")


def test_the_lab_is_the_catalog_maker_and_our_own_and_unknown_are_honest() -> None:
    assert "collaboration between AI Matrx and Anthropic" in compose_identity(KNOBS, "Anthropic")
    assert "built by AI Matrx." in compose_identity(KNOBS, "AI Matrx")
    unknown = compose_identity(KNOBS, None, model_ref="mystery-1")
    assert "AI Matrx" in unknown and "{lab}" not in unknown


def test_the_catalog_reads_the_maker_by_provider_id_never_the_name() -> None:
    from matrx_ai.catalog.manager import AiCatalogManager

    manager = AiCatalogManager()
    manager._model_state = {"id-1": {"id": "id-1", "name": "claude-x", "provider_id": "p-1"}}
    manager._providers = {"p-1": "Anthropic"}
    manager._model_ids = frozenset({"id-1"})
    manager._model_names = {"claude-x": "id-1"}
    assert manager.model_maker("id-1") == "Anthropic"
    assert manager.model_maker("claude-x") == "Anthropic"
    assert manager.model_maker("gpt-unknown") is None


@pytest.mark.asyncio
async def test_every_send_names_the_lab_of_the_model_answering(bound) -> None:
    config = _config("claude-sonnet-4-6")
    prep = await prepare_for_send(config, stage=STAGE_LOOP, policy=TrimPolicy(), organization_id="org-1")
    assert "agent_identity" in prep.steps
    assert "AI Matrx and Anthropic" in _identity(config)
    assert bound == ["org-1"]
    # A model switch mid-conversation: the next send names the NEW lab.
    config.model = "grok-4"
    await prepare_for_send(config, stage=STAGE_LOOP, policy=TrimPolicy(), organization_id="org-1")
    assert "AI Matrx and xAI" in _identity(config) and "Anthropic" not in _identity(config)
    # It never enters the system text (the cached prefix).
    assert "AI Matrx" not in (config.resolved_system_instruction or "")


@pytest.mark.asyncio
async def test_no_host_resolver_means_no_part_never_invented_words() -> None:
    agent_identity.set_identity_statement_resolver(None)
    config = _config()
    prep = await prepare_for_send(config, stage=STAGE_LOOP, policy=TrimPolicy())
    assert "agent_identity" not in prep.steps
    assert _identity(config) == ""


@pytest.mark.asyncio
async def test_a_frozen_conversation_keeps_its_stored_prompt_and_never_alarms(bound, monkeypatch) -> None:
    screams: list[dict[str, Any]] = []
    monkeypatch.setattr(
        "matrx_ai.providers.cache_guard.scream_cache_line_violation", lambda **kw: screams.append(kw)
    )
    # Turn one of a conversation that began BEFORE this part existed: its stored prompt
    # carries no identity text at all.
    first = _config()
    first.system_instruction.date_anchor = "2026-10-20"
    stored = first.resolved_system_instruction
    row = SimpleNamespace(system_instruction=stored, created_at="2026-10-20T10:00:00Z")

    later = _config()
    later.system_prompt_frozen = True
    await prepare_for_send(later, stage=STAGE_RESOLVE, conversation_row=row, policy=TrimPolicy())
    await prepare_for_send(later, stage=STAGE_LOOP, policy=TrimPolicy(), organization_id="org-1")
    assert screams == []
    assert later.resolved_system_instruction == stored
    assert "AI Matrx and Anthropic" in _identity(later)


def test_a_held_prompt_is_kept_byte_for_byte(bound) -> None:
    from matrx_ai.agents.live_structure import catalog_fingerprint
    from matrx_ai.config.send_boundary import _settle_held_prompt

    config = _config()
    text = config.resolved_system_instruction
    config.held_prompt = {
        "holder": "h1",
        "stored": {"text": text, "holder": "h1", "catalog": catalog_fingerprint(config)},
    }
    _settle_held_prompt(config, conversation_id="c-1")
    assert config.held_prompt["outcome"] == "kept"


@pytest.mark.asyncio
async def test_a_non_chat_model_never_carries_it(bound) -> None:
    from matrx_ai.providers.unified_client import _strip_chat_decorations_if_non_fc

    config = _config()
    await prepare_for_send(config, stage=STAGE_LOOP, policy=TrimPolicy())
    assert _identity(config)
    _strip_chat_decorations_if_non_fc(config, SimpleNamespace(supports_function_calling=False))
    assert _identity(config) == ""
    assert config.system_instruction.include_identity is False
    # And once stripped, the next send stages nothing.
    await prepare_for_send(config, stage=STAGE_LOOP, policy=TrimPolicy())
    assert _identity(config) == ""


def test_the_builder_model_view_labels_it() -> None:
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    assert PLATFORM_PARTS["agent_identity"].label == "Who made this agent"
    config = _config()
    config.messages.attach_turn_context(compose_identity(KNOBS, "Anthropic"), slot=IDENTITY_SLOT)
    request = AnthropicTranslator().build_request(config, make_profile(model_name="m", wire_format="anthropic_chat"))
    parts = [p for p in platform_parts_in_request(request) if p["id"] == "agent_identity"]
    assert len(parts) == 1 and "AI Matrx and Anthropic" in parts[0]["text"]
    for _where, text in __import__("matrx_ai.config.platform_parts", fromlist=["_strings"])._strings(request):
        assert "AI Matrx and Anthropic" not in without_platform_parts(text)
