from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="RuntimeResourceLimits")


@_attrs_define
class RuntimeResourceLimits:
    """Runtime resource limits.

    Attributes:
        memory_mib (int): Maximum memory in MiB.
    """

    memory_mib: int

    def to_dict(self) -> dict[str, Any]:
        memory_mib = self.memory_mib

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "memory_mib": memory_mib,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        memory_mib = d.pop("memory_mib")

        runtime_resource_limits = cls(
            memory_mib=memory_mib,
        )

        return runtime_resource_limits
