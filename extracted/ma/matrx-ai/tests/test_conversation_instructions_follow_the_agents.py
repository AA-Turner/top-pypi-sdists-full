"""A conversation's own instructions follow the agent's on the wire (L3 one-chat G1).

Matrx 2's private room let a person give ONE conversation its own instructions
(confidential/ConversationSettings.tsx); the normal room had no way to. The run request now
carries ``config_overrides.conversation_instructions``; it is stored with the conversation,
restored on continuation, applied ONLY by the send boundary after the agent's own instructions
(never replacing them, never in ``user_input``), measured by the pre-flight, and absent when unset.

Fails when: the field is refused by LLMParams; it does not reach the provider payload after the
agent's text; a later turn or a restore loses it; an explicit null does not clear it; the canonical
(frozen) prompt is changed; or an unset field changes anything.
"""

from __future__ import annotations

import pytest

from matrx_ai.config import UnifiedConfig
from matrx_ai.config.context_preflight import estimate_prompt_tokens
from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.unified_client import _build_provider_wire_config
from matrx_ai.testing.profile_factory import make_profile

AGENT = "You are a careful drafter."
MINE = "Answer in French, in two sentences."


def _config() -> UnifiedConfig:
    return UnifiedConfig(
        model="claude-haiku-4-5",
        system_instruction=AGENT,
        messages=[{"role": "user", "content": [{"type": "text", "text": "Draft a reply."}]}],
    )


async def _provider_payload(config: UnifiedConfig) -> dict:
    prep = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="c1", request_id="r1", policy=TrimPolicy())
    wire = prep.wire_config if prep.wire_config is not None else config
    profile = make_profile(model_name="claude-haiku-4-5", wire_format="anthropic_chat")
    return AnthropicTranslator().to_anthropic(_build_provider_wire_config(wire, profile), profile)


def _system_text(payload: dict) -> str:
    system = payload.get("system")
    if isinstance(system, str):
        return system
    return "\n\n".join(block.get("text", "") for block in system or [])


@pytest.mark.asyncio
async def test_it_reaches_the_provider_after_the_agents_instructions() -> None:
    config = _config()
    config.apply_overrides(LLMParams(conversation_instructions=MINE))
    text = _system_text(await _provider_payload(config))
    assert AGENT in text and MINE in text
    assert text.index(AGENT) < text.index(MINE), "the agent's instructions come first"
    # The canonical config (what the row stores and the cache-line law compares) is untouched.
    assert MINE not in (config.resolved_system_instruction or "")
    # Never in the person's turn.
    assert all(MINE not in str(m) for m in config.messages)


@pytest.mark.asyncio
async def test_absent_when_unset() -> None:
    config = _config()
    text = _system_text(await _provider_payload(config))
    assert MINE not in text
    assert "conversation_instructions" not in config.to_storage_dict()["config"]


@pytest.mark.asyncio
async def test_it_survives_a_later_turn_and_a_restore_and_null_clears_it() -> None:
    config = _config()
    config.apply_overrides(LLMParams(conversation_instructions=MINE))
    # A later turn whose overrides do not name it keeps it.
    config.apply_overrides(LLMParams(temperature=0.2))
    assert config.conversation_instructions == MINE
    stored = config.to_storage_dict()
    assert stored["config"]["conversation_instructions"] == MINE
    restored = UnifiedConfig.from_dict(
        {"model": stored["model"], "system_instruction": stored["system_instruction"], **stored["config"], "messages": config.messages}
    )
    assert restored.conversation_instructions == MINE
    assert MINE in _system_text(await _provider_payload(restored))
    # An explicit null clears it.
    restored.apply_overrides(LLMParams.model_validate({"conversation_instructions": None}))
    assert restored.conversation_instructions is None
    assert "conversation_instructions" not in restored.to_storage_dict()["config"]


@pytest.mark.asyncio
async def test_a_chat_that_is_not_saved_sends_it_every_turn() -> None:
    """store:false: nothing is restored, so the client sends it on every turn's overrides."""
    for turn in range(2):
        config = _config()  # a fresh config each turn: no stored row to read back
        config.apply_overrides(LLMParams(conversation_instructions=MINE))
        assert MINE in _system_text(await _provider_payload(config)), f"turn {turn + 1}"


def test_it_counts_against_the_context_measure() -> None:
    plain = _config()
    mine = _config()
    mine.apply_overrides(LLMParams(conversation_instructions=MINE * 50))
    assert estimate_prompt_tokens(mine) > estimate_prompt_tokens(plain)


def test_llm_params_refuses_an_unknown_neighbor() -> None:
    LLMParams(conversation_instructions=MINE)
    with pytest.raises(Exception):
        LLMParams.model_validate({"conversation_instructionz": MINE})
