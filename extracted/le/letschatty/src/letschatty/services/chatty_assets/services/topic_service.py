"""Topic Service - Pre-configured AssetService for Topics"""

from ..asset_service import AssetService, CacheConfig
from ..collections.topic_collection import TopicCollection
from ....models.analytics.smart_messages.topic import Topic
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....models.analytics.events import CompanyAssetType, EventType


class TopicService(AssetService[Topic, ChattyAssetPreview]):
    """Pre-configured service for Topic assets with sensible defaults"""

    # Event configuration - enables automatic event handling in API
    asset_type_enum = CompanyAssetType.TOPICS
    event_type_created = EventType.TOPIC_CREATED
    event_type_updated = EventType.TOPIC_UPDATED
    event_type_deleted = EventType.TOPIC_DELETED

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = CacheConfig()):
        collection = TopicCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

