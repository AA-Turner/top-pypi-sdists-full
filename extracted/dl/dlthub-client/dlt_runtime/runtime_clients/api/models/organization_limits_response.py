from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationLimitsResponse")


@_attrs_define
class OrganizationLimitsResponse:
    """
    Attributes:
        current_concurrent_runs (int): Non-terminal runs in flight right now.
        seconds_used_this_month (int): Run-seconds consumed since the start of the current UTC month.
        max_concurrent_runs (int | None | Unset): Concurrent-run cap; null when unlimited.
        max_run_seconds (int | None | Unset): Per-run duration cap in seconds; null when unlimited.
        max_seconds_per_month (int | None | Unset): Monthly run-seconds cap; null when unlimited.
    """

    current_concurrent_runs: int
    seconds_used_this_month: int
    max_concurrent_runs: int | None | Unset = UNSET
    max_run_seconds: int | None | Unset = UNSET
    max_seconds_per_month: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_concurrent_runs = self.current_concurrent_runs

        seconds_used_this_month = self.seconds_used_this_month

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

        max_seconds_per_month: int | None | Unset
        if isinstance(self.max_seconds_per_month, Unset):
            max_seconds_per_month = UNSET
        else:
            max_seconds_per_month = self.max_seconds_per_month

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_concurrent_runs": current_concurrent_runs,
                "seconds_used_this_month": seconds_used_this_month,
            }
        )
        if max_concurrent_runs is not UNSET:
            field_dict["max_concurrent_runs"] = max_concurrent_runs
        if max_run_seconds is not UNSET:
            field_dict["max_run_seconds"] = max_run_seconds
        if max_seconds_per_month is not UNSET:
            field_dict["max_seconds_per_month"] = max_seconds_per_month

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        current_concurrent_runs = d.pop("current_concurrent_runs")

        seconds_used_this_month = d.pop("seconds_used_this_month")

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

        def _parse_max_seconds_per_month(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_seconds_per_month = _parse_max_seconds_per_month(
            d.pop("max_seconds_per_month", UNSET)
        )

        organization_limits_response = cls(
            current_concurrent_runs=current_concurrent_runs,
            seconds_used_this_month=seconds_used_this_month,
            max_concurrent_runs=max_concurrent_runs,
            max_run_seconds=max_run_seconds,
            max_seconds_per_month=max_seconds_per_month,
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
