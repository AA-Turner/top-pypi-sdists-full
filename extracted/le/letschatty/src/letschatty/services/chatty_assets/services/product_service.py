"""Product Service - Pre-configured AssetService for Products"""

from ..asset_service import AssetService, CacheConfig
from ..collections import ProductCollection
from ....models.company.assets.product import Product, ProductPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....models.analytics.events import CompanyAssetType, EventType


class ProductService(AssetService[Product, ProductPreview]):
    """Pre-configured service for Product assets with sensible defaults"""

    # Event configuration - enables automatic event handling in API
    asset_type_enum = CompanyAssetType.PRODUCTS
    event_type_created = EventType.PRODUCT_CREATED
    event_type_updated = EventType.PRODUCT_UPDATED
    event_type_deleted = EventType.PRODUCT_DELETED

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = CacheConfig()):
        collection = ProductCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

