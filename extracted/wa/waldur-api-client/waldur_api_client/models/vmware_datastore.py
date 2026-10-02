from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmwareDatastore")


@_attrs_define
class VmwareDatastore:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        type_ (str):
        capacity (Union[None, Unset, int]): Capacity, in MB.
        free_space (Union[None, Unset, int]): Available space, in MB.
    """

    url: str
    uuid: UUID
    name: str
    type_: str
    capacity: Union[None, Unset, int] = UNSET
    free_space: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        type_ = self.type_

        capacity: Union[None, Unset, int]
        if isinstance(self.capacity, Unset):
            capacity = UNSET
        else:
            capacity = self.capacity

        free_space: Union[None, Unset, int]
        if isinstance(self.free_space, Unset):
            free_space = UNSET
        else:
            free_space = self.free_space

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "type": type_,
            }
        )
        if capacity is not UNSET:
            field_dict["capacity"] = capacity
        if free_space is not UNSET:
            field_dict["free_space"] = free_space

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        type_ = d.pop("type")

        def _parse_capacity(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        capacity = _parse_capacity(d.pop("capacity", UNSET))

        def _parse_free_space(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        free_space = _parse_free_space(d.pop("free_space", UNSET))

        vmware_datastore = cls(
            url=url,
            uuid=uuid,
            name=name,
            type_=type_,
            capacity=capacity,
            free_space=free_space,
        )

        vmware_datastore.additional_properties = d
        return vmware_datastore

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
