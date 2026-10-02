from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ProblemRunUsageResponseDtoItemsItemResourceUsageType0GpuType0")



@_attrs_define
class ProblemRunUsageResponseDtoItemsItemResourceUsageType0GpuType0:
    """ 
        Attributes:
            count (float): GPUs visible to the container.
            avg_utilization_percent (float): Interval-weighted mean GPU utilization, 0-100.
            peak_utilization_percent (float): Highest sampled GPU utilization, 0-100.
            peak_memory_used_bytes (float): Highest sampled GPU memory in use.
            memory_total_bytes (float): Total GPU memory across the visible devices.
     """

    count: float
    avg_utilization_percent: float
    peak_utilization_percent: float
    peak_memory_used_bytes: float
    memory_total_bytes: float





    def to_dict(self) -> dict[str, Any]:
        count = self.count

        avg_utilization_percent = self.avg_utilization_percent

        peak_utilization_percent = self.peak_utilization_percent

        peak_memory_used_bytes = self.peak_memory_used_bytes

        memory_total_bytes = self.memory_total_bytes


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "count": count,
            "avgUtilizationPercent": avg_utilization_percent,
            "peakUtilizationPercent": peak_utilization_percent,
            "peakMemoryUsedBytes": peak_memory_used_bytes,
            "memoryTotalBytes": memory_total_bytes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        avg_utilization_percent = d.pop("avgUtilizationPercent")

        peak_utilization_percent = d.pop("peakUtilizationPercent")

        peak_memory_used_bytes = d.pop("peakMemoryUsedBytes")

        memory_total_bytes = d.pop("memoryTotalBytes")

        problem_run_usage_response_dto_items_item_resource_usage_type_0_gpu_type_0 = cls(
            count=count,
            avg_utilization_percent=avg_utilization_percent,
            peak_utilization_percent=peak_utilization_percent,
            peak_memory_used_bytes=peak_memory_used_bytes,
            memory_total_bytes=memory_total_bytes,
        )

        return problem_run_usage_response_dto_items_item_resource_usage_type_0_gpu_type_0

