"""The Redis cache the cached repositories put in front of their store: exactly what the asset service does.

`ChattyAssetContainerWithCollection` (`services/chatty_assets/base_container_with_collection.py`) is how every module
used the cache before the layered refactor, and other readers still go through it on the same keys. Each
`Cached*Repository` (ADR-001: the cache is a decorator of the repository) uses this one helper so the observable
behavior stays the asset service's (ADR-006): the same keys, TTLs, invalidation, logger, log texts and levels, and
the same reads to the store — a cached read reaches the store only on a miss.

- reads: cache first; a failed read is a miss logged at ERROR, an unreadable value is a silent miss, and on a miss
  the store's answer is written back (a failed write is silent: the read already logged once per request). A fresh
  read (`ignore_cache=True`, the asset service's `get_by_id`/`get_all(ignore_cache=True)`) skips the cache read and
  still writes the answer back (ENG-135).
- writes: after the store accepted the write, the item key and the company's and the global list keys are deleted;
  a failed delete never fails the write and is logged at ERROR (`invalidate`, `invalidate_item`). A drop the legacy
  service did by hand says who handles its failure, which may let it through (`drop`, `drop_key`).

This is the only place in `letschatty/redis` that talks to Redis for an asset (ENG-68; the guard is
`tests/unit/redis/test_only_the_asset_cache_talks_to_redis.py`). What a legacy service did differently on top of the
asset service is a parameter here, never a copy in the repository:

- `build`: how a cached document comes back (a polymorphic asset uses its factory; by default `item_type`);
- `raise_read_failures`: a failed cache read goes up instead of being a miss (`Sources`, `AiComponents`: ENG-133).
  It holds for EVERY read of the cache that sets it (`item`, `all` and `previews`), not only the ones the repository
  reads today: a new previews read on Sources or on AI components will raise too;
- `on_failure` of a drop: who handles a failed delete (`None` lets it through, as the writes of `main` that were not
  wrapped); by default the asset service's ERROR.
"""
from __future__ import annotations

import json
import logging
from typing import Any, Awaitable, Callable, Dict, Generic, Iterable, List, Optional, Type, TypeVar

from ..models.cache import CacheProtocol
from ..models.utils.types import StrObjectId
from ..services.chatty_assets.base_container_with_collection import CacheConfig

# The asset service's logger: the logs stay as they were before the refactor (alerts and searches read them).
logger = logging.getLogger("ChattyAssetContainerWithCollection")

T = TypeVar("T")

# Who handles a failed delete, inside the failure (so `exc_info=True` still sees it). `None` lets it through.
OnFailure = Optional[Callable[[Exception], None]]


def _log_stale_keys(keys: List[str]) -> Callable[[Exception], None]:
    def log(e: Exception) -> None:
        logger.error(
            "Redis cache invalidation failed after a saved write, keys may be stale until their TTL: %s (%s: %s)",
            keys, type(e).__name__, e,
        )
    return log


class AssetCache(Generic[T]):
    def __init__(self, prefix: str, item_type: Type[T], cache: CacheProtocol, config: Optional[CacheConfig] = None,
                 *, build: Optional[Callable[[Any], T]] = None, raise_read_failures: bool = False):
        self.prefix = prefix
        self.item_type = item_type
        self.cache = cache
        self.config = config or CacheConfig.default()
        self.build = build or item_type.model_validate
        self.raise_read_failures = raise_read_failures

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

    def company_keys(self, company_id: StrObjectId, item_ids: Iterable[StrObjectId]) -> List[str]:
        """The items and the company's lists, without the global ones (`Sources._invalidar_fuentes`)."""
        return [self.item_key(i) for i in item_ids] + [self.previews_key(company_id), self.all_key(company_id)]

    async def item(self, item_id: StrObjectId, load: Callable[[], Awaitable[T]], *, ignore_cache: bool = False) -> T:
        """The asset service's `get_by_id(id, ignore_cache)`."""
        key = self.item_key(item_id)
        cached = None if ignore_cache else await self._read(key)
        if cached:
            try:
                return self.build(json.loads(cached))
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

    async def all(self, company_id: StrObjectId, load: Callable[[], Awaitable[List[T]]], *,
                  ignore_cache: bool = False) -> List[T]:
        """The asset service's `get_all(company_id, ignore_cache)`, without pagination."""
        key = self.all_key(company_id)
        cached = None if ignore_cache else await self._read(key)
        if cached:
            try:
                return [self.build(doc) for doc in json.loads(cached)]
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
        keys = [self.item_key(item_id), *self.list_keys(company_id)]
        await self.drop(keys, on_failure=_log_stale_keys(keys))

    async def invalidate_item(self, item_id: StrObjectId) -> None:
        """Only the item: the asset service's `partial_update` without `invalidate_previews`."""
        keys = [self.item_key(item_id)]
        await self.drop(keys, on_failure=_log_stale_keys(keys))

    async def drop(self, keys: List[str], *, on_failure: OnFailure) -> None:
        """One `delete_many` of `keys`. `on_failure=None` lets a failure through; a handler is called with the error,
        inside the failure."""
        try:
            await self.cache.delete_many(keys)
        except Exception as e:
            self._failed(e, on_failure)

    async def drop_key(self, key: str, *, on_failure: OnFailure) -> None:
        """One `delete` of one key, for a service that never batched it (`CoexistenceImportSyncs`)."""
        try:
            await self.cache.delete(key)
        except Exception as e:
            self._failed(e, on_failure)

    @staticmethod
    def _failed(e: Exception, on_failure: OnFailure) -> None:
        """Only called from an `except` block: the bare `raise` re-raises the failure being handled."""
        if on_failure is None:
            raise  # the failure being handled, with its own traceback
        on_failure(e)

    async def _read(self, key: str) -> Optional[str]:
        if self.raise_read_failures:
            return await self.cache.get(key)
        try:
            return await self.cache.get(key)
        except Exception as e:
            logger.error(
                "Redis cache read failed, falling back to MongoDB: %s (%s: %s)",
                key, type(e).__name__, e,
            )
            return None
