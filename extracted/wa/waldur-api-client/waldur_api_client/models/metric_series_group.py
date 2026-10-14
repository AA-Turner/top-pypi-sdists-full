from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metric_point_value import MetricPointValue
    from ..models.metric_series_group_attributes import MetricSeriesGroupAttributes


T = TypeVar("T", bound="MetricSeriesGroup")


@_attrs_define
class MetricSeriesGroup:
    """
    Attributes:
        attributes (MetricSeriesGroupAttributes):
        points (list['MetricPointValue']):
    """

    attributes: "MetricSeriesGroupAttributes"
    points: list["MetricPointValue"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attributes = self.attributes.to_dict()

        points = []
        for points_item_data in self.points:
            points_item = points_item_data.to_dict()
            points.append(points_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attributes": attributes,
                "points": points,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_point_value import MetricPointValue
        from ..models.metric_series_group_attributes import MetricSeriesGroupAttributes

        d = dict(src_dict)
        attributes = MetricSeriesGroupAttributes.from_dict(d.pop("attributes"))

        points = []
        _points = d.pop("points")
        for points_item_data in _points:
            points_item = MetricPointValue.from_dict(points_item_data)

            points.append(points_item)

        metric_series_group = cls(
            attributes=attributes,
            points=points,
        )

        metric_series_group.additional_properties = d
        return metric_series_group

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
