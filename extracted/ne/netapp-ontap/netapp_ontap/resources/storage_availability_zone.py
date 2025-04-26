r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

Provides information on nodes and storage details for all availability zones present in the cluster. Storage details include storage efficiency and other storage related information.
</br>
---
Example
### Retrieving the list of availability zones in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageAvailabilityZone

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(StorageAvailabilityZone.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    StorageAvailabilityZone(
        {
            "uuid": "05be85be-2a5f-11ef-890a-005056bb9bec",
            "_links": {
                "self": {
                    "href": "/api/storage/availability-zones/05be85be-2a5f-11ef-890a-005056bb9bec"
                }
            },
        }
    ),
    StorageAvailabilityZone(
        {
            "uuid": "9b3ff559-3333-11ef-b420-005056ae6060",
            "_links": {
                "self": {
                    "href": "/api/storage/availability-zones/9b3ff559-3333-11ef-b420-005056ae6060"
                }
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving nodes and storage details for all availability zones in the cluster
### The following example GET request shows the nodes and storage details returned for all availability zones:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageAvailabilityZone

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(StorageAvailabilityZone.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    StorageAvailabilityZone(
        {
            "space": {
                "delayed_frees": 81920,
                "total_metadata_used": 32768,
                "full_threshold_percent": 98,
                "logical_user_data_without_snapshots": 49152,
                "nearly_full_threshold_percent": 95,
                "physical_used_percent": 0,
                "physical_user_data_without_snapshots": 40960,
                "efficiency_without_snapshots": {"ratio": 1.2, "savings": 8192},
                "size": 2457600,
                "available": 2441216,
                "physical_used": 16384,
            },
            "name": "storage_availability_zone_2",
            "uuid": "05be85be-2a5f-11ef-890a-005056bb9bec",
            "_links": {
                "self": {
                    "href": "/api/storage/availability-zones/05be85be-2a5f-11ef-890a-005056bb9bec"
                }
            },
            "nodes": [
                {"name": "node3", "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1"},
                {"name": "node4", "uuid": "cf9ab500-ff3e-4bce-bfd7-d679e6078f47"},
            ],
        }
    ),
    StorageAvailabilityZone(
        {
            "space": {
                "delayed_frees": 13832192,
                "total_metadata_used": 58693394432,
                "full_threshold_percent": 98,
                "logical_user_data_without_snapshots": 102400,
                "nearly_full_threshold_percent": 95,
                "physical_used_percent": 46,
                "physical_user_data_without_snapshots": 114688,
                "efficiency_without_snapshots": {"ratio": 1.0, "savings": 8192},
                "size": 125357654016,
                "available": 66676547584,
                "physical_used": 58681106432,
            },
            "name": "storage_availability_zone_1",
            "uuid": "9b3ff559-3333-11ef-b420-005056ae6060",
            "_links": {
                "self": {
                    "href": "/api/storage/availability-zones/9b3ff559-3333-11ef-b420-005056ae6060"
                }
            },
            "nodes": [
                {"name": "node1", "uuid": "e02dbef1-6126-11e9-b8fb-005056bb9ce4"},
                {"name": "node2", "uuid": "54440ec3-6127-11e9-a959-005056bb76f9"},
            ],
        }
    ),
]

```
</div>
</div>

---
### Retrieving storage details for a specific storage availability zone
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageAvailabilityZone

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageAvailabilityZone(uuid="<availability-zone.uuid>")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
StorageAvailabilityZone(
    {
        "space": {
            "delayed_frees": 100458496,
            "total_metadata_used": 58780037120,
            "full_threshold_percent": 98,
            "logical_user_data_without_snapshots": 122880,
            "nearly_full_threshold_percent": 95,
            "physical_used_percent": 46,
            "physical_user_data_without_snapshots": 114688,
            "efficiency_without_snapshots": {"ratio": 1.0, "savings": 8192},
            "size": 125357654016,
            "available": 66676559872,
            "physical_used": 58681094144,
        },
        "name": "storage_availability_zone_1",
        "uuid": "9b3ff559-3333-11ef-b420-005056ae6060",
        "nodes": [
            {"name": "node1", "uuid": "e02dbef1-6126-11e9-b8fb-005056bb9ce4"},
            {"name": "node2", "uuid": "54440ec3-6127-11e9-a959-005056bb76f9"},
        ],
    }
)

```
</div>
</div>

---
### Updating the threshold value for a storage availability zone
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageAvailabilityZone

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageAvailabilityZone(uuid="<availability-zone.uuid>")
    resource.space.nearly_full_threshold_percent = "55"
    resource.patch()

```

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


__all__ = ["StorageAvailabilityZone", "StorageAvailabilityZoneSchema"]
__pdoc__ = {
    "StorageAvailabilityZoneSchema.resource": False,
    "StorageAvailabilityZoneSchema.opts": False,
}


class StorageAvailabilityZoneSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageAvailabilityZone object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the storage_availability_zone."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Availability zone name."""

    nodes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.node_response_records_ha_partners.NodeResponseRecordsHaPartnersSchema", unknown=EXCLUDE, allow_none=True), data_key="nodes", allow_none=True)
    r""" Nodes in the availability zone."""

    space = marshmallow_fields.Nested("netapp_ontap.models.storage_availability_zone_space.StorageAvailabilityZoneSpaceSchema", data_key="space", unknown=EXCLUDE, allow_none=True)
    r""" The space field of the storage_availability_zone."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Availability zone UUID."""

    @property
    def resource(self):
        return StorageAvailabilityZone

    gettable_fields = [
        "links",
        "name",
        "nodes.links",
        "nodes.name",
        "nodes.uuid",
        "space",
        "uuid",
    ]
    """links,name,nodes.links,nodes.name,nodes.uuid,space,uuid,"""

    patchable_fields = [
        "space",
    ]
    """space,"""

    postable_fields = [
        "space",
    ]
    """space,"""

class StorageAvailabilityZone(Resource):
    r""" Provides information on nodes and storage details for each availability zone present in the cluster. Storage details include storage efficiency and other storage related information. """

    _schema = StorageAvailabilityZoneSchema
    _path = "/api/storage/availability-zones"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves storage details for all availability zones of the cluster. By default, the availability zone UUID is retrieved. Other Storage details can
be retrieved using fields parameter. Storage details include storage efficiency and other storage related information.

### Learn more
* [`DOC /storage/availability-zones`](#docs-storage-storage_availability-zones)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all StorageAvailabilityZone resources that match the provided query"""
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
        """Returns a list of RawResources that represent StorageAvailabilityZone resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["StorageAvailabilityZone"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates full_threshold_percent and nearly_full_threshold_percent for an individual availability zone of the cluster.

### Learn more
* [`DOC /storage/availability-zones`](#docs-storage-storage_availability-zones)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves storage details for all availability zones of the cluster. By default, the availability zone UUID is retrieved. Other Storage details can
be retrieved using fields parameter. Storage details include storage efficiency and other storage related information.

### Learn more
* [`DOC /storage/availability-zones`](#docs-storage-storage_availability-zones)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves storage details for an individual availability zone of the cluster. By default, this endpoint returns all fields.
Storage details include storage efficiency and other storage related information.

### Learn more
* [`DOC /storage/availability-zones`](#docs-storage-storage_availability-zones)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates full_threshold_percent and nearly_full_threshold_percent for an individual availability zone of the cluster.

### Learn more
* [`DOC /storage/availability-zones`](#docs-storage-storage_availability-zones)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



