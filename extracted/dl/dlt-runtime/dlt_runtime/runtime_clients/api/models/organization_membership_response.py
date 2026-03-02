from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.organization_response import OrganizationResponse


T = TypeVar("T", bound="OrganizationMembershipResponse")


@_attrs_define
class OrganizationMembershipResponse:
    """
    Attributes:
        active (bool): Whether the membership is active
        identity_id (UUID): The ID of the organization member
        organization (OrganizationResponse): The user's personal organization (immutable)
        role (str): The role of the user in the organization
    """

    active: bool
    identity_id: UUID
    organization: "OrganizationResponse"
    role: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active = self.active

        identity_id = str(self.identity_id)

        organization = self.organization.to_dict()

        role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active": active,
                "identity_id": identity_id,
                "organization": organization,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_response import OrganizationResponse

        d = dict(src_dict)
        active = d.pop("active")

        identity_id = UUID(d.pop("identity_id"))

        organization = OrganizationResponse.from_dict(d.pop("organization"))

        role = d.pop("role")

        organization_membership_response = cls(
            active=active,
            identity_id=identity_id,
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
