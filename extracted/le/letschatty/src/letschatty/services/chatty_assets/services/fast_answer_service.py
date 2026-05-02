"""Fast Answer Service - Pre-configured AssetService for Fast Answers"""

from ..asset_service import AssetService, CacheConfig
from ..collections.fast_answer_collection import FastAnswerCollection
from ....models.company.assets import ChattyFastAnswer
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....models.analytics.events import CompanyAssetType, EventType


class FastAnswerService(AssetService[ChattyFastAnswer, ChattyAssetPreview]):
    """Pre-configured service for Fast Answer assets with sensible defaults"""

    # Event configuration - enables automatic event handling in API
    asset_type_enum = CompanyAssetType.FAST_ANSWERS
    event_type_created = EventType.FAST_ANSWER_CREATED
    event_type_updated = EventType.FAST_ANSWER_UPDATED
    event_type_deleted = EventType.FAST_ANSWER_DELETED

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = None):
        collection = FastAnswerCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

