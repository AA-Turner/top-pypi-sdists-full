from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="Usage")


@_attrs_define
class Usage:
    """Current-period usage against the account's plan allotments.

    Attributes:
        period (str): The usage period this report covers, as `YYYY-MM` (UTC).
        runs_used (int): Runs metered so far this period.
        runs_included (int): Runs included in the plan this period (`-1` means unlimited).
        active_jobs (int): Number of permanent jobs (recurring and manual) counted against the plan's job limit.
        active_jobs_limit (int): Maximum permanent jobs the plan allows (`-1` means unlimited).
    """

    period: str
    runs_used: int
    runs_included: int
    active_jobs: int
    active_jobs_limit: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period

        runs_used = self.runs_used

        runs_included = self.runs_included

        active_jobs = self.active_jobs

        active_jobs_limit = self.active_jobs_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
                "runs_used": runs_used,
                "runs_included": runs_included,
                "active_jobs": active_jobs,
                "active_jobs_limit": active_jobs_limit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period = d.pop("period")

        runs_used = d.pop("runs_used")

        runs_included = d.pop("runs_included")

        active_jobs = d.pop("active_jobs")

        active_jobs_limit = d.pop("active_jobs_limit")

        usage = cls(
            period=period,
            runs_used=runs_used,
            runs_included=runs_included,
            active_jobs=active_jobs,
            active_jobs_limit=active_jobs_limit,
        )

        usage.additional_properties = d
        return usage

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
