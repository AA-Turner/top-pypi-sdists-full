"""A mandate-held conversation's history is read from the database ONCE per turn.

THE DEFECT (measured 2026-11-19, a phone hand-off to the Personal Chief of Staff, request 9c954c55). The
resolver loaded the whole conversation (config + every message, rebuilt and healed) FIRST, and only then
asked whether the row is mandate-held; it is, so it recursed with the live Holder and loaded the messages
AGAIN. On a 109-message staff thread the first, wasted load was 3.6 s of the 5.6 s the latency ledger
filed under "tools". The fix asks the one-row question first.

WHAT THIS CATCHES. Move the structure-source read back below the load and both history counts go to 2.
The positive control proves an ordinary conversation still loads its own config exactly once.
"""

from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace

import pytest

from matrx_ai.agents import live_structure
from matrx_ai.agents.resolver import ConversationResolver
from matrx_ai.config import UnifiedConfig

CONVERSATION_ID = "3af9e95c-699d-5e78-a506-736e4768273e"
PERSON = "87a6e699-3622-4869-8843-d0867456c0dd"
ORGANIZATION = "0907939e-2b75-43e8-bfee-da758e5ea75b"
HOLDER = "4383174d-aae9-4bb8-a2ea-0498f3cc47a3"


@pytest.fixture(autouse=True)
def _no_registered_resolver():
    live_structure.register_live_holder_resolver(None)  # type: ignore[arg-type]
    yield
    live_structure.register_live_holder_resolver(None)  # type: ignore[arg-type]


def _wire(monkeypatch: pytest.MonkeyPatch, *, mandate_held: bool, cached: bool) -> dict[str, int]:
    calls = {"config": 0, "messages": 0}
    row_config: dict = {"model": "claude-sonnet-5", "tools": ["memory"], "system_prompt_frozen": True}
    if mandate_held:
        row_config[live_structure.LIVE_STRUCTURE_KEY] = True
        row_config[live_structure.RESPONDER_MANDATE_KEY] = "personal_staff.front_line"
    row = SimpleNamespace(
        id=CONVERSATION_ID,
        config=row_config,
        initial_agent_id=HOLDER,
        initial_agent_version_id=None,
        created_by=PERSON,
        organization_id=ORGANIZATION,
    )

    async def load_by_id(_id: str):
        return row

    monkeypatch.setattr(
        "matrx_ai.db.cxm", SimpleNamespace(conversation=SimpleNamespace(load_by_id=load_by_id)), raising=False
    )
    monkeypatch.setattr("matrx_ai.client_host.get_conversation_store", lambda: None, raising=False)
    own = UnifiedConfig(model="claude-sonnet-5", system_instruction="own", tools=["memory"], messages=[])

    async def _load_unified_config(_cid: str) -> UnifiedConfig:
        calls["config"] += 1
        calls["messages"] += 1  # the unified config carries the rebuilt history
        return deepcopy(own)

    async def _load_persisted_messages(_cid: str) -> list:
        calls["messages"] += 1
        return []

    async def _load_sticky_toolset(_cid: str):
        return [], {}

    async def _adopt_newer_tool_record(_config, _cid):
        return None

    monkeypatch.setattr("matrx_ai.agents.resolver._load_unified_config", _load_unified_config)
    monkeypatch.setattr("matrx_ai.agents.resolver._load_persisted_messages", _load_persisted_messages)
    monkeypatch.setattr("matrx_ai.agents.resolver._load_sticky_toolset", _load_sticky_toolset)
    monkeypatch.setattr("matrx_ai.agents.resolver._adopt_newer_tool_record", _adopt_newer_tool_record)

    async def _finish(config, **_kwargs):
        return config

    monkeypatch.setattr(ConversationResolver, "_finish", staticmethod(_finish))
    live = UnifiedConfig(model="claude-opus-5", system_instruction="live", tools=["memory", "ask_person"], messages=[])

    async def from_agent(agent_id: str, is_version: bool = False, variables=None):
        holder = SimpleNamespace(config=deepcopy(live))

        async def run_first_turn_pass():
            return holder

        holder.run_first_turn_pass = run_first_turn_pass
        return holder

    monkeypatch.setattr("matrx_ai.agents.definition.Agent.from_agent", staticmethod(from_agent))
    cached_agent = SimpleNamespace(config=deepcopy(own)) if cached else None
    monkeypatch.setattr("matrx_ai.agents.cache.AgentCache.get", staticmethod(lambda _c: cached_agent))
    monkeypatch.setattr("matrx_ai.agents.cache.AgentCache.set", staticmethod(lambda *_a, **_k: None))
    return calls


@pytest.mark.asyncio
@pytest.mark.parametrize("cached", [False, True], ids=["cache_miss", "cache_hit"])
async def test_a_mandate_held_turn_reads_its_history_once(monkeypatch: pytest.MonkeyPatch, cached: bool) -> None:
    calls = _wire(monkeypatch, mandate_held=True, cached=cached)
    config = await ConversationResolver.from_conversation_id(CONVERSATION_ID)
    assert "ask_person" in (config.tools or []), "the live Holder's belt must still win"
    assert calls["messages"] == 1, (
        f"the conversation's history was read {calls['messages']} times for one turn; a mandate-held row "
        "must ask where its structure lives BEFORE loading anything (3.6 s per phone hand-off, 2026-11-19)"
    )
    assert calls["config"] == 0, "the row's own frozen config is never the authority on a mandate-held row"


@pytest.mark.asyncio
async def test_an_ordinary_conversation_still_loads_its_own_config_once(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = _wire(monkeypatch, mandate_held=False, cached=False)
    config = await ConversationResolver.from_conversation_id(CONVERSATION_ID)
    assert config.system_instruction is not None
    assert calls == {"config": 1, "messages": 1}
