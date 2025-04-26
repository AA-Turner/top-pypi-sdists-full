r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Updating storage pools
The PATCH operation is used to modify properties of the storage pool. There are several properties that can be modified on a storage pool.
PATCH operations on a storage pool are restricted when another PATCH operation is in progress.
The following is a list of properties that can be modified using the PATCH operation including a brief description for each:

* name - Can be updated to rename the storage pool.
* capacity.disk_count - Can be updated to increase the number of disks in a storage pool.
* capacity.spare_allocation_units[].count - Modifying this value requires that the user specify capacity.spare_allocation_units[].node as well. Modifying this value redistributes spare cache capacity among the nodes specified in the operation
When expanding a storage pool, the cache tiers of all aggregates using the storage pool's allocation units are expanded automatically.
### Simulated storage pool expansion
The PATCH operation also supports simulated expansion of a storage pool.
Running PATCH with the query "simulate" set to "true", and "capacity.disk_count" set to the final disk count will return a response containing the projected new capacity and the new constituent disk list for the storage pool.
## Deleting storage pools
If cache capacity from a storage pool is being used in an aggregate, it cannot be deleted.
See the /storage/aggregates API for details on deleting aggregates.
---
## Examples
### Retrieving a specific pool from the cluster
The following example shows the response of the requested storage pool. If there is no storage pool with the requested UUID, an error is returned.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePool(uuid="870dd9f2-bdfa-4167-b692-57d1cec874d4")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
StoragePool(
    {
        "name": "new_sp",
        "storage_type": "ssd",
        "uuid": "8255fef7-4737-11ec-bd1b-005056bbb879",
        "capacity": {
            "remaining": 1846542336,
            "spare_allocation_units": [
                {
                    "node": {
                        "name": "node-1",
                        "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1",
                    },
                    "syncmirror_pool": "pool0",
                    "count": 1,
                    "available_size": 1846542336,
                    "size": 1846542336,
                },
                {
                    "node": {
                        "name": "node-2",
                        "uuid": "cf9ab500-ff3e-4bce-bfd7-d679e6078f47",
                    },
                    "syncmirror_pool": "pool0",
                    "count": 0,
                    "available_size": 0,
                    "size": 1846542336,
                },
            ],
            "disk_count": 4,
            "total": 7386169344,
            "used_allocation_units": [
                {
                    "aggregate": {
                        "name": "test_a",
                        "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
                    },
                    "node": {
                        "name": "node-1",
                        "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1",
                    },
                },
                {
                    "aggregate": {
                        "name": "test_b",
                        "uuid": "f4cc30d5-b052-493a-a49f-19781425f987",
                    },
                    "node": {
                        "name": "node-2",
                        "uuid": "cf9ab500-ff3e-4bce-bfd7-d679e6078f47",
                    },
                },
            ],
            "disks": [
                {
                    "usable_size": 1902379008,
                    "disk": {"name": "VMw-1.11"},
                    "total_size": 1908871168,
                },
                {
                    "usable_size": 1902379008,
                    "disk": {"name": "VMw-1.12"},
                    "total_size": 1908871168,
                },
                {
                    "usable_size": 1902379008,
                    "disk": {"name": "VMw-1.23"},
                    "total_size": 1908871168,
                },
                {
                    "usable_size": 1902379008,
                    "disk": {"name": "VMw-1.24"},
                    "total_size": 1908871168,
                },
            ],
        },
        "nodes": [
            {"name": "node-1", "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1"},
            {"name": "node-2", "uuid": "cf9ab500-ff3e-4bce-bfd7-d679e6078f47"},
        ],
        "health": {"is_healthy": True, "state": "normal"},
    }
)

```
</div>
</div>

### Simulating storage pool expansion
The following example shows the response for a simulated storage pool expansion based on the values of the 'capacity.disk_count' attribute passed in.
The query does not modify the existing storage pool, but rather returns how it will look after the expansion.
This will be reflected in the following attributes:

* capacity.total- Total space, in bytes.
* capacity.remaining - New remaining capacity, in bytes.
* capacity.disks.disk - New list of constituent disks.
* capacity.disk_count - New number of disks in the pool.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePool(uuid="cae60cfe-deae-42bd-babb-ef437d118314")
    resource.capacity = {"disk_count": 6}
    resource.patch(hydrate=True, simulate=True)

```

