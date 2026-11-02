"""Redis cache in front of any `FilterCriteriaRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because both still run side by side and
other code reads them (the AI readers, the enricher): `filter_criterias:item:{id}`,
`filter_criterias:previews:{company}`, `filter_criterias:all:{company}` (and the global `…:all` lists), TTL from the
caller (24 h). Every write invalidates them; a cache failure never fails the request. CINTIA writes the collection
straight to Mongo and invalidates nothing: what it writes is seen when the keys expire.
"""
from __future__ import annotations

from ...models.company.assets.filter_criteria import FilterCriteria
from ..cached_catalog_repository import CachedCatalogWithPreviews


class CachedFilterCriteriaRepository(CachedCatalogWithPreviews[FilterCriteria]):
    """A simple catalog's cache (`CachedCatalogWithPreviews`, ADR-010 of api-chatty)."""

    prefix = "filter_criterias"
    item_type = FilterCriteria
