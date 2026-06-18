import abc
import logging
from typing import ClassVar
from uuid import UUID

from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.downloadable import Downloadable
from picsellia.types.enums import AssignmentStatus
from picsellia.types.schemas import (
    AssignmentSchema,
)

logger = logging.getLogger("picsellia")


class AbstractAssignment(Dao, Downloadable, abc.ABC):
    _base_path: ClassVar[str]

    def __init__(self, connexion: Connection, campaign_id: UUID, data: dict):
        Dao.__init__(self, connexion, data)
        Downloadable.__init__(self)
        self._campaign_id = campaign_id

    @property
    def campaign_id(self) -> UUID:
        """UUID of (Campaign) where this (Assignment) is"""
        return self._campaign_id

    @property
    def asset_id(self) -> UUID:
        """UUID of (Asset) of this (Assignment)"""
        return self._asset_id

    @property
    def step_id(self) -> UUID:
        """UUID of (Step) of this (Assignment)"""
        return self._step_id

    @property
    def user_id(self) -> UUID | None:
        """UUID of (Step) of this (Assignment). If None, this assignment is not assigned"""
        return self._user_id

    @property
    def status(self) -> AssignmentStatus:
        """Status of this (Assignment)"""
        return self._status

    @property
    def data_id(self) -> UUID:
        """UUID of (Data) of this (Assignment)"""
        return self._data_id

    @property
    def object_name(self) -> str:
        """Object name of this (Assignment)"""
        return self._object_name

    @property
    def filename(self) -> str:
        """Filename of this (Assignment)"""
        return self._filename

    @property
    def large(self) -> bool:
        """If true, this (Assignment) file is considered large"""
        return True

    @exception_handler
    @beartype
    def reset_url(self) -> str:
        """Reset url property of this (Assignment) by calling platform.

        Returns:
            A url as a string of this (Assignment).
        """
        r = self.connection.get(f"/api/data/{self.data_id}/presigned-url")
        self._url = r.json()["presigned_url"]
        return self._url

    def __str__(self):
        return f"{Colors.YELLOW}Assignment {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> AssignmentSchema:
        schema = AssignmentSchema(**data)
        self._asset_id = schema.asset_id
        self._status = schema.status
        self._step_id = schema.step_id
        self._user_id = schema.user_id

        # Data properties
        self._data_id = schema.data.id
        self._object_name = schema.data.object_name
        self._filename = schema.data.filename
        self._url = schema.data.url
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/{self._base_path}/{self.id}").json()
        self.refresh(r)
        return r
