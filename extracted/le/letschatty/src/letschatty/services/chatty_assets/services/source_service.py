"""Source Service - Pre-configured AssetService for Sources"""

from ..asset_service import AssetService, CacheConfig
from ..collections import SourceCollection
from ....models.analytics.sources import SourceBase
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....models.analytics.events import CompanyAssetType, EventType


class SourceService(AssetService[SourceBase, ChattyAssetPreview]):
    """Pre-configured service for Source assets with sensible defaults"""

    # Event configuration - enables automatic event handling in API
    asset_type_enum = CompanyAssetType.SOURCES
    event_type_created = EventType.SOURCE_CREATED
    event_type_updated = EventType.SOURCE_UPDATED
    event_type_deleted = EventType.SOURCE_DELETED

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = CacheConfig()):
        collection = SourceCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

