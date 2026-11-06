"""`WabaIncidentRepository` and `WabaIncidentOverviewRepository` on `waba_health_incidents`: the operations api-chatty's
`company/analytics/health/waba_incidents.py` and the signal `salud_de_waba` ran, filter by filter (the upsert by `_id`
that returns the document as it was before, the `update_one` of the alert, the close filtered by state, the `find`
projected to `waba_id`, and the reads of the board).

The stored shape is known only here: `{_id (the WABA), abierto_at, alertado_at, company_id, estado, razon, resuelto_at,
ultima_falla_at, updated_at, waba_id}`. No cache."""
from __future__ import annotations

from datetime import datetime
from typing import Any, List, Mapping, Optional, Set

from pymongo import ReturnDocument

from ...domain.whatsapp.waba_incidents import INCIDENT_OPEN, INCIDENT_RESOLVED, WabaIncident

WABA_INCIDENTS = "waba_health_incidents"


def incident_of(document: Mapping[str, Any]) -> WabaIncident:
    return WabaIncident(
        id=document["_id"], waba_id=document.get("waba_id"), company_id=document.get("company_id"),
        status=document.get("estado"), reason=document.get("razon"), opened_at=document.get("abierto_at"),
        last_failure_at=document.get("ultima_falla_at"), alerted_at=document.get("alertado_at"),
        resolved_at=document.get("resuelto_at"), updated_at=document.get("updated_at"),
    )


class MongoWabaIncidentRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def open(self, company_id: Optional[str], waba_id: str, reason: str, at: datetime) -> bool:
        previous = await self.collection.find_one_and_update(
            {"_id": waba_id},
            {
                "$set": {
                    "waba_id": waba_id,
                    "company_id": company_id,
                    "estado": INCIDENT_OPEN,
                    "razon": reason,
                    "ultima_falla_at": at,
                    "updated_at": at,
                },
                "$setOnInsert": {"abierto_at": at},
            },
            upsert=True,
            return_document=ReturnDocument.BEFORE,
        )
        return not (bool(previous) and previous.get("estado") == INCIDENT_OPEN)

    async def mark_alerted(self, waba_id: str, at: datetime) -> None:
        await self.collection.update_one({"_id": waba_id}, {"$set": {"alertado_at": at}})

    async def resolve(self, waba_id: str, at: datetime) -> Optional[WabaIncident]:
        document = await self.collection.find_one_and_update(
            {"_id": waba_id, "estado": INCIDENT_OPEN},
            {"$set": {"estado": INCIDENT_RESOLVED, "resuelto_at": at, "updated_at": at}},
        )
        return None if document is None else incident_of(document)

    async def open_wabas(self) -> Set[str]:
        cursor = self.collection.find({"estado": INCIDENT_OPEN}, {"waba_id": 1})
        return {document["waba_id"] async for document in cursor if document.get("waba_id")}

    async def count_open(self) -> int:
        return await self.collection.count_documents({"estado": INCIDENT_OPEN})

    async def count_resolved_since(self, since: datetime) -> int:
        return await self.collection.count_documents({"estado": INCIDENT_RESOLVED, "resuelto_at": {"$gte": since}})

    async def newest_open(self, limit: int) -> List[WabaIncident]:
        cursor = self.collection.find({"estado": INCIDENT_OPEN}).sort("abierto_at", -1).limit(limit)
        return [incident_of(document) async for document in cursor]

    async def oldest_open(self) -> Optional[WabaIncident]:
        document = await self.collection.find_one({"estado": INCIDENT_OPEN}, sort=[("abierto_at", 1)])
        return None if document is None else incident_of(document)
