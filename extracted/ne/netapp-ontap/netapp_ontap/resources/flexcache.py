r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
FlexCache is a persistent cache of an origin volume. An origin volume can only be a FlexVol while a FlexCache is always a FlexGroup.</br>
The following relationship configurations are supported:</br>

* Intra-Vserver where FlexCache and the corresponding origin volume reside in the same Vserver.
* Cross-Vserver but intra-cluster where FlexCache and the origin volume reside in the same cluster but belong to different Vservers.
* Cross-cluster where FlexCache and the origin volume reside in different clusters.</br>
FlexCache supports fan-out and more than one FlexCache can be created from one origin volume.
This API retrieves and manages FlexCache configurations in the cache cluster.
## FlexCache APIs
The following APIs can be used to perform operations related with FlexCache:

* GET       /api/storage/flexcache/flexcaches
* GET       /api/storage/flexcache/flexcaches/{uuid}
* POST      /api/storage/flexcache/flexcaches
* DELETE    /api/storage/flexcache/flexcaches/{uuid}
## Examples
### Creating a FlexCache
The POST request is used to create a FlexCache.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Flexcache

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Flexcache()
    resource.aggregates = [{"name": "aggr_1"}]
    resource.name = "fc_333"
    resource.origins = [{"svm": {"name": "vs_3"}, "volume": {"name": "vol_o1"}}]
    resource.svm = {"name": "vs_1"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Flexcache(
    {
        "name": "fc_333",
        "svm": {"name": "vs_1"},
        "aggregates": [{"name": "aggr_1"}],
        "origins": [{"volume": {"name": "vol_o1"}, "svm": {"name": "vs_3"}}],
    }
)

```
</div>
</div>

curl -X POST "https://<mgmt-ip>/api/storage/flexcache/flexcaches" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{ \"aggregates\": [ { \"name\": \"aggr_1\" } ], \"name\": \"fc_333\", \"origins\": [ {  \"svm\": { \"name\": \"vs_3\"  }, \"volume\": { \"name\": \"vol_o1\" } } ], \"svm\": { \"name\": \"vs_1\" },  \"path\": \"/fc_333\", \"prepopulate\": { \"dir_paths\": [ \"/dir1\" ] } }"
# The response:
{
  "job": {
    "uuid": "e751dd5d-0f3c-11e9-8b2b-0050568e0b79",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/e751dd5d-0f3c-11e9-8b2b-0050568e0b79"
      }
    }
  }
}
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Flexcache

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Flexcache()
    resource.aggregates = [{"name": "aggr_1"}]
    resource.name = "fc_333"
    resource.origins = [{"svm": {"name": "vs_3"}, "volume": {"name": "vol_o1"}}]
    resource.svm = {"name": "vs_1"}
    resource.path = "/       fc_333"
    resource.prepopulate = {
        "dir_paths": ["/dir1"],
        "exclude_dir_paths": ["/dir1/dir11"],
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Flexcache(
    {
        "name": "fc_333",
        "svm": {"name": "vs_1"},
        "aggregates": [{"name": "aggr_1"}],
        "path": "/       fc_333",
        "prepopulate": {"dir_paths": ["/dir1"], "exclude_dir_paths": ["/dir1/dir11"]},
        "origins": [{"volume": {"name": "vol_o1"}, "svm": {"name": "vs_3"}}],
    }
)

```
</div>
</div>
`
curl -X POST "https://<mgmt-ip>/api/storage/flexcache/flexcaches" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{ \"aggregates\": [ { \"name\": \"aggr_1\" } ], \"name\": \"fc_333\", \"origins\": [ {  \"svm\": { \"name\": \"vs_3\"  }, \"volume\": { \"name\": \"vol_o1\" } } ], \"svm\":{ \"name\": \"vs_1\" }, \"dr_cache\": true,  \"path\": \"/fc_333\", \"prepopulate\": { \"dir_paths\": [ \"/dir1\" ] } }"
# The response:
{
  "job": {
    "uuid": "e751dd5d-0f3c-11e9-8b2b-0050568e0b79",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/e751dd5d-0f3c-11e9-8b2b-0050568e0b79"
      }
    }
  }
}
```
### Retrieving FlexCache attributes
The GET request is used to retrieve FlexCache attributes. The object includes a large set of fields which can be expensive to retrieve. Most notably, the fields size, guarantee.type, aggregates, path, origins.ip_address, origins.size, and origins.state are expensive to retrieve. The recommended method to use this API is to filter and retrieve only the required fields.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Flexcache

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Flexcache.get_collection()))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    Flexcache(
        {
            "name": "fc_322",
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/flexcaches/04d5e07b-0ebe-11e9-8180-0050568e0b79"
                }
            },
            "uuid": "04d5e07b-0ebe-11e9-8180-0050568e0b79",
        }
    ),
    Flexcache(
        {
            "name": "fc_321",
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/flexcaches/47902654-0ea4-11e9-8180-0050568e0b79"
                }
            },
            "uuid": "47902654-0ea4-11e9-8180-0050568e0b79",
        }
    ),
    Flexcache(
        {
            "name": "fc_323",
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/flexcaches/77e911ff-0ebe-11e9-8180-0050568e0b79"
                }
            },
            "uuid": "77e911ff-0ebe-11e9-8180-0050568e0b79",
        }
    ),
    Flexcache(
        {
            "name": "fc_32",
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/flexcaches/ddb42bbc-0e95-11e9-8180-0050568e0b79"
                }
            },
            "uuid": "ddb42bbc-0e95-11e9-8180-0050568e0b79",
        }
    ),
    Flexcache(
        {
            "name": "fc_333",
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/flexcaches/ec774932-0f3c-11e9-8b2b-0050568e0b79"
                }
            },
            "uuid": "ec774932-0f3c-11e9-8b2b-0050568e0b79",
        }
    ),
]

