from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.organization_membership_response import OrganizationMembershipResponse
    from ..models.organization_response import OrganizationResponse
    from ..models.workspace_response import WorkspaceResponse


T = TypeVar("T", bound="CurrentUserResponse")


@_attrs_define
class CurrentUserResponse:
    """
    Attributes:
        email (str): The email of the current user
        identity_id (UUID): The ID of the current identity in the current organization.
        last_organization (OrganizationResponse): The organization where new workspaces are created by default
        primary_organization (OrganizationResponse): The organization where new workspaces are created by default
        user_id (UUID): The ID of the current user
        last_workspace (None | Unset | WorkspaceResponse): The most recently accessed workspace; null when the user's
            current organization has no workspaces
        name (None | str | Unset): The user's display name (full name), or null if the identity provider supplied none
        organizations (list[OrganizationMembershipResponse] | Unset): All organizations the user is a member of
    """

    email: str
    identity_id: UUID
    last_organization: OrganizationResponse
    primary_organization: OrganizationResponse
    user_id: UUID
    last_workspace: None | Unset | WorkspaceResponse = UNSET
    name: None | str | Unset = UNSET
    organizations: list[OrganizationMembershipResponse] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.workspace_response import WorkspaceResponse

        email = self.email

        identity_id = str(self.identity_id)

        last_organization = self.last_organization.to_dict()

        primary_organization = self.primary_organization.to_dict()

        user_id = str(self.user_id)

        last_workspace: dict[str, Any] | None | Unset
        if isinstance(self.last_workspace, Unset):
            last_workspace = UNSET
        elif isinstance(self.last_workspace, WorkspaceResponse):
            last_workspace = self.last_workspace.to_dict()
        else:
            last_workspace = self.last_workspace

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        organizations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.organizations, Unset):
            organizations = []
            for organizations_item_data in self.organizations:
                organizations_item = organizations_item_data.to_dict()
                organizations.append(organizations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "identity_id": identity_id,
                "last_organization": last_organization,
                "primary_organization": primary_organization,
                "user_id": user_id,
            }
        )
        if last_workspace is not UNSET:
            field_dict["last_workspace"] = last_workspace
        if name is not UNSET:
            field_dict["name"] = name
        if organizations is not UNSET:
            field_dict["organizations"] = organizations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_membership_response import (
            OrganizationMembershipResponse,
        )
        from ..models.organization_response import OrganizationResponse
        from ..models.workspace_response import WorkspaceResponse

        d = dict(src_dict)
        email = d.pop("email")

        identity_id = UUID(d.pop("identity_id"))

        last_organization = OrganizationResponse.from_dict(d.pop("last_organization"))

        primary_organization = OrganizationResponse.from_dict(
            d.pop("primary_organization")
        )

        user_id = UUID(d.pop("user_id"))

        def _parse_last_workspace(data: object) -> None | Unset | WorkspaceResponse:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_workspace_type_0 = WorkspaceResponse.from_dict(data)

                return last_workspace_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | WorkspaceResponse, data)

        last_workspace = _parse_last_workspace(d.pop("last_workspace", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        _organizations = d.pop("organizations", UNSET)
        organizations: list[OrganizationMembershipResponse] | Unset = UNSET
        if _organizations is not UNSET:
            organizations = []
            for organizations_item_data in _organizations:
                organizations_item = OrganizationMembershipResponse.from_dict(
                    organizations_item_data
                )

                organizations.append(organizations_item)

        current_user_response = cls(
            email=email,
            identity_id=identity_id,
            last_organization=last_organization,
            primary_organization=primary_organization,
            user_id=user_id,
            last_workspace=last_workspace,
            name=name,
            organizations=organizations,
        )

        current_user_response.additional_properties = d
        return current_user_response

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
