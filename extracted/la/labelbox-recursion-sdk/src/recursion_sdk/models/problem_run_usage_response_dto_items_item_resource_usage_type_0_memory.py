from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ProblemRunUsageResponseDtoItemsItemResourceUsageType0Memory")



@_attrs_define
class ProblemRunUsageResponseDtoItemsItemResourceUsageType0Memory:
    """ Memory consumed against what was requested.

        Attributes:
            avg_working_set_bytes (float): Interval-weighted mean working-set memory in bytes.
            peak_working_set_bytes (float): Highest sampled working-set memory in bytes.
            capacity_bytes (float | None): Memory the container was granted (its cgroup limit) — the requested amount. Null
                when the runner could not read a limit.
     """

    avg_working_set_bytes: float
    peak_working_set_bytes: float
    capacity_bytes: float | None





    def to_dict(self) -> dict[str, Any]:
        avg_working_set_bytes = self.avg_working_set_bytes

        peak_working_set_bytes = self.peak_working_set_bytes

        capacity_bytes: float | None
        capacity_bytes = self.capacity_bytes


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "avgWorkingSetBytes": avg_working_set_bytes,
            "peakWorkingSetBytes": peak_working_set_bytes,
            "capacityBytes": capacity_bytes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        avg_working_set_bytes = d.pop("avgWorkingSetBytes")

        peak_working_set_bytes = d.pop("peakWorkingSetBytes")

        def _parse_capacity_bytes(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        capacity_bytes = _parse_capacity_bytes(d.pop("capacityBytes"))


        problem_run_usage_response_dto_items_item_resource_usage_type_0_memory = cls(
            avg_working_set_bytes=avg_working_set_bytes,
            peak_working_set_bytes=peak_working_set_bytes,
            capacity_bytes=capacity_bytes,
        )

        return problem_run_usage_response_dto_items_item_resource_usage_type_0_memory

