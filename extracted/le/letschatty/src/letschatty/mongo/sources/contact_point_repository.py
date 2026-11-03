"""`ContactPointRepository` on the `contact_points` collection: a catalog read by id (`MongoCatalogById`) plus the reads
the source analysis needs. Only Mongo: the cache is a decorator (ADR-001)."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from bson import ObjectId

from ...models.company.assets.contact_point import ContactPoint
from ...models.utils.types import StrObjectId
from ...services.chatty_assets.collections.contact_point_collection import ContactPointCollection
from ..catalog_repository import MongoCatalogById


class MongoContactPointRepository(MongoCatalogById[ContactPoint]):
    """Reuses `ContactPointCollection`, so the stored document keeps exactly the shape analytics and the Conversions API
    read (`match_timestamp` as text included)."""

    collection: ContactPointCollection

    async def get_fresh(self, contact_point_id: StrObjectId) -> ContactPoint:
        return await self._read(contact_point_id)

    async def of_source(self, company_id: Optional[StrObjectId], source_id: StrObjectId) -> List[ContactPoint]:
        # The id as the caller gives it, compared as stored (text), as the asset service's `get_by_query` did.
        return await self.collection.get_docs(query={"source_id": source_id}, company_id=company_id)

    async def of_chat(self, company_id: Optional[StrObjectId], chat_id: StrObjectId) -> List[ContactPoint]:
        return await self.collection.get_docs(query={"chat_id": chat_id}, company_id=company_id)

    async def set_ad_creative(self, contact_point_id: StrObjectId, ad_creative: Dict[str, Any]) -> None:
        await self.collection.partial_update(contact_point_id, {"ad_creative": ad_creative})

    async def has_live_of_another_source(self, chat_id: StrObjectId, contact_point_id: StrObjectId,
                                         source_id: Optional[StrObjectId]) -> bool:
        # The collection, not the chat's references: a stub and the real copy of a message processed at once can drop
        # the real copy's reference from the chat's list (docs/inferred-ad-attribution.md of api-chatty).
        query: Dict[str, Any] = {"chat_id": str(chat_id), "deleted_at": None,
                                 "_id": {"$ne": ObjectId(str(contact_point_id))}}
        if source_id:
            query["source_id"] = {"$ne": str(source_id)}
        return await self.collection.collection.find_one(query, {"_id": 1}) is not None
