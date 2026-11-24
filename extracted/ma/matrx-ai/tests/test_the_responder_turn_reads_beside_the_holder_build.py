"""A responder (mandate-held) turn reads its conversation BESIDE the Holder build, never after it.

THE WASTE (2026-11-19, the phone line's staff ask, proof round 4). On a responder turn the resolver built the Holder
(agent load + first-turn fill) and only THEN read, one after another, the conversation's sticky toolset, its
tool-declaration record and its whole rebuilt history (1,234 messages on the test admin's staff thread). None of
those reads depends on the Holder. They now start before the build and are awaited where they are used.

WHAT THIS CATCHES. The Holder build below waits for the history read to have STARTED. Put the reads back after the
build and the build waits forever (the test times out). The other checks prove nothing else moved: the history and
the sticky tools still land on the config, a newer tool record still wins, and a failed history read is still the
404 it always was.
"""

from __future__ import annotations

import asyncio
from copy import deepcopy
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from matrx_ai.agents.resolver import ConversationResolver
from matrx_ai.config import UnifiedConfig
from matrx_ai.config.message_config import UnifiedMessage

CONVERSATION_ID = "3af9e95c-699d-5e78-a506-736e4768273e"
HOLDER = "4383174d-aae9-4bb8-a2ea-0498f3cc47a3"


def _wire(monkeypatch: pytest.MonkeyPatch, *, history_fails: bool = False) -> dict[str, object]:
    seen: dict[str, object] = {"history_started": asyncio.Event()}

    async def _load_persisted_messages(_cid: str) -> list:
        seen["history_started"].set()  # type: ignore[union-attr]
        if history_fails:
            raise RuntimeError("history read failed")
        return [UnifiedMessage(role="user", content="earlier words")]

    async def _load_sticky_toolset(_cid: str):
        return ["sticky_tool"], {"sticky_tool": "discovery"}

    async def _load_tool_declaration_record(_cid: str):
        return {"seq": 99, "providers": {}}

    def newer_record(mine, stored):
        seen["adopted"] = stored
        return stored

    monkeypatch.setattr("matrx_ai.agents.resolver._load_persisted_messages", _load_persisted_messages)
    monkeypatch.setattr("matrx_ai.agents.resolver._load_sticky_toolset", _load_sticky_toolset)
    monkeypatch.setattr("matrx_ai.agents.resolver._load_tool_declaration_record", _load_tool_declaration_record)
    monkeypatch.setattr("matrx_ai.tools.declaration_ledger.newer_record", newer_record)

    async def _finish(config, **_kwargs):
        return config

    monkeypatch.setattr(ConversationResolver, "_finish", staticmethod(_finish))
    live = UnifiedConfig(model="claude-opus-5", system_instruction="live", tools=["memory"], messages=[])

    async def from_agent(agent_id: str, is_version: bool = False, variables=None):
        # The Holder build finishes only once the history read is under way.
        await asyncio.wait_for(seen["history_started"].wait(), timeout=2.0)  # type: ignore[union-attr]
        holder = SimpleNamespace(config=deepcopy(live))

        async def run_first_turn_pass():
            return holder

        holder.run_first_turn_pass = run_first_turn_pass
        return holder

    monkeypatch.setattr("matrx_ai.agents.definition.Agent.from_agent", staticmethod(from_agent))
    return seen


@pytest.mark.asyncio
async def test_the_conversation_reads_overlap_the_holder_build(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = _wire(monkeypatch)
    config = await ConversationResolver.from_conversation_id(CONVERSATION_ID, responder_agent_id=HOLDER)
    assert len(config.messages) == 1, "the persisted history must still land on the config"
    assert "sticky_tool" in (config.dynamic_tools or [])
    assert seen.get("adopted") == {"seq": 99, "providers": {}}, "a newer stored tool record must still win"


@pytest.mark.asyncio
async def test_a_failed_history_read_is_still_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    _wire(monkeypatch, history_fails=True)
    with pytest.raises(HTTPException) as raised:
        await ConversationResolver.from_conversation_id(CONVERSATION_ID, responder_agent_id=HOLDER)
    assert raised.value.status_code == 404