### Adding capacity to a storage pool
The following example shows the workflow of adding disks to the storage pool.<br>
Step 1: Check the current disk count on the storage pool.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePool(uuid="19425837-f2fa-4a9f-8f01-712f626c983c")
    resource.get(fields="capacity.disk_count")
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
StoragePool(
    {
        "name": "sp1",
        "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
        "capacity": {"disk_count": 4},
    }
)

```
</div>
</div>

Step 2: Update the pool with the new disk count in 'capacity.disk_count'. The response to PATCH is a job unless the request is invalid.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePool(uuid="19425837-f2fa-4a9f-8f01-712f626c983c")
    resource.capacity = {"disk_count": 6}
    resource.patch()

```

Step 3: Wait for the job to finish, then call GET to see the reflected change.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePool(uuid="19425837-f2fa-4a9f-8f01-712f626c983c")
    resource.get(fields="capacity.disk_count")
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
StoragePool(
    {
        "name": "sp1",
        "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
        "capacity": {"disk_count": 6},
    }
)

```
</div>
</div>

The following example shows the workflow to redistribute spare capacity among nodes sharing the storage pool
Step 1: Check the current spare capacity distribution of the pool.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePool(uuid="f3aafdc6-be35-4d93-9590-5a402bffbe4b")
    resource.get(fields="capacity.spare_allocation_units")
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
StoragePool(
    {
        "name": "sp1",
        "uuid": "f3aafdc6-be35-4d93-9590-5a402bffbe4b",
        "capacity": {
            "spare_allocation_units": [
                {
                    "node": {
                        "name": "node-1",
                        "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1",
                    },
                    "syncmirror_pool": "pool0",
                    "count": 1,
                    "available_size": 1846542336,
                    "size": 1846542336,
                },
                {
                    "node": {
                        "name": "node-2",
                        "uuid": "cf9ab500-ff3e-4bce-bfd7-d679e6078f47",
                    },
                    "syncmirror_pool": "pool0",
                    "count": 0,
                    "available_size": 0,
                    "size": 1846542336,
                },
            ]
        },
    }
)

```
</div>
</div>

Step 2: Update the pool so that the spare allocation unit count is symmetrically modified for each node. The response to PATCH is a job unless the request is invalid.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePool(uuid="f3aafdc6-be35-4d93-9590-5a402bffbe4b")
    resource.capacity = {
        "spare_allocation_units": [
            {"node": {"name": "node-1"}, "count": 0},
            {"node": {"name": "node-2"}, "count": 1},
        ]
    }
    resource.patch()

```

Step 3: Wait for the job to finish, then call GET to see the reflected change.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePool(uuid="f3aafdc6-be35-4d93-9590-5a402bffbe4b")
    resource.get(fields="capacity.spare_allocation_units")
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
StoragePool(
    {
        "name": "sp1",
        "uuid": "f3aafdc6-be35-4d93-9590-5a402bffbe4b",
        "capacity": {
            "spare_allocation_units": [
                {
                    "node": {
                        "name": "node-1",
                        "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1",
                    },
                    "syncmirror_pool": "pool0",
                    "count": 0,
                    "available_size": 0,
                    "size": 1846542336,
                },
                {
                    "node": {
                        "name": "node-2",
                        "uuid": "cf9ab500-ff3e-4bce-bfd7-d679e6078f47",
                    },
                    "syncmirror_pool": "pool0",
                    "count": 1,
                    "available_size": 1846542336,
                    "size": 1846542336,
                },
            ]
        },
    }
)

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


__all__ = ["StoragePool", "StoragePoolSchema"]
__pdoc__ = {
    "StoragePoolSchema.resource": False,
    "StoragePoolSchema.opts": False,
}


class StoragePoolSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StoragePool object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the storage_pool."""

    capacity = marshmallow_fields.Nested("netapp_ontap.models.storage_pool_capacity.StoragePoolCapacitySchema", data_key="capacity", unknown=EXCLUDE, allow_none=True)
    r""" The capacity field of the storage_pool."""

    health = marshmallow_fields.Nested("netapp_ontap.models.pool_health.PoolHealthSchema", data_key="health", unknown=EXCLUDE, allow_none=True)
    r""" The health field of the storage_pool."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Storage pool name."""

    nodes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, allow_none=True), data_key="nodes", allow_none=True)
    r""" Nodes that can use this storage pool for their aggregates."""

    storage_type = marshmallow_fields.Str(
        data_key="storage_type",
        validate=enum_validation(['SSD']),
        allow_none=True,
    )
    r""" Storage type for the disks used to create the storage pool.

Valid choices:

* SSD"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Storage pool UUID."""

    @property
    def resource(self):
        return StoragePool

    gettable_fields = [
        "links",
        "capacity",
        "health",
        "name",
        "nodes",
        "storage_type",
        "uuid",
    ]
    """links,capacity,health,name,nodes,storage_type,uuid,"""

    patchable_fields = [
        "capacity",
        "name",
        "nodes",
    ]
    """capacity,name,nodes,"""

    postable_fields = [
        "capacity",
        "name",
        "nodes",
    ]
    """capacity,name,nodes,"""

class StoragePool(Resource):
    """Allows interaction with StoragePool objects on the host"""

    _schema = StoragePoolSchema
    _path = "/api/storage/pools"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of storage pools for the entire cluster.
### Related ONTAP commands
* `storage pool show`

### Learn more
* [`DOC /storage/pools`](#docs-storage-storage_pools)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all StoragePool resources that match the provided query"""
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
        """Returns a list of RawResources that represent StoragePool resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["StoragePool"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the storage pool specified by the UUID with the properties in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage pool rename`
