"""Sale Collection - Pre-configured AssetCollection for Sales"""

from ..asset_service import AssetCollection
from ....models.company.assets.sale import Sale
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection


class SaleCollection(AssetCollection[Sale, ChattyAssetPreview]):
    """Pre-configured collection for Sale assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="sales",
            asset_type=Sale,
            connection=connection,
            create_instance_method=Sale.default_create_instance_method,
            preview_type=None
        )

