r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A snapshot is the view of the filesystem as it exists at the time when the snapshot is created. <br/>
In ONTAP, different types of snapshots are supported, such as scheduled snapshots, user requested snapshots, SnapMirror snapshots, and so on. <br/>
ONTAP snapshot APIs allow you to create, modify, delete and retrieve snapshots. <br/>
ONTAP Bulk snapshot APIs allow you to create, modify, delete and retrieve snapshots on multiple volumes in one request. <br/>
## Snapshot APIs
The following APIs are used to perform operations related to snapshots.

* POST      /api/storage/volumes/{volume.uuid}/snapshots
* GET       /api/storage/volumes/{volume.uuid}/snapshots
* GET       /api/storage/volumes/{volume.uuid}/snapshots/{uuid}
* PATCH     /api/storage/volumes/{volume.uuid}/snapshots/{uuid}
* DELETE    /api/storage/volumes/{volume.uuid}/snapshots/{uuid}
The following APIs are used to perform bulk operations related to snapshots.

* POST      /api/storage/volumes/*/snapshots
* GET       /api/storage/volumes/*/snapshots
* PATCH     /api/storage/volumes/*/snapshots/{uuid}
* DELETE    /api/storage/volumes/*/snapshots/{uuid}
## Examples
### Creating a snapshot
The POST operation is used to create a snapshot with the specified attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snapshot("{volume.uuid}")
    resource.name = "snapshot_copy"
    resource.comment = "Store this copy."
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Snapshot(
    {
        "name": "snapshot_copy",
        "svm": {"name": "vs0", "uuid": "8139f958-3c6e-11e9-a45f-005056bbc848"},
        "comment": "Store this copy.",
        "volume": {"name": "v2"},
    }
)

```
</div>
</div>

### Retrieving snapshot attributes
The GET operation is used to retrieve snapshot attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Snapshot.get_collection("{volume.uuid}")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    Snapshot(
        {
            "name": "hourly.2019-03-13_1305",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/0353dc05-405f-11e9-acb6-005056bbc848/snapshots/402b6c73-73a0-4e89-a58a-75ee0ab3e8c0"
                }
            },
            "uuid": "402b6c73-73a0-4e89-a58a-75ee0ab3e8c0",
        }
    ),
    Snapshot(
        {
            "name": "hourly.2019-03-13_1405",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/0353dc05-405f-11e9-acb6-005056bbc848/snapshots/f0dd497f-efe8-44b7-a4f4-bdd3890bc0c8"
                }
            },
            "uuid": "f0dd497f-efe8-44b7-a4f4-bdd3890bc0c8",
        }
    ),
    Snapshot(
        {
            "name": "hourly.2019-03-13_1522",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/0353dc05-405f-11e9-acb6-005056bbc848/snapshots/02701900-51bd-46b8-9c77-47d9a9e2ce1d"
                }
            },
            "uuid": "02701900-51bd-46b8-9c77-47d9a9e2ce1d",
        }
    ),
]

```
</div>
</div>

### Creating bulk snapshots
The POST operation is used to create a snapshot with the same name on multiple volumes in one request.
This operation accepts a volume UUID or volume name and SVM, and a snapshot name.
This operation only supports SnapMirror label attributes to be added to snapshots during creation.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snapshot("*")
    resource.records = [
        {
            "volume.uuid": "e8815adb-5209-11ec-b4ad-005056bbc3e8",
            "name": "snapshot_copy",
        },
        {
            "volume.uuid": "efda9101-5209-11ec-b4ad-005056bbc3e8",
            "name": "snapshot_copy",
        },
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
Snapshot({})

```
</div>
</div>

### Retrieving snapshot advanced attributes
A collection GET request is used to calculate the amount of snapshot reclaimable space.
When the advanced privilege field 'reclaimable space' is requested, the API returns the amount of reclaimable space for the queried list of snapshots.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            Snapshot.get_collection(
                "{volume.uuid}",
                fields="reclaimable_space",
                name="hourly.2019-03-13_1305|hourly.2019-03-13_1405|hourly.2019-03-13_1522",
            )
        )
    )

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    Snapshot(
        {
            "name": "hourly.2019-03-13_1305",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/0353dc05-405f-11e9-acb6-005056bbc848/snapshots/402b6c73-73a0-4e89-a58a-75ee0ab3e8c0"
                }
            },
            "uuid": "402b6c73-73a0-4e89-a58a-75ee0ab3e8c0",
        }
    ),
    Snapshot(
        {
            "name": "hourly.2019-03-13_1405",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/0353dc05-405f-11e9-acb6-005056bbc848/snapshots/f0dd497f-efe8-44b7-a4f4-bdd3890bc0c8"
                }
            },
            "uuid": "f0dd497f-efe8-44b7-a4f4-bdd3890bc0c8",
        }
    ),
    Snapshot(
        {
            "name": "hourly.2019-03-13_1522",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/0353dc05-405f-11e9-acb6-005056bbc848/snapshots/02701900-51bd-46b8-9c77-47d9a9e2ce1d"
                }
            },
            "uuid": "02701900-51bd-46b8-9c77-47d9a9e2ce1d",
        }
    ),
]

```
</div>
</div>

### Retrieving snapshot advanced attributes
A collection GET request is used to calculate the delta between two snapshots.
When the advanced privilege field 'delta' is requested, the API returns the delta between the queried snapshots.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            Snapshot.get_collection(
                "{volume.uuid}",
                fields="delta",
                name="hourly.2022-06-29_1105,hourly.2022-06-29_1205",
            )
        )
    )

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[
    Snapshot(
        {
            "name": "hourly.2022-06-29_1105",
            "uuid": "52a2247a-7735-4a92-bc3c-e51df1fe502f",
            "delta": {"size_consumed": 675840, "time_elapsed": "PT3H27M45S"},
        }
    ),
    Snapshot(
        {
            "name": "hourly.2022-06-29_1205",
            "uuid": "b399eb34-44fe-4689-9fb5-c8f72162dd77",
            "delta": {"size_consumed": 507904, "time_elapsed": "PT2H27M45S"},
        }
    ),
]

