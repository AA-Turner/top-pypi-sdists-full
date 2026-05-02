from typing import TypeVar, Type, List, Optional, Dict, Any, Generic
from pydantic import BaseModel, Field
from abc import ABC
from ...models.base_models.chatty_asset_model import ChattyAssetModel, CompanyAssetModel, ChattyAssetPreview
from ...models.cache import CacheProtocol, NoCache
from ...models.execution.execution import ExecutionContext
from ...models.analytics.events.event_types import EventType
from ...models.data_base.collection_interface import ChattyAssetCollectionInterface
from ...models.utils.custom_exceptions.custom_exceptions import NotFoundError
from ...models.utils.types.deletion_type import DeletionType
from ...models.utils.types import StrObjectId
from datetime import datetime
from zoneinfo import ZoneInfo
import logging
import json

logger = logging.getLogger("ChattyAssetContainerWithCollection")

T = TypeVar('T', bound=ChattyAssetModel)
P = TypeVar('P', bound=ChattyAssetPreview)


class CacheConfig(BaseModel):
    cache_ttl: int = Field(default=60 * 5, description="TTL in seconds for individual items")
    preview_cache_ttl: int = Field(default=60 * 5, description="TTL in seconds for preview lists")

    @classmethod
    def default(cls) -> 'CacheConfig':
        return cls()


