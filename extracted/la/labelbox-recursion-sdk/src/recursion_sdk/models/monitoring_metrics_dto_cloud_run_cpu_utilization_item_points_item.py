from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="MonitoringMetricsDtoCloudRunCpuUtilizationItemPointsItem")



@_attrs_define
class MonitoringMetricsDtoCloudRunCpuUtilizationItemPointsItem:
    """ A single (timestamp, value) sample within a time series.

        Attributes:
            timestamp (str): Timestamp of the sample (ISO-8601, UTC) at the start of its bucket.
            value (float): Numeric value of the metric at this sample point. Example: 42.5.
     """

    timestamp: str
    value: float





    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp

        value = self.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "timestamp": timestamp,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = d.pop("timestamp")

        value = d.pop("value")

        monitoring_metrics_dto_cloud_run_cpu_utilization_item_points_item = cls(
            timestamp=timestamp,
            value=value,
        )

        return monitoring_metrics_dto_cloud_run_cpu_utilization_item_points_item

