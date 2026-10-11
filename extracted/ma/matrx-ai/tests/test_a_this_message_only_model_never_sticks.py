""""This message only": a one-turn model choice runs that turn and nothing after.

Before this, a per-turn ``config_overrides.model`` became the conversation's
model three ways: the stored row (``last_model_id`` + ``config``), and the
process cache that the next turn deep-copies. A person who asked one question
of a stronger model silently stayed on it for every later turn.
"""

from __future__ import annotations

from copy import deepcopy
from uuid import uuid4

import pytest

from matrx_ai.agents.cache import AgentCache
from matrx_ai.agents.definition import Agent
from matrx_ai.agents.resolver import ConversationResolver
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent

BASE_MODEL = "gemini-3.8-flash"
TURN_MODEL = "claude-opus-5-5"


def _config() -> UnifiedConfig:
    return UnifiedConfig(
        model=BASE_MODEL,
        offering_id="base-class",
        messages=MessageList(
            [
                UnifiedMessage(role="user", content=[TextContent(text="Plan my week.")]),
                UnifiedMessage(role="assistant", content=[TextContent(text="Done.")]),
            ]
        ),
    )


@pytest.fixture
def conversation(monkeypatch: pytest.MonkeyPatch):
    conversation_id = str(uuid4())
    persisted = _config()

    async def load_messages(_cid: str) -> MessageList:
        return MessageList(deepcopy(persisted.messages))

    async def load_config(_cid: str) -> UnifiedConfig:
        return deepcopy(persisted)

    monkeypatch.setattr(
        "matrx_ai.agents.resolver._load_persisted_messages", load_messages, raising=False
    )
    monkeypatch.setattr("matrx_ai.agents.resolver._load_unified_config", load_config)
    AgentCache.remove(conversation_id)
    yield conversation_id
    AgentCache.remove(conversation_id)


@pytest.mark.asyncio
async def test_the_turn_runs_on_the_picked_model_and_the_row_keeps_its_own(conversation) -> None:
    resolved = await ConversationResolver.from_conversation_id(
        conversation,
        user_input="What went wrong?",
        config_overrides=LLMParams(model=TURN_MODEL),
        model_this_turn_only=True,
    )
    assert resolved.model == TURN_MODEL
    stored = resolved.to_storage_dict()
    assert stored["model"] == BASE_MODEL
    assert stored["config"].get("offering_id") == "base-class"


@pytest.mark.asyncio
async def test_the_next_turn_from_the_process_cache_is_back_on_the_conversation_model(
    conversation,
) -> None:
    resolved = await ConversationResolver.from_conversation_id(
        conversation,
        user_input="What went wrong?",
        config_overrides=LLMParams(model=TURN_MODEL),
        model_this_turn_only=True,
    )
    # What ai_task._update_cache does at the end of every turn.
    AgentCache.set(conversation, Agent(config=resolved))

    nxt = await ConversationResolver.from_conversation_id(conversation, user_input="Thanks.")
    assert nxt.model == BASE_MODEL
    assert nxt.offering_id == "base-class"
    assert nxt.model_turn_only_restore is None
    assert nxt.to_storage_dict()["model"] == BASE_MODEL


@pytest.mark.asyncio
async def test_a_sticky_pick_still_moves_the_conversation(conversation) -> None:
    """The default picker is unchanged: without the flag the pick is the conversation's."""
    resolved = await ConversationResolver.from_conversation_id(
        conversation,
        user_input="Switch me.",
        config_overrides=LLMParams(model=TURN_MODEL),
    )
    assert resolved.model == TURN_MODEL
    assert resolved.to_storage_dict()["model"] == TURN_MODEL
