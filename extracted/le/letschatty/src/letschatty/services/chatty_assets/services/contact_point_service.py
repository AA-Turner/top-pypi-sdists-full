"""Contact Point Service - Pre-configured AssetService for Contact Points"""

from ..asset_service import AssetService, CacheConfig
from ..collections import ContactPointCollection
from ....models.company.assets.contact_point import ContactPoint
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection


class ContactPointService(AssetService[ContactPoint, ChattyAssetPreview]):
    """
    Pre-configured service for ContactPoint assets with sensible defaults.

    Note: No event configuration - ContactPoint events are managed separately by the contact points system.
    """

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = None):
        collection = ContactPointCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

