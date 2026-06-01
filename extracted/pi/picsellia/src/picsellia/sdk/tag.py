import logging

import orjson
from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.multi_object import MultiObject
from picsellia.types.enums import TagTarget
from picsellia.types.schemas import TagSchema

logger = logging.getLogger("picsellia")


class Tag(Dao):
    def __init__(self, connexion: Connection, data: dict) -> None:
        Dao.__init__(self, connexion, data)

    @property
    def name(self) -> str:
        """Name of this (Tag)"""
        return self._name

    @property
    def target_type(self) -> TagTarget:
        """Target type of this tag, can be :
        DATA, ASSET, MODEL_VERSION, MODEL, DATASET_VERSION, DATASET, DEPLOYMENT, PREDICTED_ASSET
        """
        return self._target_type

    def __str__(self):
        return f"{Colors.BLUE}Tag '{self.name}'{Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/tag/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> TagSchema:
        schema = TagSchema(**data)
        self._name = schema.name
        self._target_type = schema.target_type
        return schema

    @exception_handler
    @beartype
    def update(self, name: str) -> None:
        """Update this tag with a new name.

        Examples:
            ```python
            a_tag.update(name="new name")
            ```

        Arguments:
            name (str): New name of this tag.
        """
        payload = {"name": name}
        r = self.connection.patch(
            f"/api/tag/{self.id}", data=orjson.dumps(payload)
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated")

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this tag from the platform.
        All tagged object will not have this tag anymore.

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
            tag.delete()
            ```
        """
        self.connection.delete(f"/api/tag/{self.id}")
        logger.info(f"{self} deleted.")

    @exception_handler
    @beartype
    def attach_on(self, targets: Dao | list[Dao] | MultiObject[Dao]) -> None:
        """Attach this tag on a list of target.

        Tag needs to be the same target type as the taggable object.
        For example, if it's a Data Tag, it can only be attached on Data.

        If this is not a good target type, it will not raise any Error, but it will not do anything.

        Examples:
            ```python
            data_tag = datalake.create_data_tag("home")
            some_data = datalake.list_data()
            data_tag.attach_on(some_data)
            ```

        Arguments:
            targets (Dao or list[Dao] or MultiObject[Dao]): List of target to attach this tag on.
        """
        if isinstance(targets, Dao):
            targets = [targets]
        payload = [target.id for target in targets]
        r = self.connection.post(
            f"/api/tag/{self.id}/attach", data=orjson.dumps(payload)
        ).json()
        self.refresh(r["tag"])
        logger.info(f"{self} was attached to {r['count']} object(s)")

    @exception_handler
    @beartype
    def detach_from(self, targets: Dao | list[Dao] | MultiObject[Dao]) -> None:
        """Detach this tag from a list of target.

        Tag needs to be the same target type as the taggable object.
        For example, if it's a Data Tag, it can only be detached from a Data.

        If this is not a good target type, it will not raise any Error, but it will not do anything.

        Examples:
            ```python
            data_tag = datalake.create_data_tag("home")
            some_data = datalake.list_data()
            data_tag.attach_on(some_data)

            data_tag.detach_from(some_data)
            ```

        Arguments:
            targets (Dao or list[Dao] or MultiObject[Dao]): List of target to detach this tag from.
        """
        if isinstance(targets, Dao):
            targets = [targets]
        payload = [target.id for target in targets]
        r = self.connection.post(
            f"/api/tag/{self.id}/detach", data=orjson.dumps(payload)
        ).json()
        self.refresh(r["tag"])
        logger.info(f"{self} was detached from {r['count']} object(s)")
