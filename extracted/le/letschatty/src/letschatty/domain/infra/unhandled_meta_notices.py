"""What Meta sends and Chatty does not handle («avisos de Meta sin manejar»): the port of `meta_no_manejados` and
`meta_no_manejados_tipos` (api-chatty `docs/infra/avisos-de-meta-sin-manejar.md`).

Two collections: one counter per (day, category, type, number), with the first and last time and the last sample
without the customer's content; and the state of each type (`pendiente` or `revisado`, its companies, its count of
today, the photo taken when a person reviewed it). Of every company: a notice may come from a number without one.
Without cache.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol

PENDING = "pendiente"
REVIEWED = "revisado"


class UnhandledMetaNoticeRepository(Protocol):
    async def count(self, company_id: Optional[str], *, day: datetime, category: str, kind: str,
                    phone_number_id: Optional[str], now: datetime, waba_id: Optional[str], field: Optional[str],
                    reason: Optional[str], sample: str) -> None:
        """One more notice in the counter of its day, category, type and number (created at the first one, with
        `now` as its first time). The company only when it is known: None leaves the one the day had."""
        ...

    async def add_to_type(self, *, category: str, kind: str, field: Optional[str], who: Optional[str], now: datetime,
                          day: datetime) -> Optional[Dict[str, Any]]:
        """One more notice in the state of the type, atomically, and answers the state as it was BEFORE (None: a new
        type; only one of many callers at once sees that). `who` joins its companies; the count of today starts again
        on another day."""
        ...

    async def reopen(self, *, category: str, kind: str, reviewed_at: Any, reason: str, now: datetime) -> bool:
        """A reviewed type back to pending, only if it is still the review of `reviewed_at`. True if this call did."""
        ...

    async def get_type(self, *, category: str, kind: str) -> Optional[Dict[str, Any]]:
        """The state of the type, or None."""
        ...

    async def daily_peak(self, *, category: str, kind: str, since: datetime) -> int:
        """The biggest day of the type (all its numbers summed) from `since` on; 0 without notices."""
        ...

    async def review(self, *, category: str, kind: str, reviewed_by: Optional[str], reviewed_at: datetime,
                     note: Optional[str], companies: List[str], peak: int) -> Optional[Dict[str, Any]]:
        """Marks the type reviewed with the photo of what the person saw, and answers it after."""
        ...

    async def back_to_pending(self, *, category: str, kind: str, note: Optional[str]) -> Optional[Dict[str, Any]]:
        """Marks the type pending by hand (without the review), and answers it after."""
        ...
