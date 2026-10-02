from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="CreateEnvironmentDto")



@_attrs_define
class CreateEnvironmentDto:
    """ Request body for creating a new environment under an organization.

        Example:
            {'externalId': 'vision-agent-eval', 'name': 'vision-agent-eval', 'organizationId': '60b52abd-
                bbea-4c69-987a-103cfd752060'}

        Attributes:
            name (str): Human-readable environment name shown in the UI.
            organization_id (UUID): Organization that will own the new environment.
            external_id (str | Unset): Customer-provided external identifier used to address the env. Omit to create an
                environment without one (the env will only be reachable by its internal UUID and won't participate in upsert-by-
                externalId).
     """

    name: str
    organization_id: UUID
    external_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        organization_id = str(self.organization_id)

        external_id = self.external_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "organizationId": organization_id,
        })
        if external_id is not UNSET:
            field_dict["externalId"] = external_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        organization_id = UUID(d.pop("organizationId"))




        external_id = d.pop("externalId", UNSET)

        create_environment_dto = cls(
            name=name,
            organization_id=organization_id,
            external_id=external_id,
        )


        create_environment_dto.additional_properties = d
        return create_environment_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
