"""`PendingNoticeRepository` on `ausencia_pendiente`: the same operations that `AvisosPendientes` of api-chatty ran
(`company/analytics/source_analyzer/source_automation_executor/ausencia_con_ia.py`): an upsert `$set` by `_id` (the
chat's id), a `find_one` projected to `opcion` and an atomic `find_one_and_delete` by `_id`, `opcion` and a valid
`vence_at`. The TTL index on `vence_at` is created by api-chatty (`Database/indexes/ausencia_pendiente_indexes.py`).

The stored form lives only here: what taking answers is turned into the domain's `PendingNotice`
(`pending_notice_from_stored`)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from ...domain.attention.pending_notices import PendingNotice

COLLECTION = "ausencia_pendiente"


def _utc(t: datetime) -> datetime:
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def pending_notice_from_stored(doc: Dict[str, Any]) -> PendingNotice:
    """A stored notice as the domain's."""
    company_id = doc.get("company_id")
    return PendingNotice(chat_id=str(doc["_id"]), company_id=None if company_id is None else str(company_id),
                         option=str(doc.get("opcion")), raw_account_id=doc.get("account_id"))


class MongoPendingNoticeRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def register(self, company_id: str, *, chat_id: str, option: str, expires_at: datetime, now: datetime,
                       account_id: Optional[str] = None) -> None:
        fields = {"company_id": str(company_id), "opcion": str(option), "vence_at": _utc(expires_at),
                  "creado_at": now}
        if account_id:
            fields["account_id"] = str(account_id)
        await self.collection.update_one({"_id": str(chat_id)}, {"$set": fields}, upsert=True)

    async def option(self, chat_id: str, now: datetime) -> Optional[str]:
        doc = await self.collection.find_one({"_id": str(chat_id), "vence_at": {"$gt": now}},
                                             projection={"opcion": 1})
        return (doc or {}).get("opcion")

    async def take(self, chat_id: str, option: str, now: datetime) -> Optional[PendingNotice]:
        doc = await self.collection.find_one_and_delete(
            {"_id": str(chat_id), "opcion": str(option), "vence_at": {"$gt": now}})
        return None if doc is None else pending_notice_from_stored(doc)
