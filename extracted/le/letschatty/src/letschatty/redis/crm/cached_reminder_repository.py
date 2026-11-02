"""Redis cache in front of any `ReminderRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used: `recordatorios:item:{id}`. Adding and deleting also clear
`:previews:{company}`, `:all:{company}` and the global lists; a field change clears only the item (the asset service's
`partial_update`). The reads by chat and by date range are never cached. A cache failure never fails the request.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, List, Mapping, Optional

from ...models.company.assets.recordatorio import Recordatorio
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogById


class CachedReminderRepository(CachedCatalogById[Recordatorio]):
    """The base's read by id, add and delete (`CachedCatalogById`, ADR-010 of api-chatty), plus what is its own."""

    prefix = "recordatorios"
    item_type = Recordatorio

    async def of_chat(self, company_id: StrObjectId, chat_id: StrObjectId) -> List[Recordatorio]:
        return await self.inner.of_chat(company_id, chat_id)

    async def in_range(self, company_id: StrObjectId, since: Optional[datetime], until: Optional[datetime],
                       include_resolved: bool) -> List[Recordatorio]:
        return await self.inner.in_range(company_id, since, until, include_resolved)

    async def change(self, reminder_id: StrObjectId, fields: Mapping[str, Any]) -> None:
        await self.inner.change(reminder_id, fields)
        await self.assets.invalidate_item(reminder_id)
