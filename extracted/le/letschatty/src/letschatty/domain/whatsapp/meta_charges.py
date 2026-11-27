"""A charge of Meta («cargo de Meta», api-chatty `docs/meta-gastos/tdd.md`): what Meta said about the price of ONE message
we sent, from the `pricing` of its status webhooks. One per wamid, its own aggregate: it is written before the chat is
looked for (a status whose chat does not exist still counts) and read by company and month, never by chat.

A charge counts when it was delivered and did not fail: Meta charges on delivery, and a failed message carries no
`pricing`. Every write is idempotent on the wamid, so repeated statuses and SQS retries change nothing.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional, Protocol

#: Where the country of a charge came from.
COUNTRY_FROM_RECIPIENT = "destinatario"
COUNTRY_FROM_BUSINESS_NUMBER = "numero_de_la_empresa"


@dataclass(frozen=True)
class MetaCharge:
    """A charge as the status webhook describes it. `country` is the ISO2 country of the recipient's phone or, for a
    recipient without phone (a BSUID), of the company's number (`country_from` says which); None when neither has one.
    The market of the rate card is NOT stored: Meta regroups countries quarterly, so it is decided on reading, with the
    card in force that day."""

    wamid: str
    company_id: str
    category: str
    pricing_type: Optional[str]
    subtype: Optional[str]
    country: Optional[str]
    country_from: str
    sent_at: datetime
    account_id: Optional[str] = None
    waba_id: Optional[str] = None
    phone_number_id: Optional[str] = None


@dataclass(frozen=True)
class ChargeCount:
    """How many delivered, not failed charges share every field: the month of a company is a few dozen of these, never
    one row per message. `day` is the UTC day the message was sent (it picks the rate card)."""

    day: date
    category: str
    pricing_type: Optional[str]
    subtype: Optional[str]
    country: Optional[str]
    country_from: str
    count: int
    account_id: Optional[str] = None
    waba_id: Optional[str] = None
    phone_number_id: Optional[str] = None


class MetaChargeRepository(Protocol):
    async def seen(self, charge: MetaCharge) -> None:
        """A status with `pricing` (any but `failed`): stores the charge if it is not there. Never changes a stored one."""
        ...

    async def delivered(self, charge: MetaCharge, at: datetime) -> None:
        """A `delivered`, `read` or `played`: stores the charge if it is not there and keeps the EARLIEST delivery time
        (a `read` after the `delivered` changes nothing; a `delivered` before the `sent` still counts)."""
        ...

    async def failed(self, wamid: str, at: datetime) -> None:
        """A `failed`: the charge, if stored, stops counting. Does not create one."""
        ...

    async def counts(self, company_id: str, since: datetime, until: datetime) -> List[ChargeCount]:
        """The delivered, not failed charges of the company sent in `[since, until)`, grouped."""
        ...

    async def companies_with_charges(self, since: datetime, until: datetime) -> List[str]:
        """The companies with at least one delivered charge sent in `[since, until)` (the backoffice list)."""
        ...