```
</div>
</div>

### Retrieving the attributes of a specific snapshot
The GET operation is used to retrieve the attributes of a specific snapshot.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snapshot(
        "0353dc05-405f-11e9-acb6-005056bbc848",
        uuid="402b6c73-73a0-4e89-a58a-75ee0ab3e8c0",
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
Snapshot(
    {
        "name": "hourly.2019-03-13_1305",
        "_links": {
            "self": {
                "href": "/api/storage/volumes/0353dc05-405f-11e9-acb6-005056bbc848/snapshots/402b6c73-73a0-4e89-a58a-75ee0ab3e8c0"
            }
        },
        "svm": {
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svm/svms/8139f958-3c6e-11e9-a45f-005056bbc848"}
            },
            "uuid": "8139f958-3c6e-11e9-a45f-005056bbc848",
        },
        "uuid": "402b6c73-73a0-4e89-a58a-75ee0ab3e8c0",
        "create_time": "2019-03-13T13:05:00-04:00",
        "size": 122880,
        "volume": {
            "name": "v2",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/0353dc05-405f-11e9-acb6-005056bbc848"
                }
            },
            "uuid": "0353dc05-405f-11e9-acb6-005056bbc848",
        },
    }
)

```
</div>
</div>

### Retrieving the advanced attributes of a specific snapshot
The GET operation is used to retrieve the attributes of a specific snapshot. Snapshot reclaimable space can be requested during a GET request.
When the advanced privilege field reclaimable space is requested, the API returns the amount of reclaimable space for the snapshot.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snapshot(
        "0353dc05-405f-11e9-acb6-005056bbc848",
        uuid="402b6c73-73a0-4e89-a58a-75ee0ab3e8c0",
    )
    resource.get(fields="**")
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
Snapshot(
    {
        "name": "hourly.2019-03-13_1305",
        "_links": {
            "self": {
                "href": "/api/storage/volumes/0353dc05-405f-11e9-acb6-005056bbc848/snapshots/402b6c73-73a0-4e89-a58a-75ee0ab3e8c0"
            }
        },
        "reclaimable_space": 167832,
        "svm": {
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svm/svms/8139f958-3c6e-11e9-a45f-005056bbc848"}
            },
            "uuid": "8139f958-3c6e-11e9-a45f-005056bbc848",
        },
        "uuid": "402b6c73-73a0-4e89-a58a-75ee0ab3e8c0",
        "volume": {
            "name": "v2",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/0353dc05-405f-11e9-acb6-005056bbc848"
                }
            },
            "uuid": "0353dc05-405f-11e9-acb6-005056bbc848",
        },
    }
)

