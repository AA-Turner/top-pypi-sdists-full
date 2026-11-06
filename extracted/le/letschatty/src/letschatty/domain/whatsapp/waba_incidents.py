"""An incident of WABA («incidente de WABA», api-chatty `docs/whatsapp/incidentes-de-waba.md`): Meta blocking a WABA for
good (141008), from the first send that sees it until a later send finds Meta no longer says so. One document per WABA:
the WABA names the document, so the company is never part of a filter, and the last company that failed is the one
stored.

«Am I the first?» and «am I the one who resolves?» are decided by conditional writes, so only one worker notifies each.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional, Protocol, Set

#: The two states of an incident, as they are stored.
INCIDENT_OPEN = "abierto"
INCIDENT_RESOLVED = "resuelto"


@dataclass(frozen=True)
class WabaIncident:
    """An incident as it was read. A dataclass and not a validating model: every field stays as it is stored, so a
    strange one fails (or not) where it failed before, never when it is read after a close was already written."""

    id: Any
    waba_id: Any = None
    company_id: Any = None
    status: Any = None
    reason: Any = None
    opened_at: Any = None
    last_failure_at: Any = None
    alerted_at: Any = None
    resolved_at: Any = None
    updated_at: Any = None


class WabaIncidentRepository(Protocol):
    async def open(self, company_id: Optional[str], waba_id: str, reason: str, at: datetime) -> bool:
        """One more failure of the WABA: creates the incident or moves its reason, company and dates, and leaves it
        open; `opened_at` only when it is created. True when it was not open before: the caller is the first."""
        ...

    async def mark_alerted(self, waba_id: str, at: datetime) -> None:
        """Stores when the incident was alerted."""
        ...

    async def resolve(self, waba_id: str, at: datetime) -> Optional[WabaIncident]:
        """Resolves the incident if it is open. The incident as it was before; None when there was nothing to resolve
        (another worker did)."""
        ...

    async def open_wabas(self) -> Set[str]:
        """The WABA of every open incident, of every company; one without a WABA stored is left out."""
        ...


class WabaIncidentOverviewRepository(Protocol):
    """What Chatty Health reads, of every company. Apart from `WabaIncidentRepository`: it changes for the board, not for
    the life of an incident. The same Mongo class implements both."""

    async def count_open(self) -> int:
        ...

    async def count_resolved_since(self, since: datetime) -> int:
        """The incidents resolved at or after `since`."""
        ...

    async def newest_open(self, limit: int) -> List[WabaIncident]:
        """The open incidents, newest `opened_at` first, at most `limit`."""
        ...

    async def oldest_open(self) -> Optional[WabaIncident]:
        ...
