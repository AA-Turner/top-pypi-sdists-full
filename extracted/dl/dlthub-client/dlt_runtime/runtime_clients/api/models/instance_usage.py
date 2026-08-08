from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.usage_instance_bucket import UsageInstanceBucket

T = TypeVar("T", bound="InstanceUsage")


@_attrs_define
class InstanceUsage:
    """
    Attributes:
        bucket (UsageInstanceBucket): Instance-size bucket (unsized collects runs without a size)
        multiplier (int): Consumption weight for this size.
        runs (int): Number of runs in this size bucket
        wall_clock_seconds (float): Unweighted sum of run durations in this size bucket
        weighted_seconds (float): wall_clock_seconds scaled by multiplier; sums to the enclosing weighted total
    """

    bucket: UsageInstanceBucket
    multiplier: int
    runs: int
    wall_clock_seconds: float
    weighted_seconds: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bucket = self.bucket.value

        multiplier = self.multiplier

        runs = self.runs

        wall_clock_seconds = self.wall_clock_seconds

        weighted_seconds = self.weighted_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bucket": bucket,
                "multiplier": multiplier,
                "runs": runs,
                "wall_clock_seconds": wall_clock_seconds,
                "weighted_seconds": weighted_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bucket = UsageInstanceBucket(d.pop("bucket"))

        multiplier = d.pop("multiplier")

        runs = d.pop("runs")

        wall_clock_seconds = d.pop("wall_clock_seconds")

        weighted_seconds = d.pop("weighted_seconds")

        instance_usage = cls(
            bucket=bucket,
            multiplier=multiplier,
            runs=runs,
            wall_clock_seconds=wall_clock_seconds,
            weighted_seconds=weighted_seconds,
        )

        instance_usage.additional_properties = d
        return instance_usage

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
