import logging

from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.downloadable import Downloadable
from picsellia.types.schemas import ModelFileSchema

logger = logging.getLogger("picsellia")


class ModelFile(Dao, Downloadable):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)
        Downloadable.__init__(self)

    @property
    def name(self) -> str:
        """Name of this (ModelFile)"""
        return self._name

    @property
    def object_name(self) -> str:
        """Object name of this (ModelFile)"""
        return self._object_name

    @property
    def filename(self) -> str:
        """Filename of this (ModelFile)"""
        return self._filename

    @property
    def large(self) -> bool:
        """If True, this (ModelFile) is considered having a large size"""
        return self._large

    def __str__(self):
        return (
            f"{Colors.BLUE}Model file named '{self.name}'{Colors.ENDC} (id: {self.id})"
        )

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/model/file/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> ModelFileSchema:
        schema = ModelFileSchema(**data)
        self._name = schema.name
        self._object_name = schema.object_name
        self._filename = schema.filename
        self._large = schema.large
        self._url = schema.url
        return schema

    @exception_handler
    @beartype
    def reset_url(self) -> str:
        """Reset url property of this ModelFile by calling platform.

        Returns:
            A url as a string of this ModelFile.
        """
        self._url = self.connection.init_download(self.object_name)
        return self._url

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this file

        Examples:
            ```python
            model_file.delete()
            ```
        """
        self.connection.delete(f"/api/model/file/{self.id}")
        logger.info(f"{self} deleted from platform.")
