import logging
from uuid import UUID

from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.types.enums import WorkerType
from picsellia.types.schemas import WorkerSchema

logger = logging.getLogger("picsellia")


class Worker(Dao):
    """
    This class is deprecated and should not be used anymore.
    """

    def __init__(self, connexion: Connection, data: dict, type: WorkerType | str):
        Dao.__init__(self, connexion, data)
        self.type = WorkerType.validate(type)

    @property
    def id(self) -> UUID:
        """Worker id is now the id of the user"""
        return self._user_id

    @property
    def username(self) -> str:
        """Username of the Worker"""
        return self._username

    @property
    def user_id(self) -> UUID:
        """id of the User"""
        return self._user_id

    def __str__(self):
        return (
            f"{Colors.UNDERLINE}Worker '{self.username}' of a {self.type} {Colors.ENDC}"
        )

    @exception_handler
    @beartype
    def sync(self) -> dict:
        logger.warning(
            "This method is not calling platform to refresh data. You should not call it"
        )
        return {"id": self.id, "user_id": self.user_id, "username": self.username}

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> WorkerSchema:
        schema = WorkerSchema(**data)
        self._username = schema.username
        self._user_id = schema.user_id
        return schema

    @exception_handler
    @beartype
    def get_infos(self) -> dict:
        """Retrieve worker info

        Examples:
            ```python
            worker = my_dataset.list_workers()[0]
            print(worker.get_infos())
            ```

        Returns:
            A dict with data of the worker
        """
        return {"username": self.username}
