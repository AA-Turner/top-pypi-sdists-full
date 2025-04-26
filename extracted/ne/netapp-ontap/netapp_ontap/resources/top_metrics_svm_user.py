r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to retrieve a list of users with the most I/O activity for FlexVol and FlexGroup volumes belonging to a specified SVM, within the past several seconds. To obtain this list, only the volumes which have the activity tracking feature enabled are considered. </br>
This API is used to provide insight into I/O activity and supports ordering by I/O activity types, namely `iops` and `throughput` metrics. Use the `top_metric` parameter to specify which type of I/O activity to filter for. This API supports returning only one I/O activity type per request.</br>
## Enabling and disabling activity tracking feature
The following APIs can be used to enable, disable, and retrieve the activity tracking state for a FlexVol or a FlexGroup volume.

* PATCH  /api/storage/volumes/{uuid} -d '{"activity_tracking.state":"on"}'
* PATCH  /api/storage/volumes/{uuid} -d '{"activity_tracking.state":"off"}'
* GET    /api/storage/volumes/{uuid}/?fields=activity_tracking
## Excluded volumes list
Optionally, the API returns an excluded list of activity tracking-enabled volumes, which were not accounted for when obtaining the list of clients with the most I/O activity for the SVM. This excluded list contains both the volume information and the reason for exclusion.
## Approximate accounting and error bars
When too many users have recent activity, some users might be dropped from the list. In this situation, the spread of values in the `error` field increases, indicating that there are larger error bars on the value for `iops` or `throughput`. As the list becomes increasingly more approximate due to dropped entries, some of the users that would have otherwise been included might not be present in the final list returned by the API.
## Failure to return list of users with most I/O activity
The API can sometimes fail to return the list of users with the most I/O activity, due to the following reasons.

* The volumes belonging to the SVM do not have the activity tracking feature enabled.
* The volumes belonging to the SVM have not had any recent NFS/CIFS client traffic.
* The NFS/CIFS client operations are being served by the client-side filesystem cache.
* The NFS/CIFS client operations are being buffered by the client operating system.
* On rare occasions, the incoming traffic pattern is not suitable to obtain the list of users with the most I/O activity.
## Failure to return the usernames
The API can sometimes fail to obtain the usernames for the list of userid entries, due to internal transient errors.
In such cases, instead of the username, the API will return "{<user-id>}" for the user entry.
## Retrieve a list of the users with the most I/O activity
For a report on the users with the most I/O activity returned in descending order, specify the I/O activity type you want to filter for by passing the `iops` or `throughput` property into the top_metric parameter. If the I/O activity type is not specified, by default the API returns a list of the users with the greatest number of the average read operations per second. The current maximum number of users returned by the API for an I/O activity type is 25.

* GET   /api/svm/svms/{svm.uuid}/top-metrics/users
## Examples
### Retrieving a list of the users with the greatest average number of read bytes received per second:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsSvmUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsSvmUser.get_collection("{svm.uuid}", top_metric="throughput.read")
        )
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    TopMetricsSvmUser(
        {
            "user_id": "S-1-5-21-256008430-3394229847-3930036330-1001",
            "volumes": [
                {
                    "name": "fv1",
                    "_links": {
                        "self": {
                            "href": "/api/storage/volumes/73b293df-e9d7-46cc-a9ce-2df8e52ef864"
                        }
                    },
                    "uuid": "73b293df-e9d7-46cc-a9ce-2df8e52ef864",
                },
                {
                    "name": "fv2",
                    "_links": {
                        "self": {
                            "href": "/api/storage/volumes/2ea74c3e-d5ca-11eb-8fbb-005056ac0f33"
                        }
                    },
                    "uuid": "2ea74c3e-d5ca-11eb-8fbb-005056ac0f33",
                },
                {
                    "name": "fv4",
                    "_links": {
                        "self": {
                            "href": "/api/storage/volumes/5bbfc226-3fd8-42c9-a651-fa6167c2cf84"
                        }
                    },
                    "uuid": "5bbfc226-3fd8-42c9-a651-fa6167c2cf84",
                },
            ],
            "iops": {
                "error": {"lower_bound": 1495, "upper_bound": 1505},
                "write": 1495,
            },
            "svm": {"name": "vs1"},
            "user_name": "user1",
        }
    ),
    TopMetricsSvmUser(
        {
            "user_id": "S-1-5-21-256008430-3394229847-3930036330-1002",
            "volumes": [
                {
                    "name": "fv2",
                    "_links": {
                        "self": {
                            "href": "/api/storage/volumes/2ea74c3e-d5ca-11eb-8fbb-005056ac0f33"
                        }
                    },
                    "uuid": "2ea74c3e-d5ca-11eb-8fbb-005056ac0f33",
                },
                {
                    "name": "fv3",
                    "_links": {
                        "self": {
                            "href": "/api/storage/volumes/1ca74c3e-d5ca-11eb-8fbb-005056ac0f88"
                        }
                    },
                    "uuid": "1ca74c3e-d5ca-11eb-8fbb-005056ac0f88",
                },
            ],
            "iops": {
                "error": {"lower_bound": 1022, "upper_bound": 1032},
                "write": 1022,
            },
            "svm": {"name": "vs1"},
            "user_name": "user2",
        }
    ),
    TopMetricsSvmUser(
        {
            "user_id": "S-1-5-21-256008430-3394229847-3930036330-1003",
            "volumes": [
                {
                    "name": "fv3",
                    "_links": {
                        "self": {
                            "href": "/api/storage/volumes/1ca74c3e-d5ca-11eb-8fbb-005056ac0f88"
                        }
                    },
                    "uuid": "1ca74c3e-d5ca-11eb-8fbb-005056ac0f88",
                }
            ],
            "iops": {"error": {"lower_bound": 345, "upper_bound": 355}, "write": 345},
            "svm": {"name": "vs1"},
            "user_name": "user3",
        }
    ),
    TopMetricsSvmUser(
        {
            "user_id": "1988",
            "volumes": [
                {
                    "name": "fv4",
                    "_links": {
                        "self": {
                            "href": "/api/storage/volumes/5bbfc226-3fd8-42c9-a651-fa6167c2cf84"
                        }
                    },
                    "uuid": "5bbfc226-3fd8-42c9-a651-fa6167c2cf84",
                }
            ],
            "iops": {"error": {"lower_bound": 235, "upper_bound": 245}, "write": 235},
            "svm": {"name": "vs1"},
            "user_name": "user4",
        }
    ),
    TopMetricsSvmUser(
        {
            "user_id": "S-1-5-21-256008430-3394229847-3930036330-1005",
            "volumes": [
                {
                    "name": "fv5",
                    "_links": {
                        "self": {
                            "href": "/api/storage/volumes/5bbfc227-3fd8-42c9-a651-fa6167c2cf85"
                        }
                    },
                    "uuid": "5bbfc227-3fd8-42c9-a651-fa6167c2cf85",
                }
            ],
            "iops": {"error": {"lower_bound": 235, "upper_bound": 245}, "write": 235},
            "svm": {"name": "vs1"},
            "user_name": "user5",
        }
    ),
]

