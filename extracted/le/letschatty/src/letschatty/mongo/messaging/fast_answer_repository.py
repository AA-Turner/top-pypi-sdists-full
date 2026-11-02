"""`FastAnswerRepository` on the `fast_answers` collection: a catalog (`MongoCatalogWithPreviews`) whose `get` also checks
the company (ADR-007), plus the read of any company and saving the converted messages. Only Mongo: the cache is a
decorator (ADR-001)."""
from __future__ import annotations

from typing import Any, Dict

from ...domain.messaging.fast_answers import of_company
from ...models.company.assets.chatty_fast_answers.chatty_fast_answer import ChattyFastAnswer
from ...models.utils.types import StrObjectId
from ...services.chatty_assets.collections.fast_answer_collection import FastAnswerCollection
from ..catalog_repository import MongoCatalogWithPreviews


class MongoFastAnswerRepository(MongoCatalogWithPreviews[ChattyFastAnswer]):
    """Reuses `FastAnswerCollection`, so the stored document has exactly the shape CINTIA and copilot read."""

    collection: FastAnswerCollection

    def preview_projection(self) -> Dict[str, Any]:
        return ChattyFastAnswer.preview_class.get_projection()

    async def get(self, company_id: StrObjectId, fast_answer_id: StrObjectId) -> ChattyFastAnswer:
        # The module's own: another company's fast answer is not found (the base's `update` and `delete` read by this).
        return of_company(await self.get_any_company(fast_answer_id), company_id)

    async def get_any_company(self, fast_answer_id: StrObjectId) -> ChattyFastAnswer:
        """By id, whatever its company: the caller checks the company (ENG-73: `main` converts the audios first)."""
        return await self._read(fast_answer_id)

    async def save_messages(self, fast_answer: ChattyFastAnswer) -> None:
        await self.collection.update_fields(fast_answer, {"messages"})
