import logging

from beartype import beartype

from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.types.schemas import UserSchema

logger = logging.getLogger("picsellia")


class User(Dao):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)

    @property
    def username(self) -> str:
        """Username of the Worker"""
        return self._username

    def __str__(self):
        return f"User '{self.username}'"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        logger.warning(
            "This method is not calling platform to refresh data. You should not call it"
        )
        return {"id": self.id, "username": self.username}

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> UserSchema:
        schema = UserSchema(**data)
        self._username = schema.username
        return schema
