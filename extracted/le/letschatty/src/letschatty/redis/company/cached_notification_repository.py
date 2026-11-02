"""Redis cache in front of any `NotificationRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because both still run side by side:
`notifications:item:{id}`, `notifications:all:{company}` (the lists of the home screen, also `…:all:000…` for the
global ones), `notifications:previews:{company}` (the global list of the backoffice) and the global `…:all` lists.
Every write invalidates them; a cache failure never fails the request.
"""
from __future__ import annotations

from ...models.company.assets.notification import Notification
from ..cached_catalog_repository import CachedCatalogByIdWithPreviews


class CachedNotificationRepository(CachedCatalogByIdWithPreviews[Notification]):
    """A catalog's cache read by id (`CachedCatalogByIdWithPreviews`, ADR-010 of api-chatty)."""

    prefix = "notifications"
    item_type = Notification
