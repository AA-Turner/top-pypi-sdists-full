"""Redis cache in front of any `FastAnswerRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because both still run side by side and other
code reads them: `fast_answers:item:{id}`, `fast_answers:previews:{company}`, `fast_answers:all:{company}`
(and the global `…:all` lists). TTLs come from the caller. Adding, editing and deleting invalidate them; saving the
converted messages does not, as in `main` (ENG-72). A cache failure never fails the request. A cached item of another
company is not served by `get` (`of_company`).
"""
from __future__ import annotations

from ...domain.messaging.fast_answers import of_company
from ...models.company.assets.chatty_fast_answers.chatty_fast_answer import ChattyFastAnswer
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogWithPreviews


class CachedFastAnswerRepository(CachedCatalogWithPreviews[ChattyFastAnswer]):
    """A catalog's cache (`CachedCatalogWithPreviews`, ADR-010 of api-chatty) whose `get` checks the company."""

    prefix = "fast_answers"
    item_type = ChattyFastAnswer

    async def get(self, company_id: StrObjectId, fast_answer_id: StrObjectId) -> ChattyFastAnswer:
        # As the asset service did: read by id whatever the company, cache it, and only then check the company. Another
        # company's fast answer is left in the cache and is still not found (differential QA of 2026-10-30).
        return of_company(await self.get_any_company(fast_answer_id), company_id)

    async def get_any_company(self, fast_answer_id: StrObjectId) -> ChattyFastAnswer:
        return await self.assets.item(fast_answer_id, lambda: self.inner.get_any_company(fast_answer_id))

    async def save_messages(self, fast_answer: ChattyFastAnswer) -> None:
        # As in `main` (`collection.update_fields` straight on Mongo): the converted messages clear nothing, so a cached
        # copy keeps the old audio until its TTL and is converted again on read (at most every 300 s per process).
        await self.inner.save_messages(fast_answer)
