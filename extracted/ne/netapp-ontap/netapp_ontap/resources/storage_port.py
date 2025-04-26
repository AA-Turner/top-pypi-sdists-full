r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Retrieving storage port information
The storage port GET API retrieves all of the storage ports in the cluster.
<br/>
---
## Examples
### 1) Retrieve a list of storage ports from the cluster
#### The following example shows the response with a list of storage ports in the cluster:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(StoragePort.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    StoragePort(
        {
            "name": "0a",
            "node": {
                "name": "node-1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/0530d6c1-8c6d-11e8-907f-00a0985a72ee"
                    }
                },
                "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
            },
        }
    ),
    StoragePort(
        {
            "name": "0b",
            "node": {
                "name": "node-1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/0530d6c1-8c6d-11e8-907f-00a0985a72ee"
                    }
                },
                "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
            },
        }
    ),
    StoragePort(
        {
            "name": "0c",
            "node": {
                "name": "node-1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/0530d6c1-8c6d-11e8-907f-00a0985a72ee"
                    }
                },
                "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
            },
        }
    ),
    StoragePort(
        {
            "name": "0d",
            "node": {
                "name": "node-1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/0530d6c1-8c6d-11e8-907f-00a0985a72ee"
                    }
                },
                "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
            },
        }
    ),
    StoragePort(
        {
            "name": "0e",
            "node": {
                "name": "node-1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/0530d6c1-8c6d-11e8-907f-00a0985a72ee"
                    }
                },
                "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
            },
        }
    ),
    StoragePort(
        {
            "name": "0f",
            "node": {
                "name": "node-1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/0530d6c1-8c6d-11e8-907f-00a0985a72ee"
                    }
                },
                "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
            },
        }
    ),
    StoragePort(
        {
            "name": "0g",
            "node": {
                "name": "node-1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/0530d6c1-8c6d-11e8-907f-00a0985a72ee"
                    }
                },
                "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
            },
        }
    ),
]

```
</div>
</div>

---
### 2) Retrieve a specific storage port from the cluster
#### The following example shows the response of the requested storage port. If there is no storage port with the requested node uuid and name, an error is returned.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePort(
        name="0a", **{"node.uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
StoragePort(
    {
        "name": "0a",
        "enabled": True,
        "firmware_version": "01.12.09.00",
        "speed": 6.0,
        "node": {
            "name": "node-1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/0530d6c1-8c6d-11e8-907f-00a0985a72ee"
                }
            },
            "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
        },
        "cable": {
            "length": "0.5m",
            "serial_number": "629230774",
            "part_number": "112-00429+A0",
            "vendor": "Molex Inc.",
            "identifier": "500a0980066e2c01-500a098003633df0",
            "transceiver": "mini_sas_hd",
        },
        "in_use": True,
        "state": "online",
        "wwn": "500a098003633df0",
        "description": "SAS Host Adapter 0a (PMC-Sierra PM8001 rev. C)",
        "type": "sas",
        "redundant": True,
    }
)

```
</div>
</div>

---
## Updating a storage port
The storage port PATCH API modifies the port mode for storage/network use and allows the port to be enabled/disabled.
---
## Examples
### 1) Using an Ethernet port for storage
The following example sets an Ethernet port mode for storage use:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePort(
        name="e3a", **{"node.uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee"}
    )
    resource.mode = "storage"
    resource.patch()

