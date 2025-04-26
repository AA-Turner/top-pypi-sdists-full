r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A storage unit snapshot is the view of the storage unit as it exists at the time when the snapshot is created.<br/>
In ONTAP, different types of storage unit snapshots are supported, such as scheduled snapshots, user requested snapshots, SnapMirror snapshots, and so on. <br/>
ONTAP storage unit snapshot APIs allow you to create, modify, delete and retrieve snapshots. Scheduled snapshots may be operated on, but snapshot schedules are not supported from these APIs.<br/>
## Platform Specifics
### Unified ONTAP
This endpoint is not available.
## Examples
### Creating a snapshot
The POST operation is used to create a snapshot with the specified attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageUnitSnapshot("9034e72c-1d07-11ef-bd09-005056bbbc7b")
    resource.name = "snapshot_copy"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
StorageUnitSnapshot({"name": "snapshot_copy"})

```
</div>
</div>

---
### Retrieving snapshot attributes
The GET operation is used to retrieve snapshot attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(StorageUnitSnapshot.get_collection("9034e72c-1d07-11ef-bd09-005056bbbc7b"))
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    StorageUnitSnapshot(
        {
            "name": "weekly.2024-06-02_0015",
            "uuid": "f712e3ff-d958-47ba-89eb-d2a46bad7bd7",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/f712e3ff-d958-47ba-89eb-d2a46bad7bd7"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "daily.2024-06-04_0010",
            "uuid": "fd8b5ed5-fd24-45c6-bf96-996ab36bbb24",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/fd8b5ed5-fd24-45c6-bf96-996ab36bbb24"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "daily.2024-06-05_0010",
            "uuid": "e9f28652-9460-4eef-a8fd-fa0b0bfa97f3",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/e9f28652-9460-4eef-a8fd-fa0b0bfa97f3"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0405",
            "uuid": "c5620133-52d0-4821-8805-15bfcd1a7b1e",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/c5620133-52d0-4821-8805-15bfcd1a7b1e"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0505",
            "uuid": "4a83e47a-b865-416e-885e-d159e91e943b",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/4a83e47a-b865-416e-885e-d159e91e943b"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0605",
            "uuid": "7dca6423-4fce-47ba-a4dc-b69e32bb30f4",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/7dca6423-4fce-47ba-a4dc-b69e32bb30f4"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0705",
            "uuid": "0bd1ca63-dbf8-41c3-a7ef-2023f28e622b",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/0bd1ca63-dbf8-41c3-a7ef-2023f28e622b"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0805",
            "uuid": "71bdab1e-22b3-4b2f-9b2c-0d2072ab321a",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/71bdab1e-22b3-4b2f-9b2c-0d2072ab321a"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0905",
            "uuid": "1341b465-e582-4b30-aa87-d4642fe9db51",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/1341b465-e582-4b30-aa87-d4642fe9db51"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "snap1",
            "uuid": "cb8b57a1-2342-11ef-97b9-005056bbbc7b",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/cb8b57a1-2342-11ef-97b9-005056bbbc7b"
                }
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving snapshot advanced attributes
A collection GET request is used to calculate the amount of snapshot reclaimable space.
When the advanced privilege field 'reclaimable space' is requested, the API returns the amount of reclaimable space for the queried list of snapshots.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            StorageUnitSnapshot.get_collection(
                "9034e72c-1d07-11ef-bd09-005056bbbc7b",
                fields="reclaimable_space",
                name="hourly.2024-06-05_0705|hourly.2024-06-05_0805|hourly.2024-06-05_0905",
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
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0705",
            "uuid": "0bd1ca63-dbf8-41c3-a7ef-2023f28e622b",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/0bd1ca63-dbf8-41c3-a7ef-2023f28e622b"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0805",
            "uuid": "71bdab1e-22b3-4b2f-9b2c-0d2072ab321a",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/71bdab1e-22b3-4b2f-9b2c-0d2072ab321a"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0905",
            "uuid": "1341b465-e582-4b30-aa87-d4642fe9db51",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/1341b465-e582-4b30-aa87-d4642fe9db51"
                }
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving snapshot advanced attributes
A collection GET request is used to calculate the delta between two snapshots.
When the advanced privilege field 'delta' is requested, the API returns the delta between the queried snapshots.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            StorageUnitSnapshot.get_collection(
                "9034e72c-1d07-11ef-bd09-005056bbbc7b",
                fields="delta",
                name="hourly.2024-06-05_0705|hourly.2024-06-05_0805|hourly.2024-06-05_0905",
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
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0705",
            "uuid": "0bd1ca63-dbf8-41c3-a7ef-2023f28e622b",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/0bd1ca63-dbf8-41c3-a7ef-2023f28e622b"
                }
            },
            "delta": {"size_consumed": 1642496, "time_elapsed": "PT4H12M47S"},
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0805",
            "uuid": "71bdab1e-22b3-4b2f-9b2c-0d2072ab321a",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/71bdab1e-22b3-4b2f-9b2c-0d2072ab321a"
                }
            },
            "delta": {"size_consumed": 1331200, "time_elapsed": "PT3H12M47S"},
        }
    ),
    StorageUnitSnapshot(
        {
            "name": "hourly.2024-06-05_0905",
            "uuid": "1341b465-e582-4b30-aa87-d4642fe9db51",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/1341b465-e582-4b30-aa87-d4642fe9db51"
                }
            },
            "delta": {"size_consumed": 1052672, "time_elapsed": "PT2H12M47S"},
        }
    ),
]

```
</div>
</div>

