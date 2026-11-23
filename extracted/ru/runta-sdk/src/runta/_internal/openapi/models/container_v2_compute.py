from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ContainerV2Compute")


@_attrs_define
class ContainerV2Compute:
    """
    Attributes:
        vcpus (int):
        memory_mib (int):
    """

    vcpus: int
    memory_mib: int

    def to_dict(self) -> dict[str, Any]:
        vcpus = self.vcpus

        memory_mib = self.memory_mib

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "vcpus": vcpus,
                "memory_mib": memory_mib,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vcpus = d.pop("vcpus")

        memory_mib = d.pop("memory_mib")

        container_v2_compute = cls(
            vcpus=vcpus,
            memory_mib=memory_mib,
        )

        return container_v2_compute
