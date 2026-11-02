"""The Mongo repository of a catalog (ADR-010 of api-chatty): one asset type in one collection, read by id, listed by
company, merged on update, marked deleted on delete and, where the module restores, restored.

Every catalog wrote these same methods; they live here once (ENG-82). Each module only names its collection and its
preview projection, and adds what is its own. Two flavors of the same code, which differ only in what the port's
`get`/`update`/`delete` receive:

- `MongoCatalogRepository`: `get(company_id, item_id)` (ADR-007: the company the caller asks from, which the
  repository ignores; the use case checks it). Tags, products, filter criteria, form fields, saved Meta templates and
  fast answers (whose `get` also checks it, ADR-007).
- `MongoCatalogById`: `get(item_id)`, for the catalogs whose ports read by id alone: notifications (a global one is
  every company's), topics and funnels and their stages.

A catalog listed by its previews takes the `…WithPreviews` of its flavor; one that is not (form fields, reminder
categories) has no `list_previews` at all.

Both run exactly the same Mongo operations. Only Mongo: the cache is a decorator (ADR-001), `CachedCatalogRepository`.
"""
from __future__ import annotations

from typing import Any, Dict, Generic, List, TypeVar

from ..models.utils.types import StrObjectId

T = TypeVar("T")


class MongoCatalogBase(Generic[T]):
    """What both flavors share. Reuses the module's asset collection, so the stored document has exactly the shape other
    services read."""

    def __init__(self, collection):
        self.collection = collection

    async def _read(self, item_id: StrObjectId) -> T:
        # Not filtered by company: the use case checks it (ADR-007, ENG-10).
        return await self.collection.get_by_id(item_id)

    async def _merge(self, existing: T, changes: T) -> T:
        """Merged onto what is in Mongo now, writing only what was sent (`UpdateableMixin.merge`, `update_fields`)."""
        merged, sent_fields = existing.merge(changes)
        await self.collection.update_fields(merged, sent_fields)
        return merged

    async def add(self, item: T) -> T:
        await self.collection.insert(item)
        return item

    async def mark_deleted(self, item_id: StrObjectId) -> None:
        """Only the write: for the cache decorator, which already read it through the cache."""
        await self.collection.delete(item_id)

    async def list_live(self, company_id: StrObjectId) -> List[T]:
        return await self.collection.get_docs(company_id=company_id, query={"deleted_at": None})

    async def restore(self, item_id: StrObjectId) -> T:
        """Read by id, `deleted_at` cleared and written whole (`collection.update`, which stamps `updated_at`), as the
        asset services did."""
        item = await self.collection.get_by_id(item_id)
        item.deleted_at = None
        await self.collection.update(item)
        return item


class MongoCatalogRepository(MongoCatalogBase[T]):
    async def get(self, company_id: StrObjectId, item_id: StrObjectId) -> T:
        return await self._read(item_id)

    async def update(self, company_id: StrObjectId, item_id: StrObjectId, changes: T) -> T:
        return await self._merge(await self.get(company_id, item_id), changes)

    async def delete(self, company_id: StrObjectId, item_id: StrObjectId) -> T:
        existing = await self.get(company_id, item_id)
        await self.mark_deleted(item_id)
        return existing


class _Previews:
    """A catalog whose list is its previews: the module says its projection (`preview_projection`). Only the flavors
    that have one carry `list_previews` (form fields and reminder categories list their live items)."""

    def preview_projection(self) -> Dict[str, Any]:
        raise NotImplementedError

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        previews = await self.collection.get_preview_docs(
            projection=self.preview_projection(), all=False, company_id=company_id
        )
        return [preview.model_dump(mode="json") for preview in previews]


class MongoCatalogWithPreviews(_Previews, MongoCatalogRepository[T]):
    """By company, listed by its previews: tags, products, filter criteria, saved Meta templates, fast answers."""


class MongoCatalogById(MongoCatalogBase[T]):
    async def get(self, item_id: StrObjectId) -> T:
        return await self._read(item_id)

    async def update(self, item_id: StrObjectId, changes: T) -> T:
        return await self._merge(await self.get(item_id), changes)

    async def delete(self, item_id: StrObjectId) -> T:
        existing = await self.get(item_id)
        await self.mark_deleted(item_id)
        return existing


class MongoCatalogByIdWithPreviews(_Previews, MongoCatalogById[T]):
    """By id, listed by its previews: notifications, topics, funnels and their stages."""