---
### Retrieving the attributes of a specific snapshot
The GET operation is used to retrieve the attributes of a specific snapshot.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageUnitSnapshot(
        "9034e72c-1d07-11ef-bd09-005056bbbc7b",
        uuid="402b6c73-73a0-4e89-a58a-75ee0ab3e8c0",
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
StorageUnitSnapshot(
    {
        "create_time": "2024-06-02T00:15:00-04:00",
        "version_uuid": "f712e3ff-d958-47ba-89eb-d2a46bad7bd7",
        "storage_unit": {
            "name": "lun1",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b"
                }
            },
            "uuid": "9034e72c-1d07-11ef-bd09-005056bbbc7b",
        },
        "logical_size": 11259904,
        "name": "weekly.2024-06-02_0015",
        "uuid": "f712e3ff-d958-47ba-89eb-d2a46bad7bd7",
        "size": 720896,
        "_links": {
            "self": {
                "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/f712e3ff-d958-47ba-89eb-d2a46bad7bd7"
            }
        },
        "snapmirror_label": "weekly",
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/7cb65b79-1a0f-11ef-bd09-005056bbbc7b"}
            },
            "uuid": "7cb65b79-1a0f-11ef-bd09-005056bbbc7b",
        },
    }
)

```
</div>
</div>

---
### Retrieving the advanced attributes of a specific snapshot
In this example, the `fields` query parameter is used to request all fields, including advanced fields, that would not otherwise be returned by default for the snapshot.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageUnitSnapshot(
        "0353dc05-405f-11e9-acb6-005056bbc848",
        uuid="402b6c73-73a0-4e89-a58a-75ee0ab3e8c0",
    )
    resource.get(fields="**")
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
StorageUnitSnapshot(
    {
        "create_time": "2024-06-02T00:15:00-04:00",
        "version_uuid": "f712e3ff-d958-47ba-89eb-d2a46bad7bd7",
        "storage_unit": {
            "name": "lun1",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b"
                }
            },
            "uuid": "9034e72c-1d07-11ef-bd09-005056bbbc7b",
        },
        "logical_size": 11259904,
        "name": "weekly.2024-06-02_0015",
        "uuid": "f712e3ff-d958-47ba-89eb-d2a46bad7bd7",
        "size": 720896,
        "_links": {
            "self": {
                "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/f712e3ff-d958-47ba-89eb-d2a46bad7bd7?fields=**"
            }
        },
        "snapmirror_label": "weekly",
        "reclaimable_space": 503808,
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/7cb65b79-1a0f-11ef-bd09-005056bbbc7b"}
            },
            "uuid": "7cb65b79-1a0f-11ef-bd09-005056bbbc7b",
        },
        "delta": {"size_consumed": 3395584, "time_elapsed": "P3DT11H16M8S"},
    }
)

```
</div>
</div>

