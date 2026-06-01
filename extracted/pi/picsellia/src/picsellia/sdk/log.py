import logging

import orjson
from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.exceptions import BadRequestError
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.types.enums import LogType
from picsellia.types.schemas import LogDataType, LogSchema
from picsellia.utils import filter_payload

logger = logging.getLogger("picsellia")


class Log(Dao):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)

    @property
    def name(self) -> str:
        """Name of this (Log)"""
        return self._name

    @property
    def data(self) -> LogDataType:
        """Data of this (Log)"""
        return self._data

    @property
    def type(self) -> LogType:
        """Type of this (Log)"""
        return self._type

    def __str__(self):
        return f"{Colors.GREEN}Log {self.name}{Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/log/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict):
        schema = LogSchema(**data)
        self._name = schema.name
        self._data = schema.data
        self._type = schema.type
        return schema

    @exception_handler
    @beartype
    def update(self, name: str | None = None, data: LogDataType | None = None) -> None:
        """Update this log with a new name or new data

        You cannot change the type of this Log.

        Examples:
            ```python
            my_log.update(name="new_name", data={"key": "value"})
            ```
        Arguments:
            name (str, optional): New name of the log. Defaults to None.
            data (LogDataType, optional): New data of the log. Defaults to None.
        """
        if self.type == LogType.IMAGE and data:
            raise BadRequestError(
                "You cannot update data of a log image this way, use experiment.log() method instead."
            )

        payload = {"name": name, "data": data}
        filtered_payload = filter_payload(payload)
        r = self.connection.patch(
            f"/api/log/{self.id}", data=orjson.dumps(filtered_payload)
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated.")

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this log

        Examples:
            ```python
            my_log.delete()
            ```
        """
        self.connection.delete(f"/api/log/{self.id}")

    @exception_handler
    @beartype
    def append(self, data: LogDataType) -> None:
        """Appends value to log with given name.

        You can only append log on Line logs.

        Examples:
            ```python
            my_log.append(data={"key": "value"})
            ```

        Arguments:
            data (LogDataType): Data to append to this log
        """
        assert self.type == LogType.LINE, "You can only append log on Line logs"
        payload = {"data": data}
        r = self.connection.post(
            f"/api/log/{self.id}/append", data=orjson.dumps(payload)
        ).json()
        self.refresh(r)
        logger.info(f"Append {data} on {self}.")
