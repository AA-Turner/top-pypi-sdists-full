from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instance_usage import InstanceUsage


T = TypeVar("T", bound="OrganizationLimitsResponse")


@_attrs_define
class OrganizationLimitsResponse:
    """
    Attributes:
        current_concurrent_runs (int): Non-terminal runs in flight right now.
        seconds_used_total (int): Weighted run-seconds consumed over the organization's lifetime; the figure enforcement
            compares against seconds_limit.
        by_instance (list[InstanceUsage] | Unset): Lifetime consumption split by instance size; weighted_seconds sums to
            seconds_used_total.
        max_concurrent_runs (int | None | Unset): Concurrent-run cap; null when unlimited.
        max_run_seconds (int | None | Unset): Per-run duration cap in seconds; null when unlimited.
        seconds_limit (int | None | Unset): Total lifetime run-seconds budget; null when unlimited.
    """

    current_concurrent_runs: int
    seconds_used_total: int
    by_instance: list[InstanceUsage] | Unset = UNSET
    max_concurrent_runs: int | None | Unset = UNSET
    max_run_seconds: int | None | Unset = UNSET
    seconds_limit: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_concurrent_runs = self.current_concurrent_runs

        seconds_used_total = self.seconds_used_total

        by_instance: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.by_instance, Unset):
            by_instance = []
            for by_instance_item_data in self.by_instance:
                by_instance_item = by_instance_item_data.to_dict()
                by_instance.append(by_instance_item)

        max_concurrent_runs: int | None | Unset
        if isinstance(self.max_concurrent_runs, Unset):
            max_concurrent_runs = UNSET
        else:
            max_concurrent_runs = self.max_concurrent_runs

        max_run_seconds: int | None | Unset
        if isinstance(self.max_run_seconds, Unset):
            max_run_seconds = UNSET
        else:
            max_run_seconds = self.max_run_seconds

        seconds_limit: int | None | Unset
        if isinstance(self.seconds_limit, Unset):
            seconds_limit = UNSET
        else:
            seconds_limit = self.seconds_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_concurrent_runs": current_concurrent_runs,
                "seconds_used_total": seconds_used_total,
            }
        )
        if by_instance is not UNSET:
            field_dict["by_instance"] = by_instance
        if max_concurrent_runs is not UNSET:
            field_dict["max_concurrent_runs"] = max_concurrent_runs
        if max_run_seconds is not UNSET:
            field_dict["max_run_seconds"] = max_run_seconds
        if seconds_limit is not UNSET:
            field_dict["seconds_limit"] = seconds_limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_usage import InstanceUsage

        d = dict(src_dict)
        current_concurrent_runs = d.pop("current_concurrent_runs")

        seconds_used_total = d.pop("seconds_used_total")

        _by_instance = d.pop("by_instance", UNSET)
        by_instance: list[InstanceUsage] | Unset = UNSET
        if _by_instance is not UNSET:
            by_instance = []
            for by_instance_item_data in _by_instance:
                by_instance_item = InstanceUsage.from_dict(by_instance_item_data)

                by_instance.append(by_instance_item)

        def _parse_max_concurrent_runs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_concurrent_runs = _parse_max_concurrent_runs(
            d.pop("max_concurrent_runs", UNSET)
        )

        def _parse_max_run_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_run_seconds = _parse_max_run_seconds(d.pop("max_run_seconds", UNSET))

        def _parse_seconds_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        seconds_limit = _parse_seconds_limit(d.pop("seconds_limit", UNSET))

        organization_limits_response = cls(
            current_concurrent_runs=current_concurrent_runs,
            seconds_used_total=seconds_used_total,
            by_instance=by_instance,
            max_concurrent_runs=max_concurrent_runs,
            max_run_seconds=max_run_seconds,
            seconds_limit=seconds_limit,
        )

        organization_limits_response.additional_properties = d
        return organization_limits_response

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
