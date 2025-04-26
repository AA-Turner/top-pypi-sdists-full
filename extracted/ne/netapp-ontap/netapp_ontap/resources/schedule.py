r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can  use the /cluster/schedules API to view, create, and modify job schedules in a cluster.
## Retrieving a job schedule
You can retrieve job schedules by issuing a GET request to /cluster/schedules. It is also possible to retrieve a specific schedule when qualified by its UUID to /cluster/schedules/{uuid}. You can apply queries on fields to retrieve all schedules that match the combined query.
### Example
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Schedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Schedule.get_collection(type="interval")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Schedule(
        {
            "interval": "PT7M30S",
            "name": "Balanced Placement Model Cache Update",
            "uuid": "0941e980-0158-11e9-a82c-005056bb4301",
            "_links": {
                "self": {
                    "href": "/api/cluster/schedules/0941e980-0158-11e9-a82c-005056bb4301"
                }
            },
            "type": "interval",
        }
    ),
    Schedule(
        {
            "interval": "PT1H",
            "name": "Auto Balance Aggregate Scheduler",
            "uuid": "0944b975-0158-11e9-a82c-005056bb4301",
            "_links": {
                "self": {
                    "href": "/api/cluster/schedules/0944b975-0158-11e9-a82c-005056bb4301"
                }
            },
            "type": "interval",
        }
    ),
    Schedule(
        {
            "interval": "P1D",
            "name": "Application Templates ASUP Dump",
            "uuid": "0c65f1fb-0158-11e9-a82c-005056bb4301",
            "_links": {
                "self": {
                    "href": "/api/cluster/schedules/0c65f1fb-0158-11e9-a82c-005056bb4301"
                }
            },
            "type": "interval",
        }
    ),
]

```
</div>
</div>

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Schedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Schedule(uuid="25312bd8-0158-11e9-a82c-005056bb4301")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Schedule(
    {
        "cluster": {
            "name": "my_cluster",
            "uuid": "f3f9bbfa-0157-11e9-a82c-005056bb4301",
        },
        "name": "monthly",
        "uuid": "25312bd8-0158-11e9-a82c-005056bb4301",
        "cron": {"days": [1], "hours": [0], "minutes": [20]},
        "_links": {
            "self": {
                "href": "/api/cluster/schedules/25312bd8-0158-11e9-a82c-005056bb4301"
            }
        },
        "type": "cron",
    }
)

```
</div>
</div>

---
## Creating a job schedule
You can create a job schedule by issuing a POST request to /cluster/schedules to a node in the cluster. For a successful request, the POST request returns a status code of 201.
Job schedules can be of either type "cron" or type "interval". A cron schedule is run at specific minutes within the hour, or hours of the day, days of the week, days of the month, or months of the year. An interval schedule runs repeatedly at fixed intervals.
### Required fields

* name - Name of the job schedule
You are required to provide a "minutes" field for a cron schedule. An "interval" field is required for an interval schedule. Do not provide both a "cron" field and an "interval" field.
The schedule UUID is created by the system.
### Cron schedule fields

* cron.minutes - Minutes within the hour (0 through 59)
* cron.hours -  Hours of the day (0 through 23)
* cron.weekdays - Weekdays (0 through 6, where 0 is Sunday and 6 is Saturday.)
* cron.days - Days of the month (1 through 31)
* cron.months - Months of the year (1 through 12)
### Interval schedule field

* interval - Length of time in ISO 8601 duration format.
### Examples
#### Create an interval schedule with a 1-week interval
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Schedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Schedule()
    resource.name = "test_interval_1"
    resource.interval = "P1W"
    resource.post(hydrate=True)
    print(resource)

```

#### Create a cron schedule that runs daily at 12:05
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Schedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Schedule()
    resource.name = "test_cron_1"
    resource.cron = {"minutes": [5], "hours": [12]}
    resource.post(hydrate=True)
    print(resource)

```

### Optional fields
By default, the schedule is owned by the local cluster. In a MetroCluster configuration, you can specify the partner cluster if the local cluster is in the switchover state.

* cluster.name - Name of the cluster owning the schedule.
* cluster.uuid - UUID of the cluster owning the schedule.
### Records field
You can create multiple schedules in one request by providing an array of named records with schedule entries. Each entry must follow the required and optional fields listed above.
<br/>
---
## Updating a job schedule
The following fields of an existing schedule can be modified:

* cron.minutes
* cron.hours
* cron.weekdays
* cron.days
* cron.months
* interval
Note that you cannot modify the name, cluster, and type of schedule. Also, you cannot modify a cron field of an interval schedule, or the interval field of a cron schedule. You can apply queries on fields to modify all schedules that match the combined query.
### Examples
#### Modify an interval schedule with a 2-day and 5-minute interval
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Schedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Schedule(uuid="{uuid}")
    resource.interval = "P2DT5M"
    resource.patch()

