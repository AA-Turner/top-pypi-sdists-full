"""FastAnswer Collection - Pre-configured AssetCollection for Fast Answers"""

from ..asset_service import AssetCollection
from ....models.company.assets import ChattyFastAnswer
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection
from ...factories.chatty_fast_answers.chatty_fast_answers_factory import ChattyFastAnswersFactory


class FastAnswerCollection(AssetCollection[ChattyFastAnswer, ChattyAssetPreview]):
    """Pre-configured collection for Fast Answer assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="fast_answers",
            asset_type=ChattyFastAnswer,
            connection=connection,
            create_instance_method=ChattyFastAnswersFactory.create,
            preview_type=ChattyAssetPreview
        )

