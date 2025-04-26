r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Retrieving storage tape information
The storage tape GET API retrieves all of the tapes in the cluster.
<br/>
---
## Examples
### 1) Retrieving a list of tapes from the cluster
The following example returns the list of tapes in the cluster:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TapeDevice

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(TapeDevice.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    TapeDevice(
        {
            "device_id": "2d.0",
            "node": {
                "name": "st-8020-1-01",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/4083be52-5315-11eb-a839-00a0985ebbe7"
                    }
                },
                "uuid": "4083be52-5315-11eb-a839-00a0985ebbe7",
            },
        }
    ),
    TapeDevice(
        {
            "device_id": "2d.0L1",
            "node": {
                "name": "st-8020-1-01",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/4083be52-5315-11eb-a839-00a0985ebbe7"
                    }
                },
                "uuid": "4083be52-5315-11eb-a839-00a0985ebbe7",
            },
        }
    ),
    TapeDevice(
        {
            "device_id": "qeg-tape-brocade2-8g:0.126",
            "node": {
                "name": "st-8020-1-01",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/4083be52-5315-11eb-a839-00a0985ebbe7"
                    }
                },
                "uuid": "4083be52-5315-11eb-a839-00a0985ebbe7",
            },
        }
    ),
    TapeDevice(
        {
            "device_id": "stsw-broc6510-01:11.126",
            "node": {
                "name": "st-8020-1-01",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/4083be52-5315-11eb-a839-00a0985ebbe7"
                    }
                },
                "uuid": "4083be52-5315-11eb-a839-00a0985ebbe7",
            },
        }
    ),
    TapeDevice(
        {
            "device_id": "stsw-broc6510-01:15.126",
            "node": {
                "name": "st-8020-1-01",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/4083be52-5315-11eb-a839-00a0985ebbe7"
                    }
                },
                "uuid": "4083be52-5315-11eb-a839-00a0985ebbe7",
            },
        }
    ),
    TapeDevice(
        {
            "device_id": "stsw-broc6510-01:15.126L1",
            "node": {
                "name": "st-8020-1-01",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/4083be52-5315-11eb-a839-00a0985ebbe7"
                    }
                },
                "uuid": "4083be52-5315-11eb-a839-00a0985ebbe7",
            },
        }
    ),
    TapeDevice(
        {
            "device_id": "stsw-broc6510-01:22.126",
            "node": {
                "name": "st-8020-1-01",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/4083be52-5315-11eb-a839-00a0985ebbe7"
                    }
                },
                "uuid": "4083be52-5315-11eb-a839-00a0985ebbe7",
            },
        }
    ),
    TapeDevice(
        {
            "device_id": "stsw-broc6510-01:23.126",
            "node": {
                "name": "st-8020-1-01",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/4083be52-5315-11eb-a839-00a0985ebbe7"
                    }
                },
                "uuid": "4083be52-5315-11eb-a839-00a0985ebbe7",
            },
        }
    ),
]

```
</div>
</div>

---
### 2) Retrieving a specific tape device from the cluster
The following example returns the requested tape device. If there is no tape with the requested UID, an error is returned.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TapeDevice

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = TapeDevice(
        device_id="2d.0", **{"node.uuid": "5f5275eb-5315-11eb-8ac4-00a0985e0dcf"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
TapeDevice(
    {
        "block_number": -1,
        "aliases": [{"mapping": "SN[1068000245]", "name": "st7"}],
        "device_names": [
            {
                "unload_reload_device": "urst0l",
                "no_rewind_device": "nrst0l",
                "rewind_device": "rst0l",
            },
            {
                "unload_reload_device": "urst0m",
                "no_rewind_device": "nrst0m",
                "rewind_device": "rst0m",
            },
            {
                "unload_reload_device": "urst0h",
                "no_rewind_device": "nrst0h",
                "rewind_device": "rst0h",
            },
            {
                "unload_reload_device": "urst0a",
                "no_rewind_device": "nrst0a",
                "rewind_device": "rst0a",
            },
        ],
        "formats": [
            "LTO-4/5 Native Density",
            "LTO-4/5 Compressed",
            "LTO-6 2.5TB",
            "LTO-6 6.25TB Compressed",
        ],
        "file_number": -1,
        "device_id": "2d.0",
        "storage_port": {"name": "2d"},
        "alias": {"mapping": "SN[1068000245]", "name": "st7"},
        "device_state": "offline",
        "node": {
            "name": "st-8020-1-02",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/5f5275eb-5315-11eb-8ac4-00a0985e0dcf"
                }
            },
            "uuid": "5f5275eb-5315-11eb-8ac4-00a0985e0dcf",
        },
        "interface": "sas",
        "reservation_type": "off",
        "wwnn": "5001697722ee0010",
        "description": "IBM LTO-6 ULT3580",
        "serial_number": "1068000245",
        "density": "low",
        "wwpn": "5001697722ee0011",
        "type": "tape",
        "residual_count": 0,
    }
)

```
</div>
</div>

