"""Topic Collection - Pre-configured AssetCollection for Topics"""

from ..asset_service import AssetCollection
from ....models.analytics.smart_messages.topic import Topic
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection
from ...factories.analytics.smart_messages.topics_factory import TopicFactory


class TopicCollection(AssetCollection[Topic, ChattyAssetPreview]):
    """Pre-configured collection for Topic assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="topics",
            asset_type=Topic,
            connection=connection,
            create_instance_method=TopicFactory.instantiate_topic,
            preview_type=ChattyAssetPreview
        )

