"""`WabaBillingRepository` on `meta_wabas_facturacion` (api-chatty `docs/meta-gastos/tdd.md`):
`{_id: waba_id, currency, timezone_id, read_at, source}` (`source`: «meta» or «a_mano»; missing in the first documents,
read as «meta»). Written by the reading of Meta and by the backoffice's correction."""
from __future__ import annotations

from typing import Dict, List

from ...domain.whatsapp.waba_billing import FROM_META, WabaBilling

WABA_BILLING = "meta_wabas_facturacion"


def _billing_of(document) -> WabaBilling:
    return WabaBilling(waba_id=str(document["_id"]), currency=document.get("currency"),
                       timezone_id=document.get("timezone_id"), read_at=document.get("read_at"),
                       source=document.get("source") or FROM_META)


class MongoWabaBillingRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def of(self, waba_ids: List[str]) -> Dict[str, WabaBilling]:
        out: Dict[str, WabaBilling] = {}
        async for document in self.collection.find({"_id": {"$in": list(waba_ids)}}):
            out[str(document["_id"])] = _billing_of(document)
        return out

    async def all(self) -> List[WabaBilling]:
        return [_billing_of(document) async for document in self.collection.find({})]

    async def save(self, billing: WabaBilling) -> None:
        await self.collection.replace_one(
            {"_id": billing.waba_id},
            {"currency": billing.currency, "timezone_id": billing.timezone_id, "read_at": billing.read_at,
             "source": billing.source},
            upsert=True)
