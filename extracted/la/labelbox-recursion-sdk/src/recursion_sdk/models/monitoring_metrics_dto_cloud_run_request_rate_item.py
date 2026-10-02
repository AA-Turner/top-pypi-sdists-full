from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.monitoring_metrics_dto_cloud_run_request_rate_item_points_item import MonitoringMetricsDtoCloudRunRequestRateItemPointsItem





T = TypeVar("T", bound="MonitoringMetricsDtoCloudRunRequestRateItem")



@_attrs_define
class MonitoringMetricsDtoCloudRunRequestRateItem:
    """ A labelled monitoring time series.

        Attributes:
            label (str): Human-readable label identifying the series.
            points (list[MonitoringMetricsDtoCloudRunRequestRateItemPointsItem]): Ordered samples that make up the series,
                oldest first.
     """

    label: str
    points: list[MonitoringMetricsDtoCloudRunRequestRateItemPointsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.monitoring_metrics_dto_cloud_run_request_rate_item_points_item import MonitoringMetricsDtoCloudRunRequestRateItemPointsItem # noqa: PLC0415
        label = self.label

        points = []
        for points_item_data in self.points:
            points_item = points_item_data.to_dict()
            points.append(points_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "label": label,
            "points": points,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.monitoring_metrics_dto_cloud_run_request_rate_item_points_item import MonitoringMetricsDtoCloudRunRequestRateItemPointsItem # noqa: PLC0415
        d = dict(src_dict)
        label = d.pop("label")

        points = []
        _points = d.pop("points")
        for points_item_data in (_points):
            points_item = MonitoringMetricsDtoCloudRunRequestRateItemPointsItem.from_dict(points_item_data)



            points.append(points_item)


        monitoring_metrics_dto_cloud_run_request_rate_item = cls(
            label=label,
            points=points,
        )

        return monitoring_metrics_dto_cloud_run_request_rate_item

