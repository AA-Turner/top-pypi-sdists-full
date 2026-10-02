from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.monitoring_metrics_dto_cloud_run_cpu_utilization_item import MonitoringMetricsDtoCloudRunCpuUtilizationItem
  from ..models.monitoring_metrics_dto_cloud_run_instance_count_item import MonitoringMetricsDtoCloudRunInstanceCountItem
  from ..models.monitoring_metrics_dto_cloud_run_latency_percentiles_item import MonitoringMetricsDtoCloudRunLatencyPercentilesItem
  from ..models.monitoring_metrics_dto_cloud_run_memory_utilization_item import MonitoringMetricsDtoCloudRunMemoryUtilizationItem
  from ..models.monitoring_metrics_dto_cloud_run_request_rate_item import MonitoringMetricsDtoCloudRunRequestRateItem





T = TypeVar("T", bound="MonitoringMetricsDtoCloudRun")



@_attrs_define
class MonitoringMetricsDtoCloudRun:
    """ Service health metrics for the selected window.

        Attributes:
            request_rate (list[MonitoringMetricsDtoCloudRunRequestRateItem]): Service request rate in requests per second,
                per series.
            latency_percentiles (list[MonitoringMetricsDtoCloudRunLatencyPercentilesItem]): Service latency percentiles per
                series.
            instance_count (list[MonitoringMetricsDtoCloudRunInstanceCountItem]): Number of active service instances per
                series.
            cpu_utilization (list[MonitoringMetricsDtoCloudRunCpuUtilizationItem]): Service CPU utilization fraction per
                series.
            memory_utilization (list[MonitoringMetricsDtoCloudRunMemoryUtilizationItem]): Service memory utilization
                fraction per series.
     """

    request_rate: list[MonitoringMetricsDtoCloudRunRequestRateItem]
    latency_percentiles: list[MonitoringMetricsDtoCloudRunLatencyPercentilesItem]
    instance_count: list[MonitoringMetricsDtoCloudRunInstanceCountItem]
    cpu_utilization: list[MonitoringMetricsDtoCloudRunCpuUtilizationItem]
    memory_utilization: list[MonitoringMetricsDtoCloudRunMemoryUtilizationItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.monitoring_metrics_dto_cloud_run_cpu_utilization_item import MonitoringMetricsDtoCloudRunCpuUtilizationItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_run_instance_count_item import MonitoringMetricsDtoCloudRunInstanceCountItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_run_latency_percentiles_item import MonitoringMetricsDtoCloudRunLatencyPercentilesItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_run_memory_utilization_item import MonitoringMetricsDtoCloudRunMemoryUtilizationItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_run_request_rate_item import MonitoringMetricsDtoCloudRunRequestRateItem # noqa: PLC0415
        request_rate = []
        for request_rate_item_data in self.request_rate:
            request_rate_item = request_rate_item_data.to_dict()
            request_rate.append(request_rate_item)



        latency_percentiles = []
        for latency_percentiles_item_data in self.latency_percentiles:
            latency_percentiles_item = latency_percentiles_item_data.to_dict()
            latency_percentiles.append(latency_percentiles_item)



        instance_count = []
        for instance_count_item_data in self.instance_count:
            instance_count_item = instance_count_item_data.to_dict()
            instance_count.append(instance_count_item)



        cpu_utilization = []
        for cpu_utilization_item_data in self.cpu_utilization:
            cpu_utilization_item = cpu_utilization_item_data.to_dict()
            cpu_utilization.append(cpu_utilization_item)



        memory_utilization = []
        for memory_utilization_item_data in self.memory_utilization:
            memory_utilization_item = memory_utilization_item_data.to_dict()
            memory_utilization.append(memory_utilization_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "requestRate": request_rate,
            "latencyPercentiles": latency_percentiles,
            "instanceCount": instance_count,
            "cpuUtilization": cpu_utilization,
            "memoryUtilization": memory_utilization,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.monitoring_metrics_dto_cloud_run_cpu_utilization_item import MonitoringMetricsDtoCloudRunCpuUtilizationItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_run_instance_count_item import MonitoringMetricsDtoCloudRunInstanceCountItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_run_latency_percentiles_item import MonitoringMetricsDtoCloudRunLatencyPercentilesItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_run_memory_utilization_item import MonitoringMetricsDtoCloudRunMemoryUtilizationItem # noqa: PLC0415
        from ..models.monitoring_metrics_dto_cloud_run_request_rate_item import MonitoringMetricsDtoCloudRunRequestRateItem # noqa: PLC0415
        d = dict(src_dict)
        request_rate = []
        _request_rate = d.pop("requestRate")
        for request_rate_item_data in (_request_rate):
            request_rate_item = MonitoringMetricsDtoCloudRunRequestRateItem.from_dict(request_rate_item_data)



            request_rate.append(request_rate_item)


        latency_percentiles = []
        _latency_percentiles = d.pop("latencyPercentiles")
        for latency_percentiles_item_data in (_latency_percentiles):
            latency_percentiles_item = MonitoringMetricsDtoCloudRunLatencyPercentilesItem.from_dict(latency_percentiles_item_data)



            latency_percentiles.append(latency_percentiles_item)


        instance_count = []
        _instance_count = d.pop("instanceCount")
        for instance_count_item_data in (_instance_count):
            instance_count_item = MonitoringMetricsDtoCloudRunInstanceCountItem.from_dict(instance_count_item_data)



            instance_count.append(instance_count_item)


        cpu_utilization = []
        _cpu_utilization = d.pop("cpuUtilization")
        for cpu_utilization_item_data in (_cpu_utilization):
            cpu_utilization_item = MonitoringMetricsDtoCloudRunCpuUtilizationItem.from_dict(cpu_utilization_item_data)



            cpu_utilization.append(cpu_utilization_item)


        memory_utilization = []
        _memory_utilization = d.pop("memoryUtilization")
        for memory_utilization_item_data in (_memory_utilization):
            memory_utilization_item = MonitoringMetricsDtoCloudRunMemoryUtilizationItem.from_dict(memory_utilization_item_data)



            memory_utilization.append(memory_utilization_item)


        monitoring_metrics_dto_cloud_run = cls(
            request_rate=request_rate,
            latency_percentiles=latency_percentiles,
            instance_count=instance_count,
            cpu_utilization=cpu_utilization,
            memory_utilization=memory_utilization,
        )

        return monitoring_metrics_dto_cloud_run

