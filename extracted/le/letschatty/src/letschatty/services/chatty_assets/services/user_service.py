"""User Service - Pre-configured AssetService for Users"""

from ..asset_service import AssetService, CacheConfig
from ..collections import UserCollection
from ....models.company.assets.users.user import User, UserPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....models.analytics.events import CompanyAssetType, EventType


class UserService(AssetService[User, UserPreview]):
    """Pre-configured service for User assets with sensible defaults"""

    # Event configuration - enables automatic event handling in API
    asset_type_enum = CompanyAssetType.USERS
    event_type_created = EventType.USER_CREATED
    event_type_updated = EventType.USER_UPDATED
    event_type_deleted = EventType.USER_DELETED

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = None):
        collection = UserCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

