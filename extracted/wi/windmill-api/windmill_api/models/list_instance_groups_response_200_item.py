from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_instance_groups_response_200_item_instance_role import ListInstanceGroupsResponse200ItemInstanceRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListInstanceGroupsResponse200Item")


@_attrs_define
class ListInstanceGroupsResponse200Item:
    """
    Attributes:
        name (str):
        summary (Union[Unset, str]):
        emails (Union[Unset, List[str]]):
        instance_role (Union[Unset, None, ListInstanceGroupsResponse200ItemInstanceRole]):
    """

    name: str
    summary: Union[Unset, str] = UNSET
    emails: Union[Unset, List[str]] = UNSET
    instance_role: Union[Unset, None, ListInstanceGroupsResponse200ItemInstanceRole] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        summary = self.summary
        emails: Union[Unset, List[str]] = UNSET
        if not isinstance(self.emails, Unset):
            emails = self.emails

        instance_role: Union[Unset, None, str] = UNSET
        if not isinstance(self.instance_role, Unset):
            instance_role = self.instance_role.value if self.instance_role else None

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
        if instance_role is not UNSET:
            field_dict["instance_role"] = instance_role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        summary = d.pop("summary", UNSET)

        emails = cast(List[str], d.pop("emails", UNSET))

        _instance_role = d.pop("instance_role", UNSET)
        instance_role: Union[Unset, None, ListInstanceGroupsResponse200ItemInstanceRole]
        if _instance_role is None:
            instance_role = None
        elif isinstance(_instance_role, Unset):
            instance_role = UNSET
        else:
            instance_role = ListInstanceGroupsResponse200ItemInstanceRole(_instance_role)

        list_instance_groups_response_200_item = cls(
            name=name,
            summary=summary,
            emails=emails,
            instance_role=instance_role,
        )

        list_instance_groups_response_200_item.additional_properties = d
        return list_instance_groups_response_200_item

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
