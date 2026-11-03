"""`AiAgentRepository` on the `ai_agents` collection: a catalog by company, listed by its previews
(`MongoCatalogWithPreviews`, whose reads by id ignore the company) plus the fresh read, the compare-and-set on `updated_at` of an edit that says which
version it saw, and the lookup by calendar. Only Mongo: the cache is a decorator (ADR-001)."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from bson import ObjectId

from ...models.company.assets.ai_agents_v2.chatty_ai_agent import ChattyAIAgent, ChattyAIAgentPreview
from ...models.utils.types import StrObjectId
from ...models.utils.types.serializer_type import SerializerType
from ...services.chatty_assets.collections.ai_agent_collection import AiAgentCollection
from ..catalog_repository import MongoCatalogWithPreviews


class MongoAiAgentRepository(MongoCatalogWithPreviews[ChattyAIAgent]):
    """Reuses `AiAgentCollection`, so the stored document has exactly the shape the lambdas read and write."""

    collection: AiAgentCollection

    def preview_projection(self) -> Dict[str, Any]:
        return ChattyAIAgentPreview.get_projection()

    async def get_fresh(self, company_id: Optional[StrObjectId], agent_id: StrObjectId) -> ChattyAIAgent:
        return await self._read(agent_id)

    async def stored_updated_at(self, company_id: StrObjectId, agent_id: StrObjectId) -> Tuple[bool, Any]:
        stored = await self.collection.collection.find_one({"_id": ObjectId(agent_id)}, projection={"updated_at": 1})
        return stored is not None, (stored or {}).get("updated_at")

    async def replace_if_unchanged(self, company_id: StrObjectId, agent: ChattyAIAgent, stored_updated_at: Any) -> bool:
        document = agent.model_dump_json(serializer=SerializerType.DATABASE)
        document.pop("_id", None)
        result = await self.collection.collection.update_one(
            {"_id": ObjectId(agent.id), "updated_at": stored_updated_at}, {"$set": document}
        )
        return result.matched_count != 0

    async def company_ids_with_calendar(self, calendar_email: str) -> List[Any]:
        found = await self.collection.collection.find({"calendars": calendar_email}, projection={"company_id": 1}).to_list(None)
        return [doc["company_id"] for doc in found]
