from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.interval_minutes_enum import IntervalMinutesEnum

T = TypeVar("T", bound="InstanceMetricsFasterUpdatesRequest")


@_attrs_define
class InstanceMetricsFasterUpdatesRequest:
    """
    Attributes:
        interval_minutes (IntervalMinutesEnum):
        hours (int):
    """

    interval_minutes: IntervalMinutesEnum
    hours: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        interval_minutes = self.interval_minutes.value

        hours = self.hours

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "interval_minutes": interval_minutes,
                "hours": hours,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        interval_minutes = IntervalMinutesEnum(d.pop("interval_minutes"))

        hours = d.pop("hours")

        instance_metrics_faster_updates_request = cls(
            interval_minutes=interval_minutes,
            hours=hours,
        )

        instance_metrics_faster_updates_request.additional_properties = d
        return instance_metrics_faster_updates_request

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
