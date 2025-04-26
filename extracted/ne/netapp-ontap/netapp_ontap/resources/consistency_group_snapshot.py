r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Consistency groups support snapshot create, inventory, and restore. Snapshots can be created on a specified schedule or on-demand. On-demand snapshots can have a type of application consistent or crash consistent. Crash consistent is the default. Scheduled snapshotss are always crash consistent. There is no functional difference in ONTAP between crash consistent or application consistent snapshots.
<br>The functionality provided by these APIs is not integrated with the host application. Snapshots have limited value without host coordination, so the use of the SnapCenter Backup Management suite is recommended to ensure correct interaction between host applications and ONTAP.
### On-Demand Snapshots
A manual snapshot may be created on-demand for a parent consistency group and for any of the children consistency groups within it.
<br> Scheduled and manual snapshot creation operations are subject to a pre-defined seven second internal timeout. If the snapshot creation operation does not complete within this time, it is aborted.
<br> Individual volume snapshots within a consistency group snapshots can be accessed and used with native volume snapshot operations.
<br> When an individual volume snapshot is deleted that is part of a consistency group snapshot, then that consistency group snapshot becomes invalid and which cannot be used for restoring the consistency group.
### Restoring to a Previous Snapshot
A snapshot restores to a parent consistency group from an existing parent consistency group's snapshot.  A snapshot restores to any of the children's consistency groups within it from an existing children's consistency group. Granular snapshots are supported. This is performed by a PATCH operation on the specific consistency group for the restore. An example is shown in [`PATCH /application/consistency-groups`](#/application/consistency_group_modify).
<br> Any existing snapshots that were created chronologically after the time of the snapshot used in a successful restore operation is deleted, in compliance with existing ONTAP "future-snapshot" handling principles.
<br> On failures during consistency group restores, any volumes that have been restored will remain so and will not be rolled back. The user must retry the failed restore operation until it is successful. The user can retry with consistency group restore or individual volume-granular restore.
## Consistency group Snapshot APIs
The following APIs are used to perform operations related to consistency group snapshots:

* GET       /api/application/consistency-groups/{consistency_group.uuid}/snapshots
* POST      /api/application/consistency-groups/{consistency_group.uuid}/snapshots
* POST      /api/application/consistency-groups/{consistency_group.uuid}/snapshots?action=start
* GET       /api/application/consistency-groups/{consistency_group.uuid}/snapshots/{uuid}
* PATCH     /api/application/consistency-groups/{consistency_group.uuid}/snapshots/{uuid}?action=commit
* DELETE    /api/application/consistency-groups/{consistency_group.uuid}/snapshots/{uuid}
## Examples
### Required properties

* `consistency_group.uuid` - Existing consistency group UUID in which to create the snapshot.
### Retrieving the list of existing snapshots for a consistency group
Retrieves the list of consistency group granular snapshots for a specific consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroupSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            ConsistencyGroupSnapshot.get_collection(
                "92c6c770-17a1-11eb-b141-005056acd498"
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
    ConsistencyGroupSnapshot(
        {
            "name": "sa3s1",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/a8d0626a-17a0-11eb-b141-005056acd498/snapshots/92c6c770-17a1-11eb-b141-005056acd498"
                }
            },
            "uuid": "92c6c770-17a1-11eb-b141-005056acd498",
        }
    ),
    ConsistencyGroupSnapshot(
        {
            "name": "sa3s2",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/a8d0626a-17a0-11eb-b141-005056acd498/snapshots/c5a250ba-17a1-11eb-b141-005056acd498"
                }
            },
            "uuid": "c5a250ba-17a1-11eb-b141-005056acd498",
        }
    ),
]

