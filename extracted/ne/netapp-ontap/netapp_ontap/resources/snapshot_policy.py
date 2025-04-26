r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
In ONTAP, scheduled snapshot creation works based on snapshot policies.
ONTAP provides three cluster-wide snapshot policies: "default", "default-1weekly" and "none".
A snapshot policy can have more than one schedule associated with it.
A snapshot policy can be linked to a storage object and based on the schedule in the policy, snapshots will be created on the object at that interval.
Each schedule in a snapshot policy has a snapshot name prefix attached to it. Every snapshot created using this policy will have this prefix in its name.
There is also a retention count associated with every schedule. This count indicates the maximum number of snapshots that can exist for a given schedule. Once the snapshot count reaches the retention count, on the next create operation, the oldest snapshot is deleted.
A retention period can be associated with every schedule. During snapshot creation, this period is set as SnapLock expiry time on snapshot locking enabled volumes.<br/>
## Snapshot policy APIs
The following APIs are used to perform operations related to snapshot policy information:

* POST      /api/storage/snapshot-policies
* GET       /api/storage/snapshot-policies
* GET       /api/storage/snapshot-policies/{uuid}
* PATCH     /api/storage/snapshot-policies/{uuid}
* DELETE    /api/storage/snapshot-policies/{uuid}
## Examples
### Creating a snapshot policy
The POST operation is used to create a snapshot policy with the specified attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnapshotPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SnapshotPolicy()
    resource.name = "new_policy"
    resource.enabled = True
    resource.comment = "policy comment"
    resource.copies = [
        {
            "schedule": {"name": "5min"},
            "count": "5",
            "prefix": "xyz",
            "retention_period": "PT20M",
        }
    ]
    resource.svm = {"name": "vs0"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SnapshotPolicy(
    {
        "copies": [
            {
                "schedule": {"name": "5min"},
                "count": 5,
                "snapmirror_label": "-",
                "retention_period": "PT20M",
            }
        ],
        "name": "new_policy",
        "comment": "This is a 5min schedule policy",
        "uuid": "a69d8173-450c-11e9-aa44-005056bbc848",
        "enabled": True,
        "svm": {"name": "vs0"},
    }
)

```
</div>
</div>

### Retrieving snapshot policy attributes
The GET operation is used to retrieve snapshot policy attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnapshotPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SnapshotPolicy.get_collection()))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    SnapshotPolicy(
        {
            "name": "spsv0",
            "uuid": "0fa7a554-348d-11e9-b55e-005056bbf1c8",
            "_links": {
                "self": {
                    "href": "/api/storage/snapshot-policies/0fa7a554-348d-11e9-b55e-005056bbf1c8"
                }
            },
        }
    ),
    SnapshotPolicy(
        {
            "name": "default",
            "uuid": "3c112527-2fe8-11e9-b55e-005056bbf1c8",
            "_links": {
                "self": {
                    "href": "/api/storage/snapshot-policies/3c112527-2fe8-11e9-b55e-005056bbf1c8"
                }
            },
        }
    ),
    SnapshotPolicy(
        {
            "name": "default-1weekly",
            "uuid": "3c1c1656-2fe8-11e9-b55e-005056bbf1c8",
            "_links": {
                "self": {
                    "href": "/api/storage/snapshot-policies/3c1c1656-2fe8-11e9-b55e-005056bbf1c8"
                }
            },
        }
    ),
    SnapshotPolicy(
        {
            "name": "none",
            "uuid": "3c228b82-2fe8-11e9-b55e-005056bbf1c8",
            "_links": {
                "self": {
                    "href": "/api/storage/snapshot-policies/3c228b82-2fe8-11e9-b55e-005056bbf1c8"
                }
            },
        }
    ),
]

```
</div>
</div>

### Retrieving the attributes of a specific snapshot policy
The GET operation is used to retrieve the attributes of a specific snapshot policy.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnapshotPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SnapshotPolicy(uuid="3c112527-2fe8-11e9-b55e-005056bbf1c8")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
SnapshotPolicy(
    {
        "copies": [
            {"schedule": {"name": "hourly"}, "prefix": "hourly", "count": 6},
            {"schedule": {"name": "daily"}, "prefix": "daily", "count": 2},
            {"schedule": {"name": "weekly"}, "prefix": "weekly", "count": 2},
        ],
        "name": "default",
        "comment": "Default policy with hourly, daily & weekly schedules.",
        "uuid": "3c112527-2fe8-11e9-b55e-005056bbf1c8",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/storage/snapshot-policies/3c112527-2fe8-11e9-b55e-005056bbf1c8"
            }
        },
        "scope": "cluster",
    }
)

```
</div>
</div>

### Updating a snapshot policy
The PATCH operation is used to update the specific attributes of a snapshot policy.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnapshotPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SnapshotPolicy(uuid="ae9e65c4-4506-11e9-aa44-005056bbc848")
    resource.enabled = False
    resource.patch()

```

### Deleting a snapshot policy
The DELETE operation is used to delete a snapshot policy.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SnapshotPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SnapshotPolicy(uuid="ae9e65c4-4506-11e9-aa44-005056bbc848")
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


__all__ = ["SnapshotPolicy", "SnapshotPolicySchema"]
__pdoc__ = {
    "SnapshotPolicySchema.resource": False,
    "SnapshotPolicySchema.opts": False,
}


class SnapshotPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapshotPolicy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snapshot_policy."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" A comment associated with the snapshot policy."""

    copies = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.snapshot_policy_copies.SnapshotPolicyCopiesSchema", unknown=EXCLUDE, allow_none=True), data_key="copies", allow_none=True)
    r""" The copies field of the snapshot_policy."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Is the snapshot policy enabled?

Example: true"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the snapshot policy.

Example: default"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
        allow_none=True,
    )
    r""" Set to "svm" when the request is on a data SVM, otherwise set to "cluster".

Valid choices:

* svm
* cluster"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the snapshot_policy."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The uuid field of the snapshot_policy.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return SnapshotPolicy

    gettable_fields = [
        "links",
        "comment",
        "copies",
        "enabled",
        "name",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,comment,copies,enabled,name,scope,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "comment",
        "enabled",
    ]
    """comment,enabled,"""

    postable_fields = [
        "comment",
        "copies",
        "enabled",
        "name",
        "svm.name",
        "svm.uuid",
    ]
    """comment,copies,enabled,name,svm.name,svm.uuid,"""

class SnapshotPolicy(Resource):
    r""" The snapshot policy object is associated with a read-write volume used to create and delete snapshots at regular intervals. """

    _schema = SnapshotPolicySchema
    _path = "/api/storage/snapshot-policies"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of snapshot policies.
### Related ONTAP commands
* `snapshot policy show`
### Learn more
* [`DOC /storage/snapshot-policies`](#docs-storage-storage_snapshot-policies)
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
        """Returns a count of all SnapshotPolicy resources that match the provided query"""
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
        """Returns a list of RawResources that represent SnapshotPolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SnapshotPolicy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a snapshot policy
### Related ONTAP commands
* `snapshot policy modify`
* `snapshot policy modify-schedule`
* `snapshot policy add-schedule`
### Learn more
* [`DOC /storage/snapshot-policies`](#docs-storage-storage_snapshot-policies)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnapshotPolicy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnapshotPolicy"], NetAppResponse]:
        r"""Creates a snapshot policy.
### Required properties
* `svm.uuid` or `svm.name` - Specifies an SVM for policy creation. If not specified, the snapshot policy will be created on the cluster admin SVM.
* `name` - Name for the snapshot policy.
* `copies.schedule` - Schedule at which snapshots are captured on the volume.
* `copies.count` - Number of snapshots to maintain for this schedule.
### Recommended optional properties
* `copies.prefix` - Prefix to use when creating snapshots at regular intervals.
* `copies.snapmirror_label` - Label for SnapMirror operations.
* `copies.retention_period` - Retention period for snapshot locking enabled volumes.The duration must be specified in ISO format or \"infinite\".
### Default property values
If not specified in POST, the following default property values are assigned:
* `svm.uuid` or `svm.name` - If not specified, the snapshot policy will be created on the cluster admin SVM.
* `enabled` - _true_
* `copies.prefix` - Value of `schedule.name`
### Related ONTAP commands
* `snapshot policy create`
### Learn more
* [`DOC /storage/snapshot-policies`](#docs-storage-storage_snapshot-policies)
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
        records: Iterable["SnapshotPolicy"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a snapshot policy
### Related ONTAP commands
* `snapshot policy delete`
### Learn more
* [`DOC /storage/snapshot-policies`](#docs-storage-storage_snapshot-policies)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of snapshot policies.
### Related ONTAP commands
* `snapshot policy show`
### Learn more
* [`DOC /storage/snapshot-policies`](#docs-storage-storage_snapshot-policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details of a specific snapshot policy.
### Related ONTAP commands
* `snapshot policy show`
### Learn more
* [`DOC /storage/snapshot-policies`](#docs-storage-storage_snapshot-policies)
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
        r"""Creates a snapshot policy.
### Required properties
* `svm.uuid` or `svm.name` - Specifies an SVM for policy creation. If not specified, the snapshot policy will be created on the cluster admin SVM.
* `name` - Name for the snapshot policy.
* `copies.schedule` - Schedule at which snapshots are captured on the volume.
* `copies.count` - Number of snapshots to maintain for this schedule.
### Recommended optional properties
* `copies.prefix` - Prefix to use when creating snapshots at regular intervals.
* `copies.snapmirror_label` - Label for SnapMirror operations.
* `copies.retention_period` - Retention period for snapshot locking enabled volumes.The duration must be specified in ISO format or \"infinite\".
### Default property values
If not specified in POST, the following default property values are assigned:
* `svm.uuid` or `svm.name` - If not specified, the snapshot policy will be created on the cluster admin SVM.
* `enabled` - _true_
* `copies.prefix` - Value of `schedule.name`
### Related ONTAP commands
* `snapshot policy create`
### Learn more
* [`DOC /storage/snapshot-policies`](#docs-storage-storage_snapshot-policies)
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
        r"""Updates a snapshot policy
### Related ONTAP commands
* `snapshot policy modify`
* `snapshot policy modify-schedule`
* `snapshot policy add-schedule`
### Learn more
* [`DOC /storage/snapshot-policies`](#docs-storage-storage_snapshot-policies)
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
        r"""Deletes a snapshot policy
### Related ONTAP commands
* `snapshot policy delete`
### Learn more
* [`DOC /storage/snapshot-policies`](#docs-storage-storage_snapshot-policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


