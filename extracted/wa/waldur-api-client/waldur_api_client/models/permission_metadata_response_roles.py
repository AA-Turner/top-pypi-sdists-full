from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.permission_metadata_response_roles_additional_property import (
    PermissionMetadataResponseRolesAdditionalProperty,
)

T = TypeVar("T", bound="PermissionMetadataResponseRoles")


@_attrs_define
class PermissionMetadataResponseRoles:
    """Map of role keys to role enum values from RoleEnum"""

    additional_properties: dict[str, PermissionMetadataResponseRolesAdditionalProperty] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        permission_metadata_response_roles = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = PermissionMetadataResponseRolesAdditionalProperty(prop_dict)

            additional_properties[prop_name] = additional_property

        permission_metadata_response_roles.additional_properties = additional_properties
        return permission_metadata_response_roles

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> PermissionMetadataResponseRolesAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: PermissionMetadataResponseRolesAdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
