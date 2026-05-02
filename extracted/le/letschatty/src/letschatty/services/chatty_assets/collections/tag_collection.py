"""Tag Collection - Pre-configured AssetCollection for Tags"""

from ..asset_service import AssetCollection
from ....models.company.assets.tag import Tag, TagPreview
from ....models.data_base.mongo_connection import MongoConnection


class TagCollection(AssetCollection[Tag, TagPreview]):
    """Pre-configured collection for Tag assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="tags",
            asset_type=Tag,
            connection=connection,
            create_instance_method=Tag.default_create_instance_method,
            preview_type=TagPreview
        )