```
</div>
</div>

### Retrieving snapshot advanced attributes
A collection GET request is used to calculate the delta between two snapshots.
When the advanced privilege field 'delta' is requested, the API returns the delta between the queried snapshots.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            Snapshot.get_collection(
                "{volume.uuid}",
                fields="delta",
                name="hourly.2022-06-29_1105,hourly.2022-06-29_1205",
            )
        )
    )

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[
    Snapshot(
        {
            "name": "hourly.2022-06-29_1105",
            "uuid": "52a2247a-7735-4a92-bc3c-e51df1fe502f",
            "delta": {"size_consumed": 675840, "time_elapsed": "PT3H27M45S"},
        }
    ),
    Snapshot(
        {
            "name": "hourly.2022-06-29_1205",
            "uuid": "b399eb34-44fe-4689-9fb5-c8f72162dd77",
            "delta": {"size_consumed": 507904, "time_elapsed": "PT2H27M45S"},
        }
    ),
]

```
</div>
</div>

### Retrieving bulk snapshots
The bulk GET operation is used to retrieve snapshot attributes across all volumes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Snapshot.get_collection("*")))

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
[
    Snapshot(
        {
            "name": "daily.2021-11-18_0010",
            "uuid": "3edba912-5507-4535-adce-e12fe5c0e31c",
            "volume": {"name": "v1", "uuid": "966c285f-47f7-11ec-8407-005056bbc08f"},
        }
    ),
    Snapshot(
        {
            "name": "hourly.2021-11-18_0705",
            "uuid": "3ad61153-d5ef-495d-8e0e-5c3b8bbaf5e6",
            "volume": {"name": "v1", "uuid": "966c285f-47f7-11ec-8407-005056bbc08f"},
        }
    ),
    Snapshot(
        {
            "name": "daily.2021-11-18_0010",
            "uuid": "3dd0fa97-65d9-41ea-a99d-5ceb9d2f55c5",
            "volume": {"name": "v2", "uuid": "99c974e3-47f7-11ec-8407-005056bbc08f"},
        }
    ),
    Snapshot(
        {
            "name": "hourly.2021-11-18_0705",
            "uuid": "6ca20a52-c342-4753-8865-3693fa9b7e23",
            "volume": {"name": "v2", "uuid": "99c974e3-47f7-11ec-8407-005056bbc08f"},
        }
    ),
]

```
</div>
</div>

### Updating a snapshot
The PATCH operation is used to update the specific attributes of a snapshot.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snapshot(
        "0353dc05-405f-11e9-acb6-005056bbc848",
        uuid="16f7008c-18fd-4a7d-8485-a0e290d9db7f",
    )
    resource.name = "snapshot_copy_new"
    resource.patch()

```

### Updating bulk snapshots
The bulk PATCH operation is used to update the specific attributes of snapshots across volumes in a single request.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snapshot("*")
    resource.records = [
        {
            "volume.uuid": "e8815adb-5209-11ec-b4ad-005056bbc3e8",
            "svm.uuid": "d0e6def5-5209-11ec-b4ad-005056bbc3e8",
            "uuid": "f9b7714d-1166-410a-b143-874f27969db6",
            "comment": "yay",
        },
        {
            "volume.uuid": "efda9101-5209-11ec-b4ad-005056bbc3e8",
            "svm.uuid": "d0e6def5-5209-11ec-b4ad-005056bbc3e8",
            "uuid": "514c82a7-bff7-48e2-a13c-5337b09ed41e",
            "comment": "yay",
        },
    ]
    resource.patch()

```

### Deleting a snapshot
The DELETE operation is used to delete a snapshot.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snapshot(
        "0353dc05-405f-11e9-acb6-005056bbc848",
        uuid="16f7008c-18fd-4a7d-8485-a0e290d9db7f",
    )
    resource.delete()

```

### Deleting bulk snapshots
The bulk DELETE operation is used to delete a snapshots across volumes in a single request.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snapshot("*")
    resource.delete(
        body={
            "records": [
                {
                    "volume.uuid": "e8815adb-5209-11ec-b4ad-005056bbc3e8",
                    "uuid": "f9b7714d-1166-410a-b143-874f27969db6",
                },
                {
                    "volume.uuid": "efda9101-5209-11ec-b4ad-005056bbc3e8",
                    "uuid": "1d55c97a-25f3-4366-bfa8-9ea75c255469",
                },
            ]
        }
    )

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


__all__ = ["Snapshot", "SnapshotSchema"]
__pdoc__ = {
    "SnapshotSchema.resource": False,
    "SnapshotSchema.opts": False,
}


class SnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Snapshot object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snapshot."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" A comment associated with the snapshot. This is an optional attribute for POST or PATCH."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" Creation time of the snapshot. It is the volume access time when the snapshot was created.

