"""Redis cache in front of any `SourceRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the asset service has always used, because the legacy `Sources` service still serves the message
path's readers on the same keys: `sources:item:{id}`, `sources:previews:{company}`, `sources:all:{company}` (and the
global `…:all` lists), 24 h. What is NOT the generic `AssetCache` and stays as api-chatty's `Sources` always did:

- reads: a source is built back with `SourceFactory` (the subclass of its `type`), an unreadable value is a silent
  miss, and a failed cache READ is not a miss: it raises (`Sources.get_by_id`/`get_all` never caught it);
- a whole write (add, update, delete, restore) invalidates the item and the company's and the global lists
  (`AssetCache.invalidate`, logged at ERROR on failure, never raising);
- a targeted write (`entrada_id`, the motivos) invalidates through `forget`: the items and the company's lists only,
  logged at ERROR on logger `SourcesAssetService` on failure (`Sources._invalidar_fuentes`);
- `drop_cache` (on request) deletes the same keys and lets a failure through.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from ...models.analytics.sources import SourceBase
from ...models.cache import CacheProtocol
from ...models.utils.types import StrObjectId
from ...services.chatty_assets.base_container_with_collection import CacheConfig
from ...services.factories.analytics.sources.source_factory import SourceFactory
from ..asset_cache import AssetCache
from ..cached_catalog_repository import deleted_through_the_cache

# The legacy `Sources` service's logger: the logs stay as they were before the refactor.
logger = logging.getLogger("SourcesAssetService")


class CachedSourceRepository:
    prefix = "sources"

    def __init__(self, inner, cache: CacheProtocol, config: Optional[CacheConfig] = None):
        self.inner = inner
        self.cache = cache
        self.assets = AssetCache(self.prefix, SourceBase, cache, config)

    # ── whole reads ──

    async def get(self, source_id: StrObjectId) -> SourceBase:
        key = self.assets.item_key(source_id)
        cached = await self.cache.get(key)
        if cached:
            try:
                return SourceFactory.instantiate_source(json.loads(cached))
            except Exception:
                pass
        source = await self.inner.get(source_id)
        try:
            await self.cache.set(key, json.dumps(source.model_dump(by_alias=True, mode="json")),
                                 ttl=self.assets.config.cache_ttl)
        except Exception:
            pass
        return source

    async def list_live(self, company_id: StrObjectId, fresh: bool = False) -> List[SourceBase]:
        key = self.assets.all_key(company_id)
        if not fresh:
            cached = await self.cache.get(key)
            if cached:
                try:
                    return [SourceFactory.instantiate_source(doc) for doc in json.loads(cached)]
                except Exception:
                    pass
        sources = await self.inner.list_live(company_id)
        try:
            await self.cache.set(key, json.dumps([s.model_dump(by_alias=True, mode="json") for s in sources]),
                                 ttl=self.assets.config.cache_ttl)
        except Exception:
            pass
        return sources

    async def list_for_validation(self, company_id: StrObjectId) -> List[SourceBase]:
        return await self.inner.list_for_validation(company_id)

    # ── whole writes ──

    async def add(self, source: SourceBase) -> SourceBase:
        added = await self.inner.add(source)
        await self.assets.invalidate(added.id, added.company_id)
        return added

    async def update(self, source_id: StrObjectId, changes: SourceBase) -> SourceBase:
        # The merge reads Mongo NOW, never the cached copy, as the asset service did.
        updated = await self.inner.update(source_id, changes)
        await self.assets.invalidate(updated.id, updated.company_id)
        return updated

    async def delete(self, source_id: StrObjectId) -> SourceBase:
        # Read through the cache, as `AssetService.delete` read it.
        return await deleted_through_the_cache(self.inner, self.assets, source_id, await self.get(source_id))

    async def patch(self, company_id: StrObjectId, source_id: StrObjectId, fields: Dict[str, Any]) -> None:
        """The item and the company's and the global lists: the asset service's `partial_update` with
        `invalidate_previews` (the sources' table reads the `all` list)."""
        await self.inner.patch(company_id, source_id, fields)
        await self.assets.invalidate(source_id, company_id)

    # ── targeted (the use case calls `forget` where the legacy service invalidated) ──

    async def entries_of_sources(self, company_id: StrObjectId) -> Dict[str, Optional[str]]:
        return await self.inner.entries_of_sources(company_id)

    async def accounts_of_sources(self, company_id: StrObjectId) -> Dict[str, Optional[str]]:
        return await self.inner.accounts_of_sources(company_id)

    async def set_entry(self, company_id: StrObjectId, source_ids: List[str], entry_id: Optional[str],
                        now: datetime) -> int:
        return await self.inner.set_entry(company_id, source_ids, entry_id, now)

    async def clear_entry(self, company_id: StrObjectId, entry_id: str, source_ids: Optional[List[str]],
                          now: datetime) -> List[str]:
        return await self.inner.clear_entry(company_id, entry_id, source_ids, now)

    async def find_for_mapping(self, company_id: StrObjectId, source_id: StrObjectId) -> Optional[Dict[str, Any]]:
        return await self.inner.find_for_mapping(company_id, source_id)

    async def mapping_candidates(self, company_id: StrObjectId, ad_types: List[str]) -> List[Dict[str, Any]]:
        return await self.inner.mapping_candidates(company_id, ad_types)

    async def set_fields(self, company_id: StrObjectId, source_id: StrObjectId, fields: Dict[str, Any],
                          when: Optional[str] = None) -> bool:
        return await self.inner.set_fields(company_id, source_id, fields, when)

    async def put_back_fields(self, company_id: StrObjectId, source_id: StrObjectId, fields: Dict[str, Any],
                               absent: List[str]) -> None:
        await self.inner.put_back_fields(company_id, source_id, fields, absent)

    # ── cache ──

    def _company_keys(self, company_id: StrObjectId, source_ids: List[str]) -> List[str]:
        return ([self.assets.item_key(s) for s in source_ids]
                + [self.assets.previews_key(str(company_id)), self.assets.all_key(str(company_id))])

    async def forget(self, company_id: StrObjectId, source_ids: List[str]) -> None:
        try:
            await self.cache.delete_many(self._company_keys(company_id, source_ids))
        except Exception:
            # The write is already in Mongo: a copy that could not be dropped expires (TTL) and the runtime reads the
            # source again. The trace is left at ERROR.
            logger.error("sources_cache_no_invalidada company_id=%s", company_id, exc_info=True)

    async def all_ids(self, company_id: StrObjectId) -> List[str]:
        return await self.inner.all_ids(company_id)

    async def drop_cache(self, company_id: StrObjectId, source_ids: List[str]) -> None:
        await self.cache.delete_many(self._company_keys(company_id, source_ids))
