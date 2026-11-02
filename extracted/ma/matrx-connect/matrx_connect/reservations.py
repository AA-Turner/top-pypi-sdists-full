"""Record Reservation System — pre-create DB rows and announce IDs to clients.

Generalizes the proven conversation_id pattern: generate a UUID, INSERT a
minimal 'pending' row, announce the ID via a typed stream event, then UPDATE
with real data later.  The client always references a real row, never a phantom.

Usage in any execution path::

    from matrx_connect.reservations import get_tracker

    tracker = get_tracker()
    msg_id = await tracker.reserve(
        emitter=emitter,
        db_project="matrx",
        table="message",
        parent_refs={"conversation_id": conv_id, "user_request_id": req_id},
        metadata={"role": "assistant", "position": 3},
    )

    # ... later, after execution completes ...
    await tracker.mark_active(emitter, "message", msg_id)

Error recovery — called automatically by the fatal_error path::

    await tracker.fail_all_pending(emitter, db_project="matrx")
"""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from matrx_utils import vcprint

from matrx_connect.context.events import (
    RecordReservedPayload,
    RecordUpdatePayload,
)


@dataclass
class _TrackedRecord:
    db_project: str
    table: str
    record_id: str
    status: str = "pending"


class ReservationTracker:
    """Tracks all pre-reserved DB rows for the current request scope.

    Held in a ContextVar so it's available anywhere in the async call stack
    without threading through function arguments.
    """

    def __init__(self) -> None:
        self._records: list[_TrackedRecord] = []

    @staticmethod
    def generate_id() -> str:
        return str(uuid4())

    async def reserve(
        self,
        emitter: Any,
        db_project: str,
        table: str,
        parent_refs: dict[str, str] | None = None,
        metadata: dict[str, Any] | None = None,
        record_id: str | None = None,
        created_at: str | None = None,
    ) -> str:
        """Register a pre-created row and announce it to the client.

        The caller is responsible for the DB INSERT before calling this.
        This method tracks the record and emits the stream event.

        Args:
            emitter: The StreamEmitter (or any Emitter) for the current request.
            db_project: Database project discriminator (e.g. "matrx", "scraper").
            table: The exact table name (e.g. "message").
            parent_refs: Foreign key references the client needs (e.g. conversation_id).
            metadata: Extra hints for the client (e.g. role, position).
            record_id: Optional pre-generated UUID. If None, one is created.

        Returns:
            The UUID string used as the row PK.
        """
        if record_id is None:
            record_id = self.generate_id()

        if not self._has_record(table, record_id):
            self._records.append(
                _TrackedRecord(db_project=db_project, table=table, record_id=record_id)
            )

        payload = RecordReservedPayload(
            db_project=db_project,
            table=table,
            record_id=record_id,
            parent_refs=parent_refs or {},
            metadata=metadata or {},
            created_at=created_at,
        )
        await emitter.send_record_reserved(payload)

        vcprint(
            f"[ReservationTracker] Reserved {table}.{record_id[:8]}…",
            color="blue",
        )
        return record_id

    def register_existing(
        self,
        db_project: str,
        table: str,
        record_id: str,
    ) -> None:
        """Register an already-created row so the tracker can fail it on crash.

        Deduplicated: calling this with the same table+record_id is a no-op.
        """
        if self._has_record(table, record_id):
            return
        self._records.append(
            _TrackedRecord(db_project=db_project, table=table, record_id=record_id)
        )

    async def mark_active(
        self,
        emitter: Any,
        table: str,
        record_id: str,
        db_project: str = "matrx",
        metadata: dict[str, Any] | None = None,
        created_at: str | None = None,
    ) -> None:
        """Emit a record_update event transitioning a reserved row to active."""
        self._update_status(table, record_id, "active")
        payload = RecordUpdatePayload(
            db_project=db_project,
            table=table,
            record_id=record_id,
            status="active",
            metadata=metadata or {},
            created_at=created_at,
        )
        await emitter.send_record_update(payload)

    async def mark_completed(
        self,
        emitter: Any,
        table: str,
        record_id: str,
        db_project: str = "matrx",
        metadata: dict[str, Any] | None = None,
        created_at: str | None = None,
    ) -> None:
        """Emit a record_update event transitioning a reserved row to completed."""
        self._update_status(table, record_id, "completed")
        payload = RecordUpdatePayload(
            db_project=db_project,
            table=table,
            record_id=record_id,
            status="completed",
            metadata=metadata or {},
            created_at=created_at,
        )
        await emitter.send_record_update(payload)

    async def mark_failed(
        self,
        emitter: Any,
        table: str,
        record_id: str,
        db_project: str = "matrx",
        metadata: dict[str, Any] | None = None,
        created_at: str | None = None,
    ) -> None:
        """Emit a record_update event transitioning a reserved row to failed."""
        self._update_status(table, record_id, "failed")
        payload = RecordUpdatePayload(
            db_project=db_project,
            table=table,
            record_id=record_id,
            status="failed",
            metadata=metadata or {},
            created_at=created_at,
        )
        await emitter.send_record_update(payload)

    async def fail_all_pending(
        self,
        emitter: Any,
        db_project: str | None = None,
    ) -> None:
        """Mark every still-pending reservation as failed and notify the client.

        Called by the fatal_error path so the client knows which optimistic
        records did not materialize.
        """
        for rec in self._records:
            if rec.status != "pending":
                continue
            if db_project and rec.db_project != db_project:
                continue
            rec.status = "failed"
            try:
                # Discriminator for the FE: this failure is a ROLLBACK of an
                # optimistic reservation that never materialized — distinct from
                # a normal terminal-failed record (metadata.reason='terminal_status'
                # stamped by the persist path's mark_failed).
                payload = RecordUpdatePayload(
                    db_project=rec.db_project,
                    table=rec.table,
                    record_id=rec.record_id,
                    status="failed",
                    metadata={"reason": "rollback"},
                )
                await emitter.send_record_update(payload)
            except Exception as exc:
                vcprint(
                    f"[ReservationTracker] Failed to emit failure for "
                    f"{rec.table}.{rec.record_id[:8]}…: {exc}",
                    color="yellow",
                )

    def get_reserved_ids(self, table: str) -> list[str]:
        """Return all reserved IDs for a given table, in reservation order."""
        return [r.record_id for r in self._records if r.table == table]

    def _has_record(self, table: str, record_id: str) -> bool:
        return any(
            r.table == table and r.record_id == record_id for r in self._records
        )

    def _update_status(self, table: str, record_id: str, status: str) -> None:
        for rec in self._records:
            if rec.table == table and rec.record_id == record_id:
                rec.status = status
                return


# ---------------------------------------------------------------------------
# ContextVar — one tracker per async request scope
# ---------------------------------------------------------------------------

_reservation_tracker: ContextVar[ReservationTracker | None] = ContextVar(
    "reservation_tracker", default=None
)


def get_tracker() -> ReservationTracker:
    tracker = _reservation_tracker.get(None)
    if tracker is None:
        tracker = ReservationTracker()
        _reservation_tracker.set(tracker)
    return tracker


def try_get_tracker() -> ReservationTracker | None:
    return _reservation_tracker.get(None)
