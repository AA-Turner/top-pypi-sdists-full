"""Redis cache in front of any `TopicRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because the legacy `Topics` service still serves the
smart-message readers on the same keys: `topics:item:{id}`, `topics:previews:{company}`, `topics:all:{company}` (and the
global `…:all` lists). The item key uses the id as it was asked for, as before. Adding, editing, saving the lock state
and deleting invalidate them (ADR-006, `AssetCache`). A cache failure never fails the request.
"""
from __future__ import annotations

from ...models.analytics.smart_messages.topic import Topic
from ..cached_catalog_repository import CachedCatalogByIdWithPreviews


class CachedTopicRepository(CachedCatalogByIdWithPreviews[Topic]):
    """A catalog's cache read by id (`CachedCatalogByIdWithPreviews`, ADR-010 of api-chatty) plus saving the lock state."""

    prefix = "topics"
    item_type = Topic

    async def save_messages(self, topic: Topic) -> None:
        await self.inner.save_messages(topic)
        await self.assets.invalidate(topic.id, topic.company_id)
