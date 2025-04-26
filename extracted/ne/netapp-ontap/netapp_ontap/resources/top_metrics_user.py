r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to retrieve a list of users with the most I/O activity for a specified volume, within the past several seconds. Use the `top_metric` parameter to specify which type of I/O activity to filter for. This API is used to provide insight into I/O activity and supports ordering by I/O activity types, namely `iops` or `throughput` metrics. This API also supports only returning one I/O activity type per request.
## Approximate accounting and error bars
When too many users have recent activity, some users might be dropped from the list. In this situation, the spread of values in the `error` field increases, indicating that there are larger error bars on the value for `iops` or `throughput`. As the list becomes increasingly more approximate due to dropped entries, some of the users that would have otherwise been included might not be present in the final list returned by the API.
## Failure to return list of users with most I/O activity
The API can sometimes fail to return the list of users with the most I/O activity, due to the following reasons:

* The volume does not have the activity tracking feature enabled.
* The volume has not had any recent NFS/CIFS client traffic.
* The NFS/CIFS client operations are being served by the client-side filesystem cache.
* The NFS/CIFS client operations are being buffered by the client operating system.
* On rare occasions, the incoming traffic pattern is not suitable to obtain the list of users with the most I/O activity.
## Failure to return the usernames
The API can sometimes fail to obtain the usernames for the list of userid entries, due to internal transient errors.
In such cases, instead of the username, the API will return "{<user-id>}" for the user entry.
## Retrieve a list of the users with the most I/O activity
For a report on the users with the most I/O activity returned in descending order, specify the I/O activity type you want to filter for by passing the `iops` or `throughput` property into the top_metric parameter. If the I/O activity type is not specified, by default the API returns a list of the users with the greatest number of the average read operations per second. The current maximum number of users returned by the API for an I/O activity type is 25.

* GET   /api/storage/volumes/{volume.uuid}/top-metrics/users
## Examples
### Retrieving a list of the users with the greatest average number of read bytes received per second:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsUser.get_collection("{volume.uuid}", top_metric="throughput.read")
        )
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    TopMetricsUser(
        {
            "user_id": "S-1-5-21-256008430-3394229847-3930036330-1001",
            "volume": {"name": "vol1"},
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/572361f3-e769-439d-9c04-2ba48a08ff43"
                    }
                },
                "uuid": "572361f3-e769-439d-9c04-2ba48a08ff43",
            },
            "throughput": {
                "error": {"lower_bound": 1495, "upper_bound": 1502},
                "read": 1495,
            },
            "user_name": "John",
        }
    ),
    TopMetricsUser(
        {
            "user_id": "1988",
            "volume": {"name": "vol1"},
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/572361f3-e769-439d-9c04-2ba48a08ff43"
                    }
                },
                "uuid": "572361f3-e769-439d-9c04-2ba48a08ff43",
            },
            "throughput": {
                "error": {"lower_bound": 1022, "upper_bound": 1025},
                "read": 1022,
            },
            "user_name": "Ryan",
        }
    ),
    TopMetricsUser(
        {
            "user_id": "S-1-5-21-256008430-3394229847-3930036330-1003",
            "volume": {"name": "vol1"},
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/572361f3-e769-439d-9c04-2ba48a08ff43"
                    }
                },
                "uuid": "572361f3-e769-439d-9c04-2ba48a08ff43",
            },
            "throughput": {
                "error": {"lower_bound": 345, "upper_bound": 348},
                "read": 345,
            },
            "user_name": "Julie",
        }
    ),
]

```
</div>
</div>

## Example showing the behavior of the API when there is no read/write traffic:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsUser.get_collection(
                "{volume.uuid}", top_metric="throughput.write"
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


__all__ = ["TopMetricsUser", "TopMetricsUserSchema"]
__pdoc__ = {
    "TopMetricsUserSchema.resource": False,
    "TopMetricsUserSchema.opts": False,
}


class TopMetricsUserSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsUser object"""

    iops = marshmallow_fields.Nested("netapp_ontap.models.top_metrics_svm_user_iops.TopMetricsSvmUserIopsSchema", data_key="iops", unknown=EXCLUDE, allow_none=True)
    r""" The iops field of the top_metrics_user."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the top_metrics_user."""

    throughput = marshmallow_fields.Nested("netapp_ontap.models.top_metrics_svm_user_throughput.TopMetricsSvmUserThroughputSchema", data_key="throughput", unknown=EXCLUDE, allow_none=True)
    r""" The throughput field of the top_metrics_user."""

    user_id = marshmallow_fields.Str(
        data_key="user_id",
        allow_none=True,
    )
    r""" User ID of the user.

Example: S-1-5-21-256008430-3394229847-3930036330-1001"""

    user_name = marshmallow_fields.Str(
        data_key="user_name",
        allow_none=True,
    )
    r""" Name of the user.

Example: James"""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the top_metrics_user."""

    @property
    def resource(self):
        return TopMetricsUser

    gettable_fields = [
        "iops",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "throughput",
        "user_id",
        "user_name",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """iops,svm.links,svm.name,svm.uuid,throughput,user_id,user_name,volume.links,volume.name,volume.uuid,"""

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

class TopMetricsUser(Resource):
    r""" Information about a user's IO activity. """

    _schema = TopMetricsUserSchema
    _path = "/api/storage/volumes/{volume[uuid]}/top-metrics/users"
    _keys = ["volume.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of users with the most I/O activity.
### Platform Specifics
* **Unified ONTAP**: GET must be used to retrieve a list of users with the most I/O activity.
* **ASA**: GET is not supported.

### Learn more
* [`DOC /storage/volumes/{volume.uuid}/top-metrics/users`](#docs-storage-storage_volumes_{volume.uuid}_top-metrics_users)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all TopMetricsUser resources that match the provided query"""
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
        """Returns a list of RawResources that represent TopMetricsUser resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of users with the most I/O activity.
### Platform Specifics
* **Unified ONTAP**: GET must be used to retrieve a list of users with the most I/O activity.
* **ASA**: GET is not supported.

### Learn more
* [`DOC /storage/volumes/{volume.uuid}/top-metrics/users`](#docs-storage-storage_volumes_{volume.uuid}_top-metrics_users)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






