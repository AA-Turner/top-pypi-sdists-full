"""Sale Service - Pre-configured AssetService for Sales"""

from ..asset_service import AssetService, CacheConfig
from ..collections import SaleCollection
from ....models.company.assets.sale import Sale
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection


class SaleService(AssetService[Sale, ChattyAssetPreview]):
    """
    Pre-configured service for Sale assets with sensible defaults.

    Note: No event configuration - Sale events are managed by the sales editor, not AssetService.
    """

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = CacheConfig.default()):
        collection = SaleCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

