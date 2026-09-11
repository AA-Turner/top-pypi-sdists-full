"""Org-owned machine cost anchors never impersonate a chat user."""

from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate
from matrx_ai.db.ownership_fields import is_organization_system_actor

ORG = "66666666-6666-4666-8666-666666666666"


@pytest.mark.parametrize(
    "actor,system_run,org,allowed",
    [
        (None, True, ORG, True),
        ("", True, ORG, True),
        (" ", True, ORG, True),
        ("broken", True, ORG, False),
        (None, False, ORG, False),
        (None, 1, ORG, False),
        (None, True, "", False),
        (None, True, "broken", False),
        (42, True, ORG, False),
    ],
)
def test_actor_boundary(actor, system_run, org, allowed):
    assert (
        is_organization_system_actor(
            actor, SimpleNamespace(system_run=system_run, organization_id=org)
        )
        is allowed
    )


@pytest.fixture
def guest(monkeypatch):
    import matrx_ai.context.app_context as context
    from matrx_ai.context.app_context import AppContext

    ctx = AppContext(emitter=None, user_id="", organization_id=ORG, system_run=True)
    monkeypatch.setattr(context, "try_get_app_context", lambda: ctx)
    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    monkeypatch.setattr(gate, "_get_coordinator", lambda: object())
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: object())
    gate._known_conversation_ids.clear()
    gate._ensured_request_ids.clear()
    return ctx


@pytest.mark.asyncio
async def test_guest_creates_both_cost_anchors_with_explicit_null_actor(guest, monkeypatch):
    conversation = SimpleNamespace(filter_conversations=AsyncMock(return_value=[]))
    request = SimpleNamespace(filter_user_requests=AsyncMock(return_value=[]))
    monkeypatch.setattr(
        gate, "_cxm", lambda: SimpleNamespace(conversation=conversation, user_request=request)
    )
    monkeypatch.setattr(gate, "resolve_parent_conversation_lineage", AsyncMock(return_value=None))
    queued = []
    monkeypatch.setattr(gate, "_queue_conversation_create", lambda **kw: queued.append(kw))
    monkeypatch.setattr(gate, "_queue_user_request_create", lambda **kw: queued.append(kw))
    await gate.ensure_conversation_exists(str(uuid4()), "")
    await gate.ensure_user_request_exists(str(uuid4()), "")
    # Breaks caught: either writer dropping the org, or stamping any org other
    # than the one the run explicitly carries (a default / personal / system org).
    assert [(row.get("created_by", "MISSING"), row.get("organization_id")) for row in queued] == [
        (None, ORG),
        (None, ORG),
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["conversation", "user_request"])
async def test_existing_matching_system_anchor_is_adopted_without_a_new_write(
    guest, monkeypatch, kind
):
    # Break caught: an owner check that refuses every existing anchor (or
    # re-creates it) would fail every resumed org-owned system run.
    pk = str(uuid4())
    same = [{"organization_id": ORG, "created_by": None}]
    monkeypatch.setattr(
        gate,
        "_cxm",
        lambda: SimpleNamespace(
            conversation=SimpleNamespace(filter_conversations=AsyncMock(return_value=same)),
            user_request=SimpleNamespace(filter_user_requests=AsyncMock(return_value=same)),
        ),
    )
    queued = []
    monkeypatch.setattr(gate, "_queue_conversation_create", lambda **kw: queued.append(kw))
    monkeypatch.setattr(gate, "_queue_user_request_create", lambda **kw: queued.append(kw))
    fn = (
        gate.ensure_conversation_exists
        if kind == "conversation"
        else gate.ensure_user_request_exists
    )
    await fn(pk, "")
    assert queued == []


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["conversation", "user_request"])
@pytest.mark.parametrize(
    "row",
    [
        pytest.param({"organization_id": "OTHER", "created_by": None}, id="other_org"),
        pytest.param({"organization_id": ORG, "created_by": "HUMAN"}, id="same_org_human_owned"),
    ],
)
async def test_existing_foreign_anchor_refused_even_when_memoized(guest, monkeypatch, kind, row):
    pk = str(uuid4())
    wrong = [
        {
            "organization_id": str(uuid4()) if row["organization_id"] == "OTHER" else ORG,
            "created_by": str(uuid4()) if row["created_by"] == "HUMAN" else None,
        }
    ]
    monkeypatch.setattr(
        gate,
        "_cxm",
        lambda: SimpleNamespace(
            conversation=SimpleNamespace(filter_conversations=AsyncMock(return_value=wrong)),
            user_request=SimpleNamespace(filter_user_requests=AsyncMock(return_value=wrong)),
        ),
    )
    gate._known_conversation_ids[pk] = gate._ENSURED_DURABLE
    gate._ensured_request_ids[pk] = gate._ENSURED_DURABLE
    fn = (
        gate.ensure_conversation_exists
        if kind == "conversation"
        else gate.ensure_user_request_exists
    )
    with pytest.raises(gate.ConversationGateError, match="different principal"):
        await fn(pk, "")


@pytest.mark.parametrize("system_run,actor", [(False, ""), (True, "broken")])
def test_normal_chat_and_malformed_actor_stay_strict(guest, system_run, actor, monkeypatch):
    import matrx_ai.context.app_context as context

    monkeypatch.setattr(
        context,
        "try_get_app_context",
        lambda: __import__("dataclasses").replace(guest, system_run=system_run),
    )
    with pytest.raises(gate.ConversationGateError):
        gate._require_persistence_actor(actor, "test")


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["conversation", "user_request"])
@pytest.mark.parametrize("race_row", [True, False])
async def test_failed_anchor_insert_never_admits_wrong_owner_or_missing_row(
    guest, monkeypatch, kind, race_row
):
    from contextlib import asynccontextmanager, nullcontext

    import matrx_orm

    wrong = [{"organization_id": str(uuid4()), "created_by": None}] if race_row else []

    @asynccontextmanager
    async def broken_session():
        raise RuntimeError("insertion failed")
        yield

    monkeypatch.setattr(matrx_orm, "Session", broken_session)
    monkeypatch.setattr(matrx_orm, "allow_direct_coordinator_write", lambda *a, **kw: nullcontext())
    monkeypatch.setattr(gate, "_get_coordinator", lambda: None)
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: None)
    monkeypatch.setattr(gate, "resolve_parent_conversation_lineage", AsyncMock(return_value=None))
    manager = SimpleNamespace(
        model=object(),
        filter_conversations=AsyncMock(side_effect=[[], wrong]),
        filter_user_requests=AsyncMock(side_effect=[[], wrong]),
    )
    monkeypatch.setattr(
        gate, "_cxm", lambda: SimpleNamespace(conversation=manager, user_request=manager)
    )
    expected = "different principal" if race_row else "Cannot establish organization system-run"
    with pytest.raises(gate.ConversationGateError, match=expected):
        if kind == "conversation":
            await gate.ensure_conversation_exists(str(uuid4()), "")
        else:
            await gate._create_user_request(request_id=str(uuid4()), user_id=None)


def test_missing_argument_cannot_discard_ambient_human_actor():
    assert not is_organization_system_actor(
        None, SimpleNamespace(system_run=True, organization_id=ORG, user_id=str(uuid4()))
    )
