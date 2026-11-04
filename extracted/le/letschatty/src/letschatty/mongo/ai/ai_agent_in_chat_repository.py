"""The two read-only ports of the AI assigned to a chat (`domain/ai/ai_agent_in_chat.py`) on Mongo: the reads of
`main`'s `ChattyAIAgentsInChat` (api-chatty), one by one — the same filters, projections and `max_time_ms`, no cache.

Not a simple catalog (ADR-010): reads of another service's collections (cintia-lambdas), by chat or execution id.
"""
from __future__ import annotations

import json
from typing import Dict, Iterable, List, Optional

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorCollection

from ...models.chat.preview import ChattyAiAgentStatus
from ...models.company.assets.ai_agents_v2.chain_of_thought_in_chat import (ChainOfThoughtInChat,
                                                                           ChainOfThoughtInChatPreview)
from ...models.company.assets.ai_agents_v2.chatty_ai_agent_in_chat import ChattyAIAgentInChat
from ...models.utils.types import StrObjectId

# Any other status is still running: the criterion of cintia-lambdas' `CintiaExecutionRepository.has_active_execution`,
# which is what the frontend reads as "the AI is processing".
CINTIA_TERMINAL_STATUSES = ["finished", "error", "merged", "awaiting_feedback"]


class MongoAiAgentInChatRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def of_chat(self, chat_id: StrObjectId) -> Optional[ChattyAIAgentInChat]:
        doc = await self.collection.find_one({"chat_id": chat_id, "deleted_at": None},
                                             projection={"chain_of_thoughts": 0, "events": 0})
        if not doc:
            return None
        return ChattyAIAgentInChat(**doc)

    async def status_for_preview(self, chat_id: StrObjectId, projection: Dict[str, int]) -> Optional[ChattyAiAgentStatus]:
        doc = await self.collection.find_one({"chat_id": chat_id, "deleted_at": None}, projection=projection)
        if not doc:
            return None
        if not doc.get("asset_id"):
            return None
        if doc.get("human_intervention"):
            return ChattyAiAgentStatus.ESCALATED
        return ChattyAiAgentStatus.ASSIGNED

    async def chains_of_thought(self, chat_id: StrObjectId) -> List[dict]:
        doc = await self.collection.find_one({"chat_id": chat_id, "deleted_at": None},
                                             projection={"chain_of_thoughts": 1})
        if not doc:
            return []
        previews = []
        for cot in [ChainOfThoughtInChat(**c) for c in doc.get("chain_of_thoughts", [])]:
            preview = ChainOfThoughtInChatPreview(
                _id=cot.id, chat_id=cot.chat_id, company_id=cot.company_id, trigger_id="", status=cot.status,
                name=cot.name, chain_of_thought=cot.chain_of_thought, confidence=cot.confidence, trigger=cot.trigger,
                created_at=cot.created_at, updated_at=cot.updated_at)
            previews.append(json.loads(preview.model_dump_json()))
        return previews

    async def chain_of_thought(self, chat_id: StrObjectId, chain_of_thought_id: StrObjectId) -> Optional[ChainOfThoughtInChat]:
        doc = await self.collection.find_one(
            {"chat_id": chat_id, "deleted_at": None, "chain_of_thoughts._id": chain_of_thought_id},
            projection={"chain_of_thoughts.$": 1})
        if not doc:
            return None
        return ChainOfThoughtInChat(**doc.get("chain_of_thoughts", [])[0])


class MongoCintiaExecutionRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def has_active(self, chat_id: StrObjectId) -> bool:
        doc = await self.collection.find_one(
            {"chat_id": chat_id, "status": {"$nin": CINTIA_TERMINAL_STATUSES},
             "metadata.credit_hold": {"$exists": False}},
            projection={"_id": 1})
        return doc is not None

    async def agents_of(self, cintia_ids: Iterable[str]) -> Dict[str, str]:
        oids = []
        for cintia_id in cintia_ids:
            try:
                oids.append(ObjectId(str(cintia_id)))
            except (InvalidId, TypeError):
                continue
        if not oids:
            return {}
        cursor = self.collection.find({"_id": {"$in": oids}}, projection={"ai_agent_id": 1}, max_time_ms=5000)
        return {str(doc["_id"]): str(doc["ai_agent_id"]) async for doc in cursor if doc.get("ai_agent_id")}