Example: 2019-02-04T19:00:00.000+0000"""

    delta = marshmallow_fields.Nested("netapp_ontap.models.snapshot_delta.SnapshotDeltaSchema", data_key="delta", unknown=EXCLUDE, allow_none=True)
    r""" Reports the amount of space consumed between two WAFL file systems, in bytes. The two WAFL file systems should be specified in a comma-separated format using the "name" parameter. To determine the space consumed between a snapshot and the Active File System, only the snapshot name needs to be mentioned."""

    expiry_time = ImpreciseDateTime(
        data_key="expiry_time",
        allow_none=True,
    )
    r""" The expiry time for the snapshot. This is an optional attribute for POST or PATCH. Snapshots with an expiry time set are not allowed to be deleted until the retention time is reached.

Example: 2019-02-04T19:00:00.000+0000"""

    logical_size = Size(
        data_key="logical_size",
        allow_none=True,
    )
    r""" Size of the logical used file system at the time the snapshot is captured.

Example: 1228800"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Snapshot. Valid in POST or PATCH.

Example: this_snapshot"""

    owners = marshmallow_fields.List(marshmallow_fields.Str, data_key="owners", allow_none=True)
    r""" The owners field of the snapshot."""

    provenance_volume = marshmallow_fields.Nested("netapp_ontap.models.snapshot_provenance_volume.SnapshotProvenanceVolumeSchema", data_key="provenance_volume", unknown=EXCLUDE, allow_none=True)
    r""" The provenance_volume field of the snapshot."""

    reclaimable_space = Size(
        data_key="reclaimable_space",
        allow_none=True,
    )
    r""" Space reclaimed when the snapshot is deleted, in bytes."""

    size = Size(
        data_key="size",
        allow_none=True,
    )
    r""" Size of the active file system at the time the snapshot is captured. The actual size of the snapshot also includes those blocks trapped by other snapshots. On a snapshot deletion, the "size" amount of blocks is the maximum number of blocks available. On a snapshot restore, the "afs-used size" value will match the snapshot "size" value.

Example: 122880"""

    snaplock = marshmallow_fields.Nested("netapp_ontap.models.snapshot_snaplock.SnapshotSnaplockSchema", data_key="snaplock", unknown=EXCLUDE, allow_none=True)
    r""" The snaplock field of the snapshot."""

    snaplock_expiry_time = ImpreciseDateTime(
        data_key="snaplock_expiry_time",
        allow_none=True,
    )
    r""" SnapLock expiry time for the snapshot, if the snapshot is taken on a SnapLock volume. A snapshot is not allowed to be deleted or renamed until the SnapLock ComplianceClock time goes beyond this retention time. This option can be set during snapshot POST and snapshot PATCH on snapshot locking enabled volumes. This field will no longer be supported in a future release. Use snaplock.expiry_time instead.

Example: 2019-02-04T19:00:00.000+0000"""

    snapmirror_label = marshmallow_fields.Str(
        data_key="snapmirror_label",
        allow_none=True,
    )
    r""" Label for SnapMirror operations"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['valid', 'invalid', 'partial', 'unknown', 'pre_conversion']),
        allow_none=True,
    )
    r""" State of the FlexGroup volume snapshot. In the "pre_conversion" state, the snapshot was created before converting the FlexVol to a FlexGroup volume. A recently created snapshot can be in the "unknown" state while the system is calculating the state. In the "partial" state, the snapshot is consistent but exists only on the subset of the constituents that existed prior to the FlexGroup's expansion. Partial snapshots cannot be used for a snapshot restore operation. A snapshot is in an "invalid" state when it is present in some FlexGroup constituents but not in others. At all other times, a snapshot is valid.

Valid choices:

* valid
* invalid
* partial
* unknown
* pre_conversion"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the snapshot."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The UUID of the snapshot in the volume that uniquely identifies the snapshot in that volume.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    version_uuid = marshmallow_fields.Str(
        data_key="version_uuid",
        allow_none=True,
    )
    r""" The 128 bit identifier that uniquely identifies a snapshot and its logical data layout.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the snapshot."""

    @property
    def resource(self):
        return Snapshot

    gettable_fields = [
        "links",
        "comment",
        "create_time",
        "delta",
        "expiry_time",
        "logical_size",
        "name",
        "owners",
        "provenance_volume",
        "reclaimable_space",
        "size",
        "snaplock",
        "snaplock_expiry_time",
        "snapmirror_label",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "version_uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,comment,create_time,delta,expiry_time,logical_size,name,owners,provenance_volume,reclaimable_space,size,snaplock,snaplock_expiry_time,snapmirror_label,state,svm.links,svm.name,svm.uuid,uuid,version_uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "comment",
        "delta",
        "expiry_time",
        "name",
        "provenance_volume",
        "reclaimable_space",
        "snaplock",
        "snaplock_expiry_time",
        "snapmirror_label",
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """comment,delta,expiry_time,name,provenance_volume,reclaimable_space,snaplock,snaplock_expiry_time,snapmirror_label,svm.name,svm.uuid,volume.name,volume.uuid,"""

    postable_fields = [
        "comment",
        "delta",
        "expiry_time",
        "name",
        "provenance_volume",
        "reclaimable_space",
        "snaplock",
        "snaplock_expiry_time",
        "snapmirror_label",
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """comment,delta,expiry_time,name,provenance_volume,reclaimable_space,snaplock,snaplock_expiry_time,snapmirror_label,svm.name,svm.uuid,volume.name,volume.uuid,"""

class Snapshot(Resource):
    r""" The snapshot object represents a point in time snapshot of a volume. """

    _schema = SnapshotSchema
    _path = "/api/storage/volumes/{volume[uuid]}/snapshots"
    _keys = ["volume.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of volume snapshots.
### Expensive properties
There is an added computational cost to retrieving the amount of reclaimable space for snapshots, as the calculation is done on demand based on the list of snapshots provided.
* `reclaimable_space`
* `delta`
### Related ONTAP commands
* `snapshot show`
* `snapshot compute-reclaimable`
* `snapshot show-delta`
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/snapshots`](#docs-storage-storage_volumes_{volume.uuid}_snapshots)
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
        """Returns a count of all Snapshot resources that match the provided query"""
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
        """Returns a list of RawResources that represent Snapshot resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Snapshot"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a Volume snapshot.
