"""Which model a continued conversation runs on — the resolution order (W-81).

PB-07 (2026-10-01): turn 2 of a Compass Dispatch Assistant conversation ran on
Gemini because turn 1 did — the client had sent a leaked
``config_overrides.model``. The server's order is the contract both halves
rely on, and this guard pins it:

    request ``config_overrides``  >  ``last_model_id`` (what the last turn ran on)
                                  >  ``conversation.config.model`` (the agent's
                                     model, written when the row was created)

Breaks this catches: ``last_model_id`` ignored (a person's pick would vanish
after one turn), ``last_model_id`` beating an explicit request override (the
picker could never change the model), or the agent's model never used on a
conversation whose first turn did not complete.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.agents.cache import AgentCache
from matrx_ai.agents.resolver import ConversationResolver
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.db._cx_managers_impl import CxManagers

AGENT_SONNET = "617abdcd-79e2-4a4b-be76-4a9960cdffa1"
GEMINI_FLASH = "b32f2079-4fa5-4613-a01d-726f1243ebe5"
PERSON_PICK = "c0ffee00-1111-4222-8333-944455556666"


async def _resolve_model(
    monkeypatch, *, last_model_id: str | None, request_model: str | None
) -> str:
    conversation_id = str(uuid4())
    conversation = SimpleNamespace(
        config={"model": AGENT_SONNET},
        last_model_id=last_model_id,
        system_instruction=None,
    )

    async def _conversation_data(_self, _conversation_id: str):
        assert _conversation_id == conversation_id
        return {"conversation": conversation, "messages": [], "tool_calls": [], "media": []}

    async def _no_messages(*_args, **_kwargs):
        return []

    monkeypatch.setattr(CxManagers, "get_conversation_data", _conversation_data)
    monkeypatch.setattr(
        "matrx_ai.db.conversation_rebuild.rebuild_conversation_messages", _no_messages
    )
    managers = CxManagers.__new__(CxManagers)

    async def _load(_conversation_id: str):
        # The REAL precedence code, reached through the resolver's own seam.
        return await managers.get_conversation_unified_config(_conversation_id)

    monkeypatch.setattr("matrx_ai.agents.resolver._load_unified_config", _load)
    AgentCache.remove(conversation_id)
    try:
        resolved = await ConversationResolver.from_conversation_id(
            conversation_id,
            user_input="Crew line for move 5208, please",
            config_overrides=LLMParams(model=request_model) if request_model else None,
        )
    finally:
        AgentCache.remove(conversation_id)
    return resolved.model


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("last_model_id", "request_model", "expected"),
    [
        # First turn never completed: the agent's own model answers.
        (None, None, AGENT_SONNET),
        # The previous turn's model sticks for the next turn.
        (GEMINI_FLASH, None, GEMINI_FLASH),
        # A model the person picked on THIS turn beats everything stored.
        (GEMINI_FLASH, PERSON_PICK, PERSON_PICK),
        (None, PERSON_PICK, PERSON_PICK),
    ],
)
async def test_continued_conversation_model_resolution_order(
    monkeypatch, last_model_id, request_model, expected
) -> None:
    assert (
        await _resolve_model(
            monkeypatch, last_model_id=last_model_id, request_model=request_model
        )
        == expected
    )
