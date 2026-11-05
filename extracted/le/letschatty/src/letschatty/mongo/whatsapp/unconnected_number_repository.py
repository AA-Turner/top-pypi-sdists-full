"""`UnconnectedNumberRepository` on `whatsapp_unconnected_numbers`: the same operations api-chatty's
`company/whatsapp_accounts/unconnected_numbers.py` ran (an `update_one` with upsert by `_id = "{company_id}:{digits}"`
and `$setOnInsert` of `detected_at`, a `delete_many` by WABA and digits, a `find` by company sorted by `detected_at`).

The stored shape is known only here: `{_id, company_id, waba_id, digits, detected_at}`, `detected_at` a date that Mongo
returns without zone (read as UTC) and that may be missing (read as None). Each row is a lazy view
(`StoredUnconnectedNumber`): its fields are read when asked for, as the legacy list read them."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, List, Mapping, Optional


COLLECTION = "whatsapp_unconnected_numbers"


class MongoUnconnectedNumberRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def record(self, company_id: str, *, waba_id: str, digits: str, detected_at: datetime) -> None:
        await self.collection.update_one(
            {"_id": f"{company_id}:{digits}"},
            {"$set": {"company_id": company_id, "waba_id": waba_id, "digits": digits},
             "$setOnInsert": {"detected_at": detected_at}},
            upsert=True,
        )

    async def forget_in_every_company(self, waba_id: str, digits: str) -> None:
        await self.collection.delete_many({"waba_id": waba_id, "digits": digits})

    async def of_company(self, company_id: str) -> List["StoredUnconnectedNumber"]:
        documents = await self.collection.find({"company_id": company_id}).sort("detected_at", 1).to_list(None)
        return [StoredUnconnectedNumber(d) for d in documents]


class StoredUnconnectedNumber:
    """A row as `whatsapp_unconnected_numbers` stores it, each field read when it is asked for, with `main`'s
    expressions (`d["digits"]`, `d["waba_id"]`, `d.get("detected_at")` and its `.tzinfo`)."""

    def __init__(self, document: Mapping[str, Any]):
        self._document = document

    @property
    def company_id(self) -> Any:
        return self._document.get("company_id")

    @property
    def digits(self) -> Any:
        return self._document["digits"]

    @property
    def waba_id(self) -> Any:
        return self._document["waba_id"]

    @property
    def detected_at(self) -> Optional[datetime]:
        value = self._document.get("detected_at")
        if value is None:
            return None
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
