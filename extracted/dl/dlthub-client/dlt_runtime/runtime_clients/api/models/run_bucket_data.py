from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instance_usage import InstanceUsage
    from ..models.status_counts import StatusCounts


T = TypeVar("T", bound="RunBucketData")


@_attrs_define
class RunBucketData:
    """Bucket payload data

    Attributes:
        status_counts (StatusCounts): Breakdown by terminal run status
        total_duration_seconds (float): Weighted compute-seconds: sum of run durations scaled by each run's instance-
            size multiplier.
        total_runs (int): Number of runs that started in this bucket
        by_instance (list[InstanceUsage] | Unset): Per-instance-size split of this bucket; only populated sizes appear,
            unordered (the client orders for display).
    """

    status_counts: StatusCounts
    total_duration_seconds: float
    total_runs: int
    by_instance: list[InstanceUsage] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status_counts = self.status_counts.to_dict()

        total_duration_seconds = self.total_duration_seconds

        total_runs = self.total_runs

        by_instance: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.by_instance, Unset):
            by_instance = []
            for by_instance_item_data in self.by_instance:
                by_instance_item = by_instance_item_data.to_dict()
                by_instance.append(by_instance_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status_counts": status_counts,
                "total_duration_seconds": total_duration_seconds,
                "total_runs": total_runs,
            }
        )
        if by_instance is not UNSET:
            field_dict["by_instance"] = by_instance

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_usage import InstanceUsage
        from ..models.status_counts import StatusCounts

        d = dict(src_dict)
        status_counts = StatusCounts.from_dict(d.pop("status_counts"))

        total_duration_seconds = d.pop("total_duration_seconds")

        total_runs = d.pop("total_runs")

        _by_instance = d.pop("by_instance", UNSET)
        by_instance: list[InstanceUsage] | Unset = UNSET
        if _by_instance is not UNSET:
            by_instance = []
            for by_instance_item_data in _by_instance:
                by_instance_item = InstanceUsage.from_dict(by_instance_item_data)

                by_instance.append(by_instance_item)

        run_bucket_data = cls(
            status_counts=status_counts,
            total_duration_seconds=total_duration_seconds,
            total_runs=total_runs,
            by_instance=by_instance,
        )

        run_bucket_data.additional_properties = d
        return run_bucket_data

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
