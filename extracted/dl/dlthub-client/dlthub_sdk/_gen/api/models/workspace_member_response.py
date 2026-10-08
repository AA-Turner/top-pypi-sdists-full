from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_membership_role import WorkspaceMembershipRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceMemberResponse")


@_attrs_define
class WorkspaceMemberResponse:
    """
    Attributes:
        email (str): The email of the user
        id (UUID): The ID of the workspace membership
        organization_membership_id (UUID): The ID of the member's organization membership, which `created_by` and
            `triggered_by` hold
        role (str | WorkspaceMembershipRole): The role of the user in the workspace
        user_id (UUID): The ID of the user
        name (None | str | Unset): Display name; null when the user has no name set.
    """

    email: str
    id: UUID
    organization_membership_id: UUID
    role: str | WorkspaceMembershipRole
    user_id: UUID
    name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        id = str(self.id)

        organization_membership_id = str(self.organization_membership_id)

        role: str
        if isinstance(self.role, WorkspaceMembershipRole):
            role = self.role.value
        else:
            role = self.role

        user_id = str(self.user_id)

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "id": id,
                "organization_membership_id": organization_membership_id,
                "role": role,
                "user_id": user_id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        id = UUID(d.pop("id"))

        organization_membership_id = UUID(d.pop("organization_membership_id"))

        def _parse_role(data: object) -> str | WorkspaceMembershipRole:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_0 = WorkspaceMembershipRole(data)

                return role_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | WorkspaceMembershipRole, data)

        role = _parse_role(d.pop("role"))

        user_id = UUID(d.pop("user_id"))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        workspace_member_response = cls(
            email=email,
            id=id,
            organization_membership_id=organization_membership_id,
            role=role,
            user_id=user_id,
            name=name,
        )

        workspace_member_response.additional_properties = d
        return workspace_member_response

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
