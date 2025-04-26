r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
In ONTAP, scheduled snapshot creation works based on the schedules associated with snapshot policies.
ONTAP provides six cluster-wide schedules: "5min", "8hour", "hourly", "daily", "weekly" and "monthly".
A snapshot policy is created using at least one of these schedules and up to 5 schedules can be associated with a snapshot policy.
A snapshot policy can be linked to a storage object and based on the schedule in the policy, snapshots are created on the object at that interval.
Each schedule in a snapshot policy has a snapshot name prefix attached to it. Every snapshot created using this policy has this prefix in its name.
There is also a retention count associated with every schedule. This count indicates the maximum number of snapshots that can exist for a given schedule.
Once the snapshot count reaches the retention count, on the next create operation, the oldest snapshot is deleted.
A retention period can be associated with every schedule. During snapshot creation, this period is set as SnapLock expiry time on snapshot locking enabled volumes.<br/>
A schedule can be added, modified or deleted from a snapshot policy.<br/>
## Snapshot policy schedule APIs
The following APIs are used to perform operations related to snapshot policy schedules:

* POST      /api/storage/snapshot-policies/{snapshot_policy.uuid}/schedules/
* GET       /api/storage/snapshot-policies/{snapshot_policy.uuid}/schedules/
* GET       /api/storage/snapshot-policies/{snapshot_policy.uuid}/schedules/{schedule.uuid}
* PATCH     /api/storage/snapshot-policies/{snapshot_policy.uuid}/schedules/{schedule.uuid}
* DELETE    /api/storage/snapshot-policies/{snapshot_policy.uuid}/schedules/{schedule.uuid}
## Examples
### Adding schedule to a snapshot policy
The POST operation is used to create a schedule for a snapshot policy with the specified attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnapshotPolicySchedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SnapshotPolicySchedule("32a0841a-818e-11e9-b4f4-005056bbab9c")
    resource.schedule.uuid = "7c985d80-818a-11e9-b4f4-005056bbab9c"
    resource.count = "5"
    resource.prefix = "new_hourly"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SnapshotPolicySchedule(
    {
        "schedule": {"uuid": "7c985d80-818a-11e9-b4f4-005056bbab9c"},
        "snapshot_policy": {"uuid": "32a0841a-818e-11e9-b4f4-005056bbab9c"},
        "prefix": "new_monthly",
        "count": 5,
    }
)

```
</div>
</div>

### Retrieving snapshot policy schedules
The GET operation is used to retrieve snapshot policy schedules.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnapshotPolicySchedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            SnapshotPolicySchedule.get_collection(
                "32a0841a-818e-11e9-b4f4-005056bbab9c"
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
    SnapshotPolicySchedule(
        {
            "schedule": {
                "name": "5min",
                "uuid": "63d017dc-818a-11e9-b4f4-005056bbab9c",
            },
            "snapshot_policy": {"uuid": "32a0841a-818e-11e9-b4f4-005056bbab9c"},
        }
    ),
    SnapshotPolicySchedule(
        {
            "schedule": {
                "name": "8hour",
                "uuid": "64a5c5da-818a-11e9-b4f4-005056bbab9c",
            },
            "snapshot_policy": {"uuid": "32a0841a-818e-11e9-b4f4-005056bbab9c"},
        }
    ),
    SnapshotPolicySchedule(
        {
            "schedule": {
                "name": "daily",
                "uuid": "63e21a3e-818a-11e9-b4f4-005056bbab9c",
            },
            "snapshot_policy": {"uuid": "32a0841a-818e-11e9-b4f4-005056bbab9c"},
        }
    ),
    SnapshotPolicySchedule(
        {
            "schedule": {
                "name": "monthly",
                "uuid": "7c985d80-818a-11e9-b4f4-005056bbab9c",
            },
            "snapshot_policy": {"uuid": "32a0841a-818e-11e9-b4f4-005056bbab9c"},
        }
    ),
]

```
</div>
</div>

