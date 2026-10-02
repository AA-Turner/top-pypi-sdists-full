"""Users manager (IstariAdmin surface).

``Users`` manages user administration.
"""

from __future__ import annotations

from istari_digital_client.sdk._base import _Manager
from istari_digital_client.sdk._admin.admin_types import User as UserType
from istari_digital_client.sdk._generated.v2.models.user_state_option import UserStateOption
from istari_digital_client.sdk._generated.v2.models.user_type import UserType as UserTypeEnum


class Users(_Manager):
    """Manager for user administration.

    Reached via ``admin.users``. Provides read-only access to user information.

    Usage::

        # 1. Get the current user
        me = admin.users.current()
        print(f"Logged in as: {me.display_name}")

        # 2. Get a specific user
        user = admin.users.get("user-uuid")

        # 3. List all users
        for user in admin.users.list():
            print(user.email, user.user_type)

        # 4. List only active human users
        humans = admin.users.list(user_state=UserStateOption.ACTIVE, user_type=UserTypeEnum.HUMAN)
    """

    def current(self) -> UserType:
        """Get the currently authenticated user.

        Returns:
            A User with all profile fields populated.
        """
        dto = self._call(self._engine.v2_api.get_current_user)
        return UserType._bind(dto, mgr=self)

    def get(self, user_id: str) -> UserType:
        """Get a user by their UUID.

        Args:
            user_id: The UUID of the user to fetch.

        Returns:
            A User with all profile fields populated.

        Raises:
            NotFoundError: If no user with that id exists.
        """
        dto = self._call(self._engine.v2_api.get_user_by_id, user_id)
        return UserType._bind(dto, mgr=self)

    def list(
        self,
        *,
        user_state: UserStateOption | None = None,
        user_type: UserTypeEnum | None = None,
    ) -> list[UserType]:
        """List all users.

        Note: This returns a plain list, not a paginated Page.

        Args:
            user_state: Filter by state (ACTIVE or ALL).
            user_type: Filter by type (HUMAN, AGENT, or ALL).

        Returns:
            A list of User objects.
        """
        dtos = self._call(
            self._engine.v2_api.list_users,
            user_state=user_state,
            user_type=user_type,
        )
        return [UserType._bind(dto, mgr=self) for dto in dtos]
