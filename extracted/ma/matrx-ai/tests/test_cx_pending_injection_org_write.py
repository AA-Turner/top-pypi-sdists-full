"""Regression: CxPendingInjectionManager.enqueue() must carry the parent
conversation's organization_id.

``chat.pending_injection.organization_id`` is NOT NULL. Before this fix,
``enqueue()`` built the create_item() call with ``conversation_id`` but no
``organization_id`` at all, so ANY caller (agent_call's "remember" write-back,
the /conversations/{id}/inbox endpoint) would have hit the NOT NULL
constraint the moment nothing upstream defaulted it. This test asserts the
row handed to ``create_item`` carries the pending injection's parent
conversation's organization_id — resolved from the conversation itself, not
guessed from the caller's ambient request context.
"""
from __future__ import annotations

from uuid import uuid4

import pytest

from matrx_ai.db import _cx_managers_impl as cx


class _FakeConversationQuery:
    def __init__(self, rows):
        self._rows = rows

    async def values(self, *_a, **_kw):
        return self._rows


class _FakeConversation:
    rows_by_id: dict[str, dict] = {}

    @classmethod
    def filter(cls, *, id, **_kw):  # noqa: A002 - matches the real signature
        row = cls.rows_by_id.get(id)
        return _FakeConversationQuery([row] if row else [])


class _FakeCreatedRow:
    def __init__(self, kwargs):
        self.id = kwargs.get("id") or uuid4()


@pytest.mark.asyncio
async def test_enqueue_carries_conversation_organization_id(monkeypatch):
    org_id = str(uuid4())
    conv_id = str(uuid4())
    _FakeConversation.rows_by_id = {conv_id: {"organization_id": org_id}}

    captured: dict = {}

    async def fake_create_item(self, **kwargs):
        captured.update(kwargs)
        return _FakeCreatedRow(kwargs)

    monkeypatch.setattr(cx, "CxConversation", _FakeConversation)
    monkeypatch.setattr(
        cx.CxPendingInjectionManager, "create_item", fake_create_item, raising=True
    )

    manager = cx.cx_pending_injection_manager_instance
    await manager.enqueue(
        injection_id=str(uuid4()),
        conversation_id=conv_id,
        created_by="user-1",
        kind="system_message",
        content={"text": "hi"},
        source="agent_collab",
        is_visible_to_user=False,
        is_visible_to_model=True,
    )

    assert captured.get("organization_id") == org_id
    assert captured.get("conversation_id") == conv_id


@pytest.mark.asyncio
async def test_enqueue_refuses_when_conversation_has_no_resolvable_org(monkeypatch):
    conv_id = str(uuid4())
    _FakeConversation.rows_by_id = {}  # conversation not found

    async def fake_create_item(self, **kwargs):
        raise AssertionError("create_item must not be reached without an organization_id")

    monkeypatch.setattr(cx, "CxConversation", _FakeConversation)
    monkeypatch.setattr(
        cx.CxPendingInjectionManager, "create_item", fake_create_item, raising=True
    )

    manager = cx.cx_pending_injection_manager_instance
    with pytest.raises(ValueError):
        await manager.enqueue(
            injection_id=str(uuid4()),
            conversation_id=conv_id,
            created_by="user-1",
            kind="system_message",
            content={"text": "hi"},
            source="agent_collab",
            is_visible_to_user=False,
            is_visible_to_model=True,
        )
