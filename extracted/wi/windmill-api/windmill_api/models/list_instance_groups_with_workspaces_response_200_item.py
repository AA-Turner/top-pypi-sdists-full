from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_instance_groups_with_workspaces_response_200_item_workspaces_item import (
        ListInstanceGroupsWithWorkspacesResponse200ItemWorkspacesItem,
    )


T = TypeVar("T", bound="ListInstanceGroupsWithWorkspacesResponse200Item")


@_attrs_define
class ListInstanceGroupsWithWorkspacesResponse200Item:
    """
    Attributes:
        name (str):
        summary (Union[Unset, str]):
        emails (Union[Unset, List[str]]):
        workspaces (Union[Unset, List['ListInstanceGroupsWithWorkspacesResponse200ItemWorkspacesItem']]):
    """

    name: str
    summary: Union[Unset, str] = UNSET
    emails: Union[Unset, List[str]] = UNSET
    workspaces: Union[Unset, List["ListInstanceGroupsWithWorkspacesResponse200ItemWorkspacesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        summary = self.summary
        emails: Union[Unset, List[str]] = UNSET
        if not isinstance(self.emails, Unset):
            emails = self.emails

        workspaces: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.workspaces, Unset):
            workspaces = []
            for workspaces_item_data in self.workspaces:
                workspaces_item = workspaces_item_data.to_dict()

                workspaces.append(workspaces_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if emails is not UNSET:
            field_dict["emails"] = emails
        if workspaces is not UNSET:
            field_dict["workspaces"] = workspaces

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_instance_groups_with_workspaces_response_200_item_workspaces_item import (
            ListInstanceGroupsWithWorkspacesResponse200ItemWorkspacesItem,
        )

        d = src_dict.copy()
        name = d.pop("name")

        summary = d.pop("summary", UNSET)

        emails = cast(List[str], d.pop("emails", UNSET))

        workspaces = []
        _workspaces = d.pop("workspaces", UNSET)
        for workspaces_item_data in _workspaces or []:
            workspaces_item = ListInstanceGroupsWithWorkspacesResponse200ItemWorkspacesItem.from_dict(
                workspaces_item_data
            )

            workspaces.append(workspaces_item)

        list_instance_groups_with_workspaces_response_200_item = cls(
            name=name,
            summary=summary,
            emails=emails,
            workspaces=workspaces,
        )

        list_instance_groups_with_workspaces_response_200_item.additional_properties = d
        return list_instance_groups_with_workspaces_response_200_item

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
