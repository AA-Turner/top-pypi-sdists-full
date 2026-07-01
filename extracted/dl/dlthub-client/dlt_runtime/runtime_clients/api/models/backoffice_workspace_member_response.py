from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_membership_role import WorkspaceMembershipRole

T = TypeVar("T", bound="BackofficeWorkspaceMemberResponse")


@_attrs_define
class BackofficeWorkspaceMemberResponse:
    """
    Attributes:
        email (str): The member user's email
        role (WorkspaceMembershipRole): The role to assign to the user
        user_id (UUID): The member user's id
    """

    email: str
    role: WorkspaceMembershipRole
    user_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        role = self.role.value

        user_id = str(self.user_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "role": role,
                "user_id": user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        role = WorkspaceMembershipRole(d.pop("role"))

        user_id = UUID(d.pop("user_id"))

        backoffice_workspace_member_response = cls(
            email=email,
            role=role,
            user_id=user_id,
        )

        backoffice_workspace_member_response.additional_properties = d
        return backoffice_workspace_member_response

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
