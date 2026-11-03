"""The Redis cache in front of a catalog's repository (ADR-001: the cache is a decorator; ADR-010 of api-chatty: one
base for every catalog, in the same two flavors as `MongoCatalogRepository` / `MongoCatalogById`).

Keys are the ones the generic asset service has always used, because both still run side by side and other code
reads them: `<prefix>:item:{id}`, `<prefix>:previews:{company}`, `<prefix>:all:{company}` (and the global `…:all`
lists). TTLs come from the caller. Adding, editing, deleting and restoring invalidate them; a cache failure never fails
the request (`AssetCache`, ADR-006).
"""
from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from ..models.cache import CacheProtocol
from ..models.utils.types import StrObjectId
from ..services.chatty_assets.base_container_with_collection import CacheConfig
from .asset_cache import AssetCache

T = TypeVar("T")


class CachedCatalogBase(Generic[T]):
    """`inner` also marks an item deleted without reading it (`mark_deleted`), which only this decorator needs: it
    already read the item through the cache, as the asset service did."""

    prefix: str
    item_type: Type[T]

    def __init__(self, inner, cache: CacheProtocol, config: Optional[CacheConfig] = None):
        self.inner = inner
        self.assets = AssetCache(self.prefix, self.item_type, cache, config)

    async def add(self, item: T) -> T:
        added = await self.inner.add(item)
        await self.assets.invalidate(added.id, added.company_id)
        return added

    async def list_live(self, company_id: StrObjectId) -> List[T]:
        return await self.assets.all(company_id, lambda: self.inner.list_live(company_id))

    async def restore(self, item_id: StrObjectId) -> T:
        restored = await self.inner.restore(item_id)
        await self.assets.invalidate(restored.id, restored.company_id)
        return restored

    async def _deleted(self, item_id: StrObjectId, before: T) -> T:
        return await deleted_through_the_cache(self.inner, self.assets, item_id, before)


async def deleted_through_the_cache(inner, assets, item_id: StrObjectId, before: T) -> T:
    """The asset service's `delete`: `before` was read once through the cache, the store marks the id as asked and the
    item and the lists are cleared after it. Shared with the caches that are not a catalog (`CachedSourceRepository`)."""
    await inner.mark_deleted(item_id)
    await assets.invalidate(before.id, before.company_id)
    return before


class CachedCatalogRepository(CachedCatalogBase[T]):
    async def get(self, company_id: StrObjectId, item_id: StrObjectId) -> T:
        return await self.assets.item(item_id, lambda: self.inner.get(company_id, item_id))

    async def update(self, company_id: StrObjectId, item_id: StrObjectId, changes: T) -> T:
        # The merge reads Mongo NOW, never the cached copy, as the asset service did.
        updated = await self.inner.update(company_id, item_id, changes)
        await self.assets.invalidate(updated.id, updated.company_id)
        return updated

    async def delete(self, company_id: StrObjectId, item_id: StrObjectId) -> T:
        return await self._deleted(item_id, await self.get(company_id, item_id))


class _CachedPreviews:
    """The previews of a catalog listed by them (`<prefix>:previews:{company}`)."""

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        return await self.assets.previews(company_id, lambda: self.inner.list_previews(company_id))


class CachedCatalogWithPreviews(_CachedPreviews, CachedCatalogRepository[T]):
    """The cache of a `MongoCatalogWithPreviews`."""


class CachedCatalogById(CachedCatalogBase[T]):
    async def get(self, item_id: StrObjectId) -> T:
        return await self.assets.item(item_id, lambda: self.inner.get(item_id))

    async def update(self, item_id: StrObjectId, changes: T) -> T:
        updated = await self.inner.update(item_id, changes)
        await self.assets.invalidate(updated.id, updated.company_id)
        return updated

    async def delete(self, item_id: StrObjectId) -> T:
        return await self._deleted(item_id, await self.get(item_id))


class CachedCatalogByIdWithPreviews(_CachedPreviews, CachedCatalogById[T]):
    """The cache of a `MongoCatalogByIdWithPreviews`."""
