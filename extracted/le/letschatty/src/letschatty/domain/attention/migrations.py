"""Attention migrations («migraciones de atención»): the port of `migraciones_de_atencion` (api-chatty
`docs/atencion/migracion-a-entradas.md`).

A migration moves the automation of the sources to entradas, with 30 days to undo it. It is a state machine
(`states.MIGRATION_*`): ONE active per company (a unique partial index on `company_id` among `aplicada`), and every
move of the undo is conditional on the state, so of two undos of the same migration only one wins.

The port speaks of `AttentionMigration` with English names; only the Mongo adapter knows the stored shape (Spanish
keys, `_id` as an `ObjectId`). What the migration saved of each source before touching it (`SourceCopy.fields`) is the
raw copy of what Mongo held, restored byte by byte on undo: the domain carries it as a payload it does not interpret
(ADR-013, «Excepciones»), also the keys of the motivos that migrations applied before `firma.py` changed still hold.
Without cache.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Mapping, Optional, Protocol, Tuple

__all__ = ["AttentionMigration", "AttentionMigrationRepository", "SourceCopy"]


@dataclass(frozen=True)
class SourceCopy:
    """A source as it was before the migration: `fields` is what its document held of the migrated fields (stored
    values, untouched), `absent` the migrated fields it did not have (removed on undo)."""
    source_id: str
    fields: Mapping[str, Any] = field(default_factory=dict)
    absent: Tuple[str, ...] = ()


@dataclass(frozen=True)
class AttentionMigration:
    """A migration as it was stored. A field the document lacks is None (`response` is absent until the apply
    completes). `applied_by` is None when no user applied it (an `x-api-key` call)."""
    id: Optional[str] = None
    company_id: Optional[str] = None
    state: Optional[str] = None
    complete: bool = False
    applied_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    applied_by: Optional[str] = None
    body_hash: Optional[str] = None
    sources_before: Tuple[SourceCopy, ...] = ()
    entries_created: Tuple[str, ...] = ()
    reasons_created: Tuple[str, ...] = ()
    response: Optional[Dict[str, Any]] = None


class AttentionMigrationRepository(Protocol):
    async def latest(self, company_id: str) -> Optional[AttentionMigration]:
        """The company's migration with the latest `applied_at`, whatever its state, or None."""
        ...

    async def active(self, company_id: str, now: datetime) -> Optional[AttentionMigration]:
        """The company's latest migration that is applied or being undone and expires after `now`, or None."""
        ...

    async def expire_overdue(self, company_id: str, now: datetime) -> None:
        """Every applied or undoing migration of the company that expired by `now` becomes `expired`."""
        ...

    async def open(self, migration: AttentionMigration) -> bool:
        """Stores the migration as it was built (with its id). False if the company already has an applied one (the
        unique partial index), nothing stored."""
        ...

    async def get(self, migration_id: str) -> Optional[AttentionMigration]:
        """The migration with that id (any company: the id comes from a read of the company's own), or None."""
        ...

    async def mark_failed(self, migration_id: str) -> None: ...

    async def complete(self, migration_id: str, response: Dict[str, Any]) -> None:
        """The apply finished: `complete` and its `response`."""
        ...

    async def mark_undone(self, migration_id: str, now: datetime) -> None: ...

    async def record_created_reason(self, migration_id: str, reason_id: str) -> None:
        """Appends the reason to what the migration created, right after it was created (so an undo knows it)."""
        ...

    async def record_created_entry(self, migration_id: str, entry_id: str) -> None:
        """Same, for an entry."""
        ...

    async def take_undo(self, migration_id: str, now: datetime) -> bool:
        """`applied → undoing` if it still is applied, noting `now`; whether it matched."""
        ...

    async def resume_undo(self, migration_id: str, now: datetime, stale_before: datetime) -> bool:
        """An undo left half way (`undoing` since `stale_before` or earlier) is taken again, noting `now`; whether it
        matched."""
        ...
