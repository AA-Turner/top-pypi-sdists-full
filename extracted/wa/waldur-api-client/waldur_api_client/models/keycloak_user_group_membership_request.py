from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="KeycloakUserGroupMembershipRequest")


@_attrs_define
class KeycloakUserGroupMembershipRequest:
    """
    Attributes:
        username (str): Keycloak user username
        email (str): User's email for notifications
        scope_uuid (UUID): UUID of a cluster or a project in Rancher
        role (str):
    """

    username: str
    email: str
    scope_uuid: UUID
    role: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        email = self.email

        scope_uuid = str(self.scope_uuid)

        role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "email": email,
                "scope_uuid": scope_uuid,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username")

        email = d.pop("email")

        scope_uuid = UUID(d.pop("scope_uuid"))

        role = d.pop("role")

        keycloak_user_group_membership_request = cls(
            username=username,
            email=email,
            scope_uuid=scope_uuid,
            role=role,
        )

        keycloak_user_group_membership_request.additional_properties = d
        return keycloak_user_group_membership_request

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
