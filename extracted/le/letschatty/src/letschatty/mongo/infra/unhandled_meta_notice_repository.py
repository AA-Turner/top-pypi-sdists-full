"""`UnhandledMetaNoticeRepository` on `meta_no_manejados` and `meta_no_manejados_tipos`: the same writes that
`meta_handler/avisos_sin_manejar.py` of api-chatty ran (the upsert of the day's counter, the atomic pipeline on the
type with its retry when two new ones collide, the reopening conditional on the review, the peak aggregation and the
two marks)."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from ...domain.infra.unhandled_meta_notices import PENDING, REVIEWED

DAILY_COLLECTION = "meta_no_manejados"
TYPES_COLLECTION = "meta_no_manejados_tipos"


def type_id(category: str, kind: str) -> str:
    return f"{category}:{kind}"


class MongoUnhandledMetaNoticeRepository:
    """On a Motor database, resolved by whoever wires it."""

    def __init__(self, database):
        self.database = database

    async def count(self, company_id: Optional[str], *, day: datetime, category: str, kind: str,
                    phone_number_id: Optional[str], now: datetime, waba_id: Optional[str], field: Optional[str],
                    reason: Optional[str], sample: str) -> None:
        await self.database[DAILY_COLLECTION].update_one(
            {"dia": day, "categoria": category, "tipo": kind, "phone_number_id": phone_number_id},
            {
                "$inc": {"n": 1},
                "$setOnInsert": {"primera_vez": now},
                "$set": {
                    "ultima_vez": now,
                    **({"company_id": company_id} if company_id else {}),
                    "waba_id": waba_id,
                    "field": field,
                    "motivo": reason,
                    "ejemplo": sample,
                },
            },
            upsert=True,
        )

    async def add_to_type(self, *, category: str, kind: str, field: Optional[str], who: Optional[str], now: datetime,
                          day: datetime) -> Optional[Dict[str, Any]]:
        # One `find_one_and_update` with a pipeline: Mongo serializes the writes to one document, so only ONE call
        # sees the state before empty, even with two webhooks at the same instant on two workers.
        company = [who] if who else []
        update = [{"$set": {
            "categoria": category,
            "tipo": kind,
            "field": {"$ifNull": [field, "$field"]},
            "estado": {"$ifNull": ["$estado", PENDING]},
            "primera_vez": {"$ifNull": ["$primera_vez", now]},
            "ultima_vez": now,
            "n_hoy": {"$cond": [{"$eq": ["$dia_n_hoy", day]}, {"$add": [{"$ifNull": ["$n_hoy", 0]}, 1]}, 1]},
            "dia_n_hoy": day,
            "empresas": {"$setUnion": [{"$ifNull": ["$empresas", []]}, company]},
        }}]
        collection = self.database[TYPES_COLLECTION]
        for attempt in range(2):
            try:
                return await collection.find_one_and_update(
                    {"_id": type_id(category, kind)}, update,
                    upsert=True, return_document=ReturnDocument.BEFORE,
                )
            except DuplicateKeyError:
                # Two upserts of the same new type at once: one creates the document and the other hits the _id.
                # The retry finds it and adds.
                if attempt:
                    raise
        return None

    async def reopen(self, *, category: str, kind: str, reviewed_at: Any, reason: str, now: datetime) -> bool:
        result = await self.database[TYPES_COLLECTION].update_one(
            {"_id": type_id(category, kind), "estado": REVIEWED, "revisado_at": reviewed_at},
            {"$set": {"estado": PENDING, "reabierto_por": reason, "reabierto_at": now}},
        )
        return bool(result.modified_count)

    async def get_type(self, *, category: str, kind: str) -> Optional[Dict[str, Any]]:
        return await self.database[TYPES_COLLECTION].find_one({"_id": type_id(category, kind)})

    async def daily_peak(self, *, category: str, kind: str, since: datetime) -> int:
        cursor = self.database[DAILY_COLLECTION].aggregate([
            {"$match": {"dia": {"$gte": since}, "categoria": category, "tipo": kind}},
            {"$group": {"_id": "$dia", "n": {"$sum": "$n"}}},
            {"$group": {"_id": None, "pico": {"$max": "$n"}}},
        ])
        async for row in cursor:
            return int(row.get("pico") or 0)
        return 0

    async def review(self, *, category: str, kind: str, reviewed_by: Optional[str], reviewed_at: datetime,
                     note: Optional[str], companies: List[str], peak: int) -> Optional[Dict[str, Any]]:
        return await self._set(category, kind, {
            "estado": REVIEWED, "revisado_por": reviewed_by, "revisado_at": reviewed_at, "nota": note,
            "empresas_al_revisar": companies, "pico_diario_al_revisar": peak,
            "reabierto_por": None, "reabierto_at": None,
        })

    async def back_to_pending(self, *, category: str, kind: str, note: Optional[str]) -> Optional[Dict[str, Any]]:
        return await self._set(category, kind, {"estado": PENDING, "revisado_por": None, "revisado_at": None,
                                                "nota": note, "reabierto_por": None, "reabierto_at": None})

    async def _set(self, category: str, kind: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.database[TYPES_COLLECTION].find_one_and_update(
            {"_id": type_id(category, kind)}, {"$set": changes}, return_document=ReturnDocument.AFTER)
