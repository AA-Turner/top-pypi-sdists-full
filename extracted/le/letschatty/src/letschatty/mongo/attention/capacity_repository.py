"""`CapacityRepository` on the `capacidades` collection. Not a catalog (ADR-010 of api-chatty): no cache, no events, raw
documents, and each operation is the one `main` ran (one query, one write)."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId

from ...models.company.assets.atencion.capacidad import Capacidad
from ...models.utils.types.serializer_type import SerializerType


class MongoCapacityRepository:
    """`collection` is the Motor collection `capacidades`."""

    def __init__(self, collection):
        self.collection = collection

    async def list_live(self, company_id: str) -> List[Dict[str, Any]]:
        cursor = self.collection.find({"company_id": str(company_id), "deleted_at": None}).sort("created_at", 1)
        return [doc async for doc in cursor]

    async def add(self, capacity: Capacidad) -> Dict[str, Any]:
        doc = capacity.model_dump(serializer=SerializerType.DATABASE)
        await self.collection.insert_one(doc)
        return doc

    async def find_live(self, company_id: str, capacity_id: str) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one(
            {"_id": ObjectId(str(capacity_id)), "company_id": str(company_id), "deleted_at": None})

    async def set_fields(self, company_id: str, capacity_id: str, fields: Dict[str, Any]) -> None:
        await self.collection.update_one({"_id": ObjectId(str(capacity_id)), "company_id": str(company_id)},
                                         {"$set": fields})

    async def soft_delete(self, company_id: str, capacity_id: str, now: datetime) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(str(capacity_id)), "company_id": str(company_id), "deleted_at": None},
            {"$set": {"deleted_at": now, "activa": False}})
        return bool(getattr(result, "matched_count", 0))
