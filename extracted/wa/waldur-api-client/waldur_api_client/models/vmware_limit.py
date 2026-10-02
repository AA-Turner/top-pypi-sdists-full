from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmwareLimit")


@_attrs_define
class VmwareLimit:
    """
    Attributes:
        max_cpu (int):
        max_cores_per_socket (int):
        max_ram (int):
        max_disk (int):
        max_disk_total (int):
    """

    max_cpu: int
    max_cores_per_socket: int
    max_ram: int
    max_disk: int
    max_disk_total: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_cpu = self.max_cpu

        max_cores_per_socket = self.max_cores_per_socket

        max_ram = self.max_ram

        max_disk = self.max_disk

        max_disk_total = self.max_disk_total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_cpu": max_cpu,
                "max_cores_per_socket": max_cores_per_socket,
                "max_ram": max_ram,
                "max_disk": max_disk,
                "max_disk_total": max_disk_total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_cpu = d.pop("max_cpu")

        max_cores_per_socket = d.pop("max_cores_per_socket")

        max_ram = d.pop("max_ram")

        max_disk = d.pop("max_disk")

        max_disk_total = d.pop("max_disk_total")

        vmware_limit = cls(
            max_cpu=max_cpu,
            max_cores_per_socket=max_cores_per_socket,
            max_ram=max_ram,
            max_disk=max_disk,
            max_disk_total=max_disk_total,
        )

        vmware_limit.additional_properties = d
        return vmware_limit

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
