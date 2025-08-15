from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instance_group_with_workspaces_workspaces_item import InstanceGroupWithWorkspacesWorkspacesItem


T = TypeVar("T", bound="InstanceGroupWithWorkspaces")


@_attrs_define
class InstanceGroupWithWorkspaces:
    """
    Attributes:
        name (str):
        summary (Union[Unset, str]):
        emails (Union[Unset, List[str]]):
        workspaces (Union[Unset, List['InstanceGroupWithWorkspacesWorkspacesItem']]):
    """

    name: str
    summary: Union[Unset, str] = UNSET
    emails: Union[Unset, List[str]] = UNSET
    workspaces: Union[Unset, List["InstanceGroupWithWorkspacesWorkspacesItem"]] = UNSET
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
        from ..models.instance_group_with_workspaces_workspaces_item import InstanceGroupWithWorkspacesWorkspacesItem

        d = src_dict.copy()
        name = d.pop("name")

        summary = d.pop("summary", UNSET)

        emails = cast(List[str], d.pop("emails", UNSET))

        workspaces = []
        _workspaces = d.pop("workspaces", UNSET)
        for workspaces_item_data in _workspaces or []:
            workspaces_item = InstanceGroupWithWorkspacesWorkspacesItem.from_dict(workspaces_item_data)

            workspaces.append(workspaces_item)

        instance_group_with_workspaces = cls(
            name=name,
            summary=summary,
            emails=emails,
            workspaces=workspaces,
        )

        instance_group_with_workspaces.additional_properties = d
        return instance_group_with_workspaces

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
