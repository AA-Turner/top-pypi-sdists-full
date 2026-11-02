from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ColdRestoreResourceRequests")


@_attrs_define
class ColdRestoreResourceRequests:
    """CPU and baseline memory for a cold checkpoint restore.

    Attributes:
        memory_mib (int): Baseline memory in MiB. This becomes the restored runtime's current memory. It may be smaller
            or larger than the checkpoint.
        vcpus (int): Virtual CPUs for the restored runtime. This may be smaller or larger than the checkpoint.
    """

    memory_mib: int
    vcpus: int

    def to_dict(self) -> dict[str, Any]:
        memory_mib = self.memory_mib

        vcpus = self.vcpus

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "memory_mib": memory_mib,
                "vcpus": vcpus,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        memory_mib = d.pop("memory_mib")

        vcpus = d.pop("vcpus")

        cold_restore_resource_requests = cls(
            memory_mib=memory_mib,
            vcpus=vcpus,
        )

        return cold_restore_resource_requests
