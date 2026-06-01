from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.sso_connection_group_role_mappings_additional_property import (
    check_sso_connection_group_role_mappings_additional_property,
)
from ..models.sso_connection_group_role_mappings_additional_property import (
    SSOConnectionGroupRoleMappingsAdditionalProperty,
)


T = TypeVar("T", bound="SSOConnectionGroupRoleMappings")


@_attrs_define
class SSOConnectionGroupRoleMappings:
    """Mapping of IdP group claim values to smplkit roles. The first key matching the user's group claims (in declaration
    order) decides the JIT role; if none match, `default_role` applies. Example: `{"smplkit-admins": "ADMIN"}`.

    """

    additional_properties: dict[str, SSOConnectionGroupRoleMappingsAdditionalProperty] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sso_connection_group_role_mappings = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = check_sso_connection_group_role_mappings_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        sso_connection_group_role_mappings.additional_properties = additional_properties
        return sso_connection_group_role_mappings

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> SSOConnectionGroupRoleMappingsAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: SSOConnectionGroupRoleMappingsAdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
