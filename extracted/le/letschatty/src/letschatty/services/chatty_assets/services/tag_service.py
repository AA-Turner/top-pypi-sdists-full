"""Tag Service - Pre-configured AssetService for Tags"""

from ..asset_service import AssetService, CacheConfig
from ..collections import TagCollection
from ....models.company.assets.tag import Tag, TagPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....models.analytics.events import CompanyAssetType, EventType


class TagService(AssetService[Tag, TagPreview]):
    """Pre-configured service for Tag assets with sensible defaults"""

    # Event configuration - enables automatic event handling in API
    asset_type_enum = CompanyAssetType.TAGS
    event_type_created = EventType.TAG_CREATED
    event_type_updated = EventType.TAG_UPDATED
    event_type_deleted = EventType.TAG_DELETED

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = CacheConfig()):
        collection = TagCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )
        # Load all tags into memory by default
        self.load_from_db(company_id=None)

