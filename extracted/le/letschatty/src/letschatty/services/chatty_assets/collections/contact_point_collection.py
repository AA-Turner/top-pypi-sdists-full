"""Contact Point Collection - Pre-configured AssetCollection for Contact Points"""

from ..asset_service import AssetCollection
from ....models.company.assets.contact_point import ContactPoint
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....services.factories.analytics.contact_point_factory import ContactPointFactory


class ContactPointCollection(AssetCollection[ContactPoint, ChattyAssetPreview]):
    """Pre-configured collection for ContactPoint assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="contact_points",
            asset_type=ContactPoint,
            connection=connection,
            create_instance_method=ContactPointFactory.instantiate_contact_point,
            preview_type=None
        )

