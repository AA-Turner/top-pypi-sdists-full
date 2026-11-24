"""A continued conversation keeps the mode stored in its overrides (Understanding v2 C4, review finding 8).

``set_mode`` and the person's chip write ``chat.conversation.overrides.agent_mode`` at once; ``conversation.config``
learns it only when a turn finishes. A caller that sends no ``agent_mode`` (agent_run, MCP, the iPhone, a scheduled
run, a page that missed the event) must still get the stored mode; a request that names one wins.

Fails when: the stored override is not read on a continuation; it outranks the request's own override; an
explicit stored null does not return to the first mode.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.agents.cache import AgentCache
from matrx_ai.agents.resolver import ConversationResolver
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.prompt_block_producers import produce_agent_modes
from matrx_ai.db._cx_managers_impl import CxManagers

MODES = [
    {"key": "discovery", "name": "Discovery", "description": "learn first", "instructions": "Ask first."},
    {"key": "answer", "name": "Answer", "description": "answer now", "instructions": "Answer now."},
]


async def _block(monkeypatch, *, overrides: dict, config: dict, request: LLMParams | None) -> str:
    conversation_id = str(uuid4())
    conversation = SimpleNamespace(
        config={"model": "617abdcd-79e2-4a4b-be76-4a9960cdffa1", "agent_modes": MODES, **config},
        last_model_id=None,
        system_instruction="You help.",
        overrides=overrides,
    )

    async def _conversation_data(_self, _conversation_id: str):
        return {"conversation": conversation, "messages": [], "tool_calls": [], "media": []}

    async def _no_messages(*_args, **_kwargs):
        return []

    monkeypatch.setattr(CxManagers, "get_conversation_data", _conversation_data)
    monkeypatch.setattr("matrx_ai.db.conversation_rebuild.rebuild_conversation_messages", _no_messages)
    managers = CxManagers.__new__(CxManagers)

    async def _load(_conversation_id: str):
        return await managers.get_conversation_unified_config(_conversation_id)

    monkeypatch.setattr("matrx_ai.agents.resolver._load_unified_config", _load)
    AgentCache.remove(conversation_id)
    try:
        resolved = await ConversationResolver.from_conversation_id(
            conversation_id, user_input="Next step?", config_overrides=request
        )
    finally:
        AgentCache.remove(conversation_id)
    return produce_agent_modes(resolved) or ""


@pytest.mark.asyncio
async def test_no_request_override_uses_the_stored_mode(monkeypatch) -> None:
    text = await _block(monkeypatch, overrides={"agent_mode": "answer"}, config={}, request=None)
    assert "Current mode: Answer." in text


@pytest.mark.asyncio
async def test_the_stored_override_outranks_the_configs_older_copy(monkeypatch) -> None:
    text = await _block(monkeypatch, overrides={"agent_mode": "answer"}, config={"agent_mode": "discovery"}, request=None)
    assert "Current mode: Answer." in text


@pytest.mark.asyncio
async def test_a_request_override_wins(monkeypatch) -> None:
    text = await _block(
        monkeypatch, overrides={"agent_mode": "answer"}, config={}, request=LLMParams(agent_mode="discovery")
    )
    assert "Current mode: Discovery." in text


@pytest.mark.asyncio
async def test_a_stored_null_returns_to_the_first_mode(monkeypatch) -> None:
    text = await _block(monkeypatch, overrides={"agent_mode": None}, config={"agent_mode": "answer"}, request=None)
    assert "Current mode: Discovery." in text
