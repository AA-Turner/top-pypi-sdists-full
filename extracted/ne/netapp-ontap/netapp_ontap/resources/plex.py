r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The Storage Aggregate Plex API provides relevant state information for each plex in the aggregate.
For each plex, details are provided for the RAID groups in the plex and the disks that make up each RAID group.<br>
## Examples
### Retrieving all aggregates and plexes
The following example shows the response with a list of aggregates and plexes:<br>
# The call:
curl -X GET "https://<mgmt-ip>/api/storage/aggregates/*/plexes" -H "accept: application/json"
# The response:
{
  "records": [
    {
      "aggregate": {
        "uuid": "04b7296e-a302-42a6-a2a9-dda6be054b29",
        "name": "test2"
      },
      "name": "plex0"
    },
    {
      "aggregate": {
        "uuid": "04b7296e-a302-42a6-a2a9-dda6be054b29",
        "name": "test2"
      },
      "name": "plex1",
    },
    {
      "aggregate": {
        "uuid": "66c4b221-65ff-4211-9b58-ada3c6fc41af",
        "name": "test"
      },
      "name": "plex0"
    },
    {
      "aggregate": {
        "uuid": "66c4b221-65ff-4211-9b58-ada3c6fc41af",
        "name": "test"
      },
      "name": "plex1"
    },
    {
      "aggregate": {
        "uuid": "7ee89e48-5d81-4609-9e1b-5d8d0995a886",
        "name": "aggr1",
      },
      "name": "plex0",
    },
    {
      "aggregate": {
        "uuid": "8bb2e3bf-c4f1-4748-9033-ca9231cf1c40",
        "name": "test3",
      },
      "name": "plex0",
    },
    {
      "aggregate": {
        "uuid": "8bb2e3bf-c4f1-4748-9033-ca9231cf1c40",
        "name": "test3",
      },
      "name": "plex1"
    },
    {
      "aggregate": {
        "uuid": "8f13de5c-99cf-4ada-884c-3cc32deb304a",
        "name": "aggr2",
      },
      "name": "plex0"
    }
  ],
  "num_records": 8
}
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Plex

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Plex("*", name="plex0")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Plex(
        {
            "aggregate": {
                "name": "test2",
                "uuid": "04b7296e-a302-42a6-a2a9-dda6be054b29",
            },
            "name": "plex0",
        }
    ),
    Plex(
        {
            "aggregate": {
                "name": "test",
                "uuid": "66c4b221-65ff-4211-9b58-ada3c6fc41af",
            },
            "name": "plex0",
        }
    ),
    Plex(
        {
            "aggregate": {
                "name": "aggr1",
                "uuid": "7ee89e48-5d81-4609-9e1b-5d8d0995a886",
            },
            "name": "plex0",
        }
    ),
    Plex(
        {
            "aggregate": {
                "name": "test3",
                "uuid": "8bb2e3bf-c4f1-4748-9033-ca9231cf1c40",
            },
            "name": "plex0",
        }
    ),
    Plex(
        {
            "aggregate": {
                "name": "aggr2",
                "uuid": "8f13de5c-99cf-4ada-884c-3cc32deb304a",
            },
            "name": "plex0",
        }
    ),
]

```
</div>
</div>

### Retrieving the list of plexes in an aggregate
The following example shows the response with the list of plexes in an aggregate:<br>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Plex

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Plex.get_collection("19425837-f2fa-4a9f-8f01-712f626c983c")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[Plex({"name": "plex0"}), Plex({"name": "plex4"})]

```
</div>
</div>

