from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MaintenanceStatsSummary")


@_attrs_define
class MaintenanceStatsSummary:
    """
    Attributes:
        total (int): Total number of maintenance announcements
        active (int): Number of currently active maintenances
        scheduled (int): Number of scheduled maintenances
        completed (int): Number of completed maintenances
        average_duration_hours (Union[None, float]): Average duration of completed maintenances in hours
        on_time_completion_rate (Union[None, float]): Percentage of maintenances completed on time
        on_time_rate_15min (Union[None, float]): Fraction (0-1) of completed maintenances that finished within 15
            minutes of their scheduled end
        avg_overrun_hours (Union[None, float]): Mean overrun in hours across completed maintenances that ran past their
            scheduled end
        emergency_count (int): Number of emergency-type maintenances in the window
    """

    total: int
    active: int
    scheduled: int
    completed: int
    average_duration_hours: Union[None, float]
    on_time_completion_rate: Union[None, float]
    on_time_rate_15min: Union[None, float]
    avg_overrun_hours: Union[None, float]
    emergency_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        active = self.active

        scheduled = self.scheduled

        completed = self.completed

        average_duration_hours: Union[None, float]
        average_duration_hours = self.average_duration_hours

        on_time_completion_rate: Union[None, float]
        on_time_completion_rate = self.on_time_completion_rate

        on_time_rate_15min: Union[None, float]
        on_time_rate_15min = self.on_time_rate_15min

        avg_overrun_hours: Union[None, float]
        avg_overrun_hours = self.avg_overrun_hours

        emergency_count = self.emergency_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "active": active,
                "scheduled": scheduled,
                "completed": completed,
                "average_duration_hours": average_duration_hours,
                "on_time_completion_rate": on_time_completion_rate,
                "on_time_rate_15min": on_time_rate_15min,
                "avg_overrun_hours": avg_overrun_hours,
                "emergency_count": emergency_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total = d.pop("total")

        active = d.pop("active")

        scheduled = d.pop("scheduled")

        completed = d.pop("completed")

        def _parse_average_duration_hours(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        average_duration_hours = _parse_average_duration_hours(d.pop("average_duration_hours"))

        def _parse_on_time_completion_rate(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        on_time_completion_rate = _parse_on_time_completion_rate(d.pop("on_time_completion_rate"))

        def _parse_on_time_rate_15min(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        on_time_rate_15min = _parse_on_time_rate_15min(d.pop("on_time_rate_15min"))

        def _parse_avg_overrun_hours(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        avg_overrun_hours = _parse_avg_overrun_hours(d.pop("avg_overrun_hours"))

        emergency_count = d.pop("emergency_count")

        maintenance_stats_summary = cls(
            total=total,
            active=active,
            scheduled=scheduled,
            completed=completed,
            average_duration_hours=average_duration_hours,
            on_time_completion_rate=on_time_completion_rate,
            on_time_rate_15min=on_time_rate_15min,
            avg_overrun_hours=avg_overrun_hours,
            emergency_count=emergency_count,
        )

        maintenance_stats_summary.additional_properties = d
        return maintenance_stats_summary

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
