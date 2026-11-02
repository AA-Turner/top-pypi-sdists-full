"""Redis cache in front of any `FormFieldRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because other code may still read them:
`form_fields:item:{id}`, `form_fields:all:{company}`, `form_fields:previews:{company}` (and the global `…:all` lists),
24 h by default. Adding, editing and deleting an own field invalidate them; a cache failure never fails the request.
Customizations of system fields do NOT invalidate (ENG-62): kept as it was.
"""
from __future__ import annotations

from ...models.company.form_field import FormField
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogRepository


class CachedFormFieldRepository(CachedCatalogRepository[FormField]):
    """A simple catalog's cache (`CachedCatalogRepository`, ADR-010 of api-chatty), listed whole."""

    prefix = "form_fields"
    item_type = FormField

    async def add_customization(self, customization: FormField) -> None:
        await self.inner.add_customization(customization)  # ENG-62: no invalidation

    async def replace_customization(self, customization: FormField) -> None:
        await self.inner.replace_customization(customization)  # ENG-62: no invalidation

    async def remove_customization(self, company_id: StrObjectId, customization_id: StrObjectId) -> None:
        await self.inner.remove_customization(company_id, customization_id)  # ENG-62: no invalidation
