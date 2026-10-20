"""FORCING TEST — a message is written as the person who sent it, never as the conversation's owner.

Defect 55 (PB-06, live build 62046bc5, conversation 21b9ff88-b093-46cc-aa57-020a6e35d7ac): the
EDITOR seat (test@test.com, shared in at editor) sent ``Editor here. Send the line once more.``;
the request carried the editor (``chat.user_request.created_by`` = the editor), but the stored
user row f72cc755 and the reply 210b4588 named only admin — the conversation's owner.

Why: ``chat.message`` is a COMPONENT of ``chat.conversation`` (db-rules §6d-1). The trigger
``zzz_component_created_by`` rewrites ``created_by`` to the PARENT's owner on every insert, so
``created_by`` can never say who wrote a message. The saver lives in ``updated_by``
(``aidream.services.provenance.component_actor.component_saver``), which
``platform._stamp_actor`` fills from ``app.user_id`` / ``auth.uid()`` — both empty on the
server's privileged write connection. Every server-written message therefore landed with
``updated_by`` NULL and the only person on the row was the owner.

The fix lives at the ONE chat.message write funnel (``queue_message_create`` /
``queue_message_update``): every insert carries ``updated_by`` = the request's own actor
(the carried AppContext), whatever ``created_by`` the caller passed.

Two legs, two distinct users on one shared conversation:

1. ``test_the_door_stamps_the_requests_own_actor`` — the real door onto a real Coordinator.
2. ``test_two_seats_on_one_conversation_land_as_themselves`` (``integration``) — the real flush
   against the LIVE database inside a rolled-back transaction: the owner's turn and the
   editor's turn on one conversation, read back from Postgres.
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest
from dotenv import load_dotenv

REPO = Path(__file__).resolve().parents[4]
load_dotenv(REPO / ".env")

_HAS_DB = bool(os.environ.get("SUPABASE_MATRIX_HOST"))

_ORG = "66666666-6666-4666-8666-666666666666"
OWNER = "11111111-1111-4111-8111-111111111111"
EDITOR = "22222222-2222-4222-8222-222222222222"
ADMIN_SEAT = "87a6e699-3622-4869-8843-d0867456c0dd"  # admin@admin.com
TEST_SEAT = "4060701e-706a-4c76-b3ca-0bbc69fa5a14"  # test@test.com


class _MessageMeta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "message"
    db_schema = "chat"


class _PackageMessage:
    _meta = _MessageMeta()


def _request_as(monkeypatch, user_id: str, organization_id: str = _ORG) -> None:
    from matrx_ai.persistence import queue_helpers

    monkeypatch.setattr(
        queue_helpers,
        "_resolve_app_context",
        lambda: SimpleNamespace(
            organization_id=organization_id,
            request_id=str(uuid.uuid4()),
            user_id=user_id,
            conversation_id=None,
        ),
    )


async def test_the_door_stamps_the_requests_own_actor(monkeypatch) -> None:
    from matrx_orm.session.coalesce import coalesce_ops

    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.queue_helpers import (
        _coordinator_cv,
        queue_message_create,
        queue_message_update,
    )
    from matrx_ai.persistence.registry import override_table

    coord = Coordinator(request_id=str(uuid.uuid4()))
    token = _coordinator_cv.set(coord)
    stand_in = override_table("chat.message", _PackageMessage)
    stand_in.__enter__()
    try:
        conversation_id = str(uuid.uuid4())
        owner_row, editor_row, reply_row = (str(uuid.uuid4()) for _ in range(3))

        _request_as(monkeypatch, OWNER)
        queue_message_create(
            id=owner_row, conversation_id=conversation_id, role="user", status="active",
            content=[{"type": "text", "text": "owner turn"}], created_by=OWNER,
        )

        # The editor's turn — the caller hands the CONVERSATION OWNER as created_by
        # (what a persistence path that reads the conversation row does). The row must
        # still name the editor.
        _request_as(monkeypatch, EDITOR)
        queue_message_create(
            id=editor_row, conversation_id=conversation_id, role="user", status="active",
            content=[{"type": "text", "text": "Editor here."}], created_by=OWNER,
        )
        # The reply: reserved pending, then finalized by an UPDATE carrying the author fields.
        queue_message_create(
            id=reply_row, conversation_id=conversation_id, role="assistant", status="pending",
            content=[],
        )
        queue_message_update(
            reply_row, status="active", content=[{"type": "text", "text": "line"}], created_by=OWNER,
        )

        ops = {op.pk_value: op for op in coalesce_ops(list(coord._session._ops))}
        saver = {pk: (op.payload or {}).get("updated_by") for pk, op in ops.items()}
        assert saver[owner_row] == OWNER, saver
        assert saver[editor_row] == EDITOR, (
            f"the editor's message was queued as {saver[editor_row]!r}, not the editor"
        )
        assert saver[reply_row] == EDITOR, (
            f"the reply to the editor's turn was queued as {saver[reply_row]!r}, not the editor"
        )
    finally:
        stand_in.__exit__(None, None, None)
        _coordinator_cv.reset(token)
        coord._session._ops.clear()


async def test_an_update_that_does_not_author_keeps_the_sender(monkeypatch) -> None:
    """A later bookkeeping UPDATE (no author fields) by another seat never re-attributes the row."""
    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.queue_helpers import _coordinator_cv, queue_message_update
    from matrx_ai.persistence.registry import override_table

    coord = Coordinator(request_id=str(uuid.uuid4()))
    token = _coordinator_cv.set(coord)
    stand_in = override_table("chat.message", _PackageMessage)
    stand_in.__enter__()
    try:
        _request_as(monkeypatch, OWNER)
        row = str(uuid.uuid4())
        queue_message_update(row, is_visible_to_model=False)
        (op,) = [o for o in coord._session._ops if o.pk_value == row]
        assert "updated_by" not in (op.payload or {}), op.payload
    finally:
        stand_in.__exit__(None, None, None)
        _coordinator_cv.reset(token)
        coord._session._ops.clear()


@pytest.mark.integration
@pytest.mark.skipif(not _HAS_DB, reason="needs the live platform database (SUPABASE_MATRIX_*)")
async def test_two_seats_on_one_conversation_land_as_themselves(monkeypatch) -> None:
    """Live: admin's conversation, two distinct real users, read back from Postgres, rolled back."""
    from matrx_orm import register_platform_db

    register_platform_db(
        "supabase_automation_matrix",
        package="message_sender_forcing_test",
        additional_schemas=["chat", "auth", "iam"],
    )
    from db.models.chat import Conversation, Message
    from matrx_orm.core.transaction import transaction

    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.queue_helpers import _coordinator_cv, queue_message_create
    from matrx_ai.persistence.registry import override_table

    # The two fixed test seats (aidream CLAUDE.md): the owner and the non-admin second seat.
    owner, editor = ADMIN_SEAT, TEST_SEAT
    # admin's Workspace — never the Safety Net Real Tests organization.
    rows = await Conversation.filter(
        created_by=owner, organization_id="884d1ce8-7b49-4fba-a2f3-0f7dd7c83d4f", deleted_at=None
    ).limit(1).values("id", "organization_id")
    if not rows:
        pytest.skip("no conversation of admin's in admin's Workspace to attach a turn to")
    conversation = rows[0]

    class _Rollback(Exception):
        pass

    owner_row, editor_row = str(uuid.uuid4()), str(uuid.uuid4())
    landed: dict[str, dict] = {}
    with override_table("chat.message", Message):
        try:
            async with transaction("supabase_automation_matrix"):
                for row_id, actor, position in ((owner_row, owner, 9_100_001), (editor_row, editor, 9_100_002)):
                    coord = Coordinator(request_id=str(uuid.uuid4()))
                    token = _coordinator_cv.set(coord)
                    try:
                        _request_as(monkeypatch, actor, str(conversation["organization_id"]))
                        queue_message_create(
                            id=row_id,
                            conversation_id=str(conversation["id"]),
                            role="user",
                            position=position,
                            status="active",
                            content=[{"type": "text", "text": "defect 55 forcing test"}],
                            organization_id=str(conversation["organization_id"]),
                            created_by=owner,
                        )
                        report = await coord.flush(reason="manual")
                        assert report.error is None, report.error
                    finally:
                        _coordinator_cv.reset(token)
                for r in await Message.filter(id__in=[owner_row, editor_row]).values(
                    "id", "created_by", "updated_by"
                ):
                    landed[str(r["id"])] = {k: str(v) if v else None for k, v in r.items()}
                raise _Rollback
        except _Rollback:
            pass

    assert set(landed) == {owner_row, editor_row}, landed
    # created_by is the PARENT's owner on a component — by law, for both rows.
    assert landed[editor_row]["created_by"] == owner, landed
    assert landed[owner_row]["updated_by"] == owner, landed
    assert landed[editor_row]["updated_by"] == editor, (
        f"the editor's message landed in Postgres as {landed[editor_row]['updated_by']!r}; "
        f"nothing on the row names the editor {editor}"
    )
