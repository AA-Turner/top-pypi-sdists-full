"""`TopicRepository` on the `topics` collection: a catalog read by id (`MongoCatalogByIdWithPreviews`) plus saving the lock state.
Only Mongo: the cache is a decorator (ADR-001)."""
from __future__ import annotations

from typing import Any, Dict

from ...models.analytics.smart_messages.topic import Topic
from ...services.chatty_assets.collections.topic_collection import TopicCollection
from ..catalog_repository import MongoCatalogByIdWithPreviews


class MongoTopicRepository(MongoCatalogByIdWithPreviews[Topic]):
    """Reuses `TopicCollection`, so the stored document keeps exactly the shape the smart messages read."""

    collection: TopicCollection

    def preview_projection(self) -> Dict[str, Any]:
        return Topic.preview_class.get_projection()

    async def save_messages(self, topic: Topic) -> None:
        await self.collection.update_fields(topic, {"messages"})
