"""A chat's journey through a funnel (`chat_funnels`, ADR-012 §5 of api-chatty): its own aggregate, one document per
journey with its status (`in_progress` → `completed` | `abandoned`) and its stage transitions. company-billing-lambda,
campaigns-lambda and copilot read the collection, so the document keeps its shape.

The chat keeps the reference `chats.active_funnel`, which this port never writes: api-chatty writes it through its
`ChatRepository`, always after the journey. The pointer is the truth of where the chat is (a missing journey is rebuilt
from it with the same `_id`); the journey is the truth of the history.

`company_id` comes first. The reads by id do not filter by it (as `AssetService.get_by_id`); the lists filter by it, as
before. Writes are the asset service's: an insert as it comes, a save merged onto what is stored now, writing only the
fields the journey was built or changed with.
"""
from __future__ import annotations

from typing import Dict, List, Protocol

from ...models.company.CRM.funnel import ChatFunnel
from ...models.utils.types import StrObjectId


class ChatFunnelRepository(Protocol):
    async def get(self, company_id: StrObjectId, chat_funnel_id: StrObjectId) -> ChatFunnel:
        """The journey with that id, of any company. Raises `NotFoundError`."""
        ...

    async def insert(self, company_id: StrObjectId, chat_funnel: ChatFunnel) -> ChatFunnel: ...

    async def insert_if_missing(self, company_id: StrObjectId, chat_funnel: ChatFunnel) -> bool:
        """Inserts `chat_funnel` under its own id (a rebuild). False, writing nothing, when another request already put
        one there (the unique `_id`)."""
        ...

    async def save(self, company_id: StrObjectId, chat_funnel: ChatFunnel) -> ChatFunnel:
        """Merged onto what is stored now; only the fields `chat_funnel` was built or changed with are written, plus
        `updated_at`. Raises `NotFoundError` when it is not stored."""
        ...

    async def open_of_chat(self, company_id: StrObjectId, chat_id: StrObjectId) -> List[ChatFunnel]:
        """The chat's live journeys still `in_progress`. One that does not build is left out (and logged)."""
        ...

    async def open_of_funnel(self, company_id: StrObjectId, funnel_id: StrObjectId) -> List[ChatFunnel]:
        """The funnel's live journeys still `in_progress`."""
        ...

    async def history_of_chat(self, company_id: StrObjectId, chat_id: StrObjectId) -> List[ChatFunnel]:
        """Every live journey of the chat, newest first (`started_at`)."""
        ...

    async def count_by_status(self, company_id: StrObjectId, funnel_id: StrObjectId) -> Dict[str, int]:
        """`status -> count` of the funnel's live journeys (statuses without journeys are not there)."""
        ...
