"""Flow Collection - Pre-configured AssetCollection for Flows"""

from ..asset_service import AssetCollection
from ....models.company.assets.flow import FlowPreview
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection


class FlowCollection(AssetCollection[FlowPreview, ChattyAssetPreview]):
    """Pre-configured collection for Flow assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="flows",
            asset_type=FlowPreview,
            connection=connection,
            create_instance_method=FlowPreview.default_create_instance_method,
            preview_type=None
        )

