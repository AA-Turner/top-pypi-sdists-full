import logging
from typing import Any, Optional

from httpx import HTTPStatusError
from pydantic import Field, BaseModel

from ipfabric.models.users import User
from ipfabric.tools.shared import TIMEZONES, raise_for_status
from .rbac import Roles

logger = logging.getLogger("ipfabric")


class LocalUsers(BaseModel):
    client: Any = Field(exclude=True)
    _users: Optional[list[User]] = None
    _roles: Optional[Roles] = None

    def setup(self):
        self._users = self.get_users()
        try:
            self._roles = Roles(client=self.client)
        except HTTPStatusError:
            pass

    @property
    def users(self) -> list[User]:
        if not self._users:
            self.setup()
        return self._users

    @property
    def users_by_id(self) -> dict[str, User]:
        return {_.user_id: _ for _ in self.users}

    def get_users(self, username: str = None) -> list[User]:
        """
        Gets all users or filters on one of the options.
        :param username: str: Username to filter
        :return: List of users
        """
        filters = {"username": ["ieq", username]} if username else None
        users = self.client.fetch_all("tables/users", filters=filters, snapshot=False)
        return [User(**user) for user in users]

    def get_user_by_id(self, user_id: str):
        """
        Gets a user by ID
        :param user_id: Union[str, int]: User ID to filter
        :return: User
        """
        resp = raise_for_status(self.client.get("users/" + str(user_id)))
        user = resp.json()
        return User(**user)

    def add_user(
        self,
        username: str,
        password: str,
        roles: list,
        timezone: str = "UTC",
    ):
        """
        Adds a user
        :param username: str: Username
        :param password: str: Must be 8 characters
        :param roles: list: Role IDs for Users
        :param timezone: str: v4.2 and above, Defaults UTC.  See pytz.all_timezones for correct syntax
        :return: User
        """
        if len(password) < 8:
            raise SyntaxError("Password must be 8 characters.")
        if self._roles and not all(x in [r.role_id for r in self._roles.roles] for x in roles):
            raise SyntaxError(f"Only accepted roles are {[r.role_id for r in self._roles.roles]}")
        payload = {
            "username": username,
            "password": password,
            "roleIds": roles,
        }
        if timezone.lower() not in TIMEZONES:
            raise ValueError(f"Timezone `{timezone}` is not located. Please see `ipfabric.tools.shared.TIMEZONES`.")
        payload["timezone"] = TIMEZONES[timezone.lower()]
        resp = raise_for_status(self.client.post("users", json=payload))
        self._users = self.get_users()
        return self.users_by_id[resp.json()["id"]]

    def delete_user(self, user_id: str) -> bool:
        """
        Deletes a user and returns list of remaining users
        :param user_id:
        :return:
        """
        raise_for_status(self.client.delete("users/" + str(user_id)))
        self._users = self.get_users()
        return True
