"""Reminders of a company («recordatorios»): the port every reminder store implements.

The entity is `letschatty.models.company.assets.recordatorio.Recordatorio`, unchanged. A reminder may hang on a chat
or not (a loose one); who sees it and whose it is are decided by api-chatty's use cases (`docs/crm/recordatorios.md`),
because they depend on the chat and on the person asking.

Not a simple catalog: it is read by chat and by date range, and written field by field (ADR-010 of api-chatty).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, List, Mapping, Optional, Protocol

from ...models.company.assets.recordatorio import Recordatorio
from ...models.utils.types import StrObjectId


class ReminderRepository(Protocol):
    async def get(self, reminder_id: StrObjectId) -> Recordatorio:
        """Of any company, also a deleted one. Raises `NotFoundError` (and `InvalidId` for a malformed id)."""
        ...

    async def of_chat(self, company_id: StrObjectId, chat_id: StrObjectId) -> List[Recordatorio]:
        """The live ones of the chat, resolved included, in no order. Never from a cache."""
        ...

    async def in_range(self, company_id: StrObjectId, since: Optional[datetime], until: Optional[datetime],
                       include_resolved: bool) -> List[Recordatorio]:
        """The live ones of the company due between `since` and `until` (both included; a missing end is open), in no
        order; without the resolved ones unless asked. Never from a cache."""
        ...

    async def add(self, reminder: Recordatorio) -> Recordatorio: ...

    async def change(self, reminder_id: StrObjectId, fields: Mapping[str, Any]) -> None:
        """Writes only `fields` (and `updated_at`). Raises `NotFoundError` if the reminder is gone."""
        ...

    async def delete(self, reminder_id: StrObjectId) -> Recordatorio:
        """Marks it deleted; the document stays. Returns it as it was."""
        ...
