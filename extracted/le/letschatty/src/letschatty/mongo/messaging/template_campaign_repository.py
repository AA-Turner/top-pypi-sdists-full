"""`TemplateCampaignRepository` on the `template_campaigns_` collection: a simple catalog (`MongoCatalogWithPreviews`) plus
the list by creation date and the write of the whole document."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from ...models.messages.message_templates.chatty_template_campaign import TemplateCampaign, TemplateCampaignPreview
from ...models.utils.types import StrObjectId
from ..catalog_repository import MongoCatalogWithPreviews


class MongoTemplateCampaignRepository(MongoCatalogWithPreviews[TemplateCampaign]):
    """Reuses the asset collection of the legacy `TemplateCampaigns` service, so the stored document keeps exactly the
    shape (and the types: `date` as text) that the campaign loop and the status refresh write and read."""

    def preview_projection(self) -> Dict[str, Any]:
        return TemplateCampaignPreview.get_projection()

    async def list_created_since(self, company_id: StrObjectId, since: datetime) -> List[TemplateCampaign]:
        return await self.collection.get_docs(query={"created_at": {"$gte": since}}, company_id=company_id)

    async def save(self, campaign: TemplateCampaign) -> None:
        await self.collection.update(campaign)
