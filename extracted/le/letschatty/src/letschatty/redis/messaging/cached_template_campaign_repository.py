"""Redis cache in front of any `TemplateCampaignRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, with the collection's own name:
`template_campaigns_:item:{id}`, `template_campaigns_:previews:{company}`, `template_campaigns_:all:{company}` (and the
global `…:all` lists). Adding invalidates them. The list by creation date never went through the cache and still does
not, and neither does the write of the whole document, which leaves the cached copies as they were (a bug kept, as before).
"""
from __future__ import annotations

from datetime import datetime
from typing import List

from ...models.messages.message_templates.chatty_template_campaign import TemplateCampaign
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogWithPreviews


class CachedTemplateCampaignRepository(CachedCatalogWithPreviews[TemplateCampaign]):
    """A simple catalog's cache (`CachedCatalogWithPreviews`, ADR-010 of api-chatty) plus what is the module's own."""

    prefix = "template_campaigns_"
    item_type = TemplateCampaign

    async def list_created_since(self, company_id: StrObjectId, since: datetime) -> List[TemplateCampaign]:
        return await self.inner.list_created_since(company_id, since)

    async def save(self, campaign: TemplateCampaign) -> None:
        await self.inner.save(campaign)
