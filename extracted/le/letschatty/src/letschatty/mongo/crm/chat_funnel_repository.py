"""`ChatFunnelRepository` on `chat_funnels`: the same queries `ChatFunnelsService` (api-chatty) ran, on the asset
collection it was built on, so the stored document has exactly its shape (dates as dates at the root, the transitions'
`transitioned_at` as text)."""
from __future__ import annotations

import logging
from typing import Dict, List

from pymongo.errors import DuplicateKeyError

from ...models.company.CRM.funnel import ChatFunnel, FunnelStatus
from ...models.utils.types import StrObjectId

# The legacy service's logger: the log lines stay as they were.
logger = logging.getLogger("ChatFunnelsService")


class MongoChatFunnelRepository:
    """On the `ChattyAssetCollection` of `chat_funnels`, handed in by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def get(self, company_id: StrObjectId, chat_funnel_id: StrObjectId) -> ChatFunnel:
        return await self.collection.get_by_id(chat_funnel_id)

    async def insert(self, company_id: StrObjectId, chat_funnel: ChatFunnel) -> ChatFunnel:
        await self.collection.insert(chat_funnel)
        return chat_funnel

    async def insert_if_missing(self, company_id: StrObjectId, chat_funnel: ChatFunnel) -> bool:
        try:
            await self.collection.insert(chat_funnel)
        except DuplicateKeyError:
            return False
        return True

    async def save(self, company_id: StrObjectId, chat_funnel: ChatFunnel) -> ChatFunnel:
        existing = await self.collection.get_by_id(chat_funnel.id)
        merged, sent_fields = existing.merge(chat_funnel)
        await self.collection.update_fields(merged, sent_fields)
        return merged

    async def open_of_chat(self, company_id: StrObjectId, chat_id: StrObjectId) -> List[ChatFunnel]:
        docs = await self.collection.collection.find({
            "chat_id": chat_id, "company_id": company_id, "status": FunnelStatus.IN_PROGRESS.value,
            "deleted_at": None,
        }).to_list(None)
        built: List[ChatFunnel] = []
        for doc in docs:
            # One by one: these are already in an odd state, so one that does not build cannot keep the rest open.
            try:
                built.append(ChatFunnel(**doc))
            except Exception:
                logger.exception("no se pudo cerrar el chat_funnel huérfano %s", doc.get("_id"))
        return built

    async def open_of_funnel(self, company_id: StrObjectId, funnel_id: StrObjectId) -> List[ChatFunnel]:
        docs = await self.collection.collection.find({
            "funnel_id": funnel_id, "company_id": company_id, "status": FunnelStatus.IN_PROGRESS.value,
            "deleted_at": None,
        }).to_list(None)
        return [ChatFunnel(**doc) for doc in docs]

    async def history_of_chat(self, company_id: StrObjectId, chat_id: StrObjectId) -> List[ChatFunnel]:
        docs = await self.collection.collection.find({
            "chat_id": chat_id, "company_id": company_id, "deleted_at": None,
        }, sort=[("started_at", -1)]).to_list(None)
        return [ChatFunnel(**doc) for doc in docs]

    async def count_by_status(self, company_id: StrObjectId, funnel_id: StrObjectId) -> Dict[str, int]:
        pipeline = [{"$match": {"funnel_id": funnel_id, "company_id": company_id, "deleted_at": None}},
                    {"$group": {"_id": "$status", "count": {"$sum": 1}}}]
        return {r["_id"]: r["count"] for r in await self.collection.collection.aggregate(pipeline).to_list(None)}
