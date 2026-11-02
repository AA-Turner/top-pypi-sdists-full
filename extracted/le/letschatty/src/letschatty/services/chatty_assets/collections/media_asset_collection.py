"""MediaAsset Collection - Pre-configured AssetCollection for the media library"""

from ..asset_service import AssetCollection
from ....models.company.assets import MediaAsset, MediaAssetPreview
from ....models.data_base.mongo_connection import MongoConnection


class MediaAssetCollection(AssetCollection[MediaAsset, MediaAssetPreview]):
    """Pre-configured collection for media library assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="media_assets",
            asset_type=MediaAsset,
            connection=connection,
            create_instance_method=MediaAsset.default_create_instance_method,
            preview_type=MediaAssetPreview
        )
