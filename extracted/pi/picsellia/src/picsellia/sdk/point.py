import logging
from typing import Any
from uuid import UUID

import orjson
from beartype import beartype
from deprecation import deprecated

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.label import Label
from picsellia.types.schemas import PointSchema

logger = logging.getLogger("picsellia")


class Point(Dao):
    def __init__(
        self,
        connexion: Connection,
        dataset_version_id: UUID,
        annotation_id: UUID,
        data: dict,
    ) -> None:
        self._dataset_version_id = dataset_version_id
        self._annotation_id = annotation_id
        Dao.__init__(self, connexion, data)

    @property
    def annotation_id(self) -> UUID:
        """UUID of the (Annotation) holding this (Point)"""
        return self._annotation_id

    @property
    def coords(self) -> list[list[int]]:
        """Coords of this (Point)"""
        return self._coords

    @property
    @deprecated(deprecated_in="6.27.0", details="This field is not used anymore")
    def order(self) -> int:
        return 0

    @property
    def label(self) -> Label:
        """(Label) of this (Point)"""
        return self._label

    @property
    def text(self) -> str | None:
        """OCR text of this (Point)"""
        return self._text

    @property
    def attributes(self) -> dict[str, Any] | None:
        """Attributes of this (Point)"""
        return self._attributes

    def __str__(self):
        return f"{Colors.BLUE}Point ({self.coords} with label {self.label.name} on annotation {self.annotation_id} {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/point/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> PointSchema:
        schema = PointSchema(**data)
        self._coords = schema.coords
        self._text = schema.text
        self._attributes = schema.attributes
        self._label = Label(
            self.connection,
            schema.label.model_dump(),
            dataset_version_id=self._dataset_version_id,
        )
        return schema

    @exception_handler
    @beartype
    def update(
        self,
        coords: list | None = None,
        label: Label | None = None,
        text: str | None = None,
    ) -> None:
        """Update this point with new coords or new label.

        Examples:
            ```python
            point.update(coords=[0, 0])
            ```

        Arguments:
            coords (List, optional): New coords of this (Point). It must be a list of 2 integer. Defaults to None.
            label (Label, optional): New label of this (Point). Defaults to None.
            text (str, optional): New ocr text of this (Point). Defaults to None.
        """
        payload = {}
        if coords is not None:
            payload["point"] = coords
        if label is not None:
            payload["label_id"] = label.id
        if text is not None:
            payload["text"] = text
        assert payload != {}, "You can't update this point with no data to update"
        r = self.connection.patch(
            f"/api/point/{self.id}", data=orjson.dumps(payload)
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated")

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this point from the platform.

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
            point.delete()
            ```
        """
        self.connection.delete(f"/api/point/{self.id}")
        logger.info(f"{self} deleted.")
