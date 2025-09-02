"""User handler for Crownstone cloud data."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from crownstone_cloud.cloud import CrownstoneCloud


class Users:
    """Handler for the users in a sphere."""

    def __init__(self, cloud: CrownstoneCloud, sphere_id: str) -> None:
        """Initialization."""
        self.cloud = cloud
        self.sphere_id = sphere_id
        self.data: dict[str, User] = {}

    def __iter__(self) -> Iterator[User]:
        """Iterate over users."""
        return iter(self.data.values())

    async def async_update_user_data(self) -> None:
        """
        Get the users for the sphere from the cloud.

        This method is a coroutine.
        """
        cloud_data: dict[
            str, list[dict[str, Any]]
        ] = await self.cloud.request_handler.get(
            "Spheres", "users", model_id=self.sphere_id
        )
        # process items
        removed_items: list[str] = []
        new_items: list[str] = []
        for role, users in cloud_data.items():
            for user in users:
                user_id = user["id"]
                exists = self.data.get(user_id)
                # check if the User already exists
                # it is important that we don't throw away existing objects,
                # as they need to remain functional
                if exists:
                    # update data
                    self.data[user_id].data = user
                else:
                    # add new User + their role
                    self.data[user_id] = User(user, role)

                # generate list with new id's to check with the existing id's
                new_items.append(user_id)

        # check for removed items
        for user_id in self.data:
            if user_id not in new_items:
                removed_items.append(user_id)

        # remove items from dict
        for user_id in removed_items:
            del self.data[user_id]

    def find_by_first_name(self, first_name: str) -> list[User]:
        """Search for a user by first name and return a list with the users found."""
        found_users: list[User] = []
        for user in self.data.values():
            if first_name == user.first_name:
                found_users.append(user)

        return found_users

    def find_by_last_name(self, last_name: str) -> list[User]:
        """Search for a user by last name and return a list with the users found."""
        found_users: list[User] = []
        for user in self.data.values():
            if last_name == user.last_name:
                found_users.append(user)

        return found_users

    def find_by_id(self, user_id: str) -> User | None:
        """Search for a user by id and return crownstone object if found."""
        return self.data.get(user_id)


class User:
    """Represents a user in a sphere."""

    def __init__(self, data: dict[str, Any], role: str) -> None:
        """Initialization."""
        self.data = data
        self.role = role

    @property
    def first_name(self) -> str:
        """Return the first name of this User."""
        return str(self.data["firstName"])

    @property
    def last_name(self) -> str:
        """Return the last name of this User."""
        return str(self.data["lastName"])

    @property
    def email(self) -> str:
        """Return the email of this User."""
        return str(self.data["email"])

    @property
    def cloud_id(self) -> str:
        """Return the cloud id of this User."""
        return str(self.data["id"])

    @property
    def email_verified(self) -> bool:
        """Return whether the user has verified email."""
        return bool(self.data["emailVerified"])
