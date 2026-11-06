"""Redis cache in front of any `EntryRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because the legacy `Entradas` service still serves the
readers by id on the same keys: `entradas:item:{id}`, `entradas:previews:{company}`, `entradas:all:{company}` (and the
global `…:all` lists). The fresh read writes the item key, as the asset service's `get_by_id(ignore_cache=True)` did.
Adding, editing and deleting invalidate them (ADR-006, `AssetCache`). A cache failure never fails the request.
"""
from __future__ import annotations

from typing import Any, Optional, Tuple

from ...models.company.assets.atencion import Entrada
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogById


class CachedEntryRepository(CachedCatalogById[Entrada]):
    """A catalog's cache read by id (`CachedCatalogById`, ADR-010 of api-chatty) plus the fresh read and the
    compare-and-set."""

    prefix = "entradas"
    item_type = Entrada

    async def get_fresh(self, entry_id: StrObjectId) -> Entrada:
        return await self.assets.item(entry_id, lambda: self.inner.get_fresh(entry_id), ignore_cache=True)

    async def stored_updated_at(self, entry_id: StrObjectId) -> Tuple[bool, Any]:
        return await self.inner.stored_updated_at(entry_id)

    async def update_if_unchanged(self, current: Entrada, changes: Entrada, stored_updated_at: Any) -> Optional[Entrada]:
        updated = await self.inner.update_if_unchanged(current, changes, stored_updated_at)
        if updated is not None:
            await self.assets.invalidate(updated.id, updated.company_id)
        return updated
