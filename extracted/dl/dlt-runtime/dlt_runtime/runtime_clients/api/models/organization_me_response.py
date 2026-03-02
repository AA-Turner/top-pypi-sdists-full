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
    from ..models.organization_response import OrganizationResponse
    from ..models.workspace_membership_response import WorkspaceMembershipResponse


T = TypeVar("T", bound="OrganizationMeResponse")


@_attrs_define
class OrganizationMeResponse:
    """
    Attributes:
        email (str): The email of the current user
        identity_id (UUID): The ID of the organization member for this organization
        organization (OrganizationResponse): The user's personal organization (immutable)
        role (str): The role of the user in this organization
        user_id (UUID): The ID of the current user
        workspaces (Union[Unset, list['WorkspaceMembershipResponse']]): Workspace memberships in this organization with
            role information
    """

    email: str
    identity_id: UUID
    organization: "OrganizationResponse"
    role: str
    user_id: UUID
    workspaces: Union[Unset, list["WorkspaceMembershipResponse"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        identity_id = str(self.identity_id)

        organization = self.organization.to_dict()

        role = self.role

        user_id = str(self.user_id)

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
                "organization": organization,
                "role": role,
                "user_id": user_id,
            }
        )
        if workspaces is not UNSET:
            field_dict["workspaces"] = workspaces

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_response import OrganizationResponse
        from ..models.workspace_membership_response import WorkspaceMembershipResponse

        d = dict(src_dict)
        email = d.pop("email")

        identity_id = UUID(d.pop("identity_id"))

        organization = OrganizationResponse.from_dict(d.pop("organization"))

        role = d.pop("role")

        user_id = UUID(d.pop("user_id"))

        workspaces = []
        _workspaces = d.pop("workspaces", UNSET)
        for workspaces_item_data in _workspaces or []:
            workspaces_item = WorkspaceMembershipResponse.from_dict(
                workspaces_item_data
            )

            workspaces.append(workspaces_item)

        organization_me_response = cls(
            email=email,
            identity_id=identity_id,
            organization=organization,
            role=role,
            user_id=user_id,
            workspaces=workspaces,
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
