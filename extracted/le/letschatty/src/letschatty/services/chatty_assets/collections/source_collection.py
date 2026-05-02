"""Source Collection - Pre-configured AssetCollection for Sources"""

from ..asset_service import AssetCollection
from ....models.analytics.sources import SourceBase
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....services.factories.analytics.sources.source_factory import SourceFactory


class SourceCollection(AssetCollection[SourceBase, ChattyAssetPreview]):
    """Pre-configured collection for Source assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="sources",
            asset_type=SourceBase,
            connection=connection,
            create_instance_method=SourceFactory.instantiate_source,
            preview_type=None
        )

