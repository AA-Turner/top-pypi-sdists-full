from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="SharedEnvironmentDto")



@_attrs_define
class SharedEnvironmentDto:
    """ A single grant of read-visibility for one environment to one recipient organization.

        Example:
            {'id': 'b0d8e5d2-7b91-4a9b-9a4f-0b1f3e9b9a1c', 'environmentId': '784e2386-e297-4f9d-a886-838422383b65',
                'organizationId': 'a1b2c3d4-e5f6-4890-abcd-ef1234567890', 'createdAt': '2026-06-12T20:30:00.000Z'}

        Attributes:
            id (UUID): Internal UUID of the share row.
            environment_id (UUID): Environment being shared.
            organization_id (UUID): Recipient organization the environment is shared with.
            created_at (datetime.datetime): When the share was created.
     """

    id: UUID
    environment_id: UUID
    organization_id: UUID
    created_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        environment_id = str(self.environment_id)

        organization_id = str(self.organization_id)

        created_at = self.created_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "organizationId": organization_id,
            "createdAt": created_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        organization_id = UUID(d.pop("organizationId"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        shared_environment_dto = cls(
            id=id,
            environment_id=environment_id,
            organization_id=organization_id,
            created_at=created_at,
        )

        return shared_environment_dto

