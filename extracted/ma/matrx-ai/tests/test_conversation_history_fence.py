"""Regression coverage for the persisted-history fence at conversation resolution."""

from __future__ import annotations

from copy import deepcopy
from uuid import uuid4

import pytest

from matrx_ai.agents.cache import AgentCache
from matrx_ai.agents.definition import Agent
from matrx_ai.agents.resolver import ConversationResolver
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent


def _message(role: str, text: str) -> UnifiedMessage:
    return UnifiedMessage(role=role, content=[TextContent(text=text)])


def _config(*messages: UnifiedMessage) -> UnifiedConfig:
    return UnifiedConfig(model="test-model", messages=MessageList(list(messages)))


@pytest.mark.asyncio
async def test_cached_continuation_fences_history_from_persistence_before_new_turn(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A rapid follow-up cannot inherit a cache snapshot that predates the answer.

    This is the exact live ConversationRelay sequence: the first request completed
    with ``12.``, but the cache lookup for the next prompt occurred before that
    completion was reflected in the cache. The database is the durable turn order.
    """
    conversation_id = str(uuid4())
    persisted = _config(
        _message("user", "What is seven plus five?"),
        _message("assistant", "12."),
    )
    stale_cache = _config(
        _message("user", "What is seven plus five?"),
        # Deliberately not in the durable projection: cache contents must not
        # leak an unfinished response into the next provider request.
        _message("assistant", "uncommitted cache draft"),
    )
    stale_cache.system_instruction = "Keep the configured owner context."
    stale_cache.system_prompt_frozen = True
    stale_cache.tools = [{"name": "configured_tool"}]

    async def load_messages(received_id: str) -> MessageList:
        assert received_id == conversation_id
        return MessageList(deepcopy(persisted.messages))

    async def full_config_load_must_not_run_on_cache_hit(_received_id: str) -> UnifiedConfig:
        raise AssertionError("cached continuation must use the narrow message fence")

    monkeypatch.setattr(
        "matrx_ai.agents.resolver._load_persisted_messages", load_messages, raising=False
    )
    monkeypatch.setattr(
        "matrx_ai.agents.resolver._load_unified_config", full_config_load_must_not_run_on_cache_hit
    )
    AgentCache.set(conversation_id, Agent(config=stale_cache))
    try:
        resolved = await ConversationResolver.from_conversation_id(
            conversation_id,
            user_input="What number did you just tell me?",
        )
    finally:
        AgentCache.remove(conversation_id)

    assert [message.get_output() for message in resolved.messages] == [
        "What is seven plus five?",
        "12.",
        "What number did you just tell me?",
    ]
    assert resolved.resolved_system_instruction == "Keep the configured owner context."
    assert resolved.system_prompt_frozen is True
    assert resolved.tools == [{"name": "configured_tool"}]
