"""`ReminderCategoryRepository` on the `recordatorio_categorias` collection. Not a simple catalog (it renames and its
delete takes the category), but it shares the base's add, live list and restore (`MongoCatalogBase`). Only Mongo: the
cache is a decorator (ADR-001)."""
from __future__ import annotations

from typing import List

from ...models.company.assets.recordatorio_categoria import RecordatorioCategoria
from ...models.utils.types import StrObjectId
from ..catalog_repository import MongoCatalogBase


class MongoReminderCategoryRepository(MongoCatalogBase[RecordatorioCategoria]):
    """Reuses the collection the asset service was built on, so the stored document keeps its shape."""

    async def get(self, category_id: StrObjectId) -> RecordatorioCategoria:
        return await self._read(category_id)

    async def list_deleted(self, company_id: StrObjectId) -> List[RecordatorioCategoria]:
        return await self.collection.get_docs(company_id=company_id, query={"deleted_at": {"$ne": None}})

    async def rename(self, category: RecordatorioCategoria, name: str) -> None:
        await self.collection.partial_update(category.id, {"name": name})

    async def delete(self, category: RecordatorioCategoria) -> None:
        await self.mark_deleted(category.id)
