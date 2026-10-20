"""A server that already holds a conversation never sends a stale tools array.

Adversarial review I1 (2026-10-18): on an AgentCache hit the resolver refreshed only the
messages ("cached tools, variables, and runtime configuration remain intact"), so
``config.tool_declarations`` was this server's copy from the last turn IT ran. Server B
appended a tool on turn 2; back on server A on turn 3, A hydrated its stale record (its
in-memory ledger is released at loop end) and sent the turn-1 array: the cached tools head
shrank and no guard saw it. The row's record (newer ``seq``) now wins on every server.

Failed on origin/main before the fix ("turn 3 head ['a', 'b'] is not an append of turn 2
head ['a', 'b', 'x']"); passes after it.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai.agents import resolver as resolver_mod
from matrx_ai.agents.cache import AgentCache
from matrx_ai.agents.definition import Agent
from matrx_ai.agents.resolver import ConversationResolver
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.tools import declaration_ledger


def _decl(name: str) -> dict[str, Any]:
    return {"name": name, "description": "d", "input_schema": {}}


def _send(conv: str, *names: str) -> list[str]:
    result = declaration_ledger.stabilize_declarations(
        "anthropic", [_decl(n) for n in names], name_of=lambda d: d.get("name"), conversation_id=conv
    )
    return [d["name"] for d in result.declarations]


def test_newer_record_takes_the_higher_seq_per_provider() -> None:
    held = {"anthropic": {"seq": 1, "tools": []}, "openai": {"seq": 7, "tools": []}}
    stored = {"anthropic": {"seq": 2, "tools": []}, "google": {"seq": 1, "tools": []}}
    merged = declaration_ledger.newer_record(held, stored)
    assert merged == {
        "anthropic": {"seq": 2, "tools": []},
        "openai": {"seq": 7, "tools": []},
        "google": {"seq": 1, "tools": []},
    }


@pytest.mark.asyncio
async def test_a_cache_hit_adopts_the_rows_newer_tools_array(monkeypatch: pytest.MonkeyPatch) -> None:
    conv = str(uuid4())

    # Turn 1 on server A.
    assert _send(conv, "a", "b") == ["a", "b"]
    record_a = declaration_ledger.export_record(conv)
    a_config = UnifiedConfig(model="claude-opus-5-5", messages=[])
    a_config.tool_declarations = deepcopy(record_a)
    declaration_ledger.forget_conversation(conv)  # A's loop ended

    # Turn 2 on server B (loads the row), appends `x`, saves the row.
    declaration_ledger.hydrate_from_record(conv, record_a)
    assert _send(conv, "a", "b", "x") == ["a", "b", "x"]
    row_record = declaration_ledger.export_record(conv)
    declaration_ledger.forget_conversation(conv)  # B's loop ended

    # Turn 3 back on server A: its AgentCache still holds the turn-1 config.
    AgentCache.set(conv, Agent(config=a_config))

    async def _messages(_conv: str):
        return []

    async def _row_record(_conv: str):
        assert _conv == conv
        return deepcopy(row_record)

    async def _no_live_source(_conv: str):
        return None

    monkeypatch.setattr(resolver_mod, "_load_persisted_messages", _messages)
    monkeypatch.setattr(resolver_mod, "_load_tool_declaration_record", _row_record, raising=False)
    monkeypatch.setattr(resolver_mod.live_structure, "read_structure_source", _no_live_source)
    try:
        config = await ConversationResolver.from_conversation_id(conv, user_input="turn three")
    finally:
        AgentCache.remove(conv)

    from matrx_ai.orchestrator.executor import _hydrate_tool_ledger

    _hydrate_tool_ledger(conv, config)
    head = _send(conv, "a", "b")
    assert head[:3] == ["a", "b", "x"], (
        f"turn 3 head {head} is not an append of turn 2 head ['a', 'b', 'x']"
    )
