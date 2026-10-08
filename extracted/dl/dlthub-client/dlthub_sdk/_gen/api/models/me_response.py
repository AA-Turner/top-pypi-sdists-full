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


T = TypeVar("T", bound="MeResponse")


@_attrs_define
class MeResponse:
    """
    Attributes:
        email (str): The email of the current user
        latest_organization (OrganizationResponse): The organization where new workspaces are created by default
        organization_membership_id (UUID): The ID of the current identity in the current organization.
        primary_organization (OrganizationResponse): The organization where new workspaces are created by default
        user_id (UUID): The ID of the current user
        latest_workspace (None | Unset | WorkspaceResponse): The most recently accessed workspace; null when the user's
            current organization has no workspaces
        name (None | str | Unset): The user's display name (full name), or null if the identity provider supplied none
        organization_memberships (list[OrganizationMembershipResponse] | Unset): All organizations the user is a member
            of
    """

    email: str
    latest_organization: OrganizationResponse
    organization_membership_id: UUID
    primary_organization: OrganizationResponse
    user_id: UUID
    latest_workspace: None | Unset | WorkspaceResponse = UNSET
    name: None | str | Unset = UNSET
    organization_memberships: list[OrganizationMembershipResponse] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.workspace_response import WorkspaceResponse

        email = self.email

        latest_organization = self.latest_organization.to_dict()

        organization_membership_id = str(self.organization_membership_id)

        primary_organization = self.primary_organization.to_dict()

        user_id = str(self.user_id)

        latest_workspace: dict[str, Any] | None | Unset
        if isinstance(self.latest_workspace, Unset):
            latest_workspace = UNSET
        elif isinstance(self.latest_workspace, WorkspaceResponse):
            latest_workspace = self.latest_workspace.to_dict()
        else:
            latest_workspace = self.latest_workspace

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        organization_memberships: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.organization_memberships, Unset):
            organization_memberships = []
            for organization_memberships_item_data in self.organization_memberships:
                organization_memberships_item = (
                    organization_memberships_item_data.to_dict()
                )
                organization_memberships.append(organization_memberships_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "latest_organization": latest_organization,
                "organization_membership_id": organization_membership_id,
                "primary_organization": primary_organization,
                "user_id": user_id,
            }
        )
        if latest_workspace is not UNSET:
            field_dict["latest_workspace"] = latest_workspace
        if name is not UNSET:
            field_dict["name"] = name
        if organization_memberships is not UNSET:
            field_dict["organization_memberships"] = organization_memberships

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

        latest_organization = OrganizationResponse.from_dict(
            d.pop("latest_organization")
        )

        organization_membership_id = UUID(d.pop("organization_membership_id"))

        primary_organization = OrganizationResponse.from_dict(
            d.pop("primary_organization")
        )

        user_id = UUID(d.pop("user_id"))

        def _parse_latest_workspace(data: object) -> None | Unset | WorkspaceResponse:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                latest_workspace_type_0 = WorkspaceResponse.from_dict(data)

                return latest_workspace_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | WorkspaceResponse, data)

        latest_workspace = _parse_latest_workspace(d.pop("latest_workspace", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        _organization_memberships = d.pop("organization_memberships", UNSET)
        organization_memberships: list[OrganizationMembershipResponse] | Unset = UNSET
        if _organization_memberships is not UNSET:
            organization_memberships = []
            for organization_memberships_item_data in _organization_memberships:
                organization_memberships_item = (
                    OrganizationMembershipResponse.from_dict(
                        organization_memberships_item_data
                    )
                )

                organization_memberships.append(organization_memberships_item)

        me_response = cls(
            email=email,
            latest_organization=latest_organization,
            organization_membership_id=organization_membership_id,
            primary_organization=primary_organization,
            user_id=user_id,
            latest_workspace=latest_workspace,
            name=name,
            organization_memberships=organization_memberships,
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
