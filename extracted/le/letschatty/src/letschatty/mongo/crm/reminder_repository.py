"""`ReminderRepository` on the `recordatorios` collection. Not a simple catalog (read by chat and by date range,
written field by field), but it shares the base's read by id, add and logical delete (`MongoCatalogById`). Only Mongo:
the cache is a decorator (ADR-001)."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional

from ...models.company.assets.recordatorio import Recordatorio
from ...models.utils.types import StrObjectId
from ..catalog_repository import MongoCatalogById


class MongoReminderRepository(MongoCatalogById[Recordatorio]):
    """Reuses the collection the asset service was built on, so the stored document keeps its shape (`remind_at` and
    `resolved_at` as dates: the agenda filters by range)."""

    async def of_chat(self, company_id: StrObjectId, chat_id: StrObjectId) -> List[Recordatorio]:
        return await self.collection.get_by_query(
            query={"company_id": str(company_id), "chat_id": str(chat_id), "deleted_at": None})

    async def in_range(self, company_id: StrObjectId, since: Optional[datetime], until: Optional[datetime],
                       include_resolved: bool) -> List[Recordatorio]:
        query: Dict[str, Any] = {"company_id": str(company_id), "deleted_at": None}
        if not include_resolved:
            query["resolved_at"] = None
        if since or until:
            window: Dict[str, Any] = {}
            if since:
                window["$gte"] = since
            if until:
                window["$lte"] = until
            query["remind_at"] = window
        return await self.collection.get_by_query(query=query)

    async def change(self, reminder_id: StrObjectId, fields: Mapping[str, Any]) -> None:
        await self.collection.partial_update(reminder_id, dict(fields))
