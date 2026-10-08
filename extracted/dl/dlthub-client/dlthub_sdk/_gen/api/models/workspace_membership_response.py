from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_membership_role import WorkspaceMembershipRole

if TYPE_CHECKING:
    from ..models.workspace_response import WorkspaceResponse


T = TypeVar("T", bound="WorkspaceMembershipResponse")


@_attrs_define
class WorkspaceMembershipResponse:
    """
    Attributes:
        role (str | WorkspaceMembershipRole): The role of the user in the workspace
        workspace (WorkspaceResponse):
    """

    role: str | WorkspaceMembershipRole
    workspace: WorkspaceResponse
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role: str
        if isinstance(self.role, WorkspaceMembershipRole):
            role = self.role.value
        else:
            role = self.role

        workspace = self.workspace.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "workspace": workspace,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workspace_response import WorkspaceResponse

        d = dict(src_dict)

        def _parse_role(data: object) -> str | WorkspaceMembershipRole:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_0 = WorkspaceMembershipRole(data)

                return role_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | WorkspaceMembershipRole, data)

        role = _parse_role(d.pop("role"))

        workspace = WorkspaceResponse.from_dict(d.pop("workspace"))

        workspace_membership_response = cls(
            role=role,
            workspace=workspace,
        )

        workspace_membership_response.additional_properties = d
        return workspace_membership_response

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
