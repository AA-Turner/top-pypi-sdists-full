from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="RuntimeResourceRequests")


@_attrs_define
class RuntimeResourceRequests:
    """Runtime resource requests.

    Attributes:
        memory_mib (int): Requested baseline memory in MiB.
        vcpus (int): Requested virtual CPUs.
        disk_gib (int): Target overlay virtual capacity in GiB.
    """

    memory_mib: int
    vcpus: int
    disk_gib: int

    def to_dict(self) -> dict[str, Any]:
        memory_mib = self.memory_mib

        vcpus = self.vcpus

        disk_gib = self.disk_gib

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "memory_mib": memory_mib,
                "vcpus": vcpus,
                "disk_gib": disk_gib,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        memory_mib = d.pop("memory_mib")

        vcpus = d.pop("vcpus")

        disk_gib = d.pop("disk_gib")

        runtime_resource_requests = cls(
            memory_mib=memory_mib,
            vcpus=vcpus,
            disk_gib=disk_gib,
        )

        return runtime_resource_requests
