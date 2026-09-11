from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.backoffice_user_org_membership import BackofficeUserOrgMembership
    from ..models.backoffice_user_workspace_membership import (
        BackofficeUserWorkspaceMembership,
    )


T = TypeVar("T", bound="BackofficeUserMembershipsResponse")


@_attrs_define
class BackofficeUserMembershipsResponse:
    """
    Attributes:
        organizations (list[BackofficeUserOrgMembership] | Unset): Organizations the user is a member of, with role.
        workspaces (list[BackofficeUserWorkspaceMembership] | Unset): Workspaces the user is a member of, with role and
            parent org.
    """

    organizations: list[BackofficeUserOrgMembership] | Unset = UNSET
    workspaces: list[BackofficeUserWorkspaceMembership] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        organizations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.organizations, Unset):
            organizations = []
            for organizations_item_data in self.organizations:
                organizations_item = organizations_item_data.to_dict()
                organizations.append(organizations_item)

        workspaces: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.workspaces, Unset):
            workspaces = []
            for workspaces_item_data in self.workspaces:
                workspaces_item = workspaces_item_data.to_dict()
                workspaces.append(workspaces_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if organizations is not UNSET:
            field_dict["organizations"] = organizations
        if workspaces is not UNSET:
            field_dict["workspaces"] = workspaces

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.backoffice_user_org_membership import BackofficeUserOrgMembership
        from ..models.backoffice_user_workspace_membership import (
            BackofficeUserWorkspaceMembership,
        )

        d = dict(src_dict)
        _organizations = d.pop("organizations", UNSET)
        organizations: list[BackofficeUserOrgMembership] | Unset = UNSET
        if _organizations is not UNSET:
            organizations = []
            for organizations_item_data in _organizations:
                organizations_item = BackofficeUserOrgMembership.from_dict(
                    organizations_item_data
                )

                organizations.append(organizations_item)

        _workspaces = d.pop("workspaces", UNSET)
        workspaces: list[BackofficeUserWorkspaceMembership] | Unset = UNSET
        if _workspaces is not UNSET:
            workspaces = []
            for workspaces_item_data in _workspaces:
                workspaces_item = BackofficeUserWorkspaceMembership.from_dict(
                    workspaces_item_data
                )

                workspaces.append(workspaces_item)

        backoffice_user_memberships_response = cls(
            organizations=organizations,
            workspaces=workspaces,
        )

        backoffice_user_memberships_response.additional_properties = d
        return backoffice_user_memberships_response

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
