from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.monitoring_metrics_dto_cloud_sql_active_connections_item import MonitoringMetricsDtoCloudSqlActiveConnectionsItem
  from ..models.monitoring_metrics_dto_cloud_sql_cpu_utilization_item import MonitoringMetricsDtoCloudSqlCpuUtilizationItem
  from ..models.monitoring_metrics_dto_cloud_sql_disk_utilization_item import MonitoringMetricsDtoCloudSqlDiskUtilizationItem





T = TypeVar("T", bound="MonitoringMetricsDtoCloudSql")



@_attrs_define
class MonitoringMetricsDtoCloudSql:
    """ Database health metrics for the selected window.

        Attributes:
            cpu_utilization (list[MonitoringMetricsDtoCloudSqlCpuUtilizationItem]): Database CPU utilization fraction per
                series.
            disk_utilization (list[MonitoringMetricsDtoCloudSqlDiskUtilizationItem]): Database disk utilization fraction per
                series.
            active_connections (list[MonitoringMetricsDtoCloudSqlActiveConnectionsItem]): Database active connection count
                per series.
     """

    cpu_utilization: list[MonitoringMetricsDtoCloudSqlCpuUtilizationItem]
    disk_utilization: list[MonitoringMetricsDtoCloudSqlDiskUtilizationItem]
    active_connections: list[MonitoringMetricsDtoCloudSqlActiveConnectionsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.monitoring_metrics_dto_cloud_sql_active_connections_item import MonitoringMetricsDtoCloudSqlActiveConnectionsItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_sql_cpu_utilization_item import MonitoringMetricsDtoCloudSqlCpuUtilizationItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_sql_disk_utilization_item import MonitoringMetricsDtoCloudSqlDiskUtilizationItem # noqa: PLC0415
        cpu_utilization = []
        for cpu_utilization_item_data in self.cpu_utilization:
            cpu_utilization_item = cpu_utilization_item_data.to_dict()
            cpu_utilization.append(cpu_utilization_item)



        disk_utilization = []
        for disk_utilization_item_data in self.disk_utilization:
            disk_utilization_item = disk_utilization_item_data.to_dict()
            disk_utilization.append(disk_utilization_item)



        active_connections = []
        for active_connections_item_data in self.active_connections:
            active_connections_item = active_connections_item_data.to_dict()
            active_connections.append(active_connections_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "cpuUtilization": cpu_utilization,
            "diskUtilization": disk_utilization,
            "activeConnections": active_connections,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.monitoring_metrics_dto_cloud_sql_active_connections_item import MonitoringMetricsDtoCloudSqlActiveConnectionsItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_sql_cpu_utilization_item import MonitoringMetricsDtoCloudSqlCpuUtilizationItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_sql_disk_utilization_item import MonitoringMetricsDtoCloudSqlDiskUtilizationItem # noqa: PLC0415
        d = dict(src_dict)
        cpu_utilization = []
        _cpu_utilization = d.pop("cpuUtilization")
        for cpu_utilization_item_data in (_cpu_utilization):
            cpu_utilization_item = MonitoringMetricsDtoCloudSqlCpuUtilizationItem.from_dict(cpu_utilization_item_data)



            cpu_utilization.append(cpu_utilization_item)


        disk_utilization = []
        _disk_utilization = d.pop("diskUtilization")
        for disk_utilization_item_data in (_disk_utilization):
            disk_utilization_item = MonitoringMetricsDtoCloudSqlDiskUtilizationItem.from_dict(disk_utilization_item_data)



            disk_utilization.append(disk_utilization_item)


        active_connections = []
        _active_connections = d.pop("activeConnections")
        for active_connections_item_data in (_active_connections):
            active_connections_item = MonitoringMetricsDtoCloudSqlActiveConnectionsItem.from_dict(active_connections_item_data)



            active_connections.append(active_connections_item)


        monitoring_metrics_dto_cloud_sql = cls(
            cpu_utilization=cpu_utilization,
            disk_utilization=disk_utilization,
            active_connections=active_connections,
        )

        return monitoring_metrics_dto_cloud_sql

