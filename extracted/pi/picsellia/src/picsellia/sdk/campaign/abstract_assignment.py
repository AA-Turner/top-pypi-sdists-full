import abc
import logging
from typing import ClassVar
from uuid import UUID

from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.types.enums import AssignmentStatus
from picsellia.types.schemas import (
    AssignmentSchema,
)

logger = logging.getLogger("picsellia")


class AbstractAssignment(Dao, abc.ABC):
    _base_path: ClassVar[str]

    def __init__(self, connexion: Connection, campaign_id: UUID, data: dict):
        Dao.__init__(self, connexion, data)
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
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/{self._base_path}/{self.id}").json()
        self.refresh(r)
        return r
