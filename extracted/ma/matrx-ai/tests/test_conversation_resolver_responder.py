"""A conversation with no configuration of its own can still be answered.

A coding session mirrored into AI Matrx is agentless by construction: the projector
writes no agent onto the conversation (the mirror's provenance is the provider's), and
its ``config`` blob is empty. So the ordinary continuation resolved a UnifiedConfig with
no model and the turn died at the provider — the server accepted a person's reply and
could not answer it.

``responder_agent_id`` is the seam that fixes it: the structural half of the config comes
from a named agent, the history still comes from the conversation, and the shared send
boundary still runs. This test fails if any of those three stops being true.
"""

from __future__ import annotations

import pytest

from matrx_ai.agents import resolver as module
from matrx_ai.config import UnifiedConfig
from matrx_ai.config.message_config import UnifiedMessage

CONVERSATION = "11111111-1111-4111-8111-111111111111"
RESPONDER = "22222222-2222-4222-8222-222222222222"


@pytest.mark.asyncio
async def test_a_responder_supplies_the_config_and_the_conversation_supplies_history(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    responder_config = UnifiedConfig(
        model="claude-sonnet-4-5",
        messages=[],
        system_instruction="You are the coding-conversation responder.",
    )
    responder_config.messages.append(
        UnifiedMessage.from_dict({"role": "assistant", "content": [{"type": "text", "text": "leftover"}]})
    )

    class _Responder:
        config = responder_config

    async def from_agent(agent_id: str, **_kwargs: object) -> _Responder:
        assert agent_id == RESPONDER
        return _Responder()

    mirrored = [
        UnifiedMessage.from_dict({"role": "user", "content": [{"type": "text", "text": "Build the parser"}]}),
        UnifiedMessage.from_dict({"role": "assistant", "content": [{"type": "text", "text": "Done."}]}),
    ]

    async def persisted(conversation_id: str) -> list[UnifiedMessage]:
        assert conversation_id == CONVERSATION
        return mirrored

    prepared: dict[str, object] = {}

    async def prepare_for_send(config: UnifiedConfig, **kwargs: object) -> None:
        prepared["stage"] = kwargs.get("stage")
        prepared["conversation_id"] = kwargs.get("conversation_id")

    monkeypatch.setattr(module.Agent, "from_agent", from_agent)
    monkeypatch.setattr(module, "_load_persisted_messages", persisted)
    monkeypatch.setattr(
        "matrx_ai.config.send_boundary.prepare_for_send", prepare_for_send
    )

    def _never(_conversation_id: str) -> None:
        raise AssertionError(
            "a responder turn must not read the conversation's own (empty) config"
        )

    monkeypatch.setattr(module, "_load_unified_config", _never)

    config = await module.ConversationResolver.from_conversation_id(
        CONVERSATION,
        user_input="Where did this land?",
        responder_agent_id=RESPONDER,
    )

    # The structural half is the responder's — the thing the mirror does not have.
    assert config.model == "claude-sonnet-4-5"
    assert (
        config.system_instruction.base_instruction
        == "You are the coding-conversation responder."
    )
    # The history is the conversation's, and the responder's own leftover messages are
    # NOT smuggled in beside it.
    texts = [message.get_output() for message in config.messages]
    assert "leftover" not in texts
    assert texts[:2] == ["Build the parser", "Done."]
    # The person's reply is the last user turn.
    assert config.messages[-1].get_output() == "Where did this land?"
    # And the one send boundary still ran for this turn.
    assert prepared["conversation_id"] == CONVERSATION
    assert prepared["stage"] is not None


@pytest.mark.asyncio
async def test_without_a_responder_the_conversations_own_config_is_still_used(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The no-responder path is untouched — every ordinary chat behaves as before."""
    loaded = UnifiedConfig(model="gpt-5", messages=[])

    async def own_config(conversation_id: str) -> UnifiedConfig:
        assert conversation_id == CONVERSATION
        return loaded

    async def prepare_for_send(_config: UnifiedConfig, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr(module.AgentCache, "get", staticmethod(lambda _id: None))
    monkeypatch.setattr(module.AgentCache, "set", staticmethod(lambda *_a: None))
    monkeypatch.setattr(module, "_load_unified_config", own_config)
    monkeypatch.setattr(
        "matrx_ai.config.send_boundary.prepare_for_send", prepare_for_send
    )

    def _never(_agent_id: str, **_kwargs: object) -> None:
        raise AssertionError("no responder was asked for")

    monkeypatch.setattr(module.Agent, "from_agent", _never)

    config = await module.ConversationResolver.from_conversation_id(CONVERSATION)

    assert config.model == "gpt-5"
