"""Tags of a company's catalog: the port every tag store implements.

The entity is `letschatty.models.company.assets.tag.Tag`, unchanged: other services (CINTIA, copilot,
campaigns) import it. Assigning a tag to a chat is a rule of the chat (`ChatService.add_tag`), not of
the catalog.

Every method takes the company; the repository does not filter by it. Per ADR-007, the use case checks
the company with a shared helper (`of_the_company` in api-chatty), and ENG-10 will be fixed there.
"""
from __future__ import annotations

from typing import Any, Dict, List, Protocol

from ...models.company.assets.tag import Tag
from ...models.utils.types import StrObjectId


class TagRepository(Protocol):
    """Raises `NotFoundError` when the tag does not exist."""

    async def get(self, company_id: StrObjectId, tag_id: StrObjectId) -> Tag: ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """Live tags of the company, newest first, as JSON-ready preview dicts."""
        ...

    async def add(self, tag: Tag) -> Tag: ...

    async def update(self, company_id: StrObjectId, tag_id: StrObjectId, changes: Tag) -> Tag:
        """Writes only the fields `changes` was built with; the rest stays as stored."""
        ...

    async def delete(self, company_id: StrObjectId, tag_id: StrObjectId) -> Tag:
        """Marks the tag deleted (the document stays) and returns it as it was before."""
        ...
