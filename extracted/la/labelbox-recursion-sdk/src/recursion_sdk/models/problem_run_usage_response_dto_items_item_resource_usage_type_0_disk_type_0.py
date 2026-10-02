from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ProblemRunUsageResponseDtoItemsItemResourceUsageType0DiskType0")



@_attrs_define
class ProblemRunUsageResponseDtoItemsItemResourceUsageType0DiskType0:
    """ 
        Attributes:
            peak_used_bytes (float): Highest sampled workspace disk usage in bytes.
            capacity_bytes (float): Workspace disk capacity in bytes.
     """

    peak_used_bytes: float
    capacity_bytes: float





    def to_dict(self) -> dict[str, Any]:
        peak_used_bytes = self.peak_used_bytes

        capacity_bytes = self.capacity_bytes


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "peakUsedBytes": peak_used_bytes,
            "capacityBytes": capacity_bytes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        peak_used_bytes = d.pop("peakUsedBytes")

        capacity_bytes = d.pop("capacityBytes")

        problem_run_usage_response_dto_items_item_resource_usage_type_0_disk_type_0 = cls(
            peak_used_bytes=peak_used_bytes,
            capacity_bytes=capacity_bytes,
        )

        return problem_run_usage_response_dto_items_item_resource_usage_type_0_disk_type_0

