from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RuntimeResourceLimits")


@_attrs_define
class RuntimeResourceLimits:
    """Runtime resource limits.

    Attributes:
        memory_mib (int): Maximum memory in MiB.
        vcpus (int | Unset): Maximum virtual CPUs. Omit to use the CPU request.
    """

    memory_mib: int
    vcpus: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        memory_mib = self.memory_mib

        vcpus = self.vcpus

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "memory_mib": memory_mib,
            }
        )
        if vcpus is not UNSET:
            field_dict["vcpus"] = vcpus

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        memory_mib = d.pop("memory_mib")

        vcpus = d.pop("vcpus", UNSET)

        runtime_resource_limits = cls(
            memory_mib=memory_mib,
            vcpus=vcpus,
        )

        return runtime_resource_limits
