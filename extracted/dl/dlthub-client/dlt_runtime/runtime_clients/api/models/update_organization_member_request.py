from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.organization_membership_role import OrganizationMembershipRole

T = TypeVar("T", bound="UpdateOrganizationMemberRequest")


@_attrs_define
class UpdateOrganizationMemberRequest:
    """
    Attributes:
        role (OrganizationMembershipRole): The role to assign to the user
    """

    role: OrganizationMembershipRole
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = OrganizationMembershipRole(d.pop("role"))

        update_organization_member_request = cls(
            role=role,
        )

        update_organization_member_request.additional_properties = d
        return update_organization_member_request

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
