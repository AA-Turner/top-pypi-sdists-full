"""Product Collection - Pre-configured AssetCollection for Products"""

from ..asset_service import AssetCollection
from ....models.company.assets.product import Product, ProductPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....services.factories.product_factory import ProductFactory


class ProductCollection(AssetCollection[Product, ProductPreview]):
    """Pre-configured collection for Product assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="products",
            asset_type=Product,
            connection=connection,
            create_instance_method=ProductFactory.create_product,
            preview_type=ProductPreview
        )