```
</div>
</div>

---
### Example showing the behavior of the API where there is no read/write traffic:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsSvmUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsSvmUser.get_collection(
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


__all__ = ["TopMetricsSvmUser", "TopMetricsSvmUserSchema"]
__pdoc__ = {
    "TopMetricsSvmUserSchema.resource": False,
    "TopMetricsSvmUserSchema.opts": False,
}


class TopMetricsSvmUserSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsSvmUser object"""

    iops = marshmallow_fields.Nested("netapp_ontap.models.top_metrics_svm_user_iops.TopMetricsSvmUserIopsSchema", data_key="iops", unknown=EXCLUDE, allow_none=True)
    r""" The iops field of the top_metrics_svm_user."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the top_metrics_svm_user."""

    throughput = marshmallow_fields.Nested("netapp_ontap.models.top_metrics_svm_user_throughput.TopMetricsSvmUserThroughputSchema", data_key="throughput", unknown=EXCLUDE, allow_none=True)
    r""" The throughput field of the top_metrics_svm_user."""

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

    volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cifs_session_volumes.CifsSessionVolumesSchema", unknown=EXCLUDE, allow_none=True), data_key="volumes", allow_none=True)
    r""" List of volumes where the user is generating traffic."""

    @property
    def resource(self):
        return TopMetricsSvmUser

    gettable_fields = [
        "iops",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "throughput",
        "user_id",
        "user_name",
        "volumes.links",
        "volumes.name",
        "volumes.uuid",
    ]
    """iops,svm.links,svm.name,svm.uuid,throughput,user_id,user_name,volumes.links,volumes.name,volumes.uuid,"""

    patchable_fields = [
        "iops",
        "throughput",
        "volumes.name",
        "volumes.uuid",
    ]
    """iops,throughput,volumes.name,volumes.uuid,"""

    postable_fields = [
        "iops",
        "throughput",
        "volumes.name",
        "volumes.uuid",
    ]
    """iops,throughput,volumes.name,volumes.uuid,"""

class TopMetricsSvmUser(Resource):
    r""" Aggregated information about a user's IO activity at a SVM scope. """

    _schema = TopMetricsSvmUserSchema
    _path = "/api/svm/svms/{svm[uuid]}/top-metrics/users"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of users with the most I/O activity.
### Learn more
* [`DOC /svm/svms/{svm.uuid}/top-metrics/users`](#docs-svm-svm_svms_{svm.uuid}_top-metrics_users)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all TopMetricsSvmUser resources that match the provided query"""
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
        """Returns a list of RawResources that represent TopMetricsSvmUser resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of users with the most I/O activity.
### Learn more
* [`DOC /svm/svms/{svm.uuid}/top-metrics/users`](#docs-svm-svm_svms_{svm.uuid}_top-metrics_users)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






