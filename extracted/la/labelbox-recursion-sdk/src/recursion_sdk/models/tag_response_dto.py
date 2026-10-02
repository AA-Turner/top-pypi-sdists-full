from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="TagResponseDto")



@_attrs_define
class TagResponseDto:
    """ A reusable label. Platform-default tags (environmentId null) are seeded and shared; custom tags belong to one
    environment.

        Attributes:
            id (UUID): Stable tag identifier (UUID). A tag is a reusable, environment-scoped (or platform-default) label.
            environment_id (None | UUID): Environment that owns this tag, or null for a platform-default tag available to
                every environment.
            label (str): Human-readable tag label (e.g. "FINAL"). Trimmed; unique within its scope.
            color (str): Badge color as a 6-digit hex string (e.g. "#22c55e").
            description (None | str): Optional human-readable description of what the tag signifies.
            created_by_user_id (None | UUID): User who created the tag; null for seeded platform-default tags.
            created_at (datetime.datetime): Timestamp when the tag was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the tag was last updated (ISO-8601, UTC).
     """

    id: UUID
    environment_id: None | UUID
    label: str
    color: str
    description: None | str
    created_by_user_id: None | UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        environment_id: None | str
        if isinstance(self.environment_id, UUID):
            environment_id = str(self.environment_id)
        else:
            environment_id = self.environment_id

        label = self.label

        color = self.color

        description: None | str
        description = self.description

        created_by_user_id: None | str
        if isinstance(self.created_by_user_id, UUID):
            created_by_user_id = str(self.created_by_user_id)
        else:
            created_by_user_id = self.created_by_user_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "label": label,
            "color": color,
            "description": description,
            "createdByUserId": created_by_user_id,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_environment_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                environment_id_type_0 = UUID(data)



                return environment_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        environment_id = _parse_environment_id(d.pop("environmentId"))


        label = d.pop("label")

        color = d.pop("color")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))


        def _parse_created_by_user_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_by_user_id_type_0 = UUID(data)



                return created_by_user_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        created_by_user_id = _parse_created_by_user_id(d.pop("createdByUserId"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        tag_response_dto = cls(
            id=id,
            environment_id=environment_id,
            label=label,
            color=color,
            description=description,
            created_by_user_id=created_by_user_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        return tag_response_dto

