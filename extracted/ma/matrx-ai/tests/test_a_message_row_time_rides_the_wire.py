"""The row's time is stamped once on the server and sent on the wire.

The chat's "Worked for" is the wall clock between a turn's message rows' ``createdAt``. A live
client used to stamp its own receipt time while the database kept the server's, so the live-final
line and the reloaded one differed by a second. The server now writes ``created_at`` explicitly
and puts the SAME instant on ``record_reserved`` / ``record_update`` (matrx-connect events).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

import pytest
import test_provider_id_never_message_pk as base
from matrx_connect.context.events import RecordReservedPayload, RecordUpdatePayload
from matrx_connect.reservations import ReservationTracker

from matrx_ai.orchestrator.execution_state import ExecutionState


@pytest.fixture()
def harness(monkeypatch):
    """The persistence harness of the provider-id suite (one stub set, not a second copy)."""
    return base.persist_harness.__wrapped__(monkeypatch)


class _Recorder:
    def __init__(self) -> None:
        self.reserved: list[RecordReservedPayload] = []
        self.updates: list[RecordUpdatePayload] = []

    async def send_record_reserved(self, payload: RecordReservedPayload) -> None:
        self.reserved.append(payload)

    async def send_record_update(self, payload: RecordUpdatePayload) -> None:
        self.updates.append(payload)


async def test_tracker_puts_created_at_on_the_wire():
    rec = _Recorder()
    tracker = ReservationTracker()
    stamp = "2026-10-29T12:00:00.123456+00:00"
    await tracker.reserve(rec, "matrx", "message", record_id=str(uuid4()), created_at=stamp)
    await tracker.mark_active(rec, "message", rec.reserved[0].record_id, created_at=stamp)
    assert rec.reserved[0].model_dump()["created_at"] == stamp
    assert rec.updates[0].model_dump()["created_at"] == stamp
    # Older callers that know no time still emit a valid frame.
    await tracker.mark_completed(rec, "message", rec.reserved[0].record_id)
    assert rec.updates[1].created_at is None


@pytest.mark.asyncio
async def test_persisted_row_stores_the_instant_the_stream_announced(harness, monkeypatch):
    persistence_mod, creates, updates = harness
    rec = _Recorder()
    tracker = ReservationTracker()
    monkeypatch.setattr(persistence_mod, "try_get_tracker", lambda: tracker)

    completed = base._build_tool_loop_completed()
    reserved_ids = {0: str(uuid4()), 1: str(uuid4())}
    state = ExecutionState()
    state.reserved_message_ids = dict(reserved_ids)
    from matrx_ai.context import app_context as _ctx  # emitter comes from the app context

    class _Ctx:
        user_id = "22222222-2222-2222-2222-222222222222"
        conversation_id = base.CONVERSATION_ID
        store = True
        emitter = rec

    monkeypatch.setattr(_ctx, "get_app_context", lambda: _Ctx())
    monkeypatch.setattr(_ctx, "try_get_app_context", lambda: _Ctx())

    await persistence_mod.persist_completed_request(
        completed, conversation_id=base.CONVERSATION_ID, state=state
    )

    stored: dict[str, Any] = {mid: kw["created_at"] for mid, kw in updates}
    stored.update({kw["id"]: kw["created_at"] for kw in creates})
    assert stored, "persist wrote no message rows"
    for value in stored.values():
        datetime.fromisoformat(value)

    announced = {p.record_id: p.created_at for p in rec.updates if p.table == "message"}
    assert announced, "no message record_update carried a time (emitter not reached)"
    for record_id, at in announced.items():
        assert at == stored[record_id], "the wire time must be the stored time"
