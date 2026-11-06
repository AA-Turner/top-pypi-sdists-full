"""Redis cache in front of any `CoexistenceImportSyncRepository` (ADR-001: the cache is a decorator, not part of Mongo).

What the asset service `CoexistenceImportSyncs` did, operation by operation (ADR-006):
- `get` reads `coexistence_import_sync:item:{id}` first and writes it back on a miss (`AssetCache.item`);
- `add` is the asset service's `insert`: the item key and the company's and the global list keys are deleted;
- every atomic write then drops only the item key with ONE `delete`, best-effort: a failure is logged at DEBUG on the
  `CoexistenceImportSyncs` logger and never fails the write that Mongo already accepted (the reads that matter go to
  Mongo directly). Adopting a number and the reads by company or number never touched the cache, and still do not.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Optional

from ...domain.messaging.coexistence_import_sync import CoexistenceImportSyncRepository
from ...models.cache import CacheProtocol
from ...models.chat.coexistence_import_sync import CoexistenceImportSync
from ...models.utils.types import StrObjectId
from ...services.chatty_assets.base_container_with_collection import CacheConfig
from ..asset_cache import AssetCache

# The legacy asset service's logger: the log keeps its name, text and level.
logger = logging.getLogger("CoexistenceImportSyncs")


class CachedCoexistenceImportSyncRepository:
    prefix = "coexistence_import_sync"

    def __init__(self, inner: CoexistenceImportSyncRepository, cache: CacheProtocol,
                 config: Optional[CacheConfig] = None):
        self.inner = inner
        self.cache = AssetCache(self.prefix, CoexistenceImportSync, cache, config)

    async def of_company(self, company_id: StrObjectId) -> List[CoexistenceImportSync]:
        return await self.inner.of_company(company_id)

    async def of_number(self, company_id: StrObjectId, phone_number_id: Optional[str]) -> List[CoexistenceImportSync]:
        return await self.inner.of_number(company_id, phone_number_id)

    async def adopt(self, sync_id: StrObjectId, phone_number_id: str) -> bool:
        return await self.inner.adopt(sync_id, phone_number_id)

    async def add(self, item: CoexistenceImportSync) -> None:
        await self.inner.add(item)
        await self.cache.invalidate(item.id, item.company_id)

    async def get(self, sync_id: StrObjectId) -> CoexistenceImportSync:
        return await self.cache.item(sync_id, lambda: self.inner.get(sync_id))

    async def apply_chunk(self, sync_id: StrObjectId, *, key: str, messages_delta: int, threads_delta: int,
                          contacts_delta: int, progress: Optional[float]) -> None:
        await self.inner.apply_chunk(sync_id, key=key, messages_delta=messages_delta, threads_delta=threads_delta,
                                     contacts_delta=contacts_delta, progress=progress)
        await self._drop(sync_id)

    async def add_imported(self, sync_id: StrObjectId, *, messages_delta: int, threads_delta: int) -> None:
        await self.inner.add_imported(sync_id, messages_delta=messages_delta, threads_delta=threads_delta)
        await self._drop(sync_id)

    async def touch_last_chunk(self, sync_id: StrObjectId, when: datetime) -> None:
        await self.inner.touch_last_chunk(sync_id, when)
        await self._drop(sync_id)

    async def reopen_if_completed(self, sync_id: StrObjectId) -> Optional[CoexistenceImportSync]:
        reopened = await self.inner.reopen_if_completed(sync_id)
        await self._drop(sync_id)
        return reopened

    async def complete_if_pending(self, sync_id: StrObjectId) -> Optional[CoexistenceImportSync]:
        completed = await self.inner.complete_if_pending(sync_id)
        await self._drop(sync_id)
        return completed

    async def stale_in_progress(self, older_than: datetime) -> List[CoexistenceImportSync]:
        return await self.inner.stale_in_progress(older_than)

    async def set_notification_id(self, sync_id: StrObjectId, notification_id: str) -> None:
        await self.inner.set_notification_id(sync_id, notification_id)
        await self._drop(sync_id)

    async def _drop(self, sync_id: StrObjectId) -> None:
        await self.cache.drop_key(self.cache.item_key(str(sync_id)), on_failure=lambda exc: logger.debug(
            "coexistence_import_sync cache bust failed for %s: %s", sync_id, exc))
