"""Redis cache in front of any `ChatFunnelRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used for `chat_funnels`: the read by id is cached
(`chat_funnels:item:{id}`); an insert and a save clear the item and the company's and global lists, which nobody reads
but the asset service still clears. A rebuild that found one already there clears nothing. The lists by chat and by funnel and the counts are never cached. A cache failure never fails the request.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from ...domain.crm.chat_funnels import ChatFunnelRepository
from ...models.cache import CacheProtocol
from ...models.company.CRM.funnel import ChatFunnel
from ...models.utils.types import StrObjectId
from ...services.chatty_assets.base_container_with_collection import CacheConfig
from ..asset_cache import AssetCache


class CachedChatFunnelRepository:
    def __init__(self, inner: ChatFunnelRepository, cache: CacheProtocol, config: Optional[CacheConfig] = None):
        self.inner = inner
        self.assets = AssetCache("chat_funnels", ChatFunnel, cache, config)

    async def get(self, company_id: StrObjectId, chat_funnel_id: StrObjectId) -> ChatFunnel:
        return await self.assets.item(chat_funnel_id, lambda: self.inner.get(company_id, chat_funnel_id))

    async def insert(self, company_id: StrObjectId, chat_funnel: ChatFunnel) -> ChatFunnel:
        inserted = await self.inner.insert(company_id, chat_funnel)
        await self.assets.invalidate(inserted.id, inserted.company_id)
        return inserted

    async def insert_if_missing(self, company_id: StrObjectId, chat_funnel: ChatFunnel) -> bool:
        inserted = await self.inner.insert_if_missing(company_id, chat_funnel)
        if inserted:
            await self.assets.invalidate(chat_funnel.id, chat_funnel.company_id)
        return inserted

    async def save(self, company_id: StrObjectId, chat_funnel: ChatFunnel) -> ChatFunnel:
        saved = await self.inner.save(company_id, chat_funnel)
        await self.assets.invalidate(saved.id, saved.company_id)
        return saved

    async def open_of_chat(self, company_id: StrObjectId, chat_id: StrObjectId) -> List[ChatFunnel]:
        return await self.inner.open_of_chat(company_id, chat_id)

    async def open_of_funnel(self, company_id: StrObjectId, funnel_id: StrObjectId) -> List[ChatFunnel]:
        return await self.inner.open_of_funnel(company_id, funnel_id)

    async def history_of_chat(self, company_id: StrObjectId, chat_id: StrObjectId) -> List[ChatFunnel]:
        return await self.inner.history_of_chat(company_id, chat_id)

    async def count_by_status(self, company_id: StrObjectId, funnel_id: StrObjectId) -> Dict[str, int]:
        return await self.inner.count_by_status(company_id, funnel_id)
