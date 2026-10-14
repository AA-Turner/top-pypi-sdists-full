from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InvitationExistingRole")


@_attrs_define
class InvitationExistingRole:
    """
    Attributes:
        email (str):
        role (UUID): UUID of the role requested for this email
        existing_role (UUID): UUID of the role the user already holds in the scope
        existing_role_name (str): Name of the role the user already holds in the scope
        existing_role_description (str): Human-readable description of the role the user already holds, for display.
            Falls back to the role name when the description is blank.
        is_same_role (bool): Whether the role already held is the one being requested. This reports what the scope
            currently holds, not the outcome of a grant: acceptance is decided per accepting user and also depends on the
            INVITATION_DISABLE_MULTIPLE_ROLES and ONLY_ONE_PROJECT_MANAGER settings.
    """

    email: str
    role: UUID
    existing_role: UUID
    existing_role_name: str
    existing_role_description: str
    is_same_role: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        role = str(self.role)

        existing_role = str(self.existing_role)

        existing_role_name = self.existing_role_name

        existing_role_description = self.existing_role_description

        is_same_role = self.is_same_role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "role": role,
                "existing_role": existing_role,
                "existing_role_name": existing_role_name,
                "existing_role_description": existing_role_description,
                "is_same_role": is_same_role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        role = UUID(d.pop("role"))

        existing_role = UUID(d.pop("existing_role"))

        existing_role_name = d.pop("existing_role_name")

        existing_role_description = d.pop("existing_role_description")

        is_same_role = d.pop("is_same_role")

        invitation_existing_role = cls(
            email=email,
            role=role,
            existing_role=existing_role,
            existing_role_name=existing_role_name,
            existing_role_description=existing_role_description,
            is_same_role=is_same_role,
        )

        invitation_existing_role.additional_properties = d
        return invitation_existing_role

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
