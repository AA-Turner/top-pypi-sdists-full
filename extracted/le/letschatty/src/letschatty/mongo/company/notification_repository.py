"""`NotificationRepository` on the `notifications` collection: a catalog read by id (`MongoCatalogByIdWithPreviews`: a global
notification is every company's). Only Mongo: the cache is a decorator (ADR-001)."""
from __future__ import annotations

from typing import Any, Dict

from ...models.company.assets.notification import Notification, NotificationPreview
from ..catalog_repository import MongoCatalogByIdWithPreviews


class MongoNotificationRepository(MongoCatalogByIdWithPreviews[Notification]):
    """Reuses the collection of the asset service, so the stored document keeps its shape."""

    def preview_projection(self) -> Dict[str, Any]:
        return NotificationPreview.get_projection()
