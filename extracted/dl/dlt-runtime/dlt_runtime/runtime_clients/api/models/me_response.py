from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.organization_membership_response import OrganizationMembershipResponse
    from ..models.organization_response import OrganizationResponse
    from ..models.workspace_response import WorkspaceResponse
    from ..models.workspace_with_membership_response import (
        WorkspaceWithMembershipResponse,
    )


T = TypeVar("T", bound="MeResponse")


@_attrs_define
class MeResponse:
    """
    Attributes:
        email (str): The email of the current user
        identity_id (UUID): The ID of the current identity in the current organization.
        last_organization (OrganizationResponse): The user's personal organization (immutable)
        last_workspace (WorkspaceResponse): The most recently accessed workspace
        personal_organization (OrganizationResponse): The user's personal organization (immutable)
        primary_organization (OrganizationResponse): The user's personal organization (immutable)
        user_id (UUID): The ID of the current user
        organizations (Union[Unset, list['OrganizationMembershipResponse']]): All organizations the user is a member of
        workspaces (Union[Unset, list['WorkspaceWithMembershipResponse']]): All workspaces the user is a member of, with
            role and organization info
    """

    email: str
    identity_id: UUID
    last_organization: "OrganizationResponse"
    last_workspace: "WorkspaceResponse"
    personal_organization: "OrganizationResponse"
    primary_organization: "OrganizationResponse"
    user_id: UUID
    organizations: Union[Unset, list["OrganizationMembershipResponse"]] = UNSET
    workspaces: Union[Unset, list["WorkspaceWithMembershipResponse"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        identity_id = str(self.identity_id)

        last_organization = self.last_organization.to_dict()

        last_workspace = self.last_workspace.to_dict()

        personal_organization = self.personal_organization.to_dict()

        primary_organization = self.primary_organization.to_dict()

        user_id = str(self.user_id)

        organizations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.organizations, Unset):
            organizations = []
            for organizations_item_data in self.organizations:
                organizations_item = organizations_item_data.to_dict()
                organizations.append(organizations_item)

        workspaces: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.workspaces, Unset):
            workspaces = []
            for workspaces_item_data in self.workspaces:
                workspaces_item = workspaces_item_data.to_dict()
                workspaces.append(workspaces_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "identity_id": identity_id,
                "last_organization": last_organization,
                "last_workspace": last_workspace,
                "personal_organization": personal_organization,
                "primary_organization": primary_organization,
                "user_id": user_id,
            }
        )
        if organizations is not UNSET:
            field_dict["organizations"] = organizations
        if workspaces is not UNSET:
            field_dict["workspaces"] = workspaces

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_membership_response import (
            OrganizationMembershipResponse,
        )
        from ..models.organization_response import OrganizationResponse
        from ..models.workspace_response import WorkspaceResponse
        from ..models.workspace_with_membership_response import (
            WorkspaceWithMembershipResponse,
        )

        d = dict(src_dict)
        email = d.pop("email")

        identity_id = UUID(d.pop("identity_id"))

        last_organization = OrganizationResponse.from_dict(d.pop("last_organization"))

        last_workspace = WorkspaceResponse.from_dict(d.pop("last_workspace"))

        personal_organization = OrganizationResponse.from_dict(
            d.pop("personal_organization")
        )

        primary_organization = OrganizationResponse.from_dict(
            d.pop("primary_organization")
        )

        user_id = UUID(d.pop("user_id"))

        organizations = []
        _organizations = d.pop("organizations", UNSET)
        for organizations_item_data in _organizations or []:
            organizations_item = OrganizationMembershipResponse.from_dict(
                organizations_item_data
            )

            organizations.append(organizations_item)

        workspaces = []
        _workspaces = d.pop("workspaces", UNSET)
        for workspaces_item_data in _workspaces or []:
            workspaces_item = WorkspaceWithMembershipResponse.from_dict(
                workspaces_item_data
            )

            workspaces.append(workspaces_item)

        me_response = cls(
            email=email,
            identity_id=identity_id,
            last_organization=last_organization,
            last_workspace=last_workspace,
            personal_organization=personal_organization,
            primary_organization=primary_organization,
            user_id=user_id,
            organizations=organizations,
            workspaces=workspaces,
        )

        me_response.additional_properties = d
        return me_response

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
