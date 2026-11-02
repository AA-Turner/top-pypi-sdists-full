"""Redis cache in front of any `ProductRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because both still run side by side and
other code reads them: `products:item:{id}`, `products:previews:{company}`, `products:all:{company}`
(and the global `…:all` lists). TTLs come from the caller (1 h for products: products-lambda writes Mongo
directly). Every write invalidates them; a cache failure never fails the request.
"""
from __future__ import annotations

from ...models.company.assets.product import Product
from ..cached_catalog_repository import CachedCatalogWithPreviews


class CachedProductRepository(CachedCatalogWithPreviews[Product]):
    """A simple catalog's cache (`CachedCatalogWithPreviews`, ADR-010 of api-chatty)."""

    prefix = "products"
    item_type = Product
