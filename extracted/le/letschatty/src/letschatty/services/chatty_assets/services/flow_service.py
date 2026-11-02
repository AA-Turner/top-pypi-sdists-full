"""Flow Service - Pre-configured AssetService for Flows"""

from ..asset_service import AssetService, CacheConfig
from ..collections import FlowCollection
from ....models.company.assets.flow import FlowPreview
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection


class FlowService(AssetService[FlowPreview, ChattyAssetPreview]):
    """
    Pre-configured service for Flow assets with sensible defaults.

    Note: No event configuration - Flows are previews only, not full assets with CRUD events.
    """

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = CacheConfig()):
        collection = FlowCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

