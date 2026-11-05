"""The template sync stamp («sello de sincronización de plantillas»): one per WABA and company, the durable record that
a company synced the templates of a WABA (when, the last error, Meta's quota). The port every store of it implements,
and the pure rule about it.

The stamp is per (WABA, company), not per WABA: a WABA of Meta can hold several numbers and, in Chatty, each number is
a company with its own template rows; a stamp per WABA would mark a sibling company fresh while it has no rows. It
exists so a WABA with zero templates still records that it was synced (the negative cache of the read).

Not a catalog (ADR-010 of api-chatty): it is upserted by its natural key, never listed, created by id nor deleted, and
nothing is cached.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional, Protocol, Union


@dataclass(frozen=True)
class TemplateSyncState:
    """The stamp as stored. A field the document lacks is None (prod has stamps that only ever failed: no
    `last_synced_at` nor `message_template_limit`). `last_synced_at` keeps its stored type: a date (without zone, as
    Mongo hands it back) or, in an old document, a text. `id` is the stored document's id, as text."""
    id: str
    company_id: str
    waba_id: str
    last_synced_at: Optional[Union[datetime, str]] = None
    last_sync_error: Optional[str] = None
    message_template_limit: Optional[int] = None
    updated_at: Optional[datetime] = None
    # The keys of the stored document that this model does not name, by their stored name and as stored: the legacy
    # store hands its callers the whole document, as `main` did (tanda 17b).
    others: Mapping[str, Any] = field(default_factory=dict)


def is_fresh(state: Optional[TemplateSyncState], now: datetime, ttl_seconds: int) -> bool:
    """The company synced the WABA less than `ttl_seconds` ago. No stamp or no date is stale; a text date is read with
    `fromisoformat` (and raises its `ValueError` if it is not one); a date without zone is UTC."""
    if not state or not state.last_synced_at:
        return False
    last = state.last_synced_at
    if isinstance(last, str):
        last = datetime.fromisoformat(last)
    if last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)
    return (now - last).total_seconds() < ttl_seconds


class TemplateSyncStateRepository(Protocol):
    async def get(self, company_id: str, waba_id: str) -> Optional[TemplateSyncState]:
        """The stamp of this company and WABA (the company compared as stored text), or None."""
        ...

    async def mark_synced(self, company_id: str, waba_id: str, *, at: datetime,
                          message_template_limit: Optional[int]) -> None:
        """Upserts the stamp: synced `at` (also its `updated_at`), no error, Meta's quota as it came."""
        ...

    async def mark_error(self, company_id: str, waba_id: str, *, error: str, at: datetime) -> None:
        """Upserts the stamp with the error and `updated_at`; the date of the last good sync and the quota stay."""
        ...