class ChattyAssetContainerWithCollection(Generic[T, P], ABC):
    """
    Async base class for asset services. Reads: cache → MongoDB. Writes: MongoDB → cache invalidation.
    No local in-memory state. The cache implementation is injected (CacheProtocol).

    Cached read shapes:
      get_by_id(id)                → key: {col}:item:{id}            — single full model
      get_all_previews(company_id) → key: {col}:previews:{company_id} — all previews for a company
      get_all(company_id)          → key: {col}:all:{company_id}      — all full models for a company

    Pagination (limit/skip) slices from the cached list in memory — the DB is only hit
    once per company to warm the cache; subsequent paginated calls are served from Redis.

    Direct DB access (no cache):
      get_by_query(query, company_id) — arbitrary MongoDB query, always hits DB
      get_deleted(company_id)         — always hits DB
    """

    def __init__(
        self,
        item_type: Type[T],
        preview_type: Optional[Type[P]],
        collection: ChattyAssetCollectionInterface,
        cache_config: CacheConfig = None,
        cache: CacheProtocol = None,
    ):
        if not isinstance(collection, ChattyAssetCollectionInterface):
            raise TypeError(
                f"Expected collection of type ChattyAssetCollectionInterface, "
                f"got {type(collection).__name__}"
            )
        self.item_type = item_type
        self.preview_type = preview_type
        self.collection = collection
        self.cache_config = cache_config or CacheConfig.default()
        self.cache: CacheProtocol = cache or NoCache()
        self._collection_name = collection.collection.name

    # ------------------------------------------------------------------
    # Cache key helpers
    # ------------------------------------------------------------------

    def _item_key(self, item_id: str) -> str:
        return f"{self._collection_name}:item:{item_id}"

    def _previews_key(self, company_id: Optional[str]) -> str:
        return f"{self._collection_name}:previews:{company_id or 'all'}"

    def _all_key(self, company_id: Optional[str]) -> str:
        return f"{self._collection_name}:all:{company_id or 'all'}"

    # ------------------------------------------------------------------
    # Write operations — MongoDB first, then invalidate all related keys
    # ------------------------------------------------------------------

    async def _invalidate(self, item: T) -> None:
        company_id = getattr(item, 'company_id', None)
        await self.cache.delete_many([
            self._item_key(item.id),
            self._previews_key(company_id),
            self._all_key(company_id),
        ])

    async def partial_update(
        self,
        id: str,
        fields: dict,
        execution_context: ExecutionContext,
        invalidate_previews: bool = False,
        company_id: Optional[str] = None,
    ) -> None:
        """
        $set only the given fields. Use instead of update() when you know exactly
        which fields changed and don't want to load/replace the full document.

        invalidate_previews=True also clears the previews and all-key caches for
        the company (pass company_id). Set this when the changed fields appear in
        the inbox preview (area, agent_id, is_read_status, starred, etc.).
        """
        await self.collection.partial_update(id, fields)
        execution_context.set_event_time(datetime.now(ZoneInfo("UTC")))
        keys = [self._item_key(id)]
        if invalidate_previews and company_id:
            keys += [self._previews_key(company_id), self._all_key(company_id)]
        await self.cache.delete_many(keys)

    async def insert(self, item: T, execution_context: ExecutionContext) -> T:
        if not isinstance(item, self.item_type):
            raise TypeError(f"Expected item of type {self.item_type.__name__}, got {type(item).__name__}")
        await self.collection.insert(item)
        execution_context.set_event_time(item.created_at)
        await self._invalidate(item)
        return item

    async def update(self, id: str, new_item: T, execution_context: ExecutionContext) -> T:
        existing = await self.get_by_id(id)
        updated_item = existing.update(new_item)
        await self.collection.update(updated_item)
        execution_context.set_event_time(updated_item.updated_at)
        await self._invalidate(updated_item)
        return updated_item

    async def delete(self, id: str, execution_context: ExecutionContext, deletion_type: DeletionType = DeletionType.LOGICAL) -> T:
        item = await self.get_by_id(id)
        await self.collection.delete(id, deletion_type)
        execution_context.set_event_time(datetime.now(ZoneInfo("UTC")))
        await self._invalidate(item)
        return item

    async def restore(self, id: str, execution_context: ExecutionContext) -> T:
        item = await self.collection.get_by_id(id)
        if item is None:
            raise NotFoundError(f"Item with id {id} not found in collection DB")
        item.deleted_at = None
        item.update_now()
        execution_context.set_event_time(item.updated_at)
        await self.collection.update(item)
        await self._invalidate(item)
        return item

    # ------------------------------------------------------------------
    # Cached reads — cache → MongoDB fallback
    # ------------------------------------------------------------------

    async def get_by_id(self, id: str, ignore_cache: bool = False) -> T:
        key = self._item_key(id)
        if not ignore_cache:
            cached = await self.cache.get(key)
            if cached:
                try:
                    return self.item_type.model_validate(json.loads(cached))
                except Exception:
                    pass
        item = await self.collection.get_by_id(id)
        try:
            await self.cache.set(key, json.dumps(item.model_dump(by_alias=True, mode='json')), ttl=self.cache_config.cache_ttl)
        except Exception:
            pass
        return item

    async def get_all_previews(
        self,
        company_id: Optional[StrObjectId],
        limit: int = 0,
        skip: int = 0,
        ignore_cache: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Returns preview dicts for a company, optionally paginated.

        Pagination slices from the cached full list — the DB is hit only once to warm the cache.
        limit=0 means no limit (return all).
        """
        key = self._previews_key(company_id)
        if not ignore_cache:
            cached = await self.cache.get(key)
            if cached:
                try:
                    result = json.loads(cached)
                    if isinstance(result, list):
                        return _paginate(result, skip, limit)
                except Exception:
                    pass
        if not self.preview_type:
            raise ValueError(f"{self.__class__.__name__} has no preview_type set")
        projection = self.preview_type.get_projection()
        previews = await self.collection.get_preview_docs(
            projection=projection, all=False, company_id=company_id
        )
        result = [p.model_dump(mode='json') for p in previews]
        try:
            await self.cache.set(key, json.dumps(result), ttl=self.cache_config.preview_cache_ttl)
        except Exception:
            pass
        return _paginate(result, skip, limit)

    async def get_all(
        self,
        company_id: Optional[StrObjectId],
        limit: int = 0,
        skip: int = 0,
        ignore_cache: bool = False,
    ) -> List[T]:
        """
        Returns all non-deleted items for a company, optionally paginated.

        Pagination slices from the cached full list — the DB is hit only once to warm the cache.
        limit=0 means no limit (return all).
        """
        key = self._all_key(company_id)
        if not ignore_cache:
            cached = await self.cache.get(key)
            if cached:
                try:
                    items = [self.item_type.model_validate(d) for d in json.loads(cached)]
                    return _paginate(items, skip, limit)
                except Exception:
                    pass
        items = await self.collection.get_docs(company_id=company_id, query={"deleted_at": None})
        try:
            serialized = json.dumps([i.model_dump(by_alias=True, mode='json') for i in items])
            await self.cache.set(key, serialized, ttl=self.cache_config.cache_ttl)
        except Exception:
            pass
        return _paginate(items, skip, limit)

    # ------------------------------------------------------------------
    # Direct DB reads — always bypass cache, use for arbitrary queries
    # ------------------------------------------------------------------

    async def get_by_query(self, query: dict, company_id: Optional[StrObjectId] = None) -> List[T]:
        """Always hits MongoDB. Use for filtered searches that can't be cached predictably."""
        return await self.collection.get_docs(query=query, company_id=company_id)

    async def get_deleted(self, company_id: Optional[StrObjectId]) -> List[T]:
        """Always hits MongoDB."""
        return await self.collection.get_docs(query={"deleted_at": {"$ne": None}}, company_id=company_id)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _paginate(items: list, skip: int, limit: int) -> list:
    if skip:
        items = items[skip:]
    if limit:
        items = items[:limit]
    return items
