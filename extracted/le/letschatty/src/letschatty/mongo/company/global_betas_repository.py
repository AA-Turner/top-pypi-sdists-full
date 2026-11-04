"""`GlobalBetasRepository` on the `platform_settings` collection: the same two Mongo operations api-chatty's legacy
`BetasGlobales` ran (`find_one` with a projection, and `find_one_and_update` with `$addToSet`/`$pull` and `$set`,
upsert, returning the document after)."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pymongo import ReturnDocument

from ...domain.company.global_betas import clean_global_betas

DOCUMENT_ID = "global"
FIELD = "betas_globales"
_ONLY_THE_LIST = {FIELD: 1, "_id": 0}


class MongoGlobalBetasRepository:
    """On a Motor collection, resolved by whoever wires it (api-chatty resolves it on every call)."""

    def __init__(self, collection):
        self.collection = collection

    async def enabled(self) -> List[str]:
        document = await self.collection.find_one({"_id": DOCUMENT_ID}, projection=_ONLY_THE_LIST)
        return clean_global_betas((document or {}).get(FIELD) or [])

    async def switch(self, beta: str, on: bool, *, updated_by: Optional[str], updated_at: datetime) -> List[str]:
        operation = {"$addToSet": {FIELD: beta}} if on else {"$pull": {FIELD: beta}}
        operation["$set"] = {"updated_by": updated_by, "updated_at": updated_at}
        document = await self.collection.find_one_and_update(
            {"_id": DOCUMENT_ID},
            operation,
            upsert=True,
            projection=_ONLY_THE_LIST,
            return_document=ReturnDocument.AFTER,
        )
        return clean_global_betas((document or {}).get(FIELD) or [])
