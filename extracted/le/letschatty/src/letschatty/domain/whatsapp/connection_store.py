"""The two stores of the WhatsApp connection (api-chatty `docs/whatsapp/estado-de-la-conexion.md`): the state of each
number (`whatsapp_connection_state`) and the connection log (`whatsapp_connection_events`). Two aggregates, two ports.

- The state carries its version: reading answers `(state, version)`, writing is compare-and-set on it (only the worker
  that wins the transition warns), and storing the banner moves the version too. No document means connected at
  version 0. The state is asked for by `(company_id, account_id)`: the stored `_id` is known only by the adapter.
- The log is append-only and its `_id` is the idempotency key, which is the event's `id` and a rule builds
  (`event_key_for`): claiming twice the same key loses (Meta's repeated delivery).

The sequence between the two (claim → compare-and-set → outcome, release if the transition raises) is not atomic, as in
`main`: it belongs to whoever uses them.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Protocol, Tuple

from pydantic import BaseModel

from .connection import ConnectionEvent, ConnectionState


class ConnectionEventOutcome(BaseModel):
    """What a signal did to the state, added to its log entry after the transition. A field that was not given is not
    written (the backfill writes only the two statuses)."""

    status_before: Optional[str] = None
    status_after: Optional[str] = None
    issue_code: Optional[str] = None
    notified: Optional[bool] = None


class ConnectionStateRepository(Protocol):
    async def get(self, company_id: str, account_id: Optional[str]) -> Tuple[ConnectionState, int]:
        """The state of the number and its version; without a document, connected at version 0."""
        ...

    async def compare_and_set(self, company_id: str, expected_version: int, state: ConnectionState) -> bool:
        """Writes `state` at `expected_version + 1` only if nobody changed it since `expected_version`. True if it won.
        Version 0 creates the document: a second creation loses."""
        ...

    async def set_banner(self, company_id: str, account_id: Optional[str], notification_id: Optional[str],
                         expected_version: int) -> bool:
        """Stores the banner of the state written at `expected_version` and moves the version. False if another worker
        changed it: that banner is stale and the caller retires it."""
        ...

    async def delete(self, company_id: str, account_id: Optional[str], expected_version: int) -> bool:
        """Deletes the state if nobody changed it since `expected_version`. True if it deleted it."""
        ...

    async def not_connected(self) -> List[ConnectionState]:
        """Every stored state that is not connected, of every company (the sweep and the lists)."""
        ...


class ConnectionEventLog(Protocol):
    async def claim(self, company_id: str, event: ConnectionEvent) -> bool:
        """Records the event under its `id`. False if it was already there: a repeated delivery."""
        ...

    async def release(self, company_id: str, event_id: str) -> None:
        """Undoes a claim whose transition failed: a repeated delivery retries it."""
        ...

    async def record_outcome(self, company_id: str, event_id: str, outcome: ConnectionEventOutcome) -> None:
        """Adds the outcome to the entry. An entry that is not there is not created."""
        ...

    async def has_event_since(self, company_id: str, source: str, since: datetime) -> bool:
        """Is there an entry of this `source` for the company since `since`?"""
        ...

    async def recent(self, company_id: str, limit: int) -> List[ConnectionEvent]:
        """The company's newest entries first, without Meta's raw payload. Read as stored: a field the entry does not
        have stays unset."""
        ...
