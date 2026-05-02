from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InstanceGroupWithWorkspacesWorkspacesItem")


@_attrs_define
class InstanceGroupWithWorkspacesWorkspacesItem:
    """
    Attributes:
        workspace_id (Union[Unset, str]):
        workspace_name (Union[Unset, str]):
        role (Union[Unset, str]):
    """

    workspace_id: Union[Unset, str] = UNSET
    workspace_name: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        workspace_name = self.workspace_name
        role = self.role

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if workspace_name is not UNSET:
            field_dict["workspace_name"] = workspace_name
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id", UNSET)

        workspace_name = d.pop("workspace_name", UNSET)

        role = d.pop("role", UNSET)

        instance_group_with_workspaces_workspaces_item = cls(
            workspace_id=workspace_id,
            workspace_name=workspace_name,
            role=role,
        )

        instance_group_with_workspaces_workspaces_item.additional_properties = d
        return instance_group_with_workspaces_workspaces_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
