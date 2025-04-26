r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["VolumeMetrics", "VolumeMetricsSchema"]
__pdoc__ = {
    "VolumeMetricsSchema.resource": False,
    "VolumeMetricsSchema.opts": False,
}


class VolumeMetricsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeMetrics object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the volume_metrics."""

    cloud = marshmallow_fields.Nested("netapp_ontap.models.volume_metric_cloud.VolumeMetricCloudSchema", data_key="cloud", unknown=EXCLUDE, allow_none=True)
    r""" Performance numbers (IOPS and latency) for cloud store. These numbers are relevant only for volumes hosted on FabricPools."""

    duration = marshmallow_fields.Str(
        data_key="duration",
        validate=enum_validation(['PT15S', 'PT4M', 'PT30M', 'PT2H', 'P1D', 'PT5M']),
        allow_none=True,
    )
    r""" The duration over which this sample is calculated. The time durations are represented in the ISO-8601 standard format. Samples can be calculated over the following durations:


Valid choices:

* PT15S
* PT4M
* PT30M
* PT2H
* P1D
* PT5M"""

    flexcache = marshmallow_fields.Nested("netapp_ontap.models.volume_metric_flexcache.VolumeMetricFlexcacheSchema", data_key="flexcache", unknown=EXCLUDE, allow_none=True)
    r""" Performance number for FlexCache used to measure cache effectiveness."""

    iops = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_io_type.PerformanceMetricIoTypeSchema", data_key="iops", unknown=EXCLUDE, allow_none=True)
    r""" The iops field of the volume_metrics."""

    latency = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_io_type.PerformanceMetricIoTypeSchema", data_key="latency", unknown=EXCLUDE, allow_none=True)
    r""" The latency field of the volume_metrics."""

    status = marshmallow_fields.Str(
        data_key="status",
        validate=enum_validation(['ok', 'error', 'partial_no_data', 'partial_no_uuid', 'partial_no_response', 'partial_other_error', 'negative_delta', 'backfilled_data', 'inconsistent_delta_time', 'inconsistent_old_data']),
        allow_none=True,
    )
    r""" Errors associated with the sample. For example, if the aggregation of data over multiple nodes fails, then any partial errors might return "ok" on success or "error" on an internal uncategorized failure. Whenever a sample collection is missed but done at a later time, it is back filled to the previous 15 second timestamp and tagged with "backfilled_data". "Inconsistent_ delta_time" is encountered when the time between two collections is not the same for all nodes. Therefore, the aggregated value might be over or under inflated. "Negative_delta" is returned when an expected monotonically increasing value has decreased in value. "Inconsistent_old_data" is returned when one or more nodes do not have the latest data.

Valid choices:

* ok
* error
* partial_no_data
* partial_no_uuid
* partial_no_response
* partial_other_error
* negative_delta
* backfilled_data
* inconsistent_delta_time
* inconsistent_old_data"""

    throughput = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_io_type.PerformanceMetricIoTypeSchema", data_key="throughput", unknown=EXCLUDE, allow_none=True)
    r""" The throughput field of the volume_metrics."""

    timestamp = ImpreciseDateTime(
        data_key="timestamp",
        allow_none=True,
    )
    r""" The timestamp of the performance data.

Example: 2017-01-25T11:20:13.000+0000"""

    @property
    def resource(self):
        return VolumeMetrics

    gettable_fields = [
        "links",
        "cloud",
        "duration",
        "flexcache",
        "iops.other",
        "iops.read",
        "iops.total",
        "iops.write",
        "latency.other",
        "latency.read",
        "latency.total",
        "latency.write",
        "status",
        "throughput.other",
        "throughput.read",
        "throughput.total",
        "throughput.write",
        "timestamp",
    ]
    """links,cloud,duration,flexcache,iops.other,iops.read,iops.total,iops.write,latency.other,latency.read,latency.total,latency.write,status,throughput.other,throughput.read,throughput.total,throughput.write,timestamp,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class VolumeMetrics(Resource):
    r""" Performance numbers, such as IOPS, latency and throughput. """

    _schema = VolumeMetricsSchema
    _path = "/api/storage/volumes/{volume[uuid]}/metrics"
    _keys = ["volume.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves historical performance metrics for a volume."""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all VolumeMetrics resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent VolumeMetrics resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves historical performance metrics for a volume."""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






