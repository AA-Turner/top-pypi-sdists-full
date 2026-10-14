from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metric_series_group import MetricSeriesGroup


T = TypeVar("T", bound="MetricSeriesResponse")


@_attrs_define
class MetricSeriesResponse:
    """
    Attributes:
        granularity (str):
        series (list['MetricSeriesGroup']):
    """

    granularity: str
    series: list["MetricSeriesGroup"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        granularity = self.granularity

        series = []
        for series_item_data in self.series:
            series_item = series_item_data.to_dict()
            series.append(series_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "granularity": granularity,
                "series": series,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_series_group import MetricSeriesGroup

        d = dict(src_dict)
        granularity = d.pop("granularity")

        series = []
        _series = d.pop("series")
        for series_item_data in _series:
            series_item = MetricSeriesGroup.from_dict(series_item_data)

            series.append(series_item)

        metric_series_response = cls(
            granularity=granularity,
            series=series,
        )

        metric_series_response.additional_properties = d
        return metric_series_response

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