```
</div>
</div>

### Retrieves details of a specific snapshot for a consistency group
Retrieves details for a specific snapshot in a consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroupSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroupSnapshot(
        "92c6c770-17a1-11eb-b141-005056acd498",
        uuid="a175c021-4199-11ec-8674-005056accf3f",
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
ConsistencyGroupSnapshot(
    {
        "name": "sa3s2",
        "_links": {
            "self": {
                "href": "/api/application/consistency-groups/ddabc6a5-4196-11ec-8674-005056accf3f/snapshots/a175c021-4199-11ec-8674-005056accf3f"
            }
        },
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/7379fecb-4195-11ec-8674-005056accf3f"}
            },
            "uuid": "7379fecb-4195-11ec-8674-005056accf3f",
        },
        "consistency_group": {
            "name": "CG_1",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/ddabc6a5-4196-11ec-8674-005056accf3f"
                }
            },
            "uuid": "ddabc6a5-4196-11ec-8674-005056accf3f",
        },
        "uuid": "a175c021-4199-11ec-8674-005056accf3f",
        "create_time": "2021-11-09T15:14:23-05:00",
        "comment": "manually created snapshot",
        "consistency_type": "crash",
    }
)

```
</div>
</div>

### Retrieving bulk snapshots
Retrieves the list of consistency group granular snapshots for all consistency groups on the cluster.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroupSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ConsistencyGroupSnapshot.get_collection("*")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    ConsistencyGroupSnapshot(
        {
            "name": "cg3ss",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/1218f900-c124-11ee-bbfe-005056acb65e/snapshots/7da4d364-c12e-11ee-bbfe-005056acb65e"
                }
            },
            "consistency_group": {
                "name": "cg3",
                "_links": {
                    "self": {
                        "href": "/api/application/consistency-groups/1218f900-c124-11ee-bbfe-005056acb65e"
                    }
                },
                "uuid": "1218f900-c124-11ee-bbfe-005056acb65e",
            },
            "uuid": "7da4d364-c12e-11ee-bbfe-005056acb65e",
        }
    ),
    ConsistencyGroupSnapshot(
        {
            "name": "cg2ss",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/15a8f66e-c124-11ee-bbfe-005056acb65e/snapshots/83595384-c12e-11ee-bbfe-005056acb65e"
                }
            },
            "consistency_group": {
                "name": "cg2",
                "_links": {
                    "self": {
                        "href": "/api/application/consistency-groups/15a8f66e-c124-11ee-bbfe-005056acb65e"
                    }
                },
                "uuid": "15a8f66e-c124-11ee-bbfe-005056acb65e",
            },
            "uuid": "83595384-c12e-11ee-bbfe-005056acb65e",
        }
    ),
    ConsistencyGroupSnapshot(
        {
            "name": "cg1ss",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/1c101d17-c124-11ee-bbfe-005056acb65e/snapshots/87d0e49c-c12e-11ee-bbfe-005056acb65e"
                }
            },
            "consistency_group": {
                "name": "cg1",
                "_links": {
                    "self": {
                        "href": "/api/application/consistency-groups/1c101d17-c124-11ee-bbfe-005056acb65e"
                    }
                },
                "uuid": "1c101d17-c124-11ee-bbfe-005056acb65e",
            },
            "uuid": "87d0e49c-c12e-11ee-bbfe-005056acb65e",
        }
    ),
]

```
</div>
</div>

### Creating a crash-consistent snapshot of a consistency group
Creates an on-demand crash-consistent snapshot of an existing consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroupSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroupSnapshot("a8d0626a-17a0-11eb-b141-005056acd498")
    resource.name = "name_of_this_snapshot"
    resource.consistency_type = "crash"
    resource.comment = "this is a manually created on-demand snapshot"
    resource.snapmirror_label = "my_special_sm_label"
    resource.post(hydrate=True)
    print(resource)

```

### Creating a app-consistent snapshot of a consistency group
Creates an on-demand crash-consistent snapshot of an existing consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroupSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroupSnapshot("a8d0626a-17a0-11eb-b141-005056acd498")
    resource.name = "name_of_this_snapshot"
    resource.consistency_type = "application"
    resource.comment = "this is a manually created on-demand snapshot"
    resource.snapmirror_label = "my_special_sm_label"
    resource.post(hydrate=True)
    print(resource)

```

### Starting a two-phase crash-consistent snapshot creation for a consistency group
Starts a two-phase on-demand crash-consistent snapshot creation for an existing consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroupSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroupSnapshot("a8d0626a-17a0-11eb-b141-005056acd498")
    resource.name = "name_of_this_snapshot"
    resource.consistency_type = "application"
    resource.comment = "this is a manually created on-demand snapshot"
    resource.snapmirror_label = "my_special_sm_label"
    resource.post(hydrate=True, action="start", action_timeout=7)
    print(resource)

```

