from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.organization_membership_role import OrganizationMembershipRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.organization_response import OrganizationResponse
    from ..models.workspace_membership_response import WorkspaceMembershipResponse


T = TypeVar("T", bound="OrganizationMeResponse")


@_attrs_define
class OrganizationMeResponse:
    """
    Attributes:
        email (str): The email of the current user
        organization (OrganizationResponse): The organization where new workspaces are created by default
        organization_membership_id (UUID): The ID of the organization member for this organization
        role (OrganizationMembershipRole | str): The role of the user in this organization
        user_id (UUID): The ID of the current user
        workspace_memberships (list[WorkspaceMembershipResponse] | Unset): Workspace memberships in this organization
            with role information
    """

    email: str
    organization: OrganizationResponse
    organization_membership_id: UUID
    role: OrganizationMembershipRole | str
    user_id: UUID
    workspace_memberships: list[WorkspaceMembershipResponse] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        organization = self.organization.to_dict()

        organization_membership_id = str(self.organization_membership_id)

        role: str
        if isinstance(self.role, OrganizationMembershipRole):
            role = self.role.value
        else:
            role = self.role

        user_id = str(self.user_id)

        workspace_memberships: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.workspace_memberships, Unset):
            workspace_memberships = []
            for workspace_memberships_item_data in self.workspace_memberships:
                workspace_memberships_item = workspace_memberships_item_data.to_dict()
                workspace_memberships.append(workspace_memberships_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "organization": organization,
                "organization_membership_id": organization_membership_id,
                "role": role,
                "user_id": user_id,
            }
        )
        if workspace_memberships is not UNSET:
            field_dict["workspace_memberships"] = workspace_memberships

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_response import OrganizationResponse
        from ..models.workspace_membership_response import WorkspaceMembershipResponse

        d = dict(src_dict)
        email = d.pop("email")

        organization = OrganizationResponse.from_dict(d.pop("organization"))

        organization_membership_id = UUID(d.pop("organization_membership_id"))

        def _parse_role(data: object) -> OrganizationMembershipRole | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_0 = OrganizationMembershipRole(data)

                return role_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(OrganizationMembershipRole | str, data)

        role = _parse_role(d.pop("role"))

        user_id = UUID(d.pop("user_id"))

        _workspace_memberships = d.pop("workspace_memberships", UNSET)
        workspace_memberships: list[WorkspaceMembershipResponse] | Unset = UNSET
        if _workspace_memberships is not UNSET:
            workspace_memberships = []
            for workspace_memberships_item_data in _workspace_memberships:
                workspace_memberships_item = WorkspaceMembershipResponse.from_dict(
                    workspace_memberships_item_data
                )

                workspace_memberships.append(workspace_memberships_item)

        organization_me_response = cls(
            email=email,
            organization=organization,
            organization_membership_id=organization_membership_id,
            role=role,
            user_id=user_id,
            workspace_memberships=workspace_memberships,
        )

        organization_me_response.additional_properties = d
        return organization_me_response

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
