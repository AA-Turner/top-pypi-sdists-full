from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ShareEnvironmentDto")



@_attrs_define
class ShareEnvironmentDto:
    """ Request body for sharing an environment with another organization. Idempotent: re-sharing returns the existing share
    row.

        Example:
            {'organizationExternalId': 'recipient-org'}

        Attributes:
            organization_external_id (str): External identifier of the organization the environment is being shared with.
     """

    organization_external_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        organization_external_id = self.organization_external_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "organizationExternalId": organization_external_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        organization_external_id = d.pop("organizationExternalId")

        share_environment_dto = cls(
            organization_external_id=organization_external_id,
        )


        share_environment_dto.additional_properties = d
        return share_environment_dto

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
