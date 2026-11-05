"""The WhatsApp Business profile snapshot of a number («foto del perfil de WhatsApp»): photo, about, vertical, verified
name and quality, as Meta answered them at `last_synced_at`. One per `(company_id, account_id)`; the documents written
before accounts existed have no `account_id` (one per company). The model and the port every store of it implements.

Not a catalog (ADR-010 of api-chatty): nobody creates, edits or lists it by hand. The refresh writes it, adopting in
place the document without account, and a concurrent insert of the same account is retried as an update.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Protocol

from pydantic import BaseModel, SkipValidation

#: The fields a refresh stores, in the order it stores them (the identity — company, account, number — goes apart).
CONTENT_FIELDS = ("last_synced_at", "display_phone_number", "verified_name", "photo_url", "about", "description",
                  "email", "websites", "vertical", "quality_rating", "waba_id", "business_id")


class ProfileSnapshot(BaseModel):
    """What a document of `company_whatsapp_profiles` says. `account_id` and `phone_number_id` are None on a document
    of before the accounts. `id` is not read: it is the id an `add` gave the snapshot (as `insert_one` gives the dict it
    sends its `_id`, also when the insert is refused), and a later write of the same snapshot carries it.

    The content is NOT validated (`SkipValidation`): the types are the ones measured in prod, but a value of another
    type (what Meta answers, or what is stored) is kept as it comes, as the dict of before kept it. Validating would
    turn a refresh or a read that works today into a `ValidationError` (ADR-010 of api-chatty, «Puertos que no
    devuelven un modelo de dominio»)."""

    company_id: str
    id: Optional[str] = None
    account_id: SkipValidation[Optional[str]] = None
    phone_number_id: SkipValidation[Optional[str]] = None
    last_synced_at: SkipValidation[Optional[datetime]] = None
    display_phone_number: SkipValidation[Optional[str]] = None
    verified_name: SkipValidation[Optional[str]] = None
    photo_url: SkipValidation[Optional[str]] = None
    about: SkipValidation[Optional[str]] = None
    description: SkipValidation[Optional[str]] = None
    email: SkipValidation[Optional[str]] = None
    websites: SkipValidation[Optional[List[str]]] = None
    vertical: SkipValidation[Optional[str]] = None
    quality_rating: SkipValidation[Optional[str]] = None
    waba_id: SkipValidation[Optional[str]] = None
    business_id: SkipValidation[Optional[str]] = None


class ProfileSnapshotRepository(Protocol):
    async def first_of_company(self, company_id: str) -> Optional[ProfileSnapshot]:
        """The first document of the company in the store's order, of any account or of none."""
        ...

    async def of_account(self, company_id: str, account_id: str) -> Optional[ProfileSnapshot]:
        ...

    async def without_account(self, company_id: str) -> Optional[ProfileSnapshot]:
        """The document of before the accounts (no `account_id` stored)."""
        ...

    async def save_first_of_company(self, company_id: str, snapshot: ProfileSnapshot) -> None:
        """Writes the content on the first document of the company, or creates one with only the company and the
        content (a company without accounts). Never writes the account or the number."""
        ...

    async def update_of_account(self, company_id: str, snapshot: ProfileSnapshot) -> bool:
        """Writes content, account and number on the document of `snapshot.account_id`; False if there is none. With
        the `id` of an earlier `add` it writes that id too, and a document with another one refuses it (`WriteError`)."""
        ...

    async def adopt_without_account(self, company_id: str, snapshot: ProfileSnapshot) -> bool:
        """Writes content, account and number on the document of before the accounts; False if there is none."""
        ...

    async def add(self, company_id: str, snapshot: ProfileSnapshot) -> bool:
        """Creates the document of `snapshot.account_id`; False if the account already has one. Either way the snapshot
        keeps the id the insert gave it (`snapshot.id`)."""
        ...

    async def stamp_without_account(self, company_id: str, account_id: str, phone_number_id: Optional[str]) -> None:
        """Gives the account and the number to the document of before the accounts, if there is one."""
        ...