---
### Retrieving bulk snapshots
The bulk GET operation is used to retrieve snapshot attributes across all storage units.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(StorageUnitSnapshot.get_collection("*")))

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
[
    StorageUnitSnapshot(
        {
            "storage_unit": {
                "name": "ns1",
                "_links": {
                    "self": {
                        "href": "/api/storage/storage-units/3d9c001f-227e-11ef-97b9-005056bbbc7b"
                    }
                },
                "uuid": "3d9c001f-227e-11ef-97b9-005056bbbc7b",
            },
            "name": "daily.2024-06-05_0010",
            "uuid": "387d7ec5-1c56-4cbc-b50e-07ea67396712",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/3d9c001f-227e-11ef-97b9-005056bbbc7b/snapshots/387d7ec5-1c56-4cbc-b50e-07ea67396712"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "storage_unit": {
                "name": "ns1",
                "_links": {
                    "self": {
                        "href": "/api/storage/storage-units/3d9c001f-227e-11ef-97b9-005056bbbc7b"
                    }
                },
                "uuid": "3d9c001f-227e-11ef-97b9-005056bbbc7b",
            },
            "name": "hourly.2024-06-05_0805",
            "uuid": "44bfa234-c978-423c-a0d5-14fe5427e7ab",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/3d9c001f-227e-11ef-97b9-005056bbbc7b/snapshots/44bfa234-c978-423c-a0d5-14fe5427e7ab"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "storage_unit": {
                "name": "lun1",
                "_links": {
                    "self": {
                        "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b"
                    }
                },
                "uuid": "9034e72c-1d07-11ef-bd09-005056bbbc7b",
            },
            "name": "daily.2024-06-05_0010",
            "uuid": "e9f28652-9460-4eef-a8fd-fa0b0bfa97f3",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/e9f28652-9460-4eef-a8fd-fa0b0bfa97f3"
                }
            },
        }
    ),
    StorageUnitSnapshot(
        {
            "storage_unit": {
                "name": "lun1",
                "_links": {
                    "self": {
                        "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b"
                    }
                },
                "uuid": "9034e72c-1d07-11ef-bd09-005056bbbc7b",
            },
            "name": "hourly.2024-06-05_0805",
            "uuid": "71bdab1e-22b3-4b2f-9b2c-0d2072ab321a",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b/snapshots/71bdab1e-22b3-4b2f-9b2c-0d2072ab321a"
                }
            },
        }
    ),
]

```
</div>
</div>

---
### Updating a snapshot
The PATCH operation is used to update the specific attributes of a snapshot.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageUnitSnapshot(
        "9034e72c-1d07-11ef-bd09-005056bbbc7b",
        uuid="71bdab1e-22b3-4b2f-9b2c-0d2072ab321a",
    )
    resource.name = "snapshot_copy_new"
    resource.patch()

```

---
### Updating bulk snapshots
The bulk PATCH operation is used to update the specific attributes of snapshots across storage units in a single request. The storage unit and snapshot must be identified using their UUIDs.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageUnitSnapshot("*")
    resource.records = [
        {
            "storage_unit": {"uuid": "eaebc659-237b-11ef-a1bc-005056bbf4ce"},
            "svm": {"uuid": "97930c7c-2376-11ef-a1bc-005056bbf4ce"},
            "uuid": "d68eaa29-1d9d-4f6c-8069-c472dd6cc5f1",
            "comment": "new comment on lun1",
        },
        {
            "storage_unit": {"uuid": "d8ddfae9-240b-11ef-a1bc-005056bbf4ce"},
            "svm": {"uuid": "97930c7c-2376-11ef-a1bc-005056bbf4ce"},
            "uuid": "d4c1112f-1bca-4893-b21f-f1b3ef61049c",
            "comment": "new comment on ns1",
        },
    ]
    resource.patch()

```

---
### Deleting a snapshot
The DELETE operation is used to delete a snapshot.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageUnitSnapshot(
        "9034e72c-1d07-11ef-bd09-005056bbbc7b",
        uuid="ef73b086-2430-4b8b-b1a8-2d9b6f1bf48e",
    )
    resource.delete()

```

