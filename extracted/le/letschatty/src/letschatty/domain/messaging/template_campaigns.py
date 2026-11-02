"""Template campaigns («campañas de plantilla»): the port every store of them implements.

A campaign is one template sent to a list of recipients, kept as one document with its recipients inside. The entity is
`letschatty.models.messages.message_templates.chatty_template_campaign.TemplateCampaign`, unchanged: the stored document
keeps its shape. This is the catalog of campaigns only: its lock, its heartbeat and the loop that sends are not part of
it. A read by the row's own id (`get`) is not scoped to a company: whoever calls it checks that (ADR-007; ENG-10 where
it does not yet).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Protocol

from ...models.messages.message_templates.chatty_template_campaign import TemplateCampaign
from ...models.utils.types import StrObjectId


class TemplateCampaignRepository(Protocol):
    """Raises `NotFoundError` when no row has that id."""

    async def get(self, company_id: StrObjectId, campaign_id: StrObjectId) -> TemplateCampaign:
        """By the row's id, whatever its company, also a deleted one."""
        ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """Live rows of the company, newest first, as JSON-ready preview dicts."""
        ...

    async def list_created_since(self, company_id: StrObjectId, since: datetime) -> List[TemplateCampaign]:
        """The company's rows created at or after `since`, deleted ones included. Always read from the store."""
        ...

    async def add(self, campaign: TemplateCampaign) -> TemplateCampaign:
        ...

    async def save(self, campaign: TemplateCampaign) -> None:
        """Writes the whole document and stamps `updated_at` on `campaign`. It does not touch any cache."""
        ...
