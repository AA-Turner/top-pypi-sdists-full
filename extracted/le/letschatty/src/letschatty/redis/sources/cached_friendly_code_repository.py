"""Redis in front of any `FriendlyCodeRepository` (ADR-001: the cache is a decorator).

Two kinds of keys, both as the legacy `FriendlyURLGenerator` has always written them:

- the pair, without TTL (a code never changes): `friendly_code:{company}:{code}` → source id and
  `friendly_code:reverse:{company}:{source_id}` → code. Written together every time a code is found in the store or
  created. Reading or writing them is not guarded: a Redis failure fails the lookup, as before. Only the batch read
  (`known_codes`, one MGET) falls back to «none known», logged at WARNING (logger `FriendlyURLGenerator`).
- the asset service's keys of the collection (`friendly_codes:item:{id}` and the lists, ADR-006, `AssetCache`):
  nobody reads them, but adding and editing a record deleted them, and still does.

Editing a record (the source merger moving a code) does not touch the pair, as before: the code's key keeps naming
the old source until Redis loses it.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from ...models.analytics.smart_messages.friendly_code_for_source import FriendlyCodeForSource
from ...models.cache import CacheProtocol
from ...models.utils.types import StrObjectId
from ...services.chatty_assets.base_container_with_collection import CacheConfig
from ..asset_cache import AssetCache

# The legacy service's logger: the line stays as it was (searches read it).
logger = logging.getLogger("FriendlyURLGenerator")


def code_key(company_id: StrObjectId, code: str) -> str:
    return f"friendly_code:{company_id}:{code}"


def source_key(company_id: StrObjectId, source_id: StrObjectId) -> str:
    return f"friendly_code:reverse:{company_id}:{source_id}"


class CachedFriendlyCodeRepository:
    def __init__(self, inner, cache: CacheProtocol, config: Optional[CacheConfig] = None):
        self.inner = inner
        self.cache = cache
        self.assets = AssetCache("friendly_codes", FriendlyCodeForSource, cache, config)

    async def code_of_source(self, company_id: StrObjectId, source_id: StrObjectId) -> Optional[str]:
        cached = await self.cache.get(source_key(company_id, source_id))
        if cached:
            return cached
        return await self.stored_code_of_source(company_id, source_id)

    async def stored_code_of_source(self, company_id: StrObjectId, source_id: StrObjectId) -> Optional[str]:
        code = await self.inner.stored_code_of_source(company_id, source_id)
        if code is not None:
            await self._remember(company_id, code, source_id)
        return code

    async def source_of_code(self, company_id: StrObjectId, code: str) -> Optional[str]:
        cached = await self.cache.get(code_key(company_id, code))
        if cached:
            return cached
        source_id = await self.inner.source_of_code(company_id, code)
        if source_id is not None:
            await self._remember(company_id, code, source_id)
        return source_id

    async def known_codes(self, company_id: StrObjectId, source_ids: List[str]) -> Dict[str, str]:
        keys = [source_key(company_id, source_id) for source_id in source_ids]
        try:
            codes = await self.cache.get_many(keys)
        except Exception as exc:
            logger.warning("Batch read of friendly codes failed, falling back to one read per source: %s", exc)
            return {}
        return {source_id: code for source_id, code in zip(source_ids, codes) if code}

    async def records_of_source(self, company_id: StrObjectId, source_id: StrObjectId) -> List[FriendlyCodeForSource]:
        return await self.inner.records_of_source(company_id, source_id)

    async def add(self, record: FriendlyCodeForSource) -> FriendlyCodeForSource:
        added = await self.inner.add(record)
        await self.assets.invalidate(added.id, added.company_id)
        await self._remember(added.company_id, added.friendly_code, str(added.source_id))
        return added

    async def update(self, record_id: StrObjectId, changes: FriendlyCodeForSource) -> FriendlyCodeForSource:
        updated = await self.inner.update(record_id, changes)
        await self.assets.invalidate(updated.id, updated.company_id)
        return updated

    async def _remember(self, company_id: StrObjectId, code: str, source_id: StrObjectId) -> None:
        await self.cache.set(code_key(company_id, code), source_id)
        await self.cache.set(source_key(company_id, source_id), code)
