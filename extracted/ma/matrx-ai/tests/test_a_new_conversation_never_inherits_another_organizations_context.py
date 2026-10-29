"""A first turn's context belongs to the organization the RUN carries — never to a cached slice.

Live, 2026-10-28 (Knowledge buckets proof run 1e6896c7): one person in two organizations ran a
workflow that tidied each organization in parallel. Both calls asserted ``entity_is_new=True``,
so both resolved under the shared first-turn cache key — which named the person and the scope
selection but NOT the organization. The workflow had already committed each call's conversation
row, so the resolver read the FIRST call's conversation organization (Ridgeline) into the cached
slice, and the second call (Harbor Dental) was handed it: its ``<active_context>`` named
Ridgeline, and its answer called Harbor Dental "Ridgeline Physical Therapy".

The seam is ``build_agent_context`` with the real cache and only the database answer faked: the
fake answers what ``custom.resolve_context`` answers for an already-committed conversation row
(its organization in ``context``).
"""

from __future__ import annotations

import copy
from typing import Any

import pytest

from matrx_ai import context_engine
from matrx_ai.context_engine import SystemContextNames

ORG_A = "194ecb20-0000-4000-8000-00000000000a"
ORG_B = "a93eaa92-0000-4000-8000-00000000000b"
CONVERSATION_ORG = {"conv-a": ORG_A, "conv-b": ORG_B}


def _answer_for(entity_id: str) -> dict[str, Any]:
    # What the resolver answers for a conversation whose row is already committed.
    return {
        "variables": {},
        "context": {"user_id": "user-1", "organization_id": CONVERSATION_ORG[entity_id]},
        "scope_labels": {},
    }


@pytest.fixture
def resolver(monkeypatch):
    calls: list[str] = []

    async def rpc(_db, _schema, _fn, _user, _etype, entity_id, *_rest, **_kw):
        calls.append(entity_id)
        return copy.deepcopy(_answer_for(entity_id))

    monkeypatch.setattr("matrx_orm.call_function", rpc)
    monkeypatch.setattr(context_engine, "_resolve_context_database", lambda: "test")
    context_engine.invalidate_context_cache()
    yield calls
    context_engine.invalidate_context_cache()


async def _first_turn(conversation_id: str, organization_id: str):
    return await context_engine.build_agent_context(
        "user-1",
        "conversation",
        conversation_id,
        None,
        entity_is_new=True,
        system_names=SystemContextNames.none(),
        organization_id=organization_id,
    )


async def test_the_second_organizations_first_turn_is_its_own(resolver):
    first = await _first_turn("conv-a", ORG_A)
    second = await _first_turn("conv-b", ORG_B)

    assert first.scope["organization_id"] == ORG_A
    assert second.scope["organization_id"] == ORG_B, (
        "the second organization's first turn was handed the first organization's cached context"
    )


async def test_a_committed_conversations_answer_is_never_shared_with_a_new_one(resolver):
    # Same person, same organization: a slice that carries one conversation's own answer
    # (its row was committed) is that conversation's, not every new conversation's.
    await _first_turn("conv-a", ORG_A)
    CONVERSATION_ORG["conv-c"] = ORG_A
    try:
        await _first_turn("conv-c", ORG_A)
    finally:
        CONVERSATION_ORG.pop("conv-c", None)
    assert resolver == ["conv-a", "conv-c"]


async def test_a_truly_new_conversation_still_shares_the_first_turn_slice(monkeypatch):
    # The KD-5 acceleration stays: an answer that names no entity organization is entity-free,
    # so two new conversations of one person in one organization resolve once.
    calls: list[str] = []

    async def rpc(_db, _schema, _fn, _user, _etype, entity_id, *_rest, **_kw):
        calls.append(entity_id)
        return {"variables": {}, "context": {"user_id": "user-1"}, "scope_labels": {}}

    monkeypatch.setattr("matrx_orm.call_function", rpc)
    monkeypatch.setattr(context_engine, "_resolve_context_database", lambda: "test")
    context_engine.invalidate_context_cache()
    try:
        a = await _first_turn("conv-x", ORG_A)
        b = await _first_turn("conv-y", ORG_A)
        c = await _first_turn("conv-z", ORG_B)
    finally:
        context_engine.invalidate_context_cache()
    assert calls == ["conv-x", "conv-z"]
    assert (a.scope["organization_id"], b.scope["organization_id"], c.scope["organization_id"]) == (
        ORG_A,
        ORG_A,
        ORG_B,
    )
