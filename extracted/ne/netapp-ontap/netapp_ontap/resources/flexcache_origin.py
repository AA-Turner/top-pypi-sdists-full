r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
FlexCache is a persistent cache of an origin volume. An origin volume can only be a FlexVol while a FlexCache is always a FlexGroup.</br>
The following relationship configurations are supported:

* Intra-Vserver where FlexCache and the corresponding origin volume reside in the same Vserver.
* Cross-Vserver but intra-cluster where FlexCache and the origin volume reside in the same cluster but belong to different Vservers.
* Cross-cluster where FlexCache and the origin volume reside in different clusters.</br>
FlexCache supports fan-out and more than one FlexCache can be created from one origin volume.
This API retrieves the origin of FlexCache configurations in the origin cluster.
## FlexCache APIs
The following APIs can be used to perform operations related to the origin of a FlexCache:

* GET       /api/storage/flexcache/origins
* GET       /api/storage/flexcache/origins/{uuid}
* PATCH     /api/storage/flexcache/origins/{uuid}
## Examples
### Retrieving origins of FlexCache attributes
The GET request is used to retrieve the origins of FlexCache attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FlexcacheOrigin

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FlexcacheOrigin.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    FlexcacheOrigin(
        {
            "name": "vol_o1",
            "uuid": "2bc957dd-2617-4afb-8d2f-66ac6070d313",
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/origins/2bc957dd-2617-4afb-8d2f-66ac6070d313"
                }
            },
        }
    ),
    FlexcacheOrigin(
        {
            "name": "vol_1",
            "uuid": "80fcaee4-0dc2-488b-afb8-86d28a34cda8",
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/origins/80fcaee4-0dc2-488b-afb8-86d28a34cda8"
                }
            },
        }
    ),
]

