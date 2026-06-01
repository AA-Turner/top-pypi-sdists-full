import logging
from typing import Any
from uuid import UUID

import orjson
from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.label import Label
from picsellia.types.schemas import ClassificationSchema

logger = logging.getLogger("picsellia")


class Classification(Dao):
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
        """UUID of (Annotation) holding this (Classification)"""
        return self._annotation_id

    @property
    def label(self) -> Label:
        """(Label) of this (Classification)"""
        return self._label

    @property
    def text(self) -> str | None:
        """OCR text of this (Classification)"""
        return self._text

    @property
    def attributes(self) -> dict[str, Any] | None:
        """Attributes of this (Classification)"""
        return self._attributes

    def __str__(self):
        return f"{Colors.BLUE}Classification with label {self.label.name} on annotation {self.annotation_id} {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/classification/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> ClassificationSchema:
        schema = ClassificationSchema(**data)
        self._label = Label(
            self.connection,
            schema.label.model_dump(),
            dataset_version_id=self._dataset_version_id,
        )
        self._text = schema.text
        self._attributes = schema.attributes
        return schema

    @exception_handler
    @beartype
    def update(
        self,
        label: Label | None = None,
        text: str | None = None,
    ) -> None:
        """Update this classification with another label.

        Examples:
            ```python
            classification.update(label=label_plane)
            ```

        Arguments:
            label: (Label) to update this (Classification). Defaults to None.
            text (str, optional): New ocr text of this (Classification). Defaults to None.
        """
        payload = {}
        if label is not None:
            payload["label_id"] = label.id
        if text is not None:
            payload["text"] = text
        assert payload != {}, "You can't update this point with no data to update"
        r = self.connection.patch(
            f"/api/classification/{self.id}", data=orjson.dumps(payload)
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated")

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this classification from the platform.

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
            classification.delete()
            ```
        """
        self.connection.delete(f"/api/classification/{self.id}")
        logger.info(f"{self} deleted.")
