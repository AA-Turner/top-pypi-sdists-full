import logging
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from beartype import beartype
from deprecation import deprecated
from orjson import orjson

from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.user import User

logger = logging.getLogger("picsellia")


class Resource(ABC):
    def __init__(self, resource_name: str):
        self.resource_name = resource_name

    @property
    @abstractmethod
    def id(self) -> UUID:
        pass

    @property
    @deprecated(
        deprecated_in="6.29.0",
        details="You should use connection property instead of this one.",
    )
    def connexion(self) -> Connection:
        """deprecated"""
        return self.connection

    @property
    @abstractmethod
    def connection(self) -> Connection:
        pass

    @exception_handler
    @beartype
    def list_users(self) -> list[User]:
        """List all users of this resource

        Examples:
            ```python
            resource.list_users()
            ```

        Returns:
            list of (User) objects
        """
        r = self.connection.get(
            f"/api/access/{self.resource_name}/{self.id}/users"
        ).json()
        return [User(self.connection, item) for item in r["users"]]

    @exception_handler
    @beartype
    def add_user(self, user: User, role: str | None = None) -> None:
        """Add given user to this resource, with given role.
        If user is UNPRIVILEGED on Organization, then its role will be forced to LABELER.
        If role is None, user will be assigned configured role on Organization, or if not configured, USER.

        :warning: **DANGER ZONE**: This method will create access for a user. Role depends on type of resource you're adding the user.

        Examples:
            ```python
            user = client.find_user("foo")
            resource.add_user(user, "ADMIN")
            ```
        """
        payload: dict[str, Any] = {"user_id": user.id}
        if role:
            payload["role"] = role

        self.connection.post(
            f"/api/access/{self.resource_name}/{self.id}/users",
            data=orjson.dumps(payload),
        ).json()
        logger.info(f"User {user.username} has been added to this resource.")