### Retrieving a specific plex in an aggregate
The following example shows the response when requesting a specific plex of an aggregate:<br>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Plex

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Plex("19425837-f2fa-4a9f-8f01-712f626c983c", name="plex0")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
Plex(
    {
        "aggregate": {"name": "test1", "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c"},
        "name": "plex0",
        "pool": "pool0",
        "state": "normal",
        "raid_groups": [
            {
                "reconstruct": {"active": False},
                "cache_tier": False,
                "degraded": False,
                "raid_type": "raid_dp",
                "name": "rg0",
                "disks": [
                    {
                        "position": "dparity",
                        "state": "normal",
                        "disk": {"name": "1.1.29"},
                        "usable_size": 86769664,
                        "type": "ssd",
                    },
                    {
                        "position": "parity",
                        "state": "normal",
                        "disk": {"name": "1.1.4"},
                        "usable_size": 86769664,
                        "type": "ssd",
                    },
                    {
                        "position": "data",
                        "state": "normal",
                        "disk": {"name": "1.1.30"},
                        "usable_size": 86769664,
                        "type": "ssd",
                    },
                    {
                        "position": "data",
                        "state": "normal",
                        "disk": {"name": "1.1.5"},
                        "usable_size": 86769664,
                        "type": "ssd",
                    },
                    {
                        "position": "data",
                        "state": "normal",
                        "disk": {"name": "1.1.31"},
                        "usable_size": 86769664,
                        "type": "ssd",
                    },
                    {
                        "position": "data",
                        "state": "normal",
                        "disk": {"name": "1.1.6"},
                        "usable_size": 86769664,
                        "type": "ssd",
                    },
                ],
                "recomputing_parity": {"active": False},
            }
        ],
        "resync": {"active": False},
        "online": True,
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


__all__ = ["Plex", "PlexSchema"]
__pdoc__ = {
    "PlexSchema.resource": False,
    "PlexSchema.opts": False,
}


class PlexSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Plex object"""

    aggregate = marshmallow_fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", data_key="aggregate", unknown=EXCLUDE, allow_none=True)
    r""" The aggregate field of the plex."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Plex name

Example: plex0"""

    online = marshmallow_fields.Boolean(
        data_key="online",
        allow_none=True,
    )
    r""" Plex is online"""

    pool = marshmallow_fields.Str(
        data_key="pool",
        validate=enum_validation(['pool0', 'pool1']),
        allow_none=True,
    )
    r""" SyncMirror pool assignment

Valid choices:

* pool0
* pool1"""

    raid_groups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.raid_group.RaidGroupSchema", unknown=EXCLUDE, allow_none=True), data_key="raid_groups", allow_none=True)
    r""" The raid_groups field of the plex."""

    resync = marshmallow_fields.Nested("netapp_ontap.models.plex_resync.PlexResyncSchema", data_key="resync", unknown=EXCLUDE, allow_none=True)
    r""" The resync field of the plex."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['normal', 'failed', 'out_of_date']),
        allow_none=True,
    )
    r""" Plex state

Valid choices:

* normal
* failed
* out_of_date"""

    @property
    def resource(self):
        return Plex

    gettable_fields = [
        "aggregate.links",
        "aggregate.name",
        "aggregate.uuid",
        "name",
        "online",
        "pool",
        "raid_groups",
        "resync",
        "state",
    ]
    """aggregate.links,aggregate.name,aggregate.uuid,name,online,pool,raid_groups,resync,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class Plex(Resource):
    """Allows interaction with Plex objects on the host"""

    _schema = PlexSchema
    _path = "/api/storage/aggregates/{aggregate[uuid]}/plexes"
    _keys = ["aggregate.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of plexes for the specified aggregate.
### Related ONTAP commands
* `storage aggregate plex show`

### Learn more
* [`DOC /storage/aggregates/{aggregate.uuid}/plexes`](#docs-storage-storage_aggregates_{aggregate.uuid}_plexes)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Plex resources that match the provided query"""
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
        """Returns a list of RawResources that represent Plex resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of plexes for the specified aggregate.
### Related ONTAP commands
* `storage aggregate plex show`

### Learn more
* [`DOC /storage/aggregates/{aggregate.uuid}/plexes`](#docs-storage-storage_aggregates_{aggregate.uuid}_plexes)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the plex specified by the aggregate UUID and plex name.
### Related ONTAP commands
* `storage aggregate plex show`

### Learn more
* [`DOC /storage/aggregates/{aggregate.uuid}/plexes`](#docs-storage-storage_aggregates_{aggregate.uuid}_plexes)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





