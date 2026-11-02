from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateRuntimeResourceRequests")


@_attrs_define
class CreateRuntimeResourceRequests:
    """Resource requests for runtime creation.

    Attributes:
        memory_mib (int | Unset): Requested baseline memory in MiB. Default: 1024.
        vcpus (int | Unset): Requested virtual CPUs. Default: 1.
        disk_gib (int | Unset): Requested overlay virtual capacity in GiB.
    """

    memory_mib: int | Unset = 1024
    vcpus: int | Unset = 1
    disk_gib: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        memory_mib = self.memory_mib

        vcpus = self.vcpus

        disk_gib = self.disk_gib

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if memory_mib is not UNSET:
            field_dict["memory_mib"] = memory_mib
        if vcpus is not UNSET:
            field_dict["vcpus"] = vcpus
        if disk_gib is not UNSET:
            field_dict["disk_gib"] = disk_gib

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        memory_mib = d.pop("memory_mib", UNSET)

        vcpus = d.pop("vcpus", UNSET)

        disk_gib = d.pop("disk_gib", UNSET)

        create_runtime_resource_requests = cls(
            memory_mib=memory_mib,
            vcpus=vcpus,
            disk_gib=disk_gib,
        )

        return create_runtime_resource_requests
