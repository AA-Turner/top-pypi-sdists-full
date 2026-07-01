from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.organization_response import OrganizationResponse
    from ..models.workspace_response import WorkspaceResponse


T = TypeVar("T", bound="WorkspaceMeResponse")


@_attrs_define
class WorkspaceMeResponse:
    """
    Attributes:
        email (str): The email of the current user
        organization (OrganizationResponse): The organization where new workspaces are created by default
        organization_identity_id (UUID): The ID of the organization member in the parent organization
        organization_role (str): The role of the user in the parent organization
        user_id (UUID): The ID of the current user
        workspace (WorkspaceResponse):
        workspace_role (str): The role of the user in this workspace
    """

    email: str
    organization: OrganizationResponse
    organization_identity_id: UUID
    organization_role: str
    user_id: UUID
    workspace: WorkspaceResponse
    workspace_role: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        organization = self.organization.to_dict()

        organization_identity_id = str(self.organization_identity_id)

        organization_role = self.organization_role

        user_id = str(self.user_id)

        workspace = self.workspace.to_dict()

        workspace_role = self.workspace_role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "organization": organization,
                "organization_identity_id": organization_identity_id,
                "organization_role": organization_role,
                "user_id": user_id,
                "workspace": workspace,
                "workspace_role": workspace_role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_response import OrganizationResponse
        from ..models.workspace_response import WorkspaceResponse

        d = dict(src_dict)
        email = d.pop("email")

        organization = OrganizationResponse.from_dict(d.pop("organization"))

        organization_identity_id = UUID(d.pop("organization_identity_id"))

        organization_role = d.pop("organization_role")

        user_id = UUID(d.pop("user_id"))

        workspace = WorkspaceResponse.from_dict(d.pop("workspace"))

        workspace_role = d.pop("workspace_role")

        workspace_me_response = cls(
            email=email,
            organization=organization,
            organization_identity_id=organization_identity_id,
            organization_role=organization_role,
            user_id=user_id,
            workspace=workspace,
            workspace_role=workspace_role,
        )

        workspace_me_response.additional_properties = d
        return workspace_me_response

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
