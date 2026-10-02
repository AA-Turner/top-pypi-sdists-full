import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.severity_by_day_series import SeverityByDaySeries


T = TypeVar("T", bound="SeverityByDay")


@_attrs_define
class SeverityByDay:
    """
    Attributes:
        labels (list[datetime.date]):
        series (SeverityByDaySeries):
    """

    labels: list[datetime.date]
    series: "SeverityByDaySeries"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        labels = []
        for labels_item_data in self.labels:
            labels_item = labels_item_data.isoformat()
            labels.append(labels_item)

        series = self.series.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "labels": labels,
                "series": series,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.severity_by_day_series import SeverityByDaySeries

        d = dict(src_dict)
        labels = []
        _labels = d.pop("labels")
        for labels_item_data in _labels:
            labels_item = isoparse(labels_item_data).date()

            labels.append(labels_item)

        series = SeverityByDaySeries.from_dict(d.pop("series"))

        severity_by_day = cls(
            labels=labels,
            series=series,
        )

        severity_by_day.additional_properties = d
        return severity_by_day

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