---
### Deleting bulk snapshots
The bulk DELETE operation is used to delete a snapshots across storage units in a single request.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageUnitSnapshot("*")
    resource.delete(
        body={
            "records": [
                {
                    "storage_unit": {"uuid": "d8ddfae9-240b-11ef-a1bc-005056bbf4ce"},
                    "uuid": "d4c1112f-1bca-4893-b21f-f1b3ef61049c",
                },
                {
                    "storage_unit": {"uuid": "eaebc659-237b-11ef-a1bc-005056bbf4ce"},
                    "uuid": "d68eaa29-1d9d-4f6c-8069-c472dd6cc5f1",
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


__all__ = ["StorageUnitSnapshot", "StorageUnitSnapshotSchema"]
__pdoc__ = {
    "StorageUnitSnapshotSchema.resource": False,
    "StorageUnitSnapshotSchema.opts": False,
}


class StorageUnitSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitSnapshot object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the storage_unit_snapshot."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=255),
        allow_none=True,
    )
    r""" A comment associated with the snapshot. Valid in POST and PATCH."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" Creation time of the snapshot. It is the storage unit access time when the snapshot was created.


Example: 2019-02-04T19:00:00.000+0000"""

    delta = marshmallow_fields.Nested("netapp_ontap.models.snapshot_delta.SnapshotDeltaSchema", data_key="delta", unknown=EXCLUDE, allow_none=True)
    r""" Reports the amount of space consumed between two WAFL file systems, in bytes. The two WAFL file systems should be specified in a comma-separated format using the "name" parameter. To determine the space consumed between a snapshot and the Active File System, only the snapshot name needs to be mentioned."""

    expiry_time = ImpreciseDateTime(
        data_key="expiry_time",
        allow_none=True,
    )
    r""" The expiry time for the snapshot. Snapshots with an expiry time set are not allowed to be deleted until the retention time is reached.


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
    r""" The name of the snapshot. Snapshot names cannot begin or end with whitespace. Valid in POST and PATCH.


Example: this_snapshot"""

    owners = marshmallow_fields.List(marshmallow_fields.Str, data_key="owners", allow_none=True)
    r""" The owners field of the storage_unit_snapshot."""

    reclaimable_space = Size(
        data_key="reclaimable_space",
        allow_none=True,
    )
    r""" Space reclaimed when the snapshot is deleted, in bytes."""

    size = Size(
        data_key="size",
        allow_none=True,
    )
    r""" Size of the active file system at the time the snapshot is captured. The actual size of the snapshot also includes those blocks trapped by other snapshots. On a snapshot deletion, the `size` amount of blocks is the maximum number of blocks available. On a snapshot restore, the "AFS used size" value will match the snapshot `size` value.


Example: 122880"""

    snaplock = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_snapshot_snaplock.StorageUnitSnapshotSnaplockSchema", data_key="snaplock", unknown=EXCLUDE, allow_none=True)
    r""" The snaplock field of the storage_unit_snapshot."""

    snapmirror_label = marshmallow_fields.Str(
        data_key="snapmirror_label",
        validate=len_validation(minimum=0, maximum=31),
        allow_none=True,
    )
    r""" Label for SnapMirror operations. Valid in POST and PATCH."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['valid', 'unknown']),
        allow_none=True,
    )
    r""" State of the FlexGroup volume snapshot. A recently created snapshot can be in the `unknown` state while the system is calculating the state. At all other times, a snapshot is valid.


Valid choices:

* valid
* unknown"""

    storage_unit = marshmallow_fields.Nested("netapp_ontap.resources.storage_unit.StorageUnitSchema", data_key="storage_unit", unknown=EXCLUDE, allow_none=True)
    r""" The storage_unit field of the storage_unit_snapshot."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the storage_unit_snapshot."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The UUID of the snapshot in the storage unit that uniquely identifies the snapshot in that storage unit.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    version_uuid = marshmallow_fields.Str(
        data_key="version_uuid",
        allow_none=True,
    )
    r""" The 128 bit identifier that uniquely identifies a snapshot and its logical data layout."""

    @property
    def resource(self):
        return StorageUnitSnapshot

    gettable_fields = [
        "links",
        "comment",
        "create_time",
        "delta",
        "expiry_time",
        "logical_size",
        "name",
        "owners",
        "reclaimable_space",
        "size",
        "snaplock",
        "snapmirror_label",
        "state",
        "storage_unit.links",
        "storage_unit.name",
        "storage_unit.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "version_uuid",
    ]
    """links,comment,create_time,delta,expiry_time,logical_size,name,owners,reclaimable_space,size,snaplock,snapmirror_label,state,storage_unit.links,storage_unit.name,storage_unit.uuid,svm.links,svm.name,svm.uuid,uuid,version_uuid,"""

    patchable_fields = [
        "comment",
        "expiry_time",
        "name",
        "snaplock",
        "snapmirror_label",
        "storage_unit.name",
        "storage_unit.uuid",
        "svm.name",
        "svm.uuid",
    ]
    """comment,expiry_time,name,snaplock,snapmirror_label,storage_unit.name,storage_unit.uuid,svm.name,svm.uuid,"""

    postable_fields = [
        "comment",
        "expiry_time",
        "name",
        "snaplock",
        "snapmirror_label",
        "storage_unit.name",
        "storage_unit.uuid",
        "svm.name",
        "svm.uuid",
    ]
    """comment,expiry_time,name,snaplock,snapmirror_label,storage_unit.name,storage_unit.uuid,svm.name,svm.uuid,"""

class StorageUnitSnapshot(Resource):
    r""" The snapshot object represents a point in time snapshot of a storage unit. """

    _schema = StorageUnitSnapshotSchema
    _path = "/api/storage/storage-units/{storage_unit[uuid]}/snapshots"
    _keys = ["storage_unit.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of volume snapshots.
### Expensive properties
There is an added computational cost to retrieving the amount of reclaimable space for snapshots, as the calculation is done on demand based on the list of snapshots provided.
* `reclaimable_space`
* `delta`
### Learn more
* [`DOC /storage/storage-units/{storage_unit.uuid}/snapshots`](#docs-SAN-storage_storage-units_{storage_unit.uuid}_snapshots)
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
        """Returns a count of all StorageUnitSnapshot resources that match the provided query"""
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
        """Returns a list of RawResources that represent StorageUnitSnapshot resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["StorageUnitSnapshot"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a storage unit snapshot.
### Learn more
* [`DOC /storage/storage-units/{storage_unit.uuid}/snapshots`](#docs-SAN-storage_storage-units_{storage_unit.uuid}_snapshots)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["StorageUnitSnapshot"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["StorageUnitSnapshot"], NetAppResponse]:
        r"""Creates a storage unit snapshot.
### Required properties
* `name` - Name of the snapshot to be created.
### Recommended optional properties
* `comment` - Comment associated with the snapshot.
* `expiry_time` - Snapshots with an expiry time set are not allowed to be deleted until the retention time is reached.
* `snapmirror_label` - Label for SnapMirror operations.
* `snaplock_expiry_time` - Expiry time for snapshot locking enabled volumes.
### Learn more
* [`DOC /storage/storage-units/{storage_unit.uuid}/snapshots`](#docs-SAN-storage_storage-units_{storage_unit.uuid}_snapshots)
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
        records: Iterable["StorageUnitSnapshot"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a storage unit snapshot.
### Learn more
* [`DOC /storage/storage-units/{storage_unit.uuid}/snapshots`](#docs-SAN-storage_storage-units_{storage_unit.uuid}_snapshots)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of volume snapshots.
### Expensive properties
There is an added computational cost to retrieving the amount of reclaimable space for snapshots, as the calculation is done on demand based on the list of snapshots provided.
* `reclaimable_space`
* `delta`
### Learn more
* [`DOC /storage/storage-units/{storage_unit.uuid}/snapshots`](#docs-SAN-storage_storage-units_{storage_unit.uuid}_snapshots)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details of a specific storage unit snapshot.
### Learn more
* [`DOC /storage/storage-units/{storage_unit.uuid}/snapshots`](#docs-SAN-storage_storage-units_{storage_unit.uuid}_snapshots)
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
        r"""Creates a storage unit snapshot.
### Required properties
* `name` - Name of the snapshot to be created.
### Recommended optional properties
* `comment` - Comment associated with the snapshot.
* `expiry_time` - Snapshots with an expiry time set are not allowed to be deleted until the retention time is reached.
* `snapmirror_label` - Label for SnapMirror operations.
* `snaplock_expiry_time` - Expiry time for snapshot locking enabled volumes.
### Learn more
* [`DOC /storage/storage-units/{storage_unit.uuid}/snapshots`](#docs-SAN-storage_storage-units_{storage_unit.uuid}_snapshots)
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
        r"""Updates a storage unit snapshot.
### Learn more
* [`DOC /storage/storage-units/{storage_unit.uuid}/snapshots`](#docs-SAN-storage_storage-units_{storage_unit.uuid}_snapshots)
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
        r"""Deletes a storage unit snapshot.
### Learn more
* [`DOC /storage/storage-units/{storage_unit.uuid}/snapshots`](#docs-SAN-storage_storage-units_{storage_unit.uuid}_snapshots)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


