import logging

import orjson
from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.types.schemas import DataSourceSchema

logger = logging.getLogger("picsellia")


class DataSource(Dao):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)

    def __str__(self):
        return f"{Colors.GREEN}Data source '{self.name}'{Colors.ENDC} (id: {self.id})"

    @property
    def name(self) -> str:
        """Name of this (DataSource)"""
        return self._name

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> DataSourceSchema:
        schema = DataSourceSchema(**data)
        self._name = schema.name
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/data/source/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def update(self, name: str) -> None:
        """Update this data source with a new name.

        Examples:
            ```python
            sdk_source.update(name="new name")
            ```

        Arguments:
            name: New name of this data source
        """
        payload = {"name": name}
        r = self.connection.patch(
            f"/api/data/source/{self.id}", data=orjson.dumps(payload)
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated")

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this data source from the platform.
        All data with this source will not have source anymore

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
            sdk_source.delete()
            ```
        """
        self.connection.delete(f"/api/data/source/{self.id}")
        logger.info(f"{self} deleted.")
