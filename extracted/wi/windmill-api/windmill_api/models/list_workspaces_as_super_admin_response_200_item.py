from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListWorkspacesAsSuperAdminResponse200Item")


@_attrs_define
class ListWorkspacesAsSuperAdminResponse200Item:
    """
    Attributes:
        id (str):
        name (str):
        owner (str):
        domain (Union[Unset, str]):
        color (Union[Unset, str]):
        parent_workspace_id (Union[Unset, None, str]):
    """

    id: str
    name: str
    owner: str
    domain: Union[Unset, str] = UNSET
    color: Union[Unset, str] = UNSET
    parent_workspace_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        owner = self.owner
        domain = self.domain
        color = self.color
        parent_workspace_id = self.parent_workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "owner": owner,
            }
        )
        if domain is not UNSET:
            field_dict["domain"] = domain
        if color is not UNSET:
            field_dict["color"] = color
        if parent_workspace_id is not UNSET:
            field_dict["parent_workspace_id"] = parent_workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        owner = d.pop("owner")

        domain = d.pop("domain", UNSET)

        color = d.pop("color", UNSET)

        parent_workspace_id = d.pop("parent_workspace_id", UNSET)

        list_workspaces_as_super_admin_response_200_item = cls(
            id=id,
            name=name,
            owner=owner,
            domain=domain,
            color=color,
            parent_workspace_id=parent_workspace_id,
        )

        list_workspaces_as_super_admin_response_200_item.additional_properties = d
        return list_workspaces_as_super_admin_response_200_item

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
