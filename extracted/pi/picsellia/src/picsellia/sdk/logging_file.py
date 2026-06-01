import logging
import os

import orjson
from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.downloadable import Downloadable
from picsellia.types.schemas import LoggingFileSchema
from picsellia.utils import filter_payload

logger = logging.getLogger("picsellia")


class LoggingFile(Dao, Downloadable):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)
        Downloadable.__init__(self)

    def __str__(self):
        return f"{Colors.GREEN}Logging file {self.object_name}{Colors.ENDC} (id: {self.id})"

    @property
    def object_name(self) -> str:
        """Object name of this (LoggingFile)"""
        return self._object_name

    @property
    def filename(self) -> str:
        """Filename of this (LoggingFile)."""
        return os.path.basename(self._object_name)

    @property
    def large(self) -> bool:
        """(LoggingFile) are usually not large file."""
        return False

    @exception_handler
    @beartype
    def reset_url(self) -> str:
        """Reset url property of this LoggingFile by calling platform.

        Returns:
            A url as a string of this LoggingFile.
        """
        self._url = self.connection.init_download(self.object_name)
        return self._url

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> LoggingFileSchema:
        schema = LoggingFileSchema(**data)
        self._object_name = schema.object_name
        self._url = schema.url
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/logging/file/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def update(
        self,
        object_name: str | None = None,
    ) -> None:
        """Update this artifact.

        Examples:
            ```python
            this_artifact.update(object_name="another-path-to-artifact")
            ```

        Arguments:
            object_name (str, optional): New object_name of this artifact. Defaults to None.
        """
        payload = {
            "object_name": object_name,
        }
        filtered_payload = filter_payload(payload)
        r = self.connection.patch(
            f"/api/logging/file/{self.id}", data=orjson.dumps(filtered_payload)
        ).json()
        self.refresh(r)

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this artifact

        Examples:
            ```python
            this_artifact.delete()
            ```
        """
        self.connection.delete(f"/api/logging/file/{self.id}")
