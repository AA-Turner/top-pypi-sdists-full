"""`AssignmentConfigRepository` and `AssignmentLogReader` on Motor collections. Not a catalog (ADR-010 of api-chatty):
the rows are read and written raw, with no cache and no events, because assignment-lambda reads `assignment_config`
and writes `assignment_log` directly. Each method is the one Mongo operation the legacy service ran, with the same
filter."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId

logger = logging.getLogger("Assignment")  # the legacy service's logger, whose logs about Mongo's own objects live here


def _live(company_id: str) -> Dict[str, Any]:
    return {"company_id": company_id, "$or": [{"deleted_at": {"$exists": False}}, {"deleted_at": None}]}


class MongoAssignmentConfigRepository:
    def __init__(self, collection):
        self.collection = collection

    @property
    def full_name(self) -> str:
        return self.collection.full_name

    async def count_every_company(self) -> int:
        return await self.collection.count_documents({})

    async def count_of(self, company_id: str) -> int:
        return await self.collection.count_documents({"company_id": company_id})

    async def live_for_listing(self, company_id: str) -> List[Dict[str, Any]]:
        """The sequence of the legacy list, step by step: the query logged, every row of the company read and logged,
        then the live rows read."""
        query = _live(company_id)
        logger.info(f"[LIST_CONFIGS] MongoDB query: {query}")
        all_company_docs = await self.collection.find({"company_id": company_id}).to_list(None)
        logger.info(f"[LIST_CONFIGS] ALL documents for company (including deleted): {all_company_docs}")
        return await self.collection.find(query).to_list(None)

    async def get(self, company_id: str, config_id: str, *, trace: bool = False) -> Optional[Dict[str, Any]]:
        object_id = ObjectId(config_id)
        if trace:
            logger.info(f"[GET_CONFIG_BY_ID] Converted to ObjectId: {object_id}")
        return await self.collection.find_one({"_id": object_id, "company_id": company_id})

    async def has_company_room(self, company_id: str) -> bool:
        """The «room» of the whole company of assignment-lambda (`AssignmentConfigRepo.resolve`): snake_case, then
        camelCase. A projected read with a time cap; the collection is small."""
        company = str(company_id)
        query = {"$or": [
            {"company_id": company, "funnel_id": None, "area_id": None, "deleted_at": None},
            {"companyId": company, "funnelId": None, "areaId": None, "deletedAt": None},
        ]}
        return await self.collection.find_one(query, projection={"_id": 1}, max_time_ms=2000) is not None

    async def insert(self, fields: Dict[str, Any]) -> Any:
        return (await self.collection.insert_one(fields)).inserted_id

    async def overwrite(self, config_id: str, fields: Dict[str, Any]) -> None:
        await self.collection.update_one({"_id": ObjectId(config_id)}, {"$set": fields})

    async def mark_deleted(self, config_id: str, deleted_at: datetime) -> int:
        result = await self.collection.update_one({"_id": ObjectId(config_id)}, {"$set": {"deleted_at": deleted_at}})
        return result.modified_count


class MongoAssignmentLogReader:
    """Reads what assignment-lambda writes (`assignment_log`); api-chatty never writes it."""

    def __init__(self, collection):
        self.collection = collection

    @staticmethod
    def _of(company_id: str) -> Dict[str, Any]:
        return {"$or": [{"room.company_id": company_id}, {"room.companyId": company_id}, {"company_id": company_id},
                        {"companyId": company_id}]}

    async def count_of(self, company_id: str) -> int:
        return await self.collection.count_documents(self._of(company_id))

    async def newest_of(self, company_id: str, limit: int) -> List[Dict[str, Any]]:
        return await (self.collection.find(self._of(company_id)).sort("created_at", -1).limit(limit)
                      .to_list(length=limit or None))