```
</div>
</div>

### Retrieving the attributes of a FlexCache
The GET request is used to retrieve the attributes of a FlexCache. The object includes a large set of fields which can be expensive to retrieve. Most notably, the fields size, guarantee.type, aggregates, path, origins.ip_address, origins.size, and origins.state are expensive to retrieve. The recommended method to use this API is to filter and retrieve only the required fields.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Flexcache

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Flexcache(uuid="ec774932-0f3c-11e9-8b2b-0050568e0b79")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Flexcache(
    {
        "name": "fc_333",
        "_links": {
            "self": {
                "href": "/api/storage/flexcache/flexcaches/ec774932-0f3c-11e9-8b2b-0050568e0b79"
            }
        },
        "svm": {"name": "vs_1", "uuid": "e708fbe2-0e92-11e9-8180-0050568e0b79"},
        "aggregates": [
            {"name": "aggr_1", "uuid": "26f34b76-88f8-4a47-b5e0-d8e901fb1114"}
        ],
        "uuid": "ec774932-0f3c-11e9-8b2b-0050568e0b79",
        "guarantee": {"type": "volume"},
        "dr_cache": True,
        "size": 4294967296,
        "origins": [
            {
                "volume": {
                    "name": "vol_o1",
                    "uuid": "2bc957dd-2617-4afb-8d2f-66ac6070d313",
                },
                "create_time": "2019-01-03T15:19:55+05:30",
                "cluster": {
                    "name": "node2",
                    "uuid": "50733f81-0e90-11e9-b391-0050568e4115",
                },
                "ip_address": "10.140.103.175",
                "state": "online",
                "svm": {"name": "vs_3", "uuid": "8aa2cd28-0e92-11e9-b391-0050568e4115"},
                "size": 20971520,
            }
        ],
    }
)

```
</div>
</div>

### Deleting a FlexCache
The DELETE request is used to delete a FlexCache.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Flexcache

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Flexcache(uuid="ec774932-0f3c-11e9-8b2b-0050568e0b79")
    resource.delete()

