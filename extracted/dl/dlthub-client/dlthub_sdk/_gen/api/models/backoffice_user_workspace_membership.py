from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_membership_role import WorkspaceMembershipRole

T = TypeVar("T", bound="BackofficeUserWorkspaceMembership")


@_attrs_define
class BackofficeUserWorkspaceMembership:
    """
    Attributes:
        name (str): The workspace name
        organization_id (UUID): The parent organization id
        role (WorkspaceMembershipRole): The role to assign to the user
        workspace_id (UUID): The workspace id
    """

    name: str
    organization_id: UUID
    role: WorkspaceMembershipRole
    workspace_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        organization_id = str(self.organization_id)

        role = self.role.value

        workspace_id = str(self.workspace_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "organization_id": organization_id,
                "role": role,
                "workspace_id": workspace_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        organization_id = UUID(d.pop("organization_id"))

        role = WorkspaceMembershipRole(d.pop("role"))

        workspace_id = UUID(d.pop("workspace_id"))

        backoffice_user_workspace_membership = cls(
            name=name,
            organization_id=organization_id,
            role=role,
            workspace_id=workspace_id,
        )

        backoffice_user_workspace_membership.additional_properties = d
        return backoffice_user_workspace_membership

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
