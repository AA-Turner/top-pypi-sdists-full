from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="RuntimeResourceCurrent")


@_attrs_define
class RuntimeResourceCurrent:
    """Current runtime resource allocation.

    Attributes:
        memory_mib (int): Current memory allocation in MiB.
        observed_disk_gib (int): Worker-observed overlay virtual capacity in GiB.
    """

    memory_mib: int
    observed_disk_gib: int

    def to_dict(self) -> dict[str, Any]:
        memory_mib = self.memory_mib

        observed_disk_gib = self.observed_disk_gib

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "memory_mib": memory_mib,
                "observed_disk_gib": observed_disk_gib,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        memory_mib = d.pop("memory_mib")

        observed_disk_gib = d.pop("observed_disk_gib")

        runtime_resource_current = cls(
            memory_mib=memory_mib,
            observed_disk_gib=observed_disk_gib,
        )

        return runtime_resource_current
