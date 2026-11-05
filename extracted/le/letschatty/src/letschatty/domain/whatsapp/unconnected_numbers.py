"""Numbers added in Meta to a company's WABA that are not connected to Chatty yet («números sin conectar», api-chatty
`docs/whatsapp/numeros-sin-conectar.md`): the port of `whatsapp_unconnected_numbers`.

Meta's `account_update · PHONE_NUMBER_ADDED` names only the WABA and the number's digits, so one row is kept per
company that uses that WABA, found by its natural key (company and digits). `PHONE_NUMBER_REMOVED` forgets the number
in every company with that WABA. Without cache and without events.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional, Protocol


class UnconnectedNumber(Protocol):
    """A recorded number of a company, read lazily on purpose (api-chatty `docs/whatsapp/numeros-sin-conectar.md`):
    `main` read `digits` to leave out the connected numbers and `waba_id`/`detected_at` only to show each one that is
    listed. So each property reads its field when it is asked for, with `main`'s expressions: a missing field raises
    `KeyError` there, a `null` reads as None, and a `detected_at` that is not a date raises `AttributeError` there."""

    @property
    def company_id(self) -> Any:
        ...

    @property
    def digits(self) -> Any:
        """Raises `KeyError('digits')` when the row has none."""
        ...

    @property
    def waba_id(self) -> Any:
        """Raises `KeyError('waba_id')` when the row has none; a stored `null` is None."""
        ...

    @property
    def detected_at(self) -> Optional[datetime]:
        """When Meta said it was added, in UTC (a stored date has no zone); None when missing or `null`."""
        ...


class UnconnectedNumberRepository(Protocol):
    async def record(self, company_id: str, *, waba_id: str, digits: str, detected_at: datetime) -> None:
        """One row per company and digits: created with `detected_at`, or updated keeping the first `detected_at`
        (also under concurrent calls)."""
        ...

    async def forget_in_every_company(self, waba_id: str, digits: str) -> None:
        """Deletes the rows with this WABA and digits, of every company."""
        ...

    async def of_company(self, company_id: str) -> List[UnconnectedNumber]:
        """The company's rows, oldest `detected_at` first (a row without it first)."""
        ...
