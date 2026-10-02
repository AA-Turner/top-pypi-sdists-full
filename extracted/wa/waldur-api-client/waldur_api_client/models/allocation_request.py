from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AllocationRequest")


@_attrs_define
class AllocationRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        description (Union[Unset, str]):
        node_limit (Union[Unset, int]):
        groupname (Union[None, Unset, str]):
    """

    name: str
    service_settings: str
    project: str
    description: Union[Unset, str] = UNSET
    node_limit: Union[Unset, int] = UNSET
    groupname: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        description = self.description

        node_limit = self.node_limit

        groupname: Union[None, Unset, str]
        if isinstance(self.groupname, Unset):
            groupname = UNSET
        else:
            groupname = self.groupname

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if node_limit is not UNSET:
            field_dict["node_limit"] = node_limit
        if groupname is not UNSET:
            field_dict["groupname"] = groupname

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        description = d.pop("description", UNSET)

        node_limit = d.pop("node_limit", UNSET)

        def _parse_groupname(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        groupname = _parse_groupname(d.pop("groupname", UNSET))

        allocation_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            description=description,
            node_limit=node_limit,
            groupname=groupname,
        )

        allocation_request.additional_properties = d
        return allocation_request

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
