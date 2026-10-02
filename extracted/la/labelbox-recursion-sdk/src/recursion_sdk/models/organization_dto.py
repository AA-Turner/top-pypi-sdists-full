from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="OrganizationDto")



@_attrs_define
class OrganizationDto:
    """ An organization. Top-level tenant boundary that owns environments, problems, and users.

        Attributes:
            id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
            external_id (str): External organization identifier provided by the caller's source-of-truth system.
            name (str): Human-readable display name of the organization.
            created_at (datetime.datetime): Timestamp when the organization was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the organization was last updated (ISO-8601, UTC).
     """

    id: UUID
    external_id: str
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        external_id = self.external_id

        name = self.name

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "externalId": external_id,
            "name": name,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        external_id = d.pop("externalId")

        name = d.pop("name")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        organization_dto = cls(
            id=id,
            external_id=external_id,
            name=name,
            created_at=created_at,
            updated_at=updated_at,
        )

        return organization_dto

