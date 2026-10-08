from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.organization_membership_role import OrganizationMembershipRole

if TYPE_CHECKING:
    from ..models.organization_response import OrganizationResponse


T = TypeVar("T", bound="OrganizationMembershipResponse")


@_attrs_define
class OrganizationMembershipResponse:
    """
    Attributes:
        id (UUID): The ID of the organization membership
        is_active (bool): Whether the membership is active
        organization (OrganizationResponse): The organization where new workspaces are created by default
        role (OrganizationMembershipRole | str): The role of the user in the organization
    """

    id: UUID
    is_active: bool
    organization: OrganizationResponse
    role: OrganizationMembershipRole | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        is_active = self.is_active

        organization = self.organization.to_dict()

        role: str
        if isinstance(self.role, OrganizationMembershipRole):
            role = self.role.value
        else:
            role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "is_active": is_active,
                "organization": organization,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_response import OrganizationResponse

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        is_active = d.pop("is_active")

        organization = OrganizationResponse.from_dict(d.pop("organization"))

        def _parse_role(data: object) -> OrganizationMembershipRole | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_0 = OrganizationMembershipRole(data)

                return role_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(OrganizationMembershipRole | str, data)

        role = _parse_role(d.pop("role"))

        organization_membership_response = cls(
            id=id,
            is_active=is_active,
            organization=organization,
            role=role,
        )

        organization_membership_response.additional_properties = d
        return organization_membership_response

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
