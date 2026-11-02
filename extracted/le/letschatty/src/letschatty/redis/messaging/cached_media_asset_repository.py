"""Redis cache in front of any `MediaAssetRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used: `media_assets:item:{id}` (the id as it was asked for),
`media_assets:previews:{company}`, `media_assets:all:{company}` and the global lists; TTLs from the caller (24 h).
Only the read by id is cached: the listing and the lookups by key and hash always read the store. Adding and deleting
invalidate the item and the lists; an `edit` the item and the company's lists, a `record_use` only the item, as the asset
service's `partial_update` did (the decorator decides, not the caller: ADR-001). A cache failure never fails the request (ADR-006, `AssetCache`).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol, Tuple

from ...domain.messaging.media_assets import MediaAssetFilter, MediaAssetRepository
from ...models.cache import CacheProtocol
from ...models.company.assets import MediaAsset
from ...models.utils.types import StrObjectId
from ...services.chatty_assets.base_container_with_collection import CacheConfig
from ..asset_cache import AssetCache


class MediaAssetStore(MediaAssetRepository, Protocol):
    """The store this decorator wraps: also marks one deleted without reading it, which only the decorator needs."""

    async def mark_deleted(self, asset_id: StrObjectId) -> None: ...


class CachedMediaAssetRepository:
    def __init__(self, inner: MediaAssetStore, cache: CacheProtocol, config: Optional[CacheConfig] = None):
        self.inner = inner
        self.assets = AssetCache("media_assets", MediaAsset, cache, config)

    async def get(self, asset_id: StrObjectId) -> MediaAsset:
        return await self.assets.item(asset_id, lambda: self.inner.get(asset_id))

    async def page(self, company_id: StrObjectId, filter: MediaAssetFilter, descending: bool,
                   cursor: Optional[str], limit: int) -> Tuple[List[MediaAsset], Optional[str]]:
        return await self.inner.page(company_id, filter, descending, cursor, limit)

    async def find_by_s3_key(self, company_id: StrObjectId, s3_key: str) -> Optional[MediaAsset]:
        return await self.inner.find_by_s3_key(company_id, s3_key)

    async def find_by_sha256(self, company_id: StrObjectId, sha256: str) -> Optional[MediaAsset]:
        return await self.inner.find_by_sha256(company_id, sha256)

    async def add(self, asset: MediaAsset) -> MediaAsset:
        added = await self.inner.add(asset)
        await self.assets.invalidate(added.id, added.company_id)
        return added

    async def edit(self, company_id: StrObjectId, asset_id: StrObjectId, fields: Dict[str, Any]) -> None:
        # The item and the company's lists, as the legacy service's `partial_update`.
        await self.inner.edit(company_id, asset_id, fields)
        await self.assets.invalidate(asset_id, company_id)

    async def record_use(self, asset_id: StrObjectId, use_count: int, last_used_at: datetime) -> None:
        # Only the item: a use is a sort hint and does not reorder the cached lists (as before).
        await self.inner.record_use(asset_id, use_count, last_used_at)
        await self.assets.invalidate_item(asset_id)

    async def delete(self, asset_id: StrObjectId) -> MediaAsset:
        # The file as it was is read through the cache, as the asset service always did, and only once.
        before = await self.get(asset_id)
        await self.inner.mark_deleted(asset_id)
        await self.assets.invalidate(before.id, before.company_id)
        return before
