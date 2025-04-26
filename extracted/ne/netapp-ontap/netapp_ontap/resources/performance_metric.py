r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The Storage Aggregate Metrics API provides historical performance metrics for the specified aggregate.
The collection GET operation retrieves read, write, other and total metrics for a given aggregate, in terms of IOPS, latency and throughput. The read and write categories display the I/O operations that service user reads and writes across all the hosted volumes on a given aggregate. The other category encompasses background I/O operations that implement data protection services currently running on the aggregate. IOPs are the number of I/O operations reported per second, throughput is the amount of I/O operations measured in bytes per second and latency is the average response time for an IOP, reported in microseconds.
Without a specified time interval, the output is limited to statistics collected at 15 second intervals over the last hour.
## Examples
### Retrieving metrics for an aggregate
In this example, the API returns a set of records that exist for the aggregate with the given UUID for the last hour.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import PerformanceMetric

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            PerformanceMetric.get_collection(
                "538bf337-1b2c-11e8-bad0-005056b48388", max_records=4
            )
        )
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    PerformanceMetric({"timestamp": "2019-01-14T23:33:45+00:00"}),
    PerformanceMetric({"timestamp": "2019-01-14T23:33:30+00:00"}),
    PerformanceMetric({"timestamp": "2019-01-14T23:33:15+00:00"}),
    PerformanceMetric({"timestamp": "2019-01-14T23:33:00+00:00"}),
]

```
</div>
</div>

### Retrieving metrics for an aggregate with a set timestamp
In this example, the API returns metric values for latency, IOPS, and throughput properties such as read, write and total. The status and duration
for which the metrics are requested are also returned.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import PerformanceMetric

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            PerformanceMetric.get_collection(
                "538bf337-1b2c-11e8-bad0-005056b48388", timestamp="2019-01-1T23:33:00Z"
            )
        )
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    PerformanceMetric(
        {
            "status": "ok",
            "iops": {"total": 6, "write": 5, "other": 0, "read": 1},
            "latency": {"total": 199, "write": 216, "other": 0, "read": 148},
            "timestamp": "2019-01-01T23:33:00+00:00",
            "throughput": {"total": 212718, "write": 205892, "other": 0, "read": 6826},
            "duration": "PT15S",
        }
    )
]

```
</div>
</div>

### Retrieving metrics for an aggregate for a set time interval
In this example, the API returns the requested metrics for the given time interval of 1 week. The interval value can be
1 hour, 1 day, 1 week, 1 month or 1 year. If the interval value is not set, a default value of 1 hour is used.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import PerformanceMetric

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            PerformanceMetric.get_collection(
                "538bf337-1b2c-11e8-bad0-005056b48388",
                return_timeout=15,
                fields="*",
                interval="1w",
                max_records=4,
            )
        )
    )

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    PerformanceMetric(
        {
            "status": "ok",
            "iops": {"total": 45, "write": 26, "other": 0, "read": 18},
            "latency": {"total": 318, "write": 430, "other": 0, "read": 156},
            "timestamp": "2019-01-01T23:30:00+00:00",
            "throughput": {
                "total": 5824584,
                "write": 5556255,
                "other": 0,
                "read": 268328,
            },
            "duration": "PT30M",
        }
    ),
    PerformanceMetric(
        {
            "status": "ok",
            "iops": {"total": 76, "write": 28, "other": 0, "read": 48},
            "latency": {"total": 262, "write": 448, "other": 0, "read": 154},
            "timestamp": "2019-01-01T23:00:00+00:00",
            "throughput": {
                "total": 6596175,
                "write": 6121908,
                "other": 0,
                "read": 474266,
            },
            "duration": "PT30M",
        }
    ),
    PerformanceMetric(
        {
            "status": "ok",
            "iops": {"total": 548, "write": 16, "other": 437, "read": 94},
            "latency": {"total": 193, "write": 394, "other": 192, "read": 159},
            "timestamp": "2019-01-01T22:30:00+00:00",
            "throughput": {
                "total": 29196206,
                "write": 2411356,
                "other": 26244685,
                "read": 540164,
            },
            "duration": "PT30M",
        }
    ),
    PerformanceMetric(
        {
            "status": "ok",
            "iops": {"total": 13, "write": 13, "other": 0, "read": 0},
            "latency": {"total": 523, "write": 540, "other": 0, "read": 189},
            "timestamp": "2019-01-01T22:00:00+00:00",
            "throughput": {
                "total": 2768249,
                "write": 2765407,
                "other": 0,
                "read": 2842,
            },
            "duration": "PT30M",
        }
    ),
]

