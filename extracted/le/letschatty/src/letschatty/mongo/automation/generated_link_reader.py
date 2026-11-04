"""`GeneratedLinkReader` on the `flows` collection (Motor's, as given; it may be resolved on its first use): the seven
reads of the attention follow-up chains that api-chatty's `CadenasGeneradas` ran, with the same filters, projections,
sorts, `maxTimeMS` and lengths. Only reads: copilot_v2 writes this collection."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

from bson import ObjectId

from ...domain.automation.workflows import GeneratedLink

GENERATED_MAX_TIME_MS = 5000
CHAIN_PROJECTION = {"_id": 1, "clave": 1, "hash": 1, "orden": 1, "cadena": 1}


def _link(doc: Dict[str, Any]) -> GeneratedLink:
    return GeneratedLink(id=str(doc["_id"]), key=doc.get("clave"), hash=doc.get("hash"), order=doc.get("orden"),
                         chain=doc.get("cadena"), closing=doc.get("cierre"))


class MongoGeneratedLinkReader:
    def __init__(self, flows):
        self._flows = flows

    async def visible_generated_of_company(self, company_id: str, *, generated_by: str, limit: int) -> List[GeneratedLink]:
        cursor = self._flows.find(
            {"companyId": str(company_id), "generado_por": generated_by, "visible": True},
            projection=CHAIN_PROJECTION,
        ).sort([("clave", 1), ("orden", 1)]).max_time_ms(GENERATED_MAX_TIME_MS)
        return [_link(d) for d in await cursor.to_list(length=limit)]

    async def visible_generated_of_key(self, company_id: str, key: str, *, generated_by: str,
                                       limit: int) -> List[GeneratedLink]:
        cursor = self._flows.find(
            {"companyId": str(company_id), "generado_por": generated_by, "clave": key, "visible": True},
            projection=CHAIN_PROJECTION,
        ).max_time_ms(GENERATED_MAX_TIME_MS)
        return [_link(d) for d in await cursor.to_list(length=limit)]

    async def generated_ids_among(self, company_id: str, ids: List[str], *, generated_by: str) -> Set[str]:
        cursor = self._flows.find(
            {"_id": {"$in": [ObjectId(i) for i in ids]}, "companyId": str(company_id), "generado_por": generated_by},
            projection={"_id": 1},
        ).max_time_ms(GENERATED_MAX_TIME_MS)
        return {str(d["_id"]) for d in await cursor.to_list(length=len(ids))}

    async def follow_ups_among(self, ids: List[str], *, not_generated_by: str) -> Set[str]:
        cursor = self._flows.find(
            {"_id": {"$in": [ObjectId(i) for i in ids]}, "generado_por": {"$ne": not_generated_by},
             "$or": [{"es_seguimiento": True}, {"title": {"$regex": "^smart follow up$", "$options": "i"}}]},
            projection={"_id": 1},
        ).max_time_ms(GENERATED_MAX_TIME_MS)
        return {str(d["_id"]) for d in await cursor.to_list(length=len(ids))}

    async def key_of_generated(self, company_id: str, workflow_id: str, *, generated_by: str) -> Optional[Any]:
        doc = await self._flows.find_one(
            {"_id": ObjectId(str(workflow_id)), "companyId": str(company_id), "generado_por": generated_by},
            projection={"_id": 0, "clave": 1},
            max_time_ms=GENERATED_MAX_TIME_MS,
        )
        return (doc or {}).get("clave")

    async def generated_links_among(self, company_id: str, ids: List[str], *,
                                    generated_by: str) -> List[GeneratedLink]:
        cursor = self._flows.find(
            {"_id": {"$in": [ObjectId(i) for i in ids]}, "companyId": str(company_id), "generado_por": generated_by},
            projection={"_id": 1, "clave": 1, "orden": 1, "cierre": 1},
        ).max_time_ms(GENERATED_MAX_TIME_MS)
        return [_link(d) for d in await cursor.to_list(length=len(ids))]

    async def generated_of_company(self, company_id: str, *, generated_by: str, limit: int) -> List[GeneratedLink]:
        cursor = self._flows.find(
            {"companyId": str(company_id), "generado_por": generated_by},
            projection={"_id": 1, "clave": 1},
        ).max_time_ms(GENERATED_MAX_TIME_MS)
        return [_link(d) for d in await cursor.to_list(length=int(limit))]
