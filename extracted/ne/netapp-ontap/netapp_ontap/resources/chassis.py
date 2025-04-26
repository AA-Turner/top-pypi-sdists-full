r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use the chassis GET API to retrieve all of the chassis information in the cluster.
<br/>
## Examples
### Retrieving a list of chassis from the cluster
The following example shows the response with a list of chassis in the cluster:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Chassis

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Chassis.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[Chassis({"id": "021352005981"})]

```
</div>
</div>

---
### Retrieving a specific chassis from the cluster
The following example shows the response of the requested chassis. If there is no chassis with the requested ID, an error is returned.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Chassis

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Chassis(id=21352005981)
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Chassis(
    {
        "state": "ok",
        "id": "021352005981",
        "frus": [
            {"type": "psu", "id": "PSU2", "state": "ok"},
            {"type": "psu", "id": "PSU1", "state": "ok"},
            {"type": "fan", "id": "Fan2", "state": "ok"},
            {"type": "fan", "id": "Fan3", "state": "ok"},
            {"type": "fan", "id": "Fan1", "state": "ok"},
        ],
        "nodes": [
            {
                "position": "top",
                "pcis": {
                    "cards": [
                        {
                            "device": "Gigabit Ethernet I210",
                            "slot": "0",
                            "info": "\t  e0M MAC Address:    d0:39:ea:3f:06:2b (auto-1000t-fd-up) \n\t  e0S MAC Address:    d0:39:ea:3f:06:2c (auto-1000t-fd-up) \n\t  Device Type:        1533\n\t  Firmware Version:   3.25-0.0 0x800005D1\n",
                        },
                        {
                            "device": "Intel Lewisburg series chipset SATA Controller",
                            "slot": "0",
                            "info": "\t  Additional Info: 0 (0xaaf00000)   \n\t  SHM2S86Q120GLM22NP FW1146 114473MB 512B/sect (SPG190108HJ)  \n",
                        },
                    ]
                },
                "name": "node-1",
                "usbs": {
                    "enabled": True,
                    "ports": [{"connected": False}],
                    "supported": True,
                },
                "uuid": "6ede364b-c3d0-11e8-a86a-00a098567f31",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6ede364b-c3d0-11e8-a86a-00a098567f31"
                    }
                },
            }
        ],
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


__all__ = ["Chassis", "ChassisSchema"]
__pdoc__ = {
    "ChassisSchema.resource": False,
    "ChassisSchema.opts": False,
}


class ChassisSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Chassis object"""

    frus = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.chassis_frus.ChassisFrusSchema", unknown=EXCLUDE, allow_none=True), data_key="frus", allow_none=True)
    r""" List of FRUs in the chassis."""

    id = marshmallow_fields.Str(
        data_key="id",
        allow_none=True,
    )
    r""" The id field of the chassis.

Example: 2.1352005981E10"""

    nodes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.chassis_node.ChassisNodeSchema", unknown=EXCLUDE, allow_none=True), data_key="nodes", allow_none=True)
    r""" List of nodes in the chassis."""

    shelves = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.shelf.ShelfSchema", unknown=EXCLUDE, allow_none=True), data_key="shelves", allow_none=True)
    r""" List of shelves in chassis."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['ok', 'error']),
        allow_none=True,
    )
    r""" The state field of the chassis.

Valid choices:

* ok
* error"""

    @property
    def resource(self):
        return Chassis

    gettable_fields = [
        "frus",
        "id",
        "nodes",
        "shelves",
        "state",
    ]
    """frus,id,nodes,shelves,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class Chassis(Resource):
    """Allows interaction with Chassis objects on the host"""

    _schema = ChassisSchema
    _path = "/api/cluster/chassis"
    _keys = ["id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of chassis.
### Related ONTAP commands
* `system chassis show`
* `system chassis fru show`
### Learn more
* [`DOC /cluster/chassis`](#docs-cluster-cluster_chassis)
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
        """Returns a count of all Chassis resources that match the provided query"""
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
        """Returns a list of RawResources that represent Chassis resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of chassis.
### Related ONTAP commands
* `system chassis show`
* `system chassis fru show`
### Learn more
* [`DOC /cluster/chassis`](#docs-cluster-cluster_chassis)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific chassis.
### Related ONTAP commands
* `system chassis show`
* `system chassis fru show`
### Learn more
* [`DOC /cluster/chassis`](#docs-cluster-cluster_chassis)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