```
</div>
</div>

### Related ONTAP commands

* `statistics aggregate show`"""

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


__all__ = ["PerformanceMetric", "PerformanceMetricSchema"]
__pdoc__ = {
    "PerformanceMetricSchema.resource": False,
    "PerformanceMetricSchema.opts": False,
}


class PerformanceMetricSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PerformanceMetric object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the performance_metric."""

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

    iops = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_io_type.PerformanceMetricIoTypeSchema", data_key="iops", unknown=EXCLUDE, allow_none=True)
    r""" The iops field of the performance_metric."""

    latency = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_io_type.PerformanceMetricIoTypeSchema", data_key="latency", unknown=EXCLUDE, allow_none=True)
    r""" The latency field of the performance_metric."""

    status = marshmallow_fields.Str(
        data_key="status",
        validate=enum_validation(['ok', 'error', 'partial_no_data', 'partial_no_response', 'partial_other_error', 'negative_delta', 'not_found', 'backfilled_data', 'inconsistent_delta_time', 'inconsistent_old_data', 'partial_no_uuid']),
        allow_none=True,
    )
    r""" Errors associated with the sample. For example, if the aggregation of data over multiple nodes fails, then any partial errors might return "ok" on success or "error" on an internal uncategorized failure. Whenever a sample collection is missed but done at a later time, it is back filled to the previous 15 second timestamp and tagged with "backfilled_data". "Inconsistent_ delta_time" is encountered when the time between two collections is not the same for all nodes. Therefore, the aggregated value might be over or under inflated. "Negative_delta" is returned when an expected monotonically increasing value has decreased in value. "Inconsistent_old_data" is returned when one or more nodes do not have the latest data.

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
* partial_no_uuid"""

    throughput = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_io_type.PerformanceMetricIoTypeSchema", data_key="throughput", unknown=EXCLUDE, allow_none=True)
    r""" The throughput field of the performance_metric."""

    timestamp = ImpreciseDateTime(
        data_key="timestamp",
        allow_none=True,
    )
    r""" The timestamp of the performance data.

Example: 2017-01-25T11:20:13.000+0000"""

    @property
    def resource(self):
        return PerformanceMetric

    gettable_fields = [
        "links",
        "duration",
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
    """links,duration,iops.other,iops.read,iops.total,iops.write,latency.other,latency.read,latency.total,latency.write,status,throughput.other,throughput.read,throughput.total,throughput.write,timestamp,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class PerformanceMetric(Resource):
    r""" Performance numbers, such as IOPS latency and throughput. """

    _schema = PerformanceMetricSchema
    _path = "/api/storage/aggregates/{aggregate[uuid]}/metrics"
    _keys = ["aggregate.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves historical performance metrics for an aggregate.
### Learn more
* [`DOC /storage/aggregates/{uuid}/metrics`](#docs-storage-storage_aggregates_{uuid}_metrics)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all PerformanceMetric resources that match the provided query"""
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
        """Returns a list of RawResources that represent PerformanceMetric resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves historical performance metrics for an aggregate.
### Learn more
* [`DOC /storage/aggregates/{uuid}/metrics`](#docs-storage-storage_aggregates_{uuid}_metrics)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






