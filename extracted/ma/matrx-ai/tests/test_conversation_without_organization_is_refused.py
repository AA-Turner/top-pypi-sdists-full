"""FORCING TEST — a conversation with no organization is refused BEFORE it is queued.

``chat.conversation.organization_id`` is NOT NULL and nothing may choose a tenant
(``common-docs/policies/context-is-carried-never-rebuilt.md``). On 2026-10-24 a
``server-door`` run reached the gate with no organization in its context; the gate
queued the INSERT anyway, the flush failed five times on NOT NULL, and the run went
on writing into a conversation that never existed — everything it did landed in
``ops.system_write_failure`` instead of the database.

Red before the fix: both doors queued/published the org-less row. Green after: both
raise ``ConversationGateError`` and queue nothing; with an organization they queue.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate
from matrx_ai.db.conversation_gate import ConversationGateError

ORG = "33333333-3333-4333-8333-333333333333"


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    gate._known_conversation_ids.clear()
    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    yield
    gate._known_conversation_ids.clear()


class _Conversation:
    async def filter_conversations(self, **_kwargs):
        return []


class _Coordinator:
    def set_correlation(self, **_kwargs):
        pass

    async def finalize(self, **_kwargs):
        pass


async def _none(*_args):
    return None


def _wire(monkeypatch, organization_id: str | None) -> list[dict]:
    queued: list[dict] = []
    coordinator = _Coordinator()
    monkeypatch.setattr(gate, "_get_coordinator", lambda: coordinator)
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(conversation=_Conversation()))
    monkeypatch.setattr(gate, "_queue_conversation_create", lambda **kw: queued.append(kw))
    monkeypatch.setattr(gate, "_require_valid_user_id", lambda value, _where="": value)
    monkeypatch.setattr(gate, "resolve_parent_conversation_lineage", _none)
    real_stamp = gate.stamp_org_id
    monkeypatch.setattr(gate, "stamp_org_id", lambda row, _ambient: real_stamp(row, organization_id))
    return queued


@pytest.mark.asyncio
@pytest.mark.parametrize("door", ["ensure", "create"])
async def test_no_organization_is_refused_and_nothing_is_queued(monkeypatch, door):
    queued = _wire(monkeypatch, None)
    conversation_id, user_id = str(uuid4()), str(uuid4())
    with pytest.raises(ConversationGateError, match="no organization"):
        if door == "ensure":
            await gate.ensure_conversation_exists(conversation_id, user_id)
        else:
            await gate.create_new_conversation(conversation_id, user_id)
    assert queued == []
    assert conversation_id not in gate._known_conversation_ids


@pytest.mark.asyncio
@pytest.mark.parametrize("door", ["ensure", "create"])
async def test_carried_organization_is_queued(monkeypatch, door):
    queued = _wire(monkeypatch, ORG)
    conversation_id, user_id = str(uuid4()), str(uuid4())
    if door == "ensure":
        await gate.ensure_conversation_exists(conversation_id, user_id)
    else:
        await gate.create_new_conversation(conversation_id, user_id)
    assert [row["organization_id"] for row in queued] == [ORG]
