"""Delayed entries («entradas demoradas»): the port of `entradas_pendientes` (api-chatty
`docs/atencion/entrada-demorada.md`).

The entry of a NEW chat (welcome, reason, automations, AI, `message.received`) runs `Recepcion.bienvenida_demora_s`
seconds later. One document per waiting entry; its stored form (Spanish names and values, as in `main`) is the Mongo
adapter's (`letschatty/mongo/attention/pending_entry_repository.py`): the port takes fields and answers the models
below. Without cache.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Mapping, Optional, Protocol

__all__ = ["DuePendingEntry", "PendingEntry", "PendingEntryRepository"]


@dataclass(frozen=True)
class PendingEntry:
    """A delayed entry as a claim or a read answers it. `state` is one of the stored states (`states.ENTRY_*`).

    `messages` and `processed` are the message ids, read when they are asked for, as `main` read them while running the
    messages: a stored value that is not a list fails there, after the attempts are checked, not on the claim
    (`raw_messages`/`raw_processed` keep what was stored). `contact_points` and `traces` are the stored maps, as they
    are: the first message's id is a key, and the id of an added one with a dot in it (a wamid) is nested at that dot,
    so looking it up finds nothing (ENG-166)."""
    id: str
    company_id: Optional[str]
    chat_id: Optional[str]
    state: Optional[str]
    attempts: int
    due_at: Optional[datetime]
    raw_messages: Any = ()
    raw_processed: Any = ()
    contact_points: Mapping[str, Any] = field(default_factory=dict)
    traces: Mapping[str, Any] = field(default_factory=dict)

    @property
    def messages(self) -> List[str]:
        return [str(m) for m in (self.raw_messages or [])]

    @property
    def processed(self) -> List[str]:
        return [str(m) for m in (self.raw_processed or [])]


@dataclass(frozen=True)
class DuePendingEntry:
    """An open entry that is due (the sweep and the startup recovery): `next_at` is its due time while pending and the
    end of its lease while sending. `company_id`/`chat_id` are None only if the document lacks the key (a stored null is
    the text "None", as `str(doc[key])` was in `main`)."""
    id: str
    company_id: Optional[str]
    chat_id: Optional[str]
    next_at: Optional[datetime]


class PendingEntryRepository(Protocol):
    async def open(self, company_id: str, *, chat_id: str, message_id: str, contact_point_id: Optional[str],
                   trace_id: Optional[str], delay_s: int, due_at: datetime, now: datetime) -> Optional[str]:
        """Stores a pending entry of the chat with this first message, due at `due_at`, and answers its id; None if
        the chat already had an open one."""
        ...

    async def add_message(self, chat_id: str, message_id: str, contact_point_id: Optional[str],
                          trace_id: Optional[str]) -> bool:
        """Adds the message at the end of the chat's open entry (once), with its contact point and trace under
        `contact_points.<message_id>` / `trazas.<message_id>`; True if the chat had an open entry."""
        ...

    async def claim(self, item_id: str, *, due_by: datetime, now: datetime, lease_until: datetime,
                    claimed_by: str) -> Optional[PendingEntry]:
        """Atomic, for one caller: an open entry that is pending and due by `due_by`, or sending with a lease that
        ended before `now`, becomes sending until `lease_until` with one more attempt. Answers it as it is after the
        claim, or None."""
        ...

    async def read(self, item_id: str) -> Optional[PendingEntry]:
        """The entry as it is now, or None."""
        ...

    async def mark_processed(self, item_id: str, message_id: str, *, lease_until: datetime) -> None:
        """The message ran: it is not run again; the lease lasts until `lease_until`."""
        ...

    async def close(self, item_id: str, *, messages: int, now: datetime) -> bool:
        """Done, only if it is sending and still has `messages` messages (nobody added one); True if it closed."""
        ...

    async def fail(self, item_id: str, *, now: datetime, error: str) -> None:
        """Closes it failed with `error`: it is no longer open."""
        ...

    async def due(self, *, until: datetime, limit: int) -> List[DuePendingEntry]:
        """The open ones whose next time is by `until`, up to `limit`."""
        ...
