"""User Collection - Pre-configured AssetCollection for Users"""

from ..asset_service import AssetCollection
from ....models.company.assets.users.user import User, UserPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....services.users.user_factory import UserFactory


class UserCollection(AssetCollection[User, UserPreview]):
    """Pre-configured collection for User assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="users",
            asset_type=User,
            connection=connection,
            create_instance_method=UserFactory.instantiate_user,
            preview_type=UserPreview
        )

