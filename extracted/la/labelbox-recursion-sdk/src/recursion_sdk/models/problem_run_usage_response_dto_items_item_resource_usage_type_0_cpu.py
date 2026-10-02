from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ProblemRunUsageResponseDtoItemsItemResourceUsageType0Cpu")



@_attrs_define
class ProblemRunUsageResponseDtoItemsItemResourceUsageType0Cpu:
    """ CPU consumed against what was requested.

        Attributes:
            avg_millicores (float): Interval-weighted mean CPU in millicores; 1000 is one core fully busy.
            peak_millicores (float): Highest sampled CPU in millicores.
            capacity_millicores (float | None): CPU the container was granted (its cgroup limit) — the requested amount.
                Null when the runner could not read a limit.
            core_seconds (float): Total CPU time consumed: the integral of cores over the sampled interval.
     """

    avg_millicores: float
    peak_millicores: float
    capacity_millicores: float | None
    core_seconds: float





    def to_dict(self) -> dict[str, Any]:
        avg_millicores = self.avg_millicores

        peak_millicores = self.peak_millicores

        capacity_millicores: float | None
        capacity_millicores = self.capacity_millicores

        core_seconds = self.core_seconds


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "avgMillicores": avg_millicores,
            "peakMillicores": peak_millicores,
            "capacityMillicores": capacity_millicores,
            "coreSeconds": core_seconds,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        avg_millicores = d.pop("avgMillicores")

        peak_millicores = d.pop("peakMillicores")

        def _parse_capacity_millicores(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        capacity_millicores = _parse_capacity_millicores(d.pop("capacityMillicores"))


        core_seconds = d.pop("coreSeconds")

        problem_run_usage_response_dto_items_item_resource_usage_type_0_cpu = cls(
            avg_millicores=avg_millicores,
            peak_millicores=peak_millicores,
            capacity_millicores=capacity_millicores,
            core_seconds=core_seconds,
        )

        return problem_run_usage_response_dto_items_item_resource_usage_type_0_cpu

