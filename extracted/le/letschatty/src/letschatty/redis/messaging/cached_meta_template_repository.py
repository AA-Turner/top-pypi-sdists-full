"""Redis cache in front of any `MetaTemplateRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used: `meta_templates:item:{id}`,
`meta_templates:previews:{company}`, `meta_templates:all:{company}` (and the global `…:all` lists). The reads by Meta's
id never went through the cache and still do not. Adding, editing, deleting and restoring invalidate the keys; moving a
row to another WABA does not, as before (the `update` that always follows does).
"""
from __future__ import annotations

from typing import Optional

from ...models.messages.message_templates.meta_template import MetaTemplate
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogWithPreviews


class CachedMetaTemplateRepository(CachedCatalogWithPreviews[MetaTemplate]):
    """A simple catalog's cache (`CachedCatalogWithPreviews`, ADR-010 of api-chatty) plus what is the module's own."""

    prefix = "meta_templates"
    item_type = MetaTemplate

    async def get_live(self, company_id: StrObjectId, meta_template_id: str) -> Optional[MetaTemplate]:
        return await self.inner.get_live(company_id, meta_template_id)

    async def get_any(self, company_id: StrObjectId, meta_template_id: str) -> Optional[MetaTemplate]:
        return await self.inner.get_any(company_id, meta_template_id)

    async def move_to_waba(self, template_id: StrObjectId, waba_id: str) -> None:
        await self.inner.move_to_waba(template_id, waba_id)
