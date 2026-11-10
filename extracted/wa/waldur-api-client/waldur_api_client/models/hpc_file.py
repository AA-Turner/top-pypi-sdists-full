from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HpcFile")


@_attrs_define
class HpcFile:
    """
    Attributes:
        name (str):
        type_ (str): 'd' directory, '-' file, 'l' link
        user (str):
        group (str):
        permissions (str):
        last_modified (str):
        size (str):
        link_target (Union[None, Unset, str]):
    """

    name: str
    type_: str
    user: str
    group: str
    permissions: str
    last_modified: str
    size: str
    link_target: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_

        user = self.user

        group = self.group

        permissions = self.permissions

        last_modified = self.last_modified

        size = self.size

        link_target: Union[None, Unset, str]
        if isinstance(self.link_target, Unset):
            link_target = UNSET
        else:
            link_target = self.link_target

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type_,
                "user": user,
                "group": group,
                "permissions": permissions,
                "last_modified": last_modified,
                "size": size,
            }
        )
        if link_target is not UNSET:
            field_dict["link_target"] = link_target

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        type_ = d.pop("type")

        user = d.pop("user")

        group = d.pop("group")

        permissions = d.pop("permissions")

        last_modified = d.pop("last_modified")

        size = d.pop("size")

        def _parse_link_target(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        link_target = _parse_link_target(d.pop("link_target", UNSET))

        hpc_file = cls(
            name=name,
            type_=type_,
            user=user,
            group=group,
            permissions=permissions,
            last_modified=last_modified,
            size=size,
            link_target=link_target,
        )

        hpc_file.additional_properties = d
        return hpc_file

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