### Platform Specifics
* **ASA r2**: POST is not supported.
### Related ONTAP commands
* `snapshot modify`
* `snapshot rename`
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/snapshots`](#docs-storage-storage_volumes_{volume.uuid}_snapshots)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Snapshot"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Snapshot"], NetAppResponse]:
        r"""Creates a volume snapshot.
### Platform Specifics
* **ASA r2**: POST is not supported.
### Required properties
* `name` - Name of the snapshot to be created.
### Recommended optional properties
* `comment` - Comment associated with the snapshot.
* `expiry_time` - snapshots with an expiry time set are not allowed to be deleted until the retention time is reached.
* `snapmirror_label` - Label for SnapMirror operations.
* `snaplock_expiry_time` - Expiry time for snapshot locking enabled volumes.
### Related ONTAP commands
* `snapshot create`
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/snapshots`](#docs-storage-storage_volumes_{volume.uuid}_snapshots)
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
        records: Iterable["Snapshot"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a Volume snapshot.
### Platform Specifics
* **ASA r2**: POST is not supported.
### Related ONTAP commands
* `snapshot delete`
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/snapshots`](#docs-storage-storage_volumes_{volume.uuid}_snapshots)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of volume snapshots.
### Expensive properties
There is an added computational cost to retrieving the amount of reclaimable space for snapshots, as the calculation is done on demand based on the list of snapshots provided.
* `reclaimable_space`
* `delta`
### Related ONTAP commands
* `snapshot show`
* `snapshot compute-reclaimable`
* `snapshot show-delta`
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/snapshots`](#docs-storage-storage_volumes_{volume.uuid}_snapshots)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details of a specific volume snapshot.
### Related ONTAP commands
* `snapshot show`
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/snapshots`](#docs-storage-storage_volumes_{volume.uuid}_snapshots)
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
        r"""Creates a volume snapshot.
### Platform Specifics
* **ASA r2**: POST is not supported.
### Required properties
* `name` - Name of the snapshot to be created.
### Recommended optional properties
* `comment` - Comment associated with the snapshot.
* `expiry_time` - snapshots with an expiry time set are not allowed to be deleted until the retention time is reached.
* `snapmirror_label` - Label for SnapMirror operations.
* `snaplock_expiry_time` - Expiry time for snapshot locking enabled volumes.
### Related ONTAP commands
* `snapshot create`
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/snapshots`](#docs-storage-storage_volumes_{volume.uuid}_snapshots)
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
        r"""Updates a Volume snapshot.
### Platform Specifics
* **ASA r2**: POST is not supported.
### Related ONTAP commands
* `snapshot modify`
* `snapshot rename`
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/snapshots`](#docs-storage-storage_volumes_{volume.uuid}_snapshots)
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
        r"""Deletes a Volume snapshot.
### Platform Specifics
* **ASA r2**: POST is not supported.
### Related ONTAP commands
* `snapshot delete`
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/snapshots`](#docs-storage-storage_volumes_{volume.uuid}_snapshots)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


