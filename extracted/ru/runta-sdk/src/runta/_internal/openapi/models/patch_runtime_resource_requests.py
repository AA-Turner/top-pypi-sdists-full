from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchRuntimeResourceRequests")


@_attrs_define
class PatchRuntimeResourceRequests:
    """Resource requests for runtime patching.

    Attributes:
        memory_mib (int | Unset): Requested baseline memory in MiB.
        disk_gib (int | Unset): New overlay capacity in GiB. Only growth while fully shutdown is supported.
    """

    memory_mib: int | Unset = UNSET
    disk_gib: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        memory_mib = self.memory_mib

        disk_gib = self.disk_gib

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if memory_mib is not UNSET:
            field_dict["memory_mib"] = memory_mib
        if disk_gib is not UNSET:
            field_dict["disk_gib"] = disk_gib

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        memory_mib = d.pop("memory_mib", UNSET)

        disk_gib = d.pop("disk_gib", UNSET)

        patch_runtime_resource_requests = cls(
            memory_mib=memory_mib,
            disk_gib=disk_gib,
        )

        return patch_runtime_resource_requests