---
## Updating a tape device
The tape PATCH API allows the tape device to be set online or offline, positioned, and given an alias.
---
## Examples
### 1) Taking a tape device offline
The following example takes a tape device offline:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TapeDevice

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = TapeDevice(
        device_id="2d.0", **{"node.uuid": "5f5275eb-5315-11eb-8ac4-00a0985e0dcf"}
    )
    resource.online = False
    resource.patch()

```

---
### 2) Bringing a tape device online
The following example brings a tape device online:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TapeDevice

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = TapeDevice(
        device_id="2d.0", **{"node.uuid": "5f5275eb-5315-11eb-8ac4-00a0985e0dcf"}
    )
    resource.online = True
    resource.patch()

```

---
### 3) Giving a tape device an alias
The following example assigns an alias to a tape device:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TapeDevice

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = TapeDevice(
        device_id="2d.0", **{"node.uuid": "5f5275eb-5315-11eb-8ac4-00a0985e0dcf"}
    )
    resource.aliases = [{"name": "st0"}]
    resource.patch()

```

---
### 4) Removing a tape device's aliases
The following example clears any aliases previously assigned to a tape device:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TapeDevice

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = TapeDevice(
        device_id="2d.0", **{"node.uuid": "5f5275eb-5315-11eb-8ac4-00a0985e0dcf"}
    )
    resource.aliases = []
    resource.patch()

```

---
### 5) Rewinding a tape device
The following example rewinds a tape device:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TapeDevice

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = TapeDevice(
        device_id="2d.0", **{"node.uuid": "5f5275eb-5315-11eb-8ac4-00a0985e0dcf"}
    )
    resource.position = {"operation": "rewind"}
    resource.patch()

