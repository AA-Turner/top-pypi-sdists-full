"""`TagRepository` on the `tags` collection: a simple catalog (`MongoCatalogWithPreviews`)."""
from __future__ import annotations

from typing import Any, Dict

from ...models.company.assets.tag import Tag
from ...services.chatty_assets.collections.tag_collection import TagCollection
from ..catalog_repository import MongoCatalogWithPreviews


class MongoTagRepository(MongoCatalogWithPreviews[Tag]):
    """Reuses `TagCollection`, so the stored document has exactly the shape other services read."""

    collection: TagCollection

    def preview_projection(self) -> Dict[str, Any]:
        return Tag.preview_class.get_projection()
