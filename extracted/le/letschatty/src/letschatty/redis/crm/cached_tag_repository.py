"""Redis cache in front of any `TagRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because both still run side by side and
other code reads them: `tags:item:{id}`, `tags:previews:{company}`, `tags:all:{company}` (and the global
`…:all` lists). Every write invalidates them; a cache failure never fails the request.
"""
from __future__ import annotations

from ...models.company.assets.tag import Tag
from ..cached_catalog_repository import CachedCatalogWithPreviews


class CachedTagRepository(CachedCatalogWithPreviews[Tag]):
    """A simple catalog's cache (`CachedCatalogWithPreviews`, ADR-010 of api-chatty)."""

    prefix = "tags"
    item_type = Tag