```

### Modifying a FlexCache volume
Use the PATCH request to update a FlexCache volume.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Flexcache

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Flexcache(uuid="ec774932-0f3c-11e9-8b2b-0050568e0b79")
    resource.prepopulate = {"dir_paths": ["/dir1"]}
    resource.patch()

```

# The call
curl -X PATCH "https://<mgmt-ip>/api/storage/flexcache/flexcaches/ec774932-0f3c-11e9-8b2b-0050568e0b79"  -H  "accept: application/json" -H  "Content-Type: application/json" -d "{ \"prepopulate\": { \"dir_paths\": [ \"/dir1\" ], \"exclude_dir_paths\": [ \"/dir1/dir11\" ] } }"
# The response:
{
  "job": {
    "uuid": "b574c48c-1da7-11eb-b006-005056ac6a93",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/b574c48c-1da7-11eb-b006-005056ac6a93"
      }
    }
  }
}
````python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Flexcache

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Flexcache(uuid="28f9734a-2fc2-11ed-a5d5-005056bb2b7")
    resource.writeback = {"enabled": True}
    resource.patch()

```
`
# The call
curl -X PATCH "https://<mgmt-ip>/api/storage/flexcache/flexcaches/28f9734a-2fc2-11ed-a5d5-005056bb2b7" -H "accept: application/json" -H "Content-Type: application/json" -d '{ \"writeback\" : { \"enabled\": false } }'
# The response:
{
  "job": {
    "uuid": "17e193f3-304b-11ed-a5d5-005056bbb2b7",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/17e193f3-304b-11ed-a5d5-005056bbb2b7"
      }
    }
  }
}
````python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Flexcache

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Flexcache(uuid="885dfd0f-ac37-11ed-a2ca-005056bb5573")
    resource.relative_size = {"enabled": True, "percentage": 50}
    resource.patch()

```
`
# The call
curl -X PATCH "https://<mgmt-ip>/api/storage/flexcache/flexcaches/885dfd0f-ac37-11ed-a2ca-005056bb5573" -H "accept: application/json" -d '{"relative_size" : {"enabled":false}}'
# The response:
{
  "job": {
    "uuid": "14bfcc28-ac82-11ed-83bd-005056bb5573",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/14bfcc28-ac82-11ed-83bd-005056bb5573"
      }
    }
  }
}
````python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Flexcache

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Flexcache(uuid="885dfd0f-ac37-11ed-a2ca-005056bb5573")
    resource.atime_scrub = {"enabled": True, "period": 30}
    resource.patch()

```
`
# The call
curl -X PATCH "https://<mgmt-ip>/api/storage/flexcache/flexcaches/885dfd0f-ac37-11ed-a2ca-005056bb5573" -H "accept: application/json" -d '{"atime_scrub" : {"enabled":false}}'
# The response:
{
  "job": {
    "uuid": "14bfcc28-ac82-11ed-83bd-005056bb5573",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/14bfcc28-ac82-11ed-83bd-005056bb5573"
      }
    }
  }
}
````python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Flexcache

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Flexcache(uuid="885dfd0f-ac37-11ed-a2ca-005056bb5573")
    resource.cifs_change_notify = {"enabled": True}
    resource.patch()

