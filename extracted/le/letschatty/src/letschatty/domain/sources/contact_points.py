"""Contact points («puntos de contacto», touchpoints): the port every contact point store implements.

A contact point is its own aggregate (collection `contact_points`): where a person came from before writing (an ad,
a link, a pixel click, a template). The chat keeps only a reference to it (`chat.contact_points`), which is the chat
aggregate's. The entity is `letschatty.models.company.assets.contact_point.ContactPoint`, unchanged. A read by id is
NOT scoped to a company: the use case checks the company where the caller asks for it (ADR-007 of api-chatty).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol

from ...models.company.assets.contact_point import ContactPoint
from ...models.utils.types import StrObjectId


class ContactPointRepository(Protocol):
    """Raises `NotFoundError` when no contact point has that id."""

    async def get(self, contact_point_id: StrObjectId) -> ContactPoint:
        """By id, whatever its company, also a deleted one."""
        ...

    async def get_fresh(self, contact_point_id: StrObjectId) -> ContactPoint:
        """The same, read from the store now (a cache in front keeps the answer for the next read)."""
        ...

    async def list_live(self, company_id: StrObjectId) -> List[ContactPoint]: ...

    async def of_source(self, company_id: Optional[StrObjectId], source_id: StrObjectId) -> List[ContactPoint]:
        """Every one attributed to the source (deleted ones too), of the company if one is given."""
        ...

    async def of_chat(self, company_id: Optional[StrObjectId], chat_id: StrObjectId) -> List[ContactPoint]:
        """Every one of the chat (deleted ones too), of the company if one is given."""
        ...

    async def has_live_of_another_source(self, chat_id: StrObjectId, contact_point_id: StrObjectId,
                                         source_id: Optional[StrObjectId]) -> bool:
        """Whether the chat has a live one other than `contact_point_id`, on a source other than `source_id` (any
        source when it is None)."""
        ...

    async def add(self, contact_point: ContactPoint) -> ContactPoint: ...

    async def update(self, contact_point_id: StrObjectId, changes: ContactPoint) -> ContactPoint:
        """Writes only the fields `changes` was built with, merged onto what is in the store now."""
        ...

    async def set_ad_creative(self, contact_point_id: StrObjectId, ad_creative: Dict[str, Any]) -> None:
        """Writes only `ad_creative` (and `updated_at`): the creative Meta served in this referral, mirrored. Never the
        whole document, so it cannot overwrite what the attribution writes at the same time. `NotFoundError` if the
        contact point is not there."""
        ...

    async def delete(self, contact_point_id: StrObjectId) -> ContactPoint:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...
