from typing import List

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.client.openapi_client.models import (
    AdminCreateUser as AdminCreateUserModel,
)
from anyscale.user.models import AdminCreatedUser, AdminCreateUser


class PrivateUserSDK(BaseSDK):
    def admin_batch_create(
        self, admin_create_users: List[AdminCreateUser]
    ) -> List[AdminCreatedUser]:
        created_users = self.client.admin_batch_create_users(
            [
                AdminCreateUserModel(**admin_create_user.to_dict())
                for admin_create_user in admin_create_users
            ]
        )

        return [
            AdminCreatedUser(
                user_id=created_user.user_id,
                name=created_user.name,
                email=created_user.email,
                created_at=created_user.created_at,
                is_sso_user=created_user.is_sso_user,
                lastname=created_user.lastname,
                title=created_user.title,
            )
            for created_user in created_users
        ]
