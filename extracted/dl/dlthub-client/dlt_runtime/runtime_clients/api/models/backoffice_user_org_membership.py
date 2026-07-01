from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.organization_membership_role import OrganizationMembershipRole

T = TypeVar("T", bound="BackofficeUserOrgMembership")


@_attrs_define
class BackofficeUserOrgMembership:
    """
    Attributes:
        name (None | str): The organization name
        organization_id (UUID): The organization id
        role (OrganizationMembershipRole): The role to assign to the user
    """

    name: None | str
    organization_id: UUID
    role: OrganizationMembershipRole
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: None | str
        name = self.name

        organization_id = str(self.organization_id)

        role = self.role.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "organization_id": organization_id,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))

        organization_id = UUID(d.pop("organization_id"))

        role = OrganizationMembershipRole(d.pop("role"))

        backoffice_user_org_membership = cls(
            name=name,
            organization_id=organization_id,
            role=role,
        )

        backoffice_user_org_membership.additional_properties = d
        return backoffice_user_org_membership

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
