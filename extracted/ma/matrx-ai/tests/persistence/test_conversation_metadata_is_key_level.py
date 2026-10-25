"""chat.conversation.metadata is one jsonb object many writers share — a writer keeps every key it does not own.

Measured 2026-10-05: a brand-new chat's first-turn shape picks
(``run_configuration.outputKinds``) vanished because request_context_track queued
``metadata={last_request_context}`` and the coalescer is last-write-wins per FIELD.
These tests drive the REAL Coordinator + the matrx-orm coalescer and read the one
row that would be written; each fails when the writer replaces the object whole.
"""

from __future__ import annotations

import pytest
from matrx_orm.session.coalesce import coalesce_ops

import matrx_ai.persistence.queue_helpers as qh
from matrx_ai.persistence import registry
from matrx_ai.persistence.coordinator import Coordinator


class _Meta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "conversation"
    db_schema = "chat"


class _FakeConversation:
    _meta = _Meta()

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)


@pytest.fixture
def coord(monkeypatch):
    previous = registry._tables.get("chat.conversation")
    registry.register_table("chat.conversation", _FakeConversation)
    c = Coordinator()
    monkeypatch.setattr(qh, "get_coordinator", lambda: c)
    monkeypatch.setattr(qh, "get_current_lane", lambda: None)
    yield c
    if previous is None:
        registry._tables.pop("chat.conversation", None)
    else:
        registry._tables["chat.conversation"] = previous


def _written(coord: Coordinator, conversation_id: str) -> dict:
    ops = [o for o in coalesce_ops(coord._session._ops) if str(o.pk_value) == conversation_id]
    assert len(ops) == 1, ops
    return ops[0].payload["metadata"]


PICKS = {"run_configuration": {"outputKinds": ["quiz_set", "timeline"]}}


def test_a_new_chats_picks_survive_the_request_context_write_in_either_order(coord):
    cid = "c-new"
    qh.queue_conversation_create(id=cid, created_by="u1", organization_id="o1", metadata={"source": "chat"})
    qh.queue_conversation_metadata_patch(cid, PICKS, db_metadata=None)
    # request_context_track: a stale copy of the (empty) stored object + its own key
    qh.queue_conversation_metadata_patch(cid, {"last_request_context": {"agent_id": "a1"}}, db_metadata={})
    meta = _written(coord, cid)
    assert meta["run_configuration"]["outputKinds"] == ["quiz_set", "timeline"]
    assert meta["last_request_context"] == {"agent_id": "a1"}
    assert meta["source"] == "chat"


def test_picks_queued_before_the_insert_are_merged_into_it_not_replaced(coord):
    cid = "c-early"
    qh.queue_conversation_metadata_patch(cid, PICKS, db_metadata=None)
    qh.queue_conversation_create(id=cid, created_by="u1", organization_id="o1", metadata={"source": "chat"})
    meta = _written(coord, cid)
    assert meta["run_configuration"]["outputKinds"] == ["quiz_set", "timeline"]
    assert meta["source"] == "chat"


def test_a_whole_object_update_never_erases_what_the_request_already_queued(coord):
    cid = "c-naive"
    qh.queue_conversation_create(id=cid, created_by="u1", organization_id="o1", metadata={})
    qh.queue_conversation_metadata_patch(cid, PICKS, db_metadata=None)
    qh.queue_conversation_update(cid, metadata={"observational_memory": {"enabled": True}})
    meta = _written(coord, cid)
    assert meta["run_configuration"]["outputKinds"] == ["quiz_set", "timeline"]
    assert meta["observational_memory"] == {"enabled": True}


def test_an_existing_chat_keeps_its_other_run_configuration_keys_when_picks_change(coord):
    cid = "c-old"
    stored = {"run_configuration": {"addedSkills": ["s1"], "outputKinds": ["timeline"]}, "k": 1}
    qh.queue_conversation_metadata_patch(cid, {"run_configuration": {"outputKinds": ["quiz_set"]}}, db_metadata=stored)
    ops = coalesce_ops(coord._session._ops)
    meta = ops[0].payload["metadata"]
    assert meta["run_configuration"] == {"addedSkills": ["s1"], "outputKinds": ["quiz_set"]}
    assert meta["k"] == 1


def test_the_title_backfill_writes_one_key_atomically_never_the_whole_object():
    import asyncio
    from types import SimpleNamespace

    import matrx_ai.db.cx_managers as cxmod
    from matrx_ai.db import conversation_title_backfill as tb

    calls = {"patch": [], "update": []}

    class _Conv:
        async def patch_jsonb_path(self, *a):
            calls["patch"].append(a)

        async def update_conversation(self, cid, **kw):
            calls["update"].append(kw)

    class _Plan(SimpleNamespace):
        pass

    plan = _Plan(conversation_id="c1", step_label="Label", new_title="T")
    original = getattr(cxmod, "cxm", None)
    cxmod.cxm = SimpleNamespace(conversation=_Conv())
    try:
        asyncio.run(tb.apply_backfill_plans([plan], dry_run=False))
    finally:
        cxmod.cxm = original
    assert calls["patch"] and "metadata" not in calls["update"][0]