```
</div>
</div>

### Retrieving the attributes of an origin volume
The GET request is used to retrieve the attributes of an origin volume.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FlexcacheOrigin

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FlexcacheOrigin(uuid="80fcaee4-0dc2-488b-afb8-86d28a34cda8")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
FlexcacheOrigin(
    {
        "name": "vol_1",
        "uuid": "80fcaee4-0dc2-488b-afb8-86d28a34cda8",
        "block_level_invalidation": False,
        "_links": {
            "self": {
                "href": "/api/storage/flexcache/origins/80fcaee4-0dc2-488b-afb8-86d28a34cda8"
            }
        },
        "svm": {"name": "vs_3", "uuid": "8aa2cd28-0e92-11e9-b391-0050568e4115"},
        "global_file_locking_enabled": True,
        "flexcaches": [
            {
                "volume": {
                    "name": "fc_42",
                    "uuid": "4e7f9d49-0e96-11e9-aed0-0050568eddbe",
                },
                "create_time": "2019-01-02T19:27:22+05:30",
                "cluster": {
                    "name": "node4",
                    "uuid": "c32f16b8-0e90-11e9-aed0-0050568eddbe",
                },
                "ip_address": "10.140.103.183",
                "svm": {
                    "name": "vs_1_4",
                    "uuid": "36f68322-0e93-11e9-aed0-0050568eddbe",
                },
            },
            {
                "volume": {
                    "name": "fc_421",
                    "uuid": "71ee8f36-0ea4-11e9-aed0-0050568eddbe",
                },
                "create_time": "2019-01-02T21:08:34+05:30",
                "cluster": {
                    "name": "node4",
                    "uuid": "c32f16b8-0e90-11e9-aed0-0050568eddbe",
                },
                "ip_address": "10.140.103.183",
                "svm": {
                    "name": "vs_1_4",
                    "uuid": "36f68322-0e93-11e9-aed0-0050568eddbe",
                },
            },
            {
                "volume": {"name": "fc_422"},
                "create_time": "2019-01-03T11:14:38+05:30",
                "cluster": {
                    "name": "node4",
                    "uuid": "c32f16b8-0e90-11e9-aed0-0050568eddbe",
                },
                "ip_address": "10.140.103.183",
                "svm": {
                    "name": "vs_1_4",
                    "uuid": "36f68322-0e93-11e9-aed0-0050568eddbe",
                },
            },
            {
                "volume": {
                    "name": "fc_32",
                    "uuid": "ddb42bbc-0e95-11e9-8180-0050568e0b79",
                },
                "create_time": "2019-01-02T19:24:14+05:30",
                "cluster": {
                    "name": "node3",
                    "uuid": "8eb21b3b-0e90-11e9-8180-0050568e0b79",
                },
                "ip_address": "10.140.103.179",
                "state": "online",
                "svm": {"name": "vs_1", "uuid": "e708fbe2-0e92-11e9-8180-0050568e0b79"},
                "size": 4294967296,
            },
            {
                "volume": {
                    "name": "fc_321",
                    "uuid": "47902654-0ea4-11e9-8180-0050568e0b79",
                },
                "create_time": "2019-01-02T21:07:23+05:30",
                "cluster": {
                    "name": "node3",
                    "uuid": "8eb21b3b-0e90-11e9-8180-0050568e0b79",
                },
                "ip_address": "10.140.103.179",
                "state": "online",
                "svm": {"name": "vs_1", "uuid": "e708fbe2-0e92-11e9-8180-0050568e0b79"},
                "size": 4294967296,
            },
            {
                "volume": {
                    "name": "fc_322",
                    "uuid": "04d5e07b-0ebe-11e9-8180-0050568e0b79",
                },
                "create_time": "2019-01-03T00:11:38+05:30",
                "cluster": {
                    "name": "node3",
                    "uuid": "8eb21b3b-0e90-11e9-8180-0050568e0b79",
                },
                "ip_address": "10.140.103.179",
                "state": "online",
                "svm": {"name": "vs_1", "uuid": "e708fbe2-0e92-11e9-8180-0050568e0b79"},
                "size": 4294967296,
            },
            {
                "volume": {
                    "name": "fc_323",
                    "uuid": "77e911ff-0ebe-11e9-8180-0050568e0b79",
                },
                "create_time": "2019-01-03T00:14:52+05:30",
                "cluster": {
                    "name": "node3",
                    "uuid": "8eb21b3b-0e90-11e9-8180-0050568e0b79",
                },
                "ip_address": "10.140.103.179",
                "state": "online",
                "svm": {"name": "vs_1", "uuid": "e708fbe2-0e92-11e9-8180-0050568e0b79"},
                "size": 4294967296,
            },
        ],
    }
)

```
</div>
</div>

### Modifying origin options of an origin volume
Use the PATCH request to update options of an origin volume.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FlexcacheOrigin

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FlexcacheOrigin(uuid="1fbc0ebb-2440-11eb-a86c-005056ac8ca0")
    resource.block_level_invalidation = True
    resource.patch()

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


__all__ = ["FlexcacheOrigin", "FlexcacheOriginSchema"]
__pdoc__ = {
    "FlexcacheOriginSchema.resource": False,
    "FlexcacheOriginSchema.opts": False,
}


class FlexcacheOriginSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FlexcacheOrigin object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the flexcache_origin."""

    block_level_invalidation = marshmallow_fields.Boolean(
        data_key="block_level_invalidation",
        allow_none=True,
    )
    r""" Block level invalidation enables the FlexCache volume to retain blocks that are not changed at the FlexCache volume without having to evict them. This means that the FlexCache volume does not have to again incur the computational cost of fetching blocks over the WAN from the FlexCache volume origin on the next client access. Block level invalidation is a property of the origin volume. Without block level invalidation, any write at the origin volume would evict the whole file at the FlexCache volume, since by default, origin volume does a file level invalidation."""

    flexcaches = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.flexcache_relationship.FlexcacheRelationshipSchema", unknown=EXCLUDE, allow_none=True), data_key="flexcaches", allow_none=True)
    r""" The flexcaches field of the flexcache_origin."""

    global_file_locking_enabled = marshmallow_fields.Boolean(
        data_key="global_file_locking_enabled",
        allow_none=True,
    )
    r""" Specifies whether a global file locking option is enabled for an origin volume of a FlexCache volume."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=203),
        allow_none=True,
    )
    r""" Origin volume name

Example: vol1, vol_2"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the flexcache_origin."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Origin volume UUID. Unique identifier for origin of FlexCache.

Example: 1cd8a442-86d1-11e0-ae1c-123478563512"""

    @property
    def resource(self):
        return FlexcacheOrigin

    gettable_fields = [
        "links",
        "block_level_invalidation",
        "flexcaches",
        "global_file_locking_enabled",
        "name",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,block_level_invalidation,flexcaches,global_file_locking_enabled,name,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "block_level_invalidation",
        "name",
    ]
    """block_level_invalidation,name,"""

    postable_fields = [
        "flexcaches",
        "name",
        "svm.name",
        "svm.uuid",
    ]
    """flexcaches,name,svm.name,svm.uuid,"""

class FlexcacheOrigin(Resource):
    r""" Defines the origin endpoint of FlexCache. """

    _schema = FlexcacheOriginSchema
    _path = "/api/storage/flexcache/origins"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves origin of FlexCache in the cluster.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `flexcaches.ip_address` - IP address of FlexCache.
* `flexcaches.size` - Physical size of FlexCache.
* `flexcaches.guarantee.type` - Space guarantee style of FlexCache.
* `flexcaches.state` - State of FlexCache.
### Related ONTAP commands
* `volume flexcache origin show-caches`
### Learn more
* [`DOC /storage/flexcache/origins`](#docs-storage-storage_flexcache_origins)
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
        """Returns a count of all FlexcacheOrigin resources that match the provided query"""
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
        """Returns a list of RawResources that represent FlexcacheOrigin resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["FlexcacheOrigin"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Modifies origin options for a origin volume in the cluster.
### Required properties
* `uuid` - Origin volume UUID.
* `block_level_invalidation` - Value for the Block Level Invalidation flag - options {true|false}.
### Related ONTAP commands
* `volume flexcache origin config modify`
### Learn more
* [`DOC /storage/flexcache/origins`](#docs-storage-storage_flexcache_origins)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves origin of FlexCache in the cluster.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `flexcaches.ip_address` - IP address of FlexCache.
* `flexcaches.size` - Physical size of FlexCache.
* `flexcaches.guarantee.type` - Space guarantee style of FlexCache.
* `flexcaches.state` - State of FlexCache.
### Related ONTAP commands
* `volume flexcache origin show-caches`
### Learn more
* [`DOC /storage/flexcache/origins`](#docs-storage-storage_flexcache_origins)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves attributes of the origin of a FlexCache in the cluster.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are included by default in GET results. The recommended method to use this API is to filter and retrieve only the required fields. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `flexcaches.ip_address` - IP address of FlexCache.
* `flexcaches.size` - Physical size of FlexCache.
* `flexcaches.guarantee.type` - Space guarantee style of FlexCache.
* `flexcaches.state` - State of FlexCache.
* `flexcaches.dr_cache` - True if the cache is a DR cache.
### Related ONTAP commands
* `volume flexcache origin show-caches`
### Learn more
* [`DOC /storage/flexcache/origins`](#docs-storage-storage_flexcache_origins)
"""
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
        r"""Modifies origin options for a origin volume in the cluster.
### Required properties
* `uuid` - Origin volume UUID.
* `block_level_invalidation` - Value for the Block Level Invalidation flag - options {true|false}.
### Related ONTAP commands
* `volume flexcache origin config modify`
### Learn more
* [`DOC /storage/flexcache/origins`](#docs-storage-storage_flexcache_origins)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



