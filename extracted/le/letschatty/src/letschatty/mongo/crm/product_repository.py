"""`ProductRepository` on the `products` collection: a simple catalog (`MongoCatalogWithPreviews`)."""
from __future__ import annotations

from typing import Any, Dict

from ...models.company.assets.product import Product
from ...services.chatty_assets.collections.product_collection import ProductCollection
from ..catalog_repository import MongoCatalogWithPreviews


class MongoProductRepository(MongoCatalogWithPreviews[Product]):
    """Reuses `ProductCollection`, so the stored document has exactly the shape products-lambda and the
    other services read."""

    collection: ProductCollection

    def preview_projection(self) -> Dict[str, Any]:
        return Product.preview_class.get_projection()