* `storage pool reassign`
* `storage pool add`

### Learn more
* [`DOC /storage/pools/{uuid}`](#docs-storage-storage_pools_{uuid})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["StoragePool"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["StoragePool"], NetAppResponse]:
        r"""Creates a new storage pool using available solid state capacity attached to the nodes specified.
### Required properties
The following properties are required in the POST body:
* `name` - Name of the new storage pool.
* `nodes[].name` or `nodes[].uuid` - Nodes that can use cache capacity from the new storage pool. Only nodes in the same HA pair can be specified for a given storage pool. Spare cache capacity will be distributed evenly among the specified nodes.
* `capacity.disk_count` - Number of SSDs to be used to create the storage pool.
### Related ONTAP commands
* `storage pool create`
### Example:
```
POST /api/storage/pools {"nodes": [{"name": "node1"}, {"name": "node2"}], "name": "storage_pool_1", "capacity": {"disk_count": "4"}}
```

### Learn more
* [`DOC /storage/pools`](#docs-storage-storage_pools)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["StoragePool"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the storage pool specified by the UUID. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage pool delete`

### Learn more
* [`DOC /storage/pools/{uuid}`](#docs-storage-storage_pools_{uuid})"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of storage pools for the entire cluster.
### Related ONTAP commands
* `storage pool show`

### Learn more
* [`DOC /storage/pools`](#docs-storage-storage_pools)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the storage pool specified by the UUID.
### Related ONTAP commands
* `storage pool show -storage-pool-uuid`

### Learn more
* [`DOC /storage/pools/{uuid}`](#docs-storage-storage_pools_{uuid})"""
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
        r"""Creates a new storage pool using available solid state capacity attached to the nodes specified.
### Required properties
The following properties are required in the POST body:
* `name` - Name of the new storage pool.
* `nodes[].name` or `nodes[].uuid` - Nodes that can use cache capacity from the new storage pool. Only nodes in the same HA pair can be specified for a given storage pool. Spare cache capacity will be distributed evenly among the specified nodes.
* `capacity.disk_count` - Number of SSDs to be used to create the storage pool.
### Related ONTAP commands
* `storage pool create`
### Example:
```
POST /api/storage/pools {"nodes": [{"name": "node1"}, {"name": "node2"}], "name": "storage_pool_1", "capacity": {"disk_count": "4"}}
```

### Learn more
* [`DOC /storage/pools`](#docs-storage-storage_pools)"""
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
        r"""Updates the storage pool specified by the UUID with the properties in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage pool rename`
* `storage pool reassign`
* `storage pool add`

### Learn more
* [`DOC /storage/pools/{uuid}`](#docs-storage-storage_pools_{uuid})"""
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
        r"""Deletes the storage pool specified by the UUID. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage pool delete`

### Learn more
* [`DOC /storage/pools/{uuid}`](#docs-storage-storage_pools_{uuid})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


