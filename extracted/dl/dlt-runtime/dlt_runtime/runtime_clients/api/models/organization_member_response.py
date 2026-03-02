from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OrganizationMemberResponse")


@_attrs_define
class OrganizationMemberResponse:
    """
    Attributes:
        email (str): The email of the user
        identity_id (UUID): The ID of the organization member
        role (str): The role of the user in the organization
        user_id (UUID): The ID of the user
    """

    email: str
    identity_id: UUID
    role: str
    user_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        identity_id = str(self.identity_id)

        role = self.role

        user_id = str(self.user_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "identity_id": identity_id,
                "role": role,
                "user_id": user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        identity_id = UUID(d.pop("identity_id"))

        role = d.pop("role")

        user_id = UUID(d.pop("user_id"))

        organization_member_response = cls(
            email=email,
            identity_id=identity_id,
            role=role,
            user_id=user_id,
        )

        organization_member_response.additional_properties = d
        return organization_member_response

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
