from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerV2Usage")


@_attrs_define
class ContainerV2Usage:
    """
    Attributes:
        cpu_millis (int | Unset):
        memory_bytes (int | Unset):
        disk_bytes (int | Unset):
    """

    cpu_millis: int | Unset = UNSET
    memory_bytes: int | Unset = UNSET
    disk_bytes: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu_millis = self.cpu_millis

        memory_bytes = self.memory_bytes

        disk_bytes = self.disk_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cpu_millis is not UNSET:
            field_dict["cpu_millis"] = cpu_millis
        if memory_bytes is not UNSET:
            field_dict["memory_bytes"] = memory_bytes
        if disk_bytes is not UNSET:
            field_dict["disk_bytes"] = disk_bytes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cpu_millis = d.pop("cpu_millis", UNSET)

        memory_bytes = d.pop("memory_bytes", UNSET)

        disk_bytes = d.pop("disk_bytes", UNSET)

        container_v2_usage = cls(
            cpu_millis=cpu_millis,
            memory_bytes=memory_bytes,
            disk_bytes=disk_bytes,
        )

        container_v2_usage.additional_properties = d
        return container_v2_usage

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