```

---
### 2) Disabling a storage port
The following example disables an unused storage port:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePort(
        name="e3a", **{"node.uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee"}
    )
    resource.enabled = False
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


__all__ = ["StoragePort", "StoragePortSchema"]
__pdoc__ = {
    "StoragePortSchema.resource": False,
    "StoragePortSchema.opts": False,
}


class StoragePortSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StoragePort object"""

    board_name = marshmallow_fields.Str(
        data_key="board_name",
        allow_none=True,
    )
    r""" The board_name field of the storage_port."""

    cable = marshmallow_fields.Nested("netapp_ontap.models.storage_port_cable.StoragePortCableSchema", data_key="cable", unknown=EXCLUDE, allow_none=True)
    r""" The cable field of the storage_port."""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" The description field of the storage_port.

Example: SAS Host Adapter 2a (PMC-Sierra PM8072 rev. C)"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The enabled field of the storage_port."""

    error = marshmallow_fields.Nested("netapp_ontap.models.storage_port_error.StoragePortErrorSchema", data_key="error", unknown=EXCLUDE, allow_none=True)
    r""" The error field of the storage_port."""

    firmware_version = marshmallow_fields.Str(
        data_key="firmware_version",
        allow_none=True,
    )
    r""" The firmware_version field of the storage_port.

Example: 03.08.09.00"""

    force = marshmallow_fields.Boolean(
        data_key="force",
        allow_none=True,
    )
    r""" The force field of the storage_port."""

    in_use = marshmallow_fields.Boolean(
        data_key="in_use",
        allow_none=True,
    )
    r""" Specifies whether any devices are connected through this port"""

    mac_address = marshmallow_fields.Str(
        data_key="mac_address",
        allow_none=True,
    )
    r""" The mac_address field of the storage_port."""

    mode = marshmallow_fields.Str(
        data_key="mode",
        validate=enum_validation(['network', 'storage']),
        allow_none=True,
    )
    r""" Operational mode of a non-dedicated Ethernet port

Valid choices:

* network
* storage"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name field of the storage_port.

Example: 2a"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the storage_port."""

    part_number = marshmallow_fields.Str(
        data_key="part_number",
        allow_none=True,
    )
    r""" The part_number field of the storage_port.

Example: 111-03801"""

    redundant = marshmallow_fields.Boolean(
        data_key="redundant",
        allow_none=True,
    )
    r""" Specifies whether all devices connected through this port have a redundant path from another port"""

    serial_number = marshmallow_fields.Str(
        data_key="serial_number",
        allow_none=True,
    )
    r""" The serial_number field of the storage_port.

Example: 7A2463CC45B"""

    speed = marshmallow_fields.Number(
        data_key="speed",
        allow_none=True,
    )
    r""" Operational port speed in Gbps

Example: 6.0"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['online', 'offline', 'error']),
        allow_none=True,
    )
    r""" The state field of the storage_port.

Valid choices:

* online
* offline
* error"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['sas', 'fc', 'enet']),
        allow_none=True,
    )
    r""" The type field of the storage_port.

Valid choices:

* sas
* fc
* enet"""

    wwn = marshmallow_fields.Str(
        data_key="wwn",
        allow_none=True,
    )
    r""" World Wide Name

Example: 50000d1703544b80"""

    wwpn = marshmallow_fields.Str(
        data_key="wwpn",
        allow_none=True,
    )
    r""" World Wide Port Name"""

    @property
    def resource(self):
        return StoragePort

    gettable_fields = [
        "board_name",
        "cable",
        "description",
        "enabled",
        "error",
        "firmware_version",
        "in_use",
        "mac_address",
        "mode",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "part_number",
        "redundant",
        "serial_number",
        "speed",
        "state",
        "type",
        "wwn",
        "wwpn",
    ]
    """board_name,cable,description,enabled,error,firmware_version,in_use,mac_address,mode,name,node.links,node.name,node.uuid,part_number,redundant,serial_number,speed,state,type,wwn,wwpn,"""

    patchable_fields = [
        "enabled",
        "force",
        "mode",
    ]
    """enabled,force,mode,"""

    postable_fields = [
        "enabled",
        "mode",
    ]
    """enabled,mode,"""

class StoragePort(Resource):
    """Allows interaction with StoragePort objects on the host"""

    _schema = StoragePortSchema
    _path = "/api/storage/ports"
    _keys = ["node.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of storage ports.
### Related ONTAP commands
* `storage port show`
### Learn more
* [`DOC /storage/ports`](#docs-storage-storage_ports)
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
        """Returns a count of all StoragePort resources that match the provided query"""
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
        """Returns a list of RawResources that represent StoragePort resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["StoragePort"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a storage port.
### Related ONTAP commands
* `storage port modify`
* `storage port enable`
* `storage port disable`
### Learn more
* [`DOC /storage/ports`](#docs-storage-storage_ports)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of storage ports.
### Related ONTAP commands
* `storage port show`
### Learn more
* [`DOC /storage/ports`](#docs-storage-storage_ports)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific storage port.
### Related ONTAP commands
* `storage port show`
### Learn more
* [`DOC /storage/ports`](#docs-storage-storage_ports)
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
        r"""Updates a storage port.
### Related ONTAP commands
* `storage port modify`
* `storage port enable`
* `storage port disable`
### Learn more
* [`DOC /storage/ports`](#docs-storage-storage_ports)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



