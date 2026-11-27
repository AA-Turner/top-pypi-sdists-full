"""`MetaChargeRepository` on `meta_cargos` (api-chatty `docs/meta-gastos/tdd.md`). One document per wamid:
`{_id: wamid, company_id, account_id, waba_id, phone_number_id, category, pricing_type, subtype, country, country_from,
sent_at, delivered_at, failed_at, expire_at}`. Every write is an `update_one(upsert=True)` on `_id`, so a repeated
status changes nothing; `expire_at` (sent + `RETENTION`) feeds the TTL index (api-chatty `Database/indexes`).

The stored shape is known only here. No cache: the month is read once per screen."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any, Dict, List

from ...domain.whatsapp.meta_charges import ChargeCount, MetaCharge

META_CHARGES = "meta_cargos"
#: How long a charge is kept: the current month and the three before it, whole (a month starts at most 122 days ago).
RETENTION = timedelta(days=125)

_GROUP_FIELDS = ("account_id", "waba_id", "phone_number_id", "category", "pricing_type", "subtype", "country",
                 "country_from")


def _on_insert(charge: MetaCharge) -> Dict[str, Any]:
    return {
        "company_id": charge.company_id, "account_id": charge.account_id, "waba_id": charge.waba_id,
        "phone_number_id": charge.phone_number_id, "category": charge.category, "pricing_type": charge.pricing_type,
        "subtype": charge.subtype, "country": charge.country, "country_from": charge.country_from,
        "sent_at": charge.sent_at, "expire_at": charge.sent_at + RETENTION,
    }


class MongoMetaChargeRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def seen(self, charge: MetaCharge) -> None:
        await self.collection.update_one({"_id": charge.wamid}, {"$setOnInsert": _on_insert(charge)}, upsert=True)

    async def delivered(self, charge: MetaCharge, at: datetime) -> None:
        await self.collection.update_one(
            {"_id": charge.wamid}, {"$setOnInsert": _on_insert(charge), "$min": {"delivered_at": at}}, upsert=True)

    async def failed(self, wamid: str, at: datetime) -> None:
        await self.collection.update_one({"_id": wamid}, {"$set": {"failed_at": at}})

    async def counts(self, company_id: str, since: datetime, until: datetime) -> List[ChargeCount]:
        pipeline = [
            {"$match": {"company_id": company_id, "sent_at": {"$gte": since, "$lt": until},
                        "delivered_at": {"$ne": None}, "failed_at": None}},
            {"$group": {
                "_id": {"day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$sent_at"}},
                        **{name: f"${name}" for name in _GROUP_FIELDS}},
                "count": {"$sum": 1},
            }},
        ]
        out: List[ChargeCount] = []
        async for row in self.collection.aggregate(pipeline):
            key = row["_id"]
            out.append(ChargeCount(day=date.fromisoformat(key["day"]), count=int(row["count"]),
                                   **{name: key.get(name) for name in _GROUP_FIELDS}))
        return out

    async def companies_with_charges(self, since: datetime, until: datetime) -> List[str]:
        return [str(c) for c in await self.collection.distinct(
            "company_id", {"sent_at": {"$gte": since, "$lt": until}, "delivered_at": {"$ne": None}, "failed_at": None})]
