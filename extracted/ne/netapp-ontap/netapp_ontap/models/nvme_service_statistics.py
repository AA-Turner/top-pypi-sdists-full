r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeServiceStatistics", "NvmeServiceStatisticsSchema"]
__pdoc__ = {
    "NvmeServiceStatisticsSchema.resource": False,
    "NvmeServiceStatisticsSchema.opts": False,
    "NvmeServiceStatistics": False,
}


class NvmeServiceStatisticsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeServiceStatistics object"""

    fc = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw_svm.PerformanceMetricRawSvmSchema", unknown=EXCLUDE, data_key="fc", allow_none=True)
    r""" The fc field of the nvme_service_statistics. """

    iops_raw = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_io_type.PerformanceMetricIoTypeSchema", unknown=EXCLUDE, data_key="iops_raw", allow_none=True)
    r""" The iops_raw field of the nvme_service_statistics. """

    latency_raw = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_io_type.PerformanceMetricIoTypeSchema", unknown=EXCLUDE, data_key="latency_raw", allow_none=True)
    r""" The latency_raw field of the nvme_service_statistics. """

    status = marshmallow_fields.Str(data_key="status", allow_none=True)
    r""" Any errors associated with the sample. For example, if the aggregation of data over multiple nodes fails then any of the partial errors might be returned, "ok" on success, or "error" on any internal uncategorized failure. Whenever a sample collection is missed but done at a later time, it is back filled to the previous 15 second timestamp and tagged with "backfilled_data". "Inconsistent_delta_time" is encountered when the time between two collections is not the same for all nodes. Therefore, the aggregated value might be over or under inflated. "Negative_delta" is returned when an expected monotonically increasing value has decreased in value. "Inconsistent_old_data" is returned when one or more nodes do not have the latest data.

Valid choices:

* ok
* error
* partial_no_data
* partial_no_response
* partial_other_error
* negative_delta
* not_found
* backfilled_data
* inconsistent_delta_time
* inconsistent_old_data
* partial_no_uuid """

    tcp = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw_svm.PerformanceMetricRawSvmSchema", unknown=EXCLUDE, data_key="tcp", allow_none=True)
    r""" The tcp field of the nvme_service_statistics. """

    throughput_raw = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_io_type_rwt.PerformanceMetricIoTypeRwtSchema", unknown=EXCLUDE, data_key="throughput_raw", allow_none=True)
    r""" The throughput_raw field of the nvme_service_statistics. """

    timestamp = ImpreciseDateTime(data_key="timestamp", allow_none=True)
    r""" The timestamp of the performance data.

Example: 2017-01-25T11:20:13.000+0000 """

    @property
    def resource(self):
        return NvmeServiceStatistics

    gettable_fields = [
        "fc.iops_raw",
        "fc.latency_raw",
        "fc.status",
        "fc.throughput_raw",
        "fc.timestamp",
        "iops_raw.other",
        "iops_raw.read",
        "iops_raw.total",
        "iops_raw.write",
        "latency_raw.other",
        "latency_raw.read",
        "latency_raw.total",
        "latency_raw.write",
        "status",
        "tcp.iops_raw",
        "tcp.latency_raw",
        "tcp.status",
        "tcp.throughput_raw",
        "tcp.timestamp",
        "throughput_raw.read",
        "throughput_raw.total",
        "throughput_raw.write",
        "timestamp",
    ]
    """fc.iops_raw,fc.latency_raw,fc.status,fc.throughput_raw,fc.timestamp,iops_raw.other,iops_raw.read,iops_raw.total,iops_raw.write,latency_raw.other,latency_raw.read,latency_raw.total,latency_raw.write,status,tcp.iops_raw,tcp.latency_raw,tcp.status,tcp.throughput_raw,tcp.timestamp,throughput_raw.read,throughput_raw.total,throughput_raw.write,timestamp,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class NvmeServiceStatistics(Resource):

    _schema = NvmeServiceStatisticsSchema
