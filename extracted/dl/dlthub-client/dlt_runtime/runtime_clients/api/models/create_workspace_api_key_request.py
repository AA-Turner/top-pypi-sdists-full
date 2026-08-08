from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_membership_role import WorkspaceMembershipRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWorkspaceApiKeyRequest")


@_attrs_define
class CreateWorkspaceApiKeyRequest:
    """
    Attributes:
        name (str): A user-provided label for the API key
        expires_in_days (int | Unset): Number of days until the key expires Default: 90.
        role (WorkspaceMembershipRole | Unset): The role to assign to the user
    """

    name: str
    expires_in_days: int | Unset = 90
    role: WorkspaceMembershipRole | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        expires_in_days = self.expires_in_days

        role: str | Unset = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if expires_in_days is not UNSET:
            field_dict["expires_in_days"] = expires_in_days
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        expires_in_days = d.pop("expires_in_days", UNSET)

        _role = d.pop("role", UNSET)
        role: WorkspaceMembershipRole | Unset
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = WorkspaceMembershipRole(_role)

        create_workspace_api_key_request = cls(
            name=name,
            expires_in_days=expires_in_days,
            role=role,
        )

        create_workspace_api_key_request.additional_properties = d
        return create_workspace_api_key_request

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