```

---
### 6) Forwarding the tape five files
The following example moves the tape forward five file records:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TapeDevice

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = TapeDevice(
        device_id="2d.0", **{"node.uuid": "5f5275eb-5315-11eb-8ac4-00a0985e0dcf"}
    )
    resource.position = {"operation": "fsf", "count": 5}
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


__all__ = ["TapeDevice", "TapeDeviceSchema"]
__pdoc__ = {
    "TapeDeviceSchema.resource": False,
    "TapeDeviceSchema.opts": False,
}


class TapeDeviceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TapeDevice object"""

    alias = marshmallow_fields.Nested("netapp_ontap.models.tape_device_alias.TapeDeviceAliasSchema", data_key="alias", unknown=EXCLUDE, allow_none=True)
    r""" The alias field of the tape_device."""

    aliases = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.tape_device_aliases.TapeDeviceAliasesSchema", unknown=EXCLUDE, allow_none=True), data_key="aliases", allow_none=True)
    r""" The aliases field of the tape_device."""

    block_number = Size(
        data_key="block_number",
        allow_none=True,
    )
    r""" Block number.

Example: 0"""

    density = marshmallow_fields.Str(
        data_key="density",
        validate=enum_validation(['low', 'medium', 'high', 'extended']),
        allow_none=True,
    )
    r""" Density.

Valid choices:

* low
* medium
* high
* extended"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" The description field of the tape_device.

Example: QUANTUM LTO-8 ULTRIUM"""

    device_id = marshmallow_fields.Str(
        data_key="device_id",
        allow_none=True,
    )
    r""" The device_id field of the tape_device.

Example: 1a.0"""

    device_names = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.tape_device_device_names.TapeDeviceDeviceNamesSchema", unknown=EXCLUDE, allow_none=True), data_key="device_names", allow_none=True)
    r""" The device_names field of the tape_device."""

    device_state = marshmallow_fields.Str(
        data_key="device_state",
        validate=enum_validation(['unknown', 'available', 'ready_write_enabled', 'ready_write_protected', 'offline', 'in_use', 'error', 'reserved_by_another_host', 'normal', 'rewinding', 'erasing']),
        allow_none=True,
    )
    r""" Operational state of the device.

Valid choices:

* unknown
* available
* ready_write_enabled
* ready_write_protected
* offline
* in_use
* error
* reserved_by_another_host
* normal
* rewinding
* erasing"""

    file_number = Size(
        data_key="file_number",
        allow_none=True,
    )
    r""" File number.

Example: 0"""

    formats = marshmallow_fields.List(marshmallow_fields.Str, data_key="formats", allow_none=True)
    r""" Tape cartridge format.

Example: ["LTO-7 6TB","LTO-7 15TB Compressed","LTO-8 12TB","LTO-8 30TB Compressed"]"""

    interface = marshmallow_fields.Str(
        data_key="interface",
        validate=enum_validation(['unknown', 'fibre_channel', 'sas', 'pscsi']),
        allow_none=True,
    )
    r""" Device interface type.

Valid choices:

* unknown
* fibre_channel
* sas
* pscsi"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the tape_device."""

    online = marshmallow_fields.Boolean(
        data_key="online",
        allow_none=True,
    )
    r""" The online field of the tape_device."""

    position = marshmallow_fields.Nested("netapp_ontap.models.tape_device_position.TapeDevicePositionSchema", data_key="position", unknown=EXCLUDE, allow_none=True)
    r""" The position field of the tape_device."""

    reservation_type = marshmallow_fields.Str(
        data_key="reservation_type",
        validate=enum_validation(['off', 'persistent', 'scsi']),
        allow_none=True,
    )
    r""" The reservation_type field of the tape_device.

Valid choices:

* off
* persistent
* scsi"""

    residual_count = Size(
        data_key="residual_count",
        allow_none=True,
    )
    r""" Residual count of the last I/O operation.

Example: 0"""

    serial_number = marshmallow_fields.Str(
        data_key="serial_number",
        allow_none=True,
    )
    r""" The serial_number field of the tape_device.

Example: 10WT00093"""

    storage_port = marshmallow_fields.Nested("netapp_ontap.models.tape_device_storage_port.TapeDeviceStoragePortSchema", data_key="storage_port", unknown=EXCLUDE, allow_none=True)
    r""" The storage_port field of the tape_device."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['unknown', 'tape', 'media_changer']),
        allow_none=True,
    )
    r""" Device type.

Valid choices:

* unknown
* tape
* media_changer"""

    wwnn = marshmallow_fields.Str(
        data_key="wwnn",
        allow_none=True,
    )
    r""" World Wide Node Name.

Example: 500507631295741c"""

    wwpn = marshmallow_fields.Str(
        data_key="wwpn",
        allow_none=True,
    )
    r""" World Wide Port Name.

Example: 500507631295741c"""

    @property
    def resource(self):
        return TapeDevice

    gettable_fields = [
        "alias",
        "aliases",
        "block_number",
        "density",
        "description",
        "device_id",
        "device_names",
        "device_state",
        "file_number",
        "formats",
        "interface",
        "node.links",
        "node.name",
        "node.uuid",
        "online",
        "reservation_type",
        "residual_count",
        "serial_number",
        "storage_port",
        "type",
        "wwnn",
        "wwpn",
    ]
    """alias,aliases,block_number,density,description,device_id,device_names,device_state,file_number,formats,interface,node.links,node.name,node.uuid,online,reservation_type,residual_count,serial_number,storage_port,type,wwnn,wwpn,"""

    patchable_fields = [
        "aliases",
        "online",
        "position",
    ]
    """aliases,online,position,"""

    postable_fields = [
        "aliases",
        "online",
    ]
    """aliases,online,"""

class TapeDevice(Resource):
    """Allows interaction with TapeDevice objects on the host"""

    _schema = TapeDeviceSchema
    _path = "/api/storage/tape-devices"
    _keys = ["node.uuid", "device_id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of tape devices.
### Related ONTAP commands
* `storage tape show`
### Learn more
* [`DOC /storage/tape-devices`](#docs-storage-storage_tape-devices)
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
        """Returns a count of all TapeDevice resources that match the provided query"""
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
        """Returns a list of RawResources that represent TapeDevice resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["TapeDevice"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a specific tape device.
### Related ONTAP commands
* `storage tape alias-set`
* `storage tape alias-clear`
* `storage tape online`
* `storage tape offline`
* `storage tape position`
### Learn more
* [`DOC /storage/tape-devices`](#docs-storage-storage_tape-devices)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of tape devices.
### Related ONTAP commands
* `storage tape show`
### Learn more
* [`DOC /storage/tape-devices`](#docs-storage-storage_tape-devices)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific tape device.
### Related ONTAP commands
* `storage tape show`
### Learn more
* [`DOC /storage/tape-devices`](#docs-storage-storage_tape-devices)
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
        r"""Updates a specific tape device.
### Related ONTAP commands
* `storage tape alias-set`
* `storage tape alias-clear`
* `storage tape online`
* `storage tape offline`
* `storage tape position`
### Learn more
* [`DOC /storage/tape-devices`](#docs-storage-storage_tape-devices)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



