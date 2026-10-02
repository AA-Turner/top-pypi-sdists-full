from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.monitoring_metrics_dto_time_range import MonitoringMetricsDtoTimeRange
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.monitoring_metrics_dto_cloud_run import MonitoringMetricsDtoCloudRun
  from ..models.monitoring_metrics_dto_cloud_sql import MonitoringMetricsDtoCloudSql





T = TypeVar("T", bound="MonitoringMetricsDto")



@_attrs_define
class MonitoringMetricsDto:
    """ Aggregated platform monitoring metrics across service and database infrastructure over a chosen time range.

        Attributes:
            time_range (MonitoringMetricsDtoTimeRange): Lookback window for monitoring queries.
            cloud_run (MonitoringMetricsDtoCloudRun): Service health metrics for the selected window.
            cloud_sql (MonitoringMetricsDtoCloudSql): Database health metrics for the selected window.
            truncated (bool | Unset): True if any underlying monitoring query was truncated; samples may be incomplete.
     """

    time_range: MonitoringMetricsDtoTimeRange
    cloud_run: MonitoringMetricsDtoCloudRun
    cloud_sql: MonitoringMetricsDtoCloudSql
    truncated: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.monitoring_metrics_dto_cloud_run import MonitoringMetricsDtoCloudRun # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_sql import MonitoringMetricsDtoCloudSql # noqa: PLC0415
        time_range = self.time_range.value

        cloud_run = self.cloud_run.to_dict()

        cloud_sql = self.cloud_sql.to_dict()

        truncated = self.truncated


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "timeRange": time_range,
            "cloudRun": cloud_run,
            "cloudSql": cloud_sql,
        })
        if truncated is not UNSET:
            field_dict["truncated"] = truncated

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.monitoring_metrics_dto_cloud_run import MonitoringMetricsDtoCloudRun # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_sql import MonitoringMetricsDtoCloudSql # noqa: PLC0415
        d = dict(src_dict)
        time_range = MonitoringMetricsDtoTimeRange(d.pop("timeRange"))




        cloud_run = MonitoringMetricsDtoCloudRun.from_dict(d.pop("cloudRun"))




        cloud_sql = MonitoringMetricsDtoCloudSql.from_dict(d.pop("cloudSql"))




        truncated = d.pop("truncated", UNSET)

        monitoring_metrics_dto = cls(
            time_range=time_range,
            cloud_run=cloud_run,
            cloud_sql=cloud_sql,
            truncated=truncated,
        )

        return monitoring_metrics_dto

