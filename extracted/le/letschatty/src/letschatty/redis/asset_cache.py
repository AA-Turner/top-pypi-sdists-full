"""The Redis cache the cached repositories put in front of their store: exactly what the asset service does.

`ChattyAssetContainerWithCollection` (`services/chatty_assets/base_container_with_collection.py`) is how every module
used the cache before the layered refactor, and other readers still go through it on the same keys. Each
`Cached*Repository` (ADR-001: the cache is a decorator of the repository) uses this one helper so the observable
behavior stays the asset service's (ADR-006): the same keys, TTLs, invalidation, logger, log texts and levels, and
the same reads to the store — a cached read reaches the store only on a miss.

- reads: cache first; a failed read is a miss logged at ERROR, an unreadable value is a silent miss, and on a miss
  the store's answer is written back (a failed write is silent: the read already logged once per request).
- writes: after the store accepted the write, the item key and the company's and the global list keys are deleted;
  a failed delete never fails the write and is logged at ERROR.
"""
from __future__ import annotations

import json
import logging
from typing import Any, Awaitable, Callable, Dict, Generic, List, Optional, Type, TypeVar

from ..models.cache import CacheProtocol
from ..models.utils.types import StrObjectId
from ..services.chatty_assets.base_container_with_collection import CacheConfig

# The asset service's logger: the logs stay as they were before the refactor (alerts and searches read them).
logger = logging.getLogger("ChattyAssetContainerWithCollection")

T = TypeVar("T")


class AssetCache(Generic[T]):
    def __init__(self, prefix: str, item_type: Type[T], cache: CacheProtocol, config: Optional[CacheConfig] = None):
        self.prefix = prefix
        self.item_type = item_type
        self.cache = cache
        self.config = config or CacheConfig.default()

    def item_key(self, item_id: StrObjectId) -> str:
        return f"{self.prefix}:item:{item_id}"

    def previews_key(self, company_id: Optional[StrObjectId]) -> str:
        return f"{self.prefix}:previews:{company_id or 'all'}"

    def all_key(self, company_id: Optional[StrObjectId]) -> str:
        return f"{self.prefix}:all:{company_id or 'all'}"

    def list_keys(self, company_id: Optional[StrObjectId]) -> List[str]:
        """The cached lists an item belongs to: its company's and the global ones."""
        keys = [self.previews_key(company_id), self.all_key(company_id)]
        if company_id:
            keys += [self.previews_key(None), self.all_key(None)]
        return keys

    async def item(self, item_id: StrObjectId, load: Callable[[], Awaitable[T]]) -> T:
        """The asset service's `get_by_id`."""
        key = self.item_key(item_id)
        cached = await self._read(key)
        if cached:
            try:
                return self.item_type.model_validate(json.loads(cached))
            except Exception:
                pass
        item = await load()
        try:
            await self.cache.set(key, json.dumps(item.model_dump(by_alias=True, mode="json")), ttl=self.config.cache_ttl)
        except Exception:
            pass
        return item

    async def previews(self, company_id: StrObjectId,
                       load: Callable[[], Awaitable[List[Dict[str, Any]]]]) -> List[Dict[str, Any]]:
        """The asset service's `get_all_previews`, without pagination."""
        key = self.previews_key(company_id)
        cached = await self._read(key)
        if cached:
            try:
                previews = json.loads(cached)
                if isinstance(previews, list):
                    return previews
            except Exception:
                pass
        previews = await load()
        try:
            await self.cache.set(key, json.dumps(previews), ttl=self.config.preview_cache_ttl)
        except Exception:
            pass
        return previews

    async def all(self, company_id: StrObjectId, load: Callable[[], Awaitable[List[T]]]) -> List[T]:
        """The asset service's `get_all`, without pagination."""
        key = self.all_key(company_id)
        cached = await self._read(key)
        if cached:
            try:
                return [self.item_type.model_validate(doc) for doc in json.loads(cached)]
            except Exception:
                pass
        items = await load()
        try:
            await self.cache.set(key, json.dumps([i.model_dump(by_alias=True, mode="json") for i in items]),
                                 ttl=self.config.cache_ttl)
        except Exception:
            pass
        return items

    async def invalidate(self, item_id: StrObjectId, company_id: Optional[StrObjectId]) -> None:
        """The asset service's `_invalidate`, after a write the store already accepted."""
        await self._delete([self.item_key(item_id), *self.list_keys(company_id)])

    async def invalidate_item(self, item_id: StrObjectId) -> None:
        """Only the item: the asset service's `partial_update` without `invalidate_previews`."""
        await self._delete([self.item_key(item_id)])

    async def _delete(self, keys: List[str]) -> None:
        try:
            await self.cache.delete_many(keys)
        except Exception as e:
            logger.error(
                "Redis cache invalidation failed after a saved write, keys may be stale until their TTL: %s (%s: %s)",
                keys, type(e).__name__, e,
            )

    async def _read(self, key: str) -> Optional[str]:
        try:
            return await self.cache.get(key)
        except Exception as e:
            logger.error(
                "Redis cache read failed, falling back to MongoDB: %s (%s: %s)",
                key, type(e).__name__, e,
            )
            return None
