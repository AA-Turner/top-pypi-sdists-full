from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FlavorResponse")


@_attrs_define
class FlavorResponse:
    """
    Attributes:
        id (str):
        name (str):
        vcpus (int):
        ram (int): RAM in MB
        disk (int): Disk in GB
    """

    id: str
    name: str
    vcpus: int
    ram: int
    disk: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        vcpus = self.vcpus

        ram = self.ram

        disk = self.disk

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "vcpus": vcpus,
                "ram": ram,
                "disk": disk,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        vcpus = d.pop("vcpus")

        ram = d.pop("ram")

        disk = d.pop("disk")

        flavor_response = cls(
            id=id,
            name=name,
            vcpus=vcpus,
            ram=ram,
            disk=disk,
        )

        flavor_response.additional_properties = d
        return flavor_response

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
