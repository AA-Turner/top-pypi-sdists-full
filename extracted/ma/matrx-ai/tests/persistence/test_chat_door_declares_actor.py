"""FORCING TEST — one chat turn, two rows, two authors (DD-131).

A turn persists the person's typed message AND the model's answer. They have
DIFFERENT authors, and both rows are queued onto the SAME coordinator and
committed inside the SAME flush transaction. So a declaration wrapped around
the turn — or a transaction-wide GUC — can only ever tell one of the two
truths and must lie about the other.

Two legs, both about the real system:

1. ``test_the_door_declares_an_author_per_row`` — drives the REAL chat door
   (``queue_message_create`` / ``queue_message_update``) onto a REAL
   Coordinator and reads the author off the REAL queued ops. It fails against
   a door that declares nothing.

2. ``test_the_flush_emits_each_rows_author_to_postgres`` (``integration``) —
   runs the REAL flush against the LIVE database and asserts on the SQL
   asyncpg actually sent on that connection: ``set_config('app.actor_tier',
   'human')`` immediately before the person's row is INSERTed, and
   ``set_config('app.actor_tier','ai')`` immediately before the assistant's.
   Nothing here is stubbed — the statements are recorded by asyncpg's own
   query logger on the live connection, and the whole thing runs inside an
   outer transaction that is rolled back, so the database keeps no rows.

Deliberately NOT the harness of ``test_coordinator.py``: that suite replaces
``matrx_orm.transaction()`` wholesale, so it could only ever assert what the
test itself made up.
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path

import pytest
from dotenv import load_dotenv

REPO = Path(__file__).resolve().parents[4]
load_dotenv(REPO / ".env")

_HAS_DB = bool(os.environ.get("SUPABASE_MATRIX_HOST"))

USER_ACTOR = ("human", "chat_user_turn")
ASSISTANT_ACTOR = ("ai", "chat_assistant_turn")


# --------------------------------------------------------------------------
# Leg 1 — the door declares, per row, at queue time.
# --------------------------------------------------------------------------


def _bind_message_model() -> type:
    """The REAL chat.message Model, bound into the coordinator registry.

    Leg 1 never opens a connection — queueing only reads the Model's metadata —
    so the same binding serves both legs and neither test invents a table.
    """
    from db.models.chat import Message

    from matrx_ai.persistence.registry import register_table

    register_table("chat.message", Message)
    return Message


async def test_the_door_declares_an_author_per_row() -> None:
    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.queue_helpers import (
        _coordinator_cv,
        queue_message_create,
        queue_message_update,
    )
    _bind_message_model()

    coord = Coordinator(request_id=str(uuid.uuid4()))
    token = _coordinator_cv.set(coord)
    try:
        conversation_id = str(uuid.uuid4())
        user_row = str(uuid.uuid4())
        assistant_row = str(uuid.uuid4())

        queue_message_create(
            id=user_row,
            conversation_id=conversation_id,
            role="user",
            position=0,
            status="active",
            content=[{"type": "text", "text": "what did I write?"}],
        )
        queue_message_create(
            id=assistant_row,
            conversation_id=conversation_id,
            role="assistant",
            position=1,
            status="pending",
            content=[],
        )
        # The assistant row is finalized by a later UPDATE that names no role.
        # It must not lose the author its INSERT declared.
        queue_message_update(assistant_row, status="active", content=[{"type": "text"}])

        inserts = {op.pk_value: op for op in coord._session._ops if op.op_type == "insert"}
        assert set(inserts) >= {user_row, assistant_row}

        person = inserts[user_row].actor
        assistant = inserts[assistant_row].actor
        assert person is not None, "the person's typed row was queued with NO declared author"
        assert assistant is not None, "the assistant row was queued with NO declared author"
        assert (person.tier, person.system) == USER_ACTOR
        assert (assistant.tier, assistant.system) == ASSISTANT_ACTOR

        # And through coalescing (what the flush actually executes).
        from matrx_orm.session.coalesce import coalesce_ops

        coalesced = {op.pk_value: op for op in coalesce_ops(list(coord._session._ops))}
        assert coalesced[user_row].actor.tier == "human"
        assert coalesced[assistant_row].actor.tier == "ai"
    finally:
        _coordinator_cv.reset(token)
        coord._session._ops.clear()


# --------------------------------------------------------------------------
# Leg 2 — the declaration reaches Postgres, per row, at flush.
# --------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.skipif(not _HAS_DB, reason="needs the live platform database (SUPABASE_MATRIX_*)")
async def test_the_flush_emits_each_rows_author_to_postgres() -> None:
    # No host import: the pool is opened the way any standalone consumer opens
    # it, and the ONE table this test writes is bound directly.
    from matrx_orm import register_platform_db

    register_platform_db(
        "supabase_automation_matrix",
        package="chat_door_actor_forcing_test",
        additional_schemas=["chat", "auth", "iam"],
    )
    from db.models.chat import Conversation
    from matrx_orm.core.transaction import _active_connection, transaction

    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.queue_helpers import _coordinator_cv, queue_message_create

    Message = _bind_message_model()

    rows = await Conversation.filter(deleted_at=None).limit(1).values(
        "id", "organization_id", "created_by"
    )
    if not rows:
        pytest.skip("no live conversation to attach a turn to")
    conversation = rows[0]

    recorded: list[tuple[str, tuple]] = []

    class _Rollback(Exception):
        pass

    user_row = str(uuid.uuid4())
    assistant_row = str(uuid.uuid4())
    coord = Coordinator(request_id=str(uuid.uuid4()))
    token = _coordinator_cv.set(coord)
    try:
        try:
            async with transaction("supabase_automation_matrix"):
                conn = _active_connection.get()
                conn.add_query_logger(
                    lambda record: recorded.append((record.query, tuple(record.args or ())))
                )
                for row_id, role, position in (
                    (user_row, "user", 9_000_001),
                    (assistant_row, "assistant", 9_000_002),
                ):
                    queue_message_create(
                        id=row_id,
                        conversation_id=str(conversation["id"]),
                        role=role,
                        position=position,
                        status="active",
                        content=[{"type": "text", "text": "DD-131 forcing test"}],
                        organization_id=str(conversation["organization_id"]),
                        created_by=conversation["created_by"],
                    )
                report = await coord.flush(reason="manual")
                assert report.error is None, report.error
                assert report.ops_written == 2, report
                # Both rows really are in the database — inside this transaction.
                landed = await Message.filter(id__in=[user_row, assistant_row]).values("id")
                assert len(landed) == 2, landed
                raise _Rollback
        except _Rollback:
            pass
    finally:
        _coordinator_cv.reset(token)

    # What Postgres was actually told, in order.
    timeline: list[str] = []
    for query, args in recorded:
        if "set_config" in query and args and args[0] == "app.actor_tier":
            timeline.append(f"tier={args[1]}")
        elif "INSERT INTO" in query.upper() and "message" in query:
            if user_row in str(args):
                timeline.append("insert=user_row")
            elif assistant_row in str(args):
                timeline.append("insert=assistant_row")

    assert "tier=human" in timeline, f"the person's author never reached Postgres: {timeline}"
    assert "tier=ai" in timeline, f"the assistant's author never reached Postgres: {timeline}"
    assert timeline.index("tier=human") < timeline.index("insert=user_row"), timeline
    assert timeline.index("tier=ai") < timeline.index("insert=assistant_row"), timeline
    # Each row is written under ITS OWN declaration, not one turn-wide stamp.
    assert timeline.index("insert=user_row") < timeline.index("tier=ai"), timeline
