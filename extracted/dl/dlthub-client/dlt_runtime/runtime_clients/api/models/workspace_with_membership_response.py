from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.organization_response import OrganizationResponse
    from ..models.workspace_response import WorkspaceResponse


T = TypeVar("T", bound="WorkspaceWithMembershipResponse")


@_attrs_define
class WorkspaceWithMembershipResponse:
    """
    Attributes:
        organization (OrganizationResponse): The organization where new workspaces are created by default
        role (str): The role of the user in the workspace
        workspace (WorkspaceResponse):
    """

    organization: OrganizationResponse
    role: str
    workspace: WorkspaceResponse
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        organization = self.organization.to_dict()

        role = self.role

        workspace = self.workspace.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organization": organization,
                "role": role,
                "workspace": workspace,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_response import OrganizationResponse
        from ..models.workspace_response import WorkspaceResponse

        d = dict(src_dict)
        organization = OrganizationResponse.from_dict(d.pop("organization"))

        role = d.pop("role")

        workspace = WorkspaceResponse.from_dict(d.pop("workspace"))

        workspace_with_membership_response = cls(
            organization=organization,
            role=role,
            workspace=workspace,
        )

        workspace_with_membership_response.additional_properties = d
        return workspace_with_membership_response

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
