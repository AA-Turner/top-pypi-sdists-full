from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.permission_metadata_response_permission_map_additional_property import (
    PermissionMetadataResponsePermissionMapAdditionalProperty,
)

T = TypeVar("T", bound="PermissionMetadataResponsePermissionMap")


@_attrs_define
class PermissionMetadataResponsePermissionMap:
    """Map of resource types to create permission enums"""

    additional_properties: dict[str, PermissionMetadataResponsePermissionMapAdditionalProperty] = _attrs_field(
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
        permission_metadata_response_permission_map = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = PermissionMetadataResponsePermissionMapAdditionalProperty(prop_dict)

            additional_properties[prop_name] = additional_property

        permission_metadata_response_permission_map.additional_properties = additional_properties
        return permission_metadata_response_permission_map

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> PermissionMetadataResponsePermissionMapAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: PermissionMetadataResponsePermissionMapAdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