### Committing a previously started two-phase crash-consistent snapshot creation for a consistency group
Commits a previously started two-phase on-demand crash-consistent snapshot creation for an existing consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroupSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroupSnapshot(
        "a8d0626a-17a0-11eb-b141-005056acd498",
        uuid="7aac0607-0c4d-11ee-ad32-005056a73101",
    )
    resource.patch(hydrate=True, action="commit")

```

### Deleting a snapshot from a consistency group
Deletes an existing snapshot from a consistency group.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConsistencyGroupSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConsistencyGroupSnapshot(
        "a8d0626a-17a0-11eb-b141-005056acd498",
        uuid="92c6c770-17a1-11eb-b141-005056acd498",
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


__all__ = ["ConsistencyGroupSnapshot", "ConsistencyGroupSnapshotSchema"]
__pdoc__ = {
    "ConsistencyGroupSnapshotSchema.resource": False,
    "ConsistencyGroupSnapshotSchema.opts": False,
}


class ConsistencyGroupSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupSnapshot object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the consistency_group_snapshot."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" Comment for the snapshot.


Example: My snapshot comment"""

    consistency_group = marshmallow_fields.Nested("netapp_ontap.resources.consistency_group.ConsistencyGroupSchema", data_key="consistency_group", unknown=EXCLUDE, allow_none=True)
    r""" The consistency_group field of the consistency_group_snapshot."""

    consistency_type = marshmallow_fields.Str(
        data_key="consistency_type",
        validate=enum_validation(['crash', 'application']),
        allow_none=True,
    )
    r""" Consistency type. This is for categorization purposes only. A snapshot should not be set to 'application consistent' unless the host application is quiesced for the snapshot. Valid in POST.


Valid choices:

* crash
* application"""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" Time the snapshot copy was created


Example: 2020-10-25T11:20:00.000+0000"""

    is_partial = marshmallow_fields.Boolean(
        data_key="is_partial",
        allow_none=True,
    )
    r""" Indicates whether the snapshot taken is partial or not.


Example: false"""

    luns = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.lun.LunSchema", unknown=EXCLUDE, allow_none=True), data_key="luns", allow_none=True)
    r""" The list of LUNs in this snapshot."""

    missing_luns = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.lun.LunSchema", unknown=EXCLUDE, allow_none=True), data_key="missing_luns", allow_none=True)
    r""" List of LUNs that are not in the snapshot."""

    missing_namespaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.nvme_namespace.NvmeNamespaceSchema", unknown=EXCLUDE, allow_none=True), data_key="missing_namespaces", allow_none=True)
    r""" List of NVMe namespaces that are not in the snapshot."""

    missing_volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, allow_none=True), data_key="missing_volumes", allow_none=True)
    r""" List of volumes which are not in the snapshot."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the snapshot."""

    namespaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.nvme_namespace.NvmeNamespaceSchema", unknown=EXCLUDE, allow_none=True), data_key="namespaces", allow_none=True)
    r""" The list of NVMe namespaces in this snapshot."""

    reclaimable_space = Size(
        data_key="reclaimable_space",
        allow_none=True,
    )
    r""" Space reclaimed when the snapshot is deleted, in bytes."""

    restore_size = Size(
        data_key="restore_size",
        allow_none=True,
    )
    r""" Size of the consistency group if this snapshot is restored.

Example: 4096"""

    snaplock = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_snapshot_snaplock.ConsistencyGroupSnapshotSnaplockSchema", data_key="snaplock", unknown=EXCLUDE, allow_none=True)
    r""" SnapLock Snapshot attributes."""

    snapmirror_label = marshmallow_fields.Str(
        data_key="snapmirror_label",
        allow_none=True,
    )
    r""" Snapmirror Label for the snapshot.


Example: sm_label"""

    snapshot_volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_volume_snapshot.ConsistencyGroupVolumeSnapshotSchema", unknown=EXCLUDE, allow_none=True), data_key="snapshot_volumes", allow_none=True)
    r""" List of volume and snapshot identifiers for each volume in the snapshot."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The SVM in which the consistency group is located."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the snapshot. The UUID is generated
by ONTAP when the snapshot is created.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    write_fence = marshmallow_fields.Boolean(
        data_key="write_fence",
        allow_none=True,
    )
    r""" Specifies whether a write fence will be taken when creating the snapshot. The default is false if there is only one volume in the consistency group, otherwise the default is true."""

    @property
    def resource(self):
        return ConsistencyGroupSnapshot

    gettable_fields = [
        "links",
        "comment",
        "consistency_group.links",
        "consistency_group.name",
        "consistency_group.uuid",
        "consistency_type",
        "create_time",
        "is_partial",
        "luns.links",
        "luns.name",
        "luns.uuid",
        "missing_luns",
        "missing_namespaces.links",
        "missing_namespaces.name",
        "missing_namespaces.uuid",
        "missing_volumes",
        "name",
        "namespaces.links",
        "namespaces.name",
        "namespaces.uuid",
        "reclaimable_space",
        "restore_size",
        "snaplock",
        "snapmirror_label",
        "snapshot_volumes",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "write_fence",
    ]
    """links,comment,consistency_group.links,consistency_group.name,consistency_group.uuid,consistency_type,create_time,is_partial,luns.links,luns.name,luns.uuid,missing_luns,missing_namespaces.links,missing_namespaces.name,missing_namespaces.uuid,missing_volumes,name,namespaces.links,namespaces.name,namespaces.uuid,reclaimable_space,restore_size,snaplock,snapmirror_label,snapshot_volumes,svm.links,svm.name,svm.uuid,uuid,write_fence,"""

    patchable_fields = [
        "consistency_type",
        "name",
        "snaplock",
        "svm.name",
        "svm.uuid",
        "write_fence",
    ]
    """consistency_type,name,snaplock,svm.name,svm.uuid,write_fence,"""

    postable_fields = [
        "comment",
        "consistency_type",
        "name",
        "snaplock",
        "snapmirror_label",
        "svm.name",
        "svm.uuid",
        "write_fence",
    ]
    """comment,consistency_type,name,snaplock,snapmirror_label,svm.name,svm.uuid,write_fence,"""

class ConsistencyGroupSnapshot(Resource):
    """Allows interaction with ConsistencyGroupSnapshot objects on the host"""

    _schema = ConsistencyGroupSnapshotSchema
    _path = "/api/application/consistency-groups/{consistency_group[uuid]}/snapshots"
    _keys = ["consistency_group.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves snapshots for a consistency group.
## Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `is_partial`
* `missing_volumes.uuid`
* `missing_volumes.name`

### Learn more
* [`DOC /application/consistency-groups/{consistency_group.uuid}/snapshots`](#docs-application-application_consistency-groups_{consistency_group.uuid}_snapshots)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all ConsistencyGroupSnapshot resources that match the provided query"""
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
        """Returns a list of RawResources that represent ConsistencyGroupSnapshot resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["ConsistencyGroupSnapshot"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Completes a snapshot operation of a consistency group. This can also be used to modify the SnapLock expiry time of a locked snapshot in SnapLock for SnapVault destination.
## Example
### Completing a snapshot operation
  The following example shows how to complete the snapshot operation by committing an existing snapshot to disk:
  ```
  curl -X PATCH https://<mgmt-ip>/api/application/consistency-groups/a8d0626a-17a0-11eb-b141-005056acd498/snapshots/92c6c770-17a1-11eb-b141-005056acd498?action=commit
  ```
#### Response:
  ```
  {
  }
  ```
### Modifying the SnapLock expiry time of a snapshot in SnapLock for SnapVault
  The following example shows how to modify the SnapLock expiry time of a locked snapshot in SnapLock for SnapVault destination:
  ```
  curl -X PATCH 'https://<mgmt-ip>/api/application/consistency-groups/a8d0626a-17a0-11eb-b141-005056acd498/snapshots/92c6c770-17a1-11eb-b141-005056acd498' -d '{"snaplock.expiry_time" : "2/28/2024 10:11:10 +05:30"}' -H "accept: application/hal+json"
  ```
#### Response:
  ```
  {
    "job": {
      "uuid": "8c9cabf3-0a88-11ec-a449-005056bbcf9f",
      "_links": {
        "self": {
          "href": "/api/cluster/jobs/8c9cabf3-0a88-11ec-a449-005056bbcf9f"
        }
      }
    }
  }
  ```

### Learn more
* [`DOC /application/consistency-groups/{consistency_group.uuid}/snapshots`](#docs-application-application_consistency-groups_{consistency_group.uuid}_snapshots)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["ConsistencyGroupSnapshot"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["ConsistencyGroupSnapshot"], NetAppResponse]:
        r"""Creates a snapshot of an existing consistency group.
### Required properties
* `consistency_group.uuid` - Existing consistency group UUID in which to create the snapshot.

### Learn more
* [`DOC /application/consistency-groups/{consistency_group.uuid}/snapshots`](#docs-application-application_consistency-groups_{consistency_group.uuid}_snapshots)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["ConsistencyGroupSnapshot"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a snapshot of a consistency group.
## Examples

### Learn more
* [`DOC /application/consistency-groups/{consistency_group.uuid}/snapshots`](#docs-application-application_consistency-groups_{consistency_group.uuid}_snapshots)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves snapshots for a consistency group.
## Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `is_partial`
* `missing_volumes.uuid`
* `missing_volumes.name`

### Learn more
* [`DOC /application/consistency-groups/{consistency_group.uuid}/snapshots`](#docs-application-application_consistency-groups_{consistency_group.uuid}_snapshots)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details of a specific snapshot for a consistency group.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `is_partial`
* `missing_volumes.uuid`
* `missing_volumes.name`

### Learn more
* [`DOC /application/consistency-groups/{consistency_group.uuid}/snapshots`](#docs-application-application_consistency-groups_{consistency_group.uuid}_snapshots)"""
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
        r"""Creates a snapshot of an existing consistency group.
### Required properties
* `consistency_group.uuid` - Existing consistency group UUID in which to create the snapshot.

### Learn more
* [`DOC /application/consistency-groups/{consistency_group.uuid}/snapshots`](#docs-application-application_consistency-groups_{consistency_group.uuid}_snapshots)"""
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
        r"""Completes a snapshot operation of a consistency group. This can also be used to modify the SnapLock expiry time of a locked snapshot in SnapLock for SnapVault destination.
## Example
### Completing a snapshot operation
  The following example shows how to complete the snapshot operation by committing an existing snapshot to disk:
  ```
  curl -X PATCH https://<mgmt-ip>/api/application/consistency-groups/a8d0626a-17a0-11eb-b141-005056acd498/snapshots/92c6c770-17a1-11eb-b141-005056acd498?action=commit
  ```
#### Response:
  ```
  {
  }
  ```
### Modifying the SnapLock expiry time of a snapshot in SnapLock for SnapVault
  The following example shows how to modify the SnapLock expiry time of a locked snapshot in SnapLock for SnapVault destination:
  ```
  curl -X PATCH 'https://<mgmt-ip>/api/application/consistency-groups/a8d0626a-17a0-11eb-b141-005056acd498/snapshots/92c6c770-17a1-11eb-b141-005056acd498' -d '{"snaplock.expiry_time" : "2/28/2024 10:11:10 +05:30"}' -H "accept: application/hal+json"
  ```
#### Response:
  ```
  {
    "job": {
      "uuid": "8c9cabf3-0a88-11ec-a449-005056bbcf9f",
      "_links": {
        "self": {
          "href": "/api/cluster/jobs/8c9cabf3-0a88-11ec-a449-005056bbcf9f"
        }
      }
    }
  }
  ```

### Learn more
* [`DOC /application/consistency-groups/{consistency_group.uuid}/snapshots`](#docs-application-application_consistency-groups_{consistency_group.uuid}_snapshots)"""
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
        r"""Deletes a snapshot of a consistency group.
## Examples

### Learn more
* [`DOC /application/consistency-groups/{consistency_group.uuid}/snapshots`](#docs-application-application_consistency-groups_{consistency_group.uuid}_snapshots)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


