from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.permission_metadata_response_permission_descriptions_item import (
        PermissionMetadataResponsePermissionDescriptionsItem,
    )
    from ..models.permission_metadata_response_permission_map import PermissionMetadataResponsePermissionMap
    from ..models.permission_metadata_response_permissions import PermissionMetadataResponsePermissions
    from ..models.permission_metadata_response_roles import PermissionMetadataResponseRoles


T = TypeVar("T", bound="PermissionMetadataResponse")


@_attrs_define
class PermissionMetadataResponse:
    """
    Attributes:
        roles (PermissionMetadataResponseRoles): Map of role keys to role enum values from RoleEnum
        permissions (PermissionMetadataResponsePermissions): Map of permission keys to permission enum values from
            PermissionEnum
        permission_map (PermissionMetadataResponsePermissionMap): Map of resource types to create permission enums
        permission_descriptions (list['PermissionMetadataResponsePermissionDescriptionsItem']): Grouped permission
            descriptions for UI
    """

    roles: "PermissionMetadataResponseRoles"
    permissions: "PermissionMetadataResponsePermissions"
    permission_map: "PermissionMetadataResponsePermissionMap"
    permission_descriptions: list["PermissionMetadataResponsePermissionDescriptionsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        roles = self.roles.to_dict()

        permissions = self.permissions.to_dict()

        permission_map = self.permission_map.to_dict()

        permission_descriptions = []
        for permission_descriptions_item_data in self.permission_descriptions:
            permission_descriptions_item = permission_descriptions_item_data.to_dict()
            permission_descriptions.append(permission_descriptions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "roles": roles,
                "permissions": permissions,
                "permission_map": permission_map,
                "permission_descriptions": permission_descriptions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission_metadata_response_permission_descriptions_item import (
            PermissionMetadataResponsePermissionDescriptionsItem,
        )
        from ..models.permission_metadata_response_permission_map import PermissionMetadataResponsePermissionMap
        from ..models.permission_metadata_response_permissions import PermissionMetadataResponsePermissions
        from ..models.permission_metadata_response_roles import PermissionMetadataResponseRoles

        d = dict(src_dict)
        roles = PermissionMetadataResponseRoles.from_dict(d.pop("roles"))

        permissions = PermissionMetadataResponsePermissions.from_dict(d.pop("permissions"))

        permission_map = PermissionMetadataResponsePermissionMap.from_dict(d.pop("permission_map"))

        permission_descriptions = []
        _permission_descriptions = d.pop("permission_descriptions")
        for permission_descriptions_item_data in _permission_descriptions:
            permission_descriptions_item = PermissionMetadataResponsePermissionDescriptionsItem.from_dict(
                permission_descriptions_item_data
            )

            permission_descriptions.append(permission_descriptions_item)

        permission_metadata_response = cls(
            roles=roles,
            permissions=permissions,
            permission_map=permission_map,
            permission_descriptions=permission_descriptions,
        )

        permission_metadata_response.additional_properties = d
        return permission_metadata_response

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
