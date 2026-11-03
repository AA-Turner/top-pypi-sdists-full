"""`AiComponentRepository` on the `ai_components` collection.

Not a simple catalog (ADR-010 of api-chatty): the component is polymorphic and the list skips a document it cannot
read. It reuses the catalog base for what is the same (read by id, merge on update, mark deleted, add) and
`AiComponentCollection`, so the stored document keeps exactly the shape CINTIA reads and writes.
"""
from __future__ import annotations

import logging
from typing import List

from ...models.base_models.ai_agent_component import AiAgentComponent, AiAgentComponentType
from ...models.utils.types import StrObjectId
from ...services.chatty_assets.collections.ai_component_collection import AiComponentCollection
from ..catalog_repository import MongoCatalogRepository

# The legacy service's logger: alerts and searches read `[AI_COMPONENT_ILEGIBLE]` from it.
logger = logging.getLogger("AiComponents")


class MongoAiComponentRepository(MongoCatalogRepository[AiAgentComponent]):
    collection: AiComponentCollection

    async def list_live(self, company_id: StrObjectId) -> List[AiAgentComponent]:
        """One by one: an unreadable document does not take the whole list down (incident 2026-10-06: a strategy with
        an area that no longer existed left CONTAINER's list of AI components in 400)."""
        docs = await self.collection.collection.find(
            filter={"company_id": company_id, "deleted_at": None}
        ).to_list(None)
        items: List[AiAgentComponent] = []
        for doc in docs:
            try:
                items.append(self.collection.create_instance(doc))
            except Exception as e:
                logger.error(
                    "[AI_COMPONENT_ILEGIBLE] company_id=%s id=%s type=%s — se saltea de la lista: %s",
                    company_id, doc.get("_id"), doc.get("type"), e,
                )
        return items

    async def delete_test_cases_of_chat_example(self, company_id: StrObjectId, chat_example_id: StrObjectId) -> None:
        # Not filtered by company, as before (ADR-007 of api-chatty lists it).
        await self.collection.collection.delete_many(
            {"chat_example_id": chat_example_id, "type": AiAgentComponentType.TEST_CASE.value}
        )