### Retrieving the attributes of a specific snapshot policy schedule
The GET operation is used to retrieve the attributes of a specific snapshot policy schedule.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnapshotPolicySchedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SnapshotPolicySchedule(
        "32a0841a-818e-11e9-b4f4-005056bbab9c",
        **{"schedule.uuid": "7c985d80-818a-11e9-b4f4-005056bbab9c"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
SnapshotPolicySchedule(
    {
        "schedule": {"name": "monthly", "uuid": "7c985d80-818a-11e9-b4f4-005056bbab9c"},
        "snapshot_policy": {"uuid": "32a0841a-818e-11e9-b4f4-005056bbab9c"},
        "prefix": "new_monthly",
        "count": 5,
        "snapmirror_label": "-",
        "retention_period": "PT20M",
    }
)

```
</div>
</div>

### Updating a snapshot policy schedule
The PATCH operation is used to update the specific attributes of a snapshot policy.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnapshotPolicySchedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SnapshotPolicySchedule(
        "32a0841a-818e-11e9-b4f4-005056bbab9c",
        **{"schedule.uuid": "7c985d80-818a-11e9-b4f4-005056bbab9c"}
    )
    resource.count = "10"
    resource.patch()

```

### Deleting a snapshot policy
The DELETE operation is used to delete a snapshot policy.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnapshotPolicySchedule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SnapshotPolicySchedule(
        "32a0841a-818e-11e9-b4f4-005056bbab9c",
        **{"schedule.uuid": "7c985d80-818a-11e9-b4f4-005056bbab9c"}
    )
    resource.delete()

```
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


__all__ = ["SnapshotPolicySchedule", "SnapshotPolicyScheduleSchema"]
__pdoc__ = {
    "SnapshotPolicyScheduleSchema.resource": False,
    "SnapshotPolicyScheduleSchema.opts": False,
}


class SnapshotPolicyScheduleSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapshotPolicySchedule object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snapshot_policy_schedule."""

    count = Size(
        data_key="count",
        allow_none=True,
    )
    r""" The number of snapshots to maintain for this schedule."""

    prefix = marshmallow_fields.Str(
        data_key="prefix",
        allow_none=True,
    )
    r""" The prefix to use while creating snapshots at regular intervals."""

    retention_period = marshmallow_fields.Str(
        data_key="retention_period",
        allow_none=True,
    )
    r""" The retention period of snapshots for this schedule."""

    schedule = marshmallow_fields.Nested("netapp_ontap.resources.schedule.ScheduleSchema", data_key="schedule", unknown=EXCLUDE, allow_none=True)
    r""" The schedule field of the snapshot_policy_schedule."""

    snapmirror_label = marshmallow_fields.Str(
        data_key="snapmirror_label",
        allow_none=True,
    )
    r""" Label for SnapMirror operations"""

    snapshot_policy = marshmallow_fields.Nested("netapp_ontap.resources.snapshot_policy.SnapshotPolicySchema", data_key="snapshot_policy", unknown=EXCLUDE, allow_none=True)
    r""" The snapshot_policy field of the snapshot_policy_schedule."""

    @property
    def resource(self):
        return SnapshotPolicySchedule

    gettable_fields = [
        "links",
        "count",
        "prefix",
        "retention_period",
        "schedule.links",
        "schedule.name",
        "schedule.uuid",
        "snapmirror_label",
        "snapshot_policy.links",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
    ]
    """links,count,prefix,retention_period,schedule.links,schedule.name,schedule.uuid,snapmirror_label,snapshot_policy.links,snapshot_policy.name,snapshot_policy.uuid,"""

    patchable_fields = [
        "count",
        "retention_period",
        "schedule.name",
        "schedule.uuid",
        "snapmirror_label",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
    ]
    """count,retention_period,schedule.name,schedule.uuid,snapmirror_label,snapshot_policy.name,snapshot_policy.uuid,"""

    postable_fields = [
        "count",
        "prefix",
        "retention_period",
        "schedule.name",
        "schedule.uuid",
        "snapmirror_label",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
    ]
    """count,prefix,retention_period,schedule.name,schedule.uuid,snapmirror_label,snapshot_policy.name,snapshot_policy.uuid,"""

class SnapshotPolicySchedule(Resource):
    r""" The snapshot policy schedule object is associated with a snapshot policy and it defines the interval at which snapshots are created and deleted. """

    _schema = SnapshotPolicyScheduleSchema
    _path = "/api/storage/snapshot-policies/{snapshot_policy[uuid]}/schedules"
    _keys = ["snapshot_policy.uuid", "schedule.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of snapshot policy schedules.
### Related ONTAP commands
* `snapshot policy show`
### Learn more
* [`DOC /storage/snapshot-policies/{snapshot_policy.uuid}/schedules`](#docs-storage-storage_snapshot-policies_{snapshot_policy.uuid}_schedules)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SnapshotPolicySchedule resources that match the provided query"""
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
        """Returns a list of RawResources that represent SnapshotPolicySchedule resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SnapshotPolicySchedule"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a snapshot policy schedule
### Related ONTAP commands
* `snapshot policy modify-schedule`
### Learn more
* [`DOC /storage/snapshot-policies/{snapshot_policy.uuid}/schedules`](#docs-storage-storage_snapshot-policies_{snapshot_policy.uuid}_schedules)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnapshotPolicySchedule"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnapshotPolicySchedule"], NetAppResponse]:
        r"""Adds a schedule to a snapshot policy.
### Required properties
* `schedule.uuid` or `schedule.name` - Schedule at which snapshots are captured on the volume.
* `count` - Number of snapshots to maintain for this schedule.
### Recommended optional properties
* `prefix` - Prefix to use when creating snapshots at regular intervals.
### Default property values
If not specified in POST, the following default property values are assigned:
* `prefix` - Value of `schedule.name`
### Related ONTAP commands
* `snapshot policy add-schedule`
### Learn more
* [`DOC /storage/snapshot-policies/{snapshot_policy.uuid}/schedules`](#docs-storage-storage_snapshot-policies_{snapshot_policy.uuid}_schedules)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SnapshotPolicySchedule"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a schedule from a snapshot policy
### Related ONTAP commands
* `snapshot policy remove-schedule`
### Learn more
* [`DOC /storage/snapshot-policies/{snapshot_policy.uuid}/schedules`](#docs-storage-storage_snapshot-policies_{snapshot_policy.uuid}_schedules)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of snapshot policy schedules.
### Related ONTAP commands
* `snapshot policy show`
### Learn more
* [`DOC /storage/snapshot-policies/{snapshot_policy.uuid}/schedules`](#docs-storage-storage_snapshot-policies_{snapshot_policy.uuid}_schedules)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details of a specific snapshot policy schedule.
### Related ONTAP commands
* `snapshot policy show`
### Learn more
* [`DOC /storage/snapshot-policies/{snapshot_policy.uuid}/schedules`](#docs-storage-storage_snapshot-policies_{snapshot_policy.uuid}_schedules)
"""
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
        r"""Adds a schedule to a snapshot policy.
### Required properties
* `schedule.uuid` or `schedule.name` - Schedule at which snapshots are captured on the volume.
* `count` - Number of snapshots to maintain for this schedule.
### Recommended optional properties
* `prefix` - Prefix to use when creating snapshots at regular intervals.
### Default property values
If not specified in POST, the following default property values are assigned:
* `prefix` - Value of `schedule.name`
### Related ONTAP commands
* `snapshot policy add-schedule`
### Learn more
* [`DOC /storage/snapshot-policies/{snapshot_policy.uuid}/schedules`](#docs-storage-storage_snapshot-policies_{snapshot_policy.uuid}_schedules)
"""
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
        r"""Updates a snapshot policy schedule
### Related ONTAP commands
* `snapshot policy modify-schedule`
### Learn more
* [`DOC /storage/snapshot-policies/{snapshot_policy.uuid}/schedules`](#docs-storage-storage_snapshot-policies_{snapshot_policy.uuid}_schedules)
"""
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
        r"""Deletes a schedule from a snapshot policy
### Related ONTAP commands
* `snapshot policy remove-schedule`
### Learn more
* [`DOC /storage/snapshot-policies/{snapshot_policy.uuid}/schedules`](#docs-storage-storage_snapshot-policies_{snapshot_policy.uuid}_schedules)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


