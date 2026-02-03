r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

# Overview
This API retrieves historical performance metrics for a node.
```
## Get historical performance metrics for a node
To retrieve historical performance metrics, issue a GET request to /dcn/cluster/nodes/{node.uuid}/metrics. The API will return the metric properties.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnNodeMetrics

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(DcnNodeMetrics.get_collection("{node.uuid}")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    DcnNodeMetrics(
        {
            "cpu": {"memory_used": 1024000000, "processor_utilization": 13},
            "timestamp": "2017-01-25T11:20:13+00:00",
            "gpu": {"memory_used": 1024000000, "processor_utilization": 13},
            "status": "ok",
            "duration": "PT15S",
            "uuid": "1cd8a442-86d1-11e0-ae1c-123478563412",
        }
    )
]

```
</div>
</div>
"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union
from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["DcnNodeMetrics", "DcnNodeMetricsSchema"]
__pdoc__ = {
    "DcnNodeMetricsSchema.resource": False,
    "DcnNodeMetricsSchema.opts": False,
}

class DcnNodeMetricsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeMetrics object"""

    cpu = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_node_metrics_cpu", "DcnNodeMetricsCpuSchema"),
                data_key="cpu",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The cpu field of the dcn_node_metrics."""

    duration = marshmallow_fields.Str(
        data_key="duration",
        validate=enum_validation(['PT15S', 'PT5M', 'PT30M', 'PT2H', 'P1D']),
        allow_none=True,
    )
    r""" The duration over which this sample is calculated. The time durations are represented in the ISO-8601 standard format. Samples can be calculated over the following durations:


Valid choices:

* PT15S
* PT5M
* PT30M
* PT2H
* P1D"""

    gpu = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_node_metrics_gpu", "DcnNodeMetricsGpuSchema"),
                data_key="gpu",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The gpu field of the dcn_node_metrics."""

    status = marshmallow_fields.Str(
        data_key="status",
        validate=enum_validation(['ok', 'error', 'partial_no_data', 'partial_no_uuid', 'partial_no_response', 'partial_other_error', 'negative_delta', 'backfilled_data', 'inconsistent_delta_time', 'inconsistent_old_data']),
        allow_none=True,
    )
    r""" * ok: The sample was collected successfully without any errors.
* error: An internal uncategorized failure occurred during the sample collection.
* partial_no_data: The sample collection was incomplete due to missing data.
* partial_no_uuid: The sample collection was incomplete due to a missing UUID.
* partial_no_response: The sample collection was incomplete due to no response from one or more nodes.
* partial_other_error: The sample collection was incomplete due to other unspecified errors.
* negative_delta: An expected monotonically increasing value has decreased in value.
* backfilled_data: The sample collection was completed at a later time and backfilled to the previous 15-second timestamp.
* inconsistent_delta_time: The time between two collections is not the same for all nodes, causing the aggregated value to be over or under-inflated.
* inconsistent_old_data: One or more nodes do not have the latest data.


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

    timestamp = ImpreciseDateTime(
        data_key="timestamp",
        allow_none=True,
    )
    r""" The timestamp of the performance data.

Example: 2017-01-25T11:20:13.000+0000"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier for the node.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return DcnNodeMetrics

    gettable_fields = [
        "cpu",
        "duration",
        "gpu",
        "status",
        "timestamp",
        "uuid",
    ]
    """cpu,duration,gpu,status,timestamp,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class DcnNodeMetrics(Resource):
    r""" CPU and GPU performance metrics for the nodes. It provides detailed insights into the utilization and memory usage of the processors over specified time durations. """

    _schema = DcnNodeMetricsSchema
    _path = "/api/dcn/cluster/nodes/{node[uuid]}/metrics"
    _keys = ["node.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves historical performance metrics for a node.
### Learn more
* [`DOC /dcn/cluster/nodes/{node.uuid}/metrics`](#docs-dcn-dcn_cluster_nodes_{node.uuid}_metrics)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all DcnNodeMetrics resources that match the provided query"""
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
        """Returns a list of RawResources that represent DcnNodeMetrics resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves historical performance metrics for a node.
### Learn more
* [`DOC /dcn/cluster/nodes/{node.uuid}/metrics`](#docs-dcn-dcn_cluster_nodes_{node.uuid}_metrics)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






