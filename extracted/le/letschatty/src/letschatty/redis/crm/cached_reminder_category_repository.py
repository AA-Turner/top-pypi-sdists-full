"""Redis cache in front of any `ReminderCategoryRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used: `recordatorio_categorias:item:{id}` and
`recordatorio_categorias:all:{company}` (live ones only); every write also clears `:previews:{company}` and the
global `…:all` lists. Deleted categories are always read from the store. TTLs come from the caller. A cache failure
never fails the request.
"""
from __future__ import annotations

from typing import List

from ...models.company.assets.recordatorio_categoria import RecordatorioCategoria
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogBase


class CachedReminderCategoryRepository(CachedCatalogBase[RecordatorioCategoria]):
    """The base's add, live list and restore (`CachedCatalogBase`, ADR-010 of api-chatty), plus what is its own."""

    prefix = "recordatorio_categorias"
    item_type = RecordatorioCategoria

    async def get(self, category_id: StrObjectId) -> RecordatorioCategoria:
        return await self.assets.item(category_id, lambda: self.inner.get(category_id))

    async def list_deleted(self, company_id: StrObjectId) -> List[RecordatorioCategoria]:
        return await self.inner.list_deleted(company_id)

    async def rename(self, category: RecordatorioCategoria, name: str) -> None:
        await self.inner.rename(category, name)
        await self.assets.invalidate(category.id, category.company_id)

    async def delete(self, category: RecordatorioCategoria) -> None:
        # Read once more through the cache, as the asset service's delete did, and invalidate what it read.
        before = await self.get(category.id)
        await self.inner.delete(before)
        await self.assets.invalidate(before.id, before.company_id)