```
`"""

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


__all__ = ["Flexcache", "FlexcacheSchema"]
__pdoc__ = {
    "FlexcacheSchema.resource": False,
    "FlexcacheSchema.opts": False,
}


class FlexcacheSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Flexcache object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the flexcache."""

    aggregates = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.disk_aggregates.DiskAggregatesSchema", unknown=EXCLUDE, allow_none=True), data_key="aggregates", allow_none=True)
    r""" Aggregate"""

    atime_scrub = marshmallow_fields.Nested("netapp_ontap.models.flexcache_atime_scrub.FlexcacheAtimeScrubSchema", data_key="atime_scrub", unknown=EXCLUDE, allow_none=True)
    r""" The atime_scrub field of the flexcache."""

    cifs_change_notify = marshmallow_fields.Nested("netapp_ontap.models.flexcache_cifs_change_notify.FlexcacheCifsChangeNotifySchema", data_key="cifs_change_notify", unknown=EXCLUDE, allow_none=True)
    r""" The cifs_change_notify field of the flexcache."""

    constituents_per_aggregate = Size(
        data_key="constituents_per_aggregate",
        allow_none=True,
    )
    r""" Number of FlexCache constituents per aggregate when the 'aggregates' field is mentioned."""

    dr_cache = marshmallow_fields.Boolean(
        data_key="dr_cache",
        allow_none=True,
    )
    r""" If set to true, a DR cache is created."""

    global_file_locking_enabled = marshmallow_fields.Boolean(
        data_key="global_file_locking_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not a FlexCache volume has global file locking mode enabled. Global file locking mode is a mode where protocol read locking semantics are enforced across all FlexCaches and origins of a FlexCache volume. When global file locking mode is enabled, the "is_disconnected_mode_off_for_locks" flag is always set to "true"."""

    guarantee = marshmallow_fields.Nested("netapp_ontap.models.flexcache_guarantee.FlexcacheGuaranteeSchema", data_key="guarantee", unknown=EXCLUDE, allow_none=True)
    r""" The guarantee field of the flexcache."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=203),
        allow_none=True,
    )
    r""" FlexCache name

Example: vol1"""

    origins = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.flexcache_relationship.FlexcacheRelationshipSchema", unknown=EXCLUDE, allow_none=True), data_key="origins", allow_none=True)
    r""" The origins field of the flexcache."""

    override_encryption = marshmallow_fields.Boolean(
        data_key="override_encryption",
        allow_none=True,
    )
    r""" If set to true, a plaintext FlexCache volume for an encrypted origin volume is created."""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" The fully-qualified path in the owning SVM's namespace at which the FlexCache is mounted. The path is case insensitive and must be unique within a SVM's namespace. Path must begin with '/' and must not end with '/'. Only one FlexCache be mounted at any given junction path.

Example: /user/my_fc"""

    prepopulate = marshmallow_fields.Nested("netapp_ontap.models.flexcache_prepopulate.FlexcachePrepopulateSchema", data_key="prepopulate", unknown=EXCLUDE, allow_none=True)
    r""" The prepopulate field of the flexcache."""

    relative_size = marshmallow_fields.Nested("netapp_ontap.models.flexcache_relative_size.FlexcacheRelativeSizeSchema", data_key="relative_size", unknown=EXCLUDE, allow_none=True)
    r""" The relative_size field of the flexcache."""

    size = Size(
        data_key="size",
        allow_none=True,
    )
    r""" Physical size of the FlexCache. The recommended size for a FlexCache is 10% of the origin volume. The minimum FlexCache constituent size is 1GB."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the flexcache."""

    use_tiered_aggregate = marshmallow_fields.Boolean(
        data_key="use_tiered_aggregate",
        allow_none=True,
    )
    r""" Specifies whether or not a Fabricpool-enabled aggregate can be used in FlexCache creation. The use_tiered_aggregate is only used when auto-provisioning a FlexCache volume."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" FlexCache UUID. Unique identifier for the FlexCache.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    writeback = marshmallow_fields.Nested("netapp_ontap.models.flexcache_writeback.FlexcacheWritebackSchema", data_key="writeback", unknown=EXCLUDE, allow_none=True)
    r""" The writeback field of the flexcache."""

    @property
    def resource(self):
        return Flexcache

    gettable_fields = [
        "links",
        "aggregates.links",
        "aggregates.name",
        "aggregates.uuid",
        "atime_scrub",
        "cifs_change_notify",
        "constituents_per_aggregate",
        "dr_cache",
        "global_file_locking_enabled",
        "guarantee",
        "name",
        "origins",
        "override_encryption",
        "path",
        "relative_size",
        "size",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "use_tiered_aggregate",
        "uuid",
        "writeback",
    ]
    """links,aggregates.links,aggregates.name,aggregates.uuid,atime_scrub,cifs_change_notify,constituents_per_aggregate,dr_cache,global_file_locking_enabled,guarantee,name,origins,override_encryption,path,relative_size,size,svm.links,svm.name,svm.uuid,use_tiered_aggregate,uuid,writeback,"""

    patchable_fields = [
        "atime_scrub",
        "cifs_change_notify",
        "prepopulate",
        "relative_size",
        "writeback",
    ]
    """atime_scrub,cifs_change_notify,prepopulate,relative_size,writeback,"""

    postable_fields = [
        "aggregates.name",
        "aggregates.uuid",
        "atime_scrub",
        "cifs_change_notify",
        "constituents_per_aggregate",
        "dr_cache",
        "global_file_locking_enabled",
        "guarantee",
        "name",
        "origins",
        "override_encryption",
        "path",
        "prepopulate",
        "relative_size",
        "size",
        "svm.name",
        "svm.uuid",
        "use_tiered_aggregate",
        "writeback",
    ]
    """aggregates.name,aggregates.uuid,atime_scrub,cifs_change_notify,constituents_per_aggregate,dr_cache,global_file_locking_enabled,guarantee,name,origins,override_encryption,path,prepopulate,relative_size,size,svm.name,svm.uuid,use_tiered_aggregate,writeback,"""

class Flexcache(Resource):
    r""" Defines the cache endpoint of FlexCache. """

    _schema = FlexcacheSchema
    _path = "/api/storage/flexcache/flexcaches"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves FlexCache in the cluster.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `origins.ip_address` - IP address of origin.
* `origins.size` - Physical size of origin.
* `origins.state` - State of origin.
* `size` - Physical size of FlexCache.
* `guarantee.type` - Space guarantee style of FlexCache.
* `aggregates.name` or `aggregates.uuid` - Name or UUID of aggregate of FlexCache volume.
* `path` - Fully-qualified path of the owning SVM's namespace where the FlexCache is mounted.
### Related ONTAP commands
* `volume flexcache show`
### Learn more
* [`DOC /storage/flexcache/flexcaches`](#docs-storage-storage_flexcache_flexcaches)
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
        """Returns a count of all Flexcache resources that match the provided query"""
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
        """Returns a list of RawResources that represent Flexcache resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Flexcache"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Prepopulates a FlexCache volume in the cluster, or modifies configuration of the FlexCache volume.
### Required properties
* `uuid` - FlexCache volume UUID.
### Recommended optional properties
* `prepopulate.exclude_dir_paths` - List of directory-paths to be excluded from prepopulation for the FlexCache volume.
* `prepopulate.dir_paths` - List of directory-paths to be prepopulated for the FlexCache volume.
* `writeback.enabled` - false. This property specifies whether writeback is enabled for the FlexCache volume.
* `relative_size.enabled` - This property specifies whether the relative sizing is enabled for the FlexCache volume.
* `relative_size.percentage` - This property specifies the percent size FlexCache volume should have relative to the total size of the origin volume.
* `atime_scrub.enabled` - This property specifies whether the atime based scrub is enabled for the FlexCache volume.
* `atime_scrub.period` - This property specifies the duration in days after which inactive files can be scrubbed from FlexCache volume.
* `cifs_change_notify.enabled` - This property specifies whether a CIFS change notification is enabled for the FlexCache volume.
### Default property values
If not specified in PATCH, the following default property value is assigned:
* `prepopulate.recurse` - Default value is "true".
### Related ONTAP commands
* `volume flexcache prepopulate start`
* `volume flexcache config modify`
### Learn more
* [`DOC /storage/flexcache/flexcaches`](#docs-storage-storage_flexcache_flexcaches)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Flexcache"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Flexcache"], NetAppResponse]:
        r"""Creates a FlexCache in the cluster.
### Required properties
* `name` - Name of FlexCache volume.
* `origins.volume.name` or `origins.volume.uuid` - Name or UUID of origin volume.
* `origins.svm.name` - Name of origin Vserver.
* `svm.name` or `svm.uuid` - Name or UUID of Vserver where FlexCache will be created.
### Recommended optional properties
* `path` - Path to mount the FlexCache volume
* `prepopulate.dir_paths` - List of directory-paths to be prepopulated for the FlexCache volume.
* `prepopulate.exclude_dir_paths` - List of directory-paths to be excluded from prepopulation for he FlexCache volume.
### Default property values
If not specified in POST, the following default property values are assigned:
* `size` - 10% of origin volume size or 1GB per constituent, whichever is greater.
* `guarantee.type` - none. FlexCache is thin provisioned by default.
* `constituents_per_aggregate` - 4 if aggregates.name or aggregates.uuid is used.
* `use_tiered_aggregate` - false if aggr-list is not used. This property is only used when auto-provisioning a FlexCache volume.
* `is_disconnected_mode_off_for_locks` - false. This property specifies if the origin will honor the cache side locks when doing the lock checks in the disconnected mode.
* `dr_cache` - false if FlexCache is not a DR cache. This property is used to create a DR FlexCache.
* `global_file_locking_enabled` - false. This property specifies whether global file locking is enabled on the FlexCache volume.
* `writeback.enabled` - false. This property specifies whether writeback is enabled for the FlexCache volume.
* `relative_size.enabled` - false. This property specifies whether the relative sizing is enabled for the FlexCache volume.
* `relative_size.percentage` - 10. This property specifies the percent size FlexCache volume should have relative to the total size of the origin volume.
* `override_encryption` - false. If true, this property is used to create a plaintext FlexCache volume for an encrypted origin volume.
* `atime_scrub.enabled` - false. This property specifies whether scrubbing of inactive files based on atime is enabled for the FlexCache volume.
* `atime_scrub.period` - 30. This property specifies the atime duration in days after which the file can be scrubbed from the FlexCache volume if it stays unused beyond the duration.
* `cifs_change_notify.enabled` - false. This property specifies whether a CIFS change notification is enabled for the FlexCache volume.
### Related ONTAP commands
* `volume flexcache create`
* `volume flexcache prepopulate start`
### Learn more
* [`DOC /storage/flexcache/flexcaches`](#docs-storage-storage_flexcache_flexcaches)
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
        records: Iterable["Flexcache"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a FlexCache. If a FlexCache volume is online, it is offlined before deletion.
### Related ONTAP commands
* `volume flexcache delete`
### Learn more
* [`DOC /storage/flexcache/flexcaches`](#docs-storage-storage_flexcache_flexcaches)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves FlexCache in the cluster.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `origins.ip_address` - IP address of origin.
* `origins.size` - Physical size of origin.
* `origins.state` - State of origin.
* `size` - Physical size of FlexCache.
* `guarantee.type` - Space guarantee style of FlexCache.
* `aggregates.name` or `aggregates.uuid` - Name or UUID of aggregate of FlexCache volume.
* `path` - Fully-qualified path of the owning SVM's namespace where the FlexCache is mounted.
### Related ONTAP commands
* `volume flexcache show`
### Learn more
* [`DOC /storage/flexcache/flexcaches`](#docs-storage-storage_flexcache_flexcaches)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves attributes of the FlexCache in the cluster.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are included by default in GET. The recommended method to use this API is to filter and retrieve only the required fields. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `origins.ip_address` - IP address of origin.
* `origins.size` - Physical size of origin.
* `origins.state` - State of origin.
* `size` - Physical size of FlexCache.
* `guarantee.type` - Space guarantee style of FlexCache.
* `aggregates.name` or `aggregates.uuid` - Name or UUID of aggregate of FlexCache volume.
* `path` - Fully-qualified path of the owning SVM's namespace where the FlexCache is mounted.
### Related ONTAP commands
* `volume flexcache show`
### Learn more
* [`DOC /storage/flexcache/flexcaches`](#docs-storage-storage_flexcache_flexcaches)
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
        r"""Creates a FlexCache in the cluster.
### Required properties
* `name` - Name of FlexCache volume.
* `origins.volume.name` or `origins.volume.uuid` - Name or UUID of origin volume.
* `origins.svm.name` - Name of origin Vserver.
* `svm.name` or `svm.uuid` - Name or UUID of Vserver where FlexCache will be created.
### Recommended optional properties
* `path` - Path to mount the FlexCache volume
* `prepopulate.dir_paths` - List of directory-paths to be prepopulated for the FlexCache volume.
* `prepopulate.exclude_dir_paths` - List of directory-paths to be excluded from prepopulation for he FlexCache volume.
### Default property values
If not specified in POST, the following default property values are assigned:
* `size` - 10% of origin volume size or 1GB per constituent, whichever is greater.
* `guarantee.type` - none. FlexCache is thin provisioned by default.
* `constituents_per_aggregate` - 4 if aggregates.name or aggregates.uuid is used.
* `use_tiered_aggregate` - false if aggr-list is not used. This property is only used when auto-provisioning a FlexCache volume.
* `is_disconnected_mode_off_for_locks` - false. This property specifies if the origin will honor the cache side locks when doing the lock checks in the disconnected mode.
* `dr_cache` - false if FlexCache is not a DR cache. This property is used to create a DR FlexCache.
* `global_file_locking_enabled` - false. This property specifies whether global file locking is enabled on the FlexCache volume.
* `writeback.enabled` - false. This property specifies whether writeback is enabled for the FlexCache volume.
* `relative_size.enabled` - false. This property specifies whether the relative sizing is enabled for the FlexCache volume.
* `relative_size.percentage` - 10. This property specifies the percent size FlexCache volume should have relative to the total size of the origin volume.
* `override_encryption` - false. If true, this property is used to create a plaintext FlexCache volume for an encrypted origin volume.
* `atime_scrub.enabled` - false. This property specifies whether scrubbing of inactive files based on atime is enabled for the FlexCache volume.
* `atime_scrub.period` - 30. This property specifies the atime duration in days after which the file can be scrubbed from the FlexCache volume if it stays unused beyond the duration.
* `cifs_change_notify.enabled` - false. This property specifies whether a CIFS change notification is enabled for the FlexCache volume.
### Related ONTAP commands
* `volume flexcache create`
* `volume flexcache prepopulate start`
### Learn more
* [`DOC /storage/flexcache/flexcaches`](#docs-storage-storage_flexcache_flexcaches)
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
        r"""Prepopulates a FlexCache volume in the cluster, or modifies configuration of the FlexCache volume.
### Required properties
* `uuid` - FlexCache volume UUID.
### Recommended optional properties
* `prepopulate.exclude_dir_paths` - List of directory-paths to be excluded from prepopulation for the FlexCache volume.
* `prepopulate.dir_paths` - List of directory-paths to be prepopulated for the FlexCache volume.
* `writeback.enabled` - false. This property specifies whether writeback is enabled for the FlexCache volume.
* `relative_size.enabled` - This property specifies whether the relative sizing is enabled for the FlexCache volume.
* `relative_size.percentage` - This property specifies the percent size FlexCache volume should have relative to the total size of the origin volume.
* `atime_scrub.enabled` - This property specifies whether the atime based scrub is enabled for the FlexCache volume.
* `atime_scrub.period` - This property specifies the duration in days after which inactive files can be scrubbed from FlexCache volume.
* `cifs_change_notify.enabled` - This property specifies whether a CIFS change notification is enabled for the FlexCache volume.
### Default property values
If not specified in PATCH, the following default property value is assigned:
* `prepopulate.recurse` - Default value is "true".
### Related ONTAP commands
* `volume flexcache prepopulate start`
* `volume flexcache config modify`
### Learn more
* [`DOC /storage/flexcache/flexcaches`](#docs-storage-storage_flexcache_flexcaches)
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
        r"""Deletes a FlexCache. If a FlexCache volume is online, it is offlined before deletion.
### Related ONTAP commands
* `volume flexcache delete`
### Learn more
* [`DOC /storage/flexcache/flexcaches`](#docs-storage-storage_flexcache_flexcaches)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