```

#### Modify a cron schedule to run Mondays at 2
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Schedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Schedule(uuid="{uuid}")
    resource.cron = {"hours": [2], "weekdays": [1]}
    resource.patch()

```

---
## Deleting a job schedule
You can delete job schedules based on their UUID. You can apply queries on fields to delete all schedules that match the combined query.
### Example
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Schedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Schedule(uuid="{uuid}")
    resource.delete()

```

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Schedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Schedule()
    resource.delete(name="test*")

```

---
## MetroCluster configurations
In a MetroCluster configuration, user-created schedules owned by the local cluster are replicated to the partner cluster. Likewise, user-created schedules owned by the partner cluster are replicated to the local cluster. The owning cluster for a particular schedule is shown in the "cluster.name" and "cluster.uuid" fields.
Normally, only schedules owned by the local cluster can be created, modified, and deleted on the local cluster. However, when a MetroCluster configuration is in switchover, the cluster in switchover state can create, modify, and delete schedules owned by the partner cluster."""

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


__all__ = ["Schedule", "ScheduleSchema"]
__pdoc__ = {
    "ScheduleSchema.resource": False,
    "ScheduleSchema.opts": False,
}


class ScheduleSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Schedule object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the schedule."""

    cluster = marshmallow_fields.Nested("netapp_ontap.models.schedule_cluster.ScheduleClusterSchema", data_key="cluster", unknown=EXCLUDE, allow_none=True)
    r""" The cluster that owns the schedule. Defaults to the local cluster."""

    cron = marshmallow_fields.Nested("netapp_ontap.models.schedule_cron.ScheduleCronSchema", data_key="cron", unknown=EXCLUDE, allow_none=True)
    r""" Details for schedules of type cron."""

    interval = marshmallow_fields.Str(
        data_key="interval",
        allow_none=True,
    )
    r""" An ISO-8601 duration formatted string.

Example: P1DT2H3M4S"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=256),
        allow_none=True,
    )
    r""" Schedule name. Required in the URL or POST body."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['cluster', 'svm']),
        allow_none=True,
    )
    r""" If the schedule is owned by a data SVM, then the scope is set to svm. Otherwise it will be set to cluster.

Valid choices:

* cluster
* svm"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the schedule."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['cron', 'interval']),
        allow_none=True,
    )
    r""" Schedule type

Valid choices:

* cron
* interval"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Job schedule UUID

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return Schedule

    gettable_fields = [
        "links",
        "cluster",
        "cron",
        "interval",
        "name",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "uuid",
    ]
    """links,cluster,cron,interval,name,scope,svm.links,svm.name,svm.uuid,type,uuid,"""

    patchable_fields = [
        "cron",
        "interval",
    ]
    """cron,interval,"""

    postable_fields = [
        "cluster",
        "cron",
        "interval",
        "name",
        "svm.name",
        "svm.uuid",
    ]
    """cluster,cron,interval,name,svm.name,svm.uuid,"""

class Schedule(Resource):
    r""" Complete schedule information """

    _schema = ScheduleSchema
    _path = "/api/cluster/schedules"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a schedule.
### Learn more
* [`DOC /cluster/schedules`](#docs-cluster-cluster_schedules)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Schedule resources that match the provided query"""
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
        """Returns a list of RawResources that represent Schedule resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Schedule"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a schedule. Note that you cannot modify a cron field of an interval schedule, or the interval field of a cron schedule.
### Learn more
* [`DOC /cluster/schedules`](#docs-cluster-cluster_schedules)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Schedule"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Schedule"], NetAppResponse]:
        r"""Creates a schedule.
### Required Fields
* name - Name of the job schedule.
You must provide a minutes field for a cron schedule and an interval field for an interval schedule. Do not provide both a cron field and an interval field.

### Learn more
* [`DOC /cluster/schedules`](#docs-cluster-cluster_schedules)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["Schedule"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a schedule.
### Learn more
* [`DOC /cluster/schedules`](#docs-cluster-cluster_schedules)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a schedule.
### Learn more
* [`DOC /cluster/schedules`](#docs-cluster-cluster_schedules)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a schedule.
### Learn more
* [`DOC /cluster/schedules`](#docs-cluster-cluster_schedules)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates a schedule.
### Required Fields
* name - Name of the job schedule.
You must provide a minutes field for a cron schedule and an interval field for an interval schedule. Do not provide both a cron field and an interval field.

### Learn more
* [`DOC /cluster/schedules`](#docs-cluster-cluster_schedules)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a schedule. Note that you cannot modify a cron field of an interval schedule, or the interval field of a cron schedule.
### Learn more
* [`DOC /cluster/schedules`](#docs-cluster-cluster_schedules)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a schedule.
### Learn more
* [`DOC /cluster/schedules`](#docs-cluster-cluster_schedules)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


