r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to retrieve a list of clients with the most I/O activity for FlexVol and FlexGroup volumes belonging to a specified SVM, within the past several seconds. To obtain this list, only the volumes which have the activity tracking feature enabled are considered. </br>
This API is used to provide insight into I/O activity and supports ordering by I/O activity types, namely `iops` and `throughput` metrics. Use the `top_metric` parameter to specify which type of I/O activity to filter for. This API supports returning only one I/O activity type per request.</br>
## Approximate accounting and error bars
When too many clients have had recent activity, some clients may be dropped from the list. In that situation, the spread of values in the `error` field will increase indicating we have larger error bars on the value for `iops` or `throughput`. As the list becomes increasingly more approximate due to dropped entries, some of the clients that would have otherwise been included, may not be present in the final list returned by the API.
## Enabling and disabling activity tracking feature
The following APIs can be used to enable, disable, and retrieve the activity tracking state for a FlexVol or a FlexGroup volume.

* PATCH  /api/storage/volumes/{uuid} -d '{"activity_tracking.state":"on"}'
* PATCH  /api/storage/volumes/{uuid} -d '{"activity_tracking.state":"off"}'
* GET    /api/storage/volumes/{uuid}/?fields=activity_tracking
## Excluded volumes list
Optionally, the API returns an excluded list of activity tracking-enabled volumes, which were not accounted for when obtaining the list of clients with the most I/O activity for the SVM. This excluded list contains both the volume information and the reason for exclusion. </br>
## Failure to return list of clients with most I/O activity
The API can sometimes fail to return the list of clients with the most I/O activity, due to the following reasons:

* The volumes belonging to the SVM do not have the activity tracking feature enabled.
* The volumes belonging to the SVM have not had any recent NFS/CIFS client traffic.
* The NFS/CIFS client operations are being served by the client-side filesystem cache.
* The NFS/CIFS client operations are being buffered by the client operating system.
* On rare occasions, the incoming traffic pattern is not suitable to obtain the list of clients with the most I/O activity.
## Retrieve a list of the clients with the most I/O activity
For a report on the clients with the most I/O activity returned in descending order, specify the I/O activity type you want to filter for by passing the `iops` or `throughput` I/O activity type into the top_metric parameter. If the I/O activity type is not specified, by default the API returns a list of clients with the greatest number of average read operations per second. The current maximum number of clients returned by the API for an I/O activity type is 25.

* GET   /api/svm/svms/{svm.uuid}/top-metrics/clients
## Examples
### Retrieving a list of the clients with the greatest average number of write operations per second:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsSvmClient

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(TopMetricsSvmClient.get_collection("{svm.uuid}", top_metric="iops.write"))
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    TopMetricsSvmClient(
        {
            "client_ip": "172.28.71.128",
            "svm": {"name": "vs1"},
            "iops": {
                "error": {"lower_bound": 1495, "upper_bound": 1505},
                "write": 1495,
            },
        }
    ),
    TopMetricsSvmClient(
        {
            "client_ip": "172.28.71.179",
            "svm": {"name": "vs1"},
            "iops": {
                "error": {"lower_bound": 1022, "upper_bound": 1032},
                "write": 1022,
            },
        }
    ),
    TopMetricsSvmClient(
        {
            "client_ip": "172.28.51.62",
            "svm": {"name": "vs1"},
            "iops": {"error": {"lower_bound": 345, "upper_bound": 355}, "write": 345},
        }
    ),
]

```
</div>
</div>

---
### Example showing the behavior of the API when there is no read/write traffic:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsSvmClient

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsSvmClient.get_collection(
                "{svm.uuid}", top_metric="throughput.write"
            )
        )
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[]

```
</div>
</div>

---"""

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


__all__ = ["TopMetricsSvmClient", "TopMetricsSvmClientSchema"]
__pdoc__ = {
    "TopMetricsSvmClientSchema.resource": False,
    "TopMetricsSvmClientSchema.opts": False,
}


class TopMetricsSvmClientSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsSvmClient object"""

    client_ip = marshmallow_fields.Str(
        data_key="client_ip",
        allow_none=True,
    )
    r""" IP address of the client. Both IPv4 and IPv6 IP addresses are supported.

Example: 192.168.185.170"""

    iops = marshmallow_fields.Nested("netapp_ontap.models.top_metrics_client_iops.TopMetricsClientIopsSchema", data_key="iops", unknown=EXCLUDE, allow_none=True)
    r""" The iops field of the top_metrics_svm_client."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the top_metrics_svm_client."""

    throughput = marshmallow_fields.Nested("netapp_ontap.models.top_metrics_client_throughput.TopMetricsClientThroughputSchema", data_key="throughput", unknown=EXCLUDE, allow_none=True)
    r""" The throughput field of the top_metrics_svm_client."""

    @property
    def resource(self):
        return TopMetricsSvmClient

    gettable_fields = [
        "client_ip",
        "iops",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "throughput",
    ]
    """client_ip,iops,svm.links,svm.name,svm.uuid,throughput,"""

    patchable_fields = [
        "iops",
        "throughput",
    ]
    """iops,throughput,"""

    postable_fields = [
        "iops",
        "throughput",
    ]
    """iops,throughput,"""

class TopMetricsSvmClient(Resource):
    r""" Aggregated information about a client's IO activity at a SVM scope. """

    _schema = TopMetricsSvmClientSchema
    _path = "/api/svm/svms/{svm[uuid]}/top-metrics/clients"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of clients with the most I/O activity.
### Learn more
* [`DOC /svm/svms/{svm.uuid}/top-metrics/clients`](#docs-svm-svm_svms_{svm.uuid}_top-metrics_clients)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all TopMetricsSvmClient resources that match the provided query"""
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
        """Returns a list of RawResources that represent TopMetricsSvmClient resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of clients with the most I/O activity.
### Learn more
* [`DOC /svm/svms/{svm.uuid}/top-metrics/clients`](#docs-svm-svm_svms_{svm.uuid}_top-metrics_clients)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






