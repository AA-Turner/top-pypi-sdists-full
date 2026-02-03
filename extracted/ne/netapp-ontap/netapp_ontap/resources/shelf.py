r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Retrieving storage shelf information
The storage shelf GET API retrieves all of the shelves in the cluster.
<br/>
---
## Examples
### 1) Retrieve a list of shelves from the cluster
#### The following example shows the response with a list of shelves in the cluster:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Shelf

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Shelf.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Shelf({"uid": "3109174803597886800"}),
    Shelf({"uid": "9237728366621690448"}),
    Shelf({"uid": "9946762738829886800"}),
    Shelf({"uid": "10318311901725526608"}),
    Shelf({"uid": "13477584846688355664"}),
]

```
</div>
</div>

---
### 2) Retrieve a specific shelf from the cluster
#### The following example shows the response of the requested shelf. If there is no shelf with the requested uid, an error is returned.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Shelf

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Shelf(uid=3109174803597886800)
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Shelf(
    {
        "serial_number": "SHU0954292N0HAH",
        "name": "6.10",
        "id": "10",
        "paths": [
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
            },
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
            },
        ],
        "manufacturer": {"name": "NETAPP"},
        "internal": False,
        "voltage_sensors": [
            {
                "state": "ok",
                "id": 1,
                "location": "rear of the shelf on the upper left power supply",
                "voltage": 5.11,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 2,
                "location": "rear of the shelf on the upper left power supply",
                "voltage": 12.38,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 3,
                "location": "rear of the shelf on the upper right power supply",
                "voltage": 5.11,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 4,
                "location": "rear of the shelf on the upper right power supply",
                "voltage": 12.26,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 5,
                "location": "rear of the shelf on the lower left power supply",
                "voltage": 5.7,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 6,
                "location": "rear of the shelf on the lower left power supply",
                "voltage": 12.26,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 7,
                "location": "rear of the shelf on the lower right power supply",
                "voltage": 5.15,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 8,
                "location": "rear of the shelf on the lower right power supply",
                "voltage": 12.3,
                "installed": True,
            },
        ],
        "acps": [
            {
                "connection_state": "active",
                "channel": "in_band",
                "node": {
                    "name": "cat33-01",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/cf62d23c-6100-11eb-9852-00a098fd725d"
                        }
                    },
                    "uuid": "cf62d23c-6100-11eb-9852-00a098fd725d",
                },
                "enabled": True,
            },
            {
                "connection_state": "active",
                "channel": "in_band",
                "node": {
                    "name": "cat33-02",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/d0892dd7-6100-11eb-9cdb-d039ea010238"
                        }
                    },
                    "uuid": "d0892dd7-6100-11eb-9cdb-d039ea010238",
                },
                "enabled": True,
            },
        ],
        "fans": [
            {
                "state": "ok",
                "rpm": 3150,
                "id": 1,
                "location": "rear of the shelf on the upper left power supply",
                "installed": True,
            },
            {
                "state": "ok",
                "rpm": 3000,
                "id": 2,
                "location": "rear of the shelf on the upper left power supply",
                "installed": True,
            },
            {
                "state": "ok",
                "rpm": 3220,
                "id": 3,
                "location": "rear of the shelf on the upper right power supply",
                "installed": True,
            },
            {
                "state": "ok",
                "rpm": 3000,
                "id": 4,
                "location": "rear of the shelf on the upper right power supply",
                "installed": True,
            },
            {
                "state": "ok",
                "rpm": 3000,
                "id": 5,
                "location": "rear of the shelf on the lower left power supply",
                "installed": True,
            },
            {
                "state": "ok",
                "rpm": 3150,
                "id": 6,
                "location": "rear of the shelf on the lower left power supply",
                "installed": True,
            },
            {
                "state": "ok",
                "rpm": 3150,
                "id": 7,
                "location": "rear of the shelf on the lower right power supply",
                "installed": True,
            },
            {
                "state": "ok",
                "rpm": 3000,
                "id": 8,
                "location": "rear of the shelf on the lower right power supply",
                "installed": True,
            },
        ],
        "location_led": "off",
        "state": "ok",
        "module_type": "iom6",
        "temperature_sensors": [
            {
                "ambient": True,
                "state": "ok",
                "id": 1,
                "threshold": {
                    "high": {"critical": 42, "warning": 40},
                    "low": {"critical": 0, "warning": 5},
                },
                "location": "front of the shelf on the left, on the OPS panel",
                "installed": True,
                "temperature": 20,
            },
            {
                "ambient": False,
                "state": "ok",
                "id": 2,
                "threshold": {
                    "high": {"critical": 55, "warning": 50},
                    "low": {"critical": 5, "warning": 10},
                },
                "location": "inside of the shelf on the midplane",
                "installed": True,
                "temperature": 29,
            },
            {
                "ambient": False,
                "state": "ok",
                "id": 3,
                "threshold": {
                    "high": {"critical": 55, "warning": 50},
                    "low": {"critical": 5, "warning": 10},
                },
                "location": "rear of the shelf on the upper left power supply",
                "installed": True,
                "temperature": 33,
            },
            {
                "ambient": False,
                "state": "ok",
                "id": 4,
                "threshold": {
                    "high": {"critical": 70, "warning": 65},
                    "low": {"critical": 5, "warning": 10},
                },
                "location": "rear of the shelf on the upper left power supply",
                "installed": True,
                "temperature": 41,
            },
            {
                "ambient": False,
                "state": "ok",
                "id": 5,
                "threshold": {
                    "high": {"critical": 55, "warning": 50},
                    "low": {"critical": 5, "warning": 10},
                },
                "location": "rear of the shelf on the upper right power supply",
                "installed": True,
                "temperature": 32,
            },
            {
                "ambient": False,
                "state": "ok",
                "id": 6,
                "threshold": {
                    "high": {"critical": 70, "warning": 65},
                    "low": {"critical": 5, "warning": 10},
                },
                "location": "rear of the shelf on the upper right power supply",
                "installed": True,
                "temperature": 41,
            },
            {
                "ambient": False,
                "state": "ok",
                "id": 7,
                "threshold": {
                    "high": {"critical": 55, "warning": 50},
                    "low": {"critical": 5, "warning": 10},
                },
                "location": "rear of the shelf on the lower left power supply",
                "installed": True,
                "temperature": 34,
            },
            {
                "ambient": False,
                "state": "ok",
                "id": 8,
                "threshold": {
                    "high": {"critical": 70, "warning": 65},
                    "low": {"critical": 5, "warning": 10},
                },
                "location": "rear of the shelf on the lower left power supply",
                "installed": True,
                "temperature": 45,
            },
            {
                "ambient": False,
                "state": "ok",
                "id": 9,
                "threshold": {
                    "high": {"critical": 55, "warning": 50},
                    "low": {"critical": 5, "warning": 10},
                },
                "location": "rear of the shelf on the lower right power supply",
                "installed": True,
                "temperature": 30,
            },
            {
                "ambient": False,
                "state": "ok",
                "id": 10,
                "threshold": {
                    "high": {"critical": 70, "warning": 65},
                    "low": {"critical": 5, "warning": 10},
                },
                "location": "rear of the shelf on the lower right power supply",
                "installed": True,
                "temperature": 40,
            },
            {
                "ambient": False,
                "state": "ok",
                "id": 11,
                "threshold": {
                    "high": {"critical": 60, "warning": 55},
                    "low": {"critical": 5, "warning": 10},
                },
                "location": "rear of the shelf at the top left, on shelf module A",
                "installed": True,
                "temperature": 30,
            },
            {
                "ambient": False,
                "state": "ok",
                "id": 12,
                "threshold": {
                    "high": {"critical": 60, "warning": 55},
                    "low": {"critical": 5, "warning": 10},
                },
                "location": "rear of the shelf at the top right, on shelf module B",
                "installed": True,
                "temperature": 33,
            },
        ],
        "ports": [
            {
                "speed": 100,
                "remote": {"wwn": "5001086000702488", "phy": "08"},
                "state": "connected",
                "module_id": "a",
                "wwn": "500A098000C9EDBF",
                "id": 0,
                "cable": {
                    "part_number": "112-00430+A0",
                    "identifier": "5001086000702488-500a098000c9edbf",
                    "serial_number": "APF16510229807",
                    "length": "2m",
                },
                "internal": False,
                "designator": "square",
            },
            {
                "speed": 100,
                "remote": {"wwn": "500A098000D5C4BF", "phy": "00"},
                "state": "connected",
                "module_id": "a",
                "wwn": "500A098000C9EDBF",
                "id": 1,
                "cable": {
                    "part_number": "112-00176+A0",
                    "identifier": "500a098000d5c4bf-500a098000c9edbf",
                    "serial_number": "APF133917610YT",
                    "length": "0.5-1.0m",
                },
                "internal": False,
                "designator": "circle",
            },
            {
                "speed": 100,
                "remote": {"wwn": "5001086000702648", "phy": "08"},
                "state": "connected",
                "module_id": "b",
                "wwn": "500A098004F208BF",
                "id": 2,
                "cable": {
                    "part_number": "112-00430+A0",
                    "identifier": "5001086000702648-500a098004f208bf",
                    "serial_number": "APF16510229540",
                    "length": "2m",
                },
                "internal": False,
                "designator": "square",
            },
            {
                "speed": 100,
                "remote": {"wwn": "500A0980062BA33F", "phy": "00"},
                "state": "connected",
                "module_id": "b",
                "wwn": "500A098004F208BF",
                "id": 3,
                "cable": {
                    "part_number": "112-00176+20",
                    "identifier": "500a0980062ba33f-500a098004f208bf",
                    "serial_number": "832210017",
                    "length": "0.5-1.0m",
                },
                "internal": False,
                "designator": "circle",
            },
        ],
        "model": "DS4246",
        "uid": "3109174803597886800",
        "local": True,
        "bays": [
            {"has_disk": True, "state": "ok", "id": 0, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 1, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 2, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 3, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 4, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 5, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 6, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 7, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 8, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 9, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 10, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 11, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 12, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 13, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 14, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 15, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 16, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 17, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 18, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 19, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 20, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 21, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 22, "type": "single_disk"},
            {"has_disk": True, "state": "ok", "id": 23, "type": "single_disk"},
        ],
        "disk_count": 24,
        "frus": [
            {
                "serial_number": "8001900099",
                "state": "ok",
                "part_number": "111-00690+B2",
                "firmware_version": "0191",
                "id": 0,
                "installed": True,
                "type": "module",
            },
            {
                "serial_number": "7903785183",
                "state": "ok",
                "part_number": "111-00190+B0",
                "firmware_version": "0191",
                "id": 1,
                "installed": True,
                "type": "module",
            },
            {
                "serial_number": "PMW82562007513E",
                "state": "ok",
                "part_number": "0082562-12",
                "firmware_version": "0311",
                "id": 1,
                "psu": {"model": "9C"},
                "installed": True,
                "type": "psu",
            },
            {
                "serial_number": "PMW825620075138",
                "state": "ok",
                "part_number": "0082562-12",
                "firmware_version": "0311",
                "id": 2,
                "psu": {"model": "9C"},
                "installed": True,
                "type": "psu",
            },
            {
                "serial_number": "PMW8256200750BA",
                "state": "ok",
                "part_number": "0082562-12",
                "firmware_version": "0311",
                "id": 3,
                "psu": {"model": "9C"},
                "installed": True,
                "type": "psu",
            },
            {
                "serial_number": "PMW8256200750A2",
                "state": "ok",
                "part_number": "0082562-12",
                "firmware_version": "0311",
                "id": 4,
                "psu": {"model": "9C"},
                "installed": True,
                "type": "psu",
            },
        ],
        "connection_type": "sas",
        "current_sensors": [
            {
                "state": "ok",
                "id": 1,
                "location": "rear of the shelf on the upper left power supply",
                "current": 6990,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 2,
                "location": "rear of the shelf on the upper left power supply",
                "current": 5150,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 3,
                "location": "rear of the shelf on the upper right power supply",
                "current": 4600,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 4,
                "location": "rear of the shelf on the upper right power supply",
                "current": 4800,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 5,
                "location": "rear of the shelf on the lower left power supply",
                "current": 4140,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 6,
                "location": "rear of the shelf on the lower left power supply",
                "current": 7770,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 7,
                "location": "rear of the shelf on the lower right power supply",
                "current": 4140,
                "installed": True,
            },
            {
                "state": "ok",
                "id": 8,
                "location": "rear of the shelf on the lower right power supply",
                "current": 4720,
                "installed": True,
            },
        ],
    }
)

```
</div>
</div>

---
## Modifying storage shelf
The storage shelf PATCH API modifies the shelf location LED.
---
## Example
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Shelf

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Shelf(uid=3109174803597886800)
    resource.location_led = "on"
    resource.patch()

```

---"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union
from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["Shelf", "ShelfSchema"]
__pdoc__ = {
    "ShelfSchema.resource": False,
    "ShelfSchema.opts": False,
}

class ShelfSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Shelf object"""

    acps = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.shelf_acps", "ShelfAcpsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="acps",
                allow_none=True
            )
    r""" Alternate Control Paths to ACP processors/functions in shelf modules and expanders"""

    bays = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.shelf_bays", "ShelfBaysSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="bays",
                allow_none=True
            )
    r""" The bays field of the shelf."""

    connection_type = marshmallow_fields.Str(
        data_key="connection_type",
        validate=enum_validation(['unknown', 'fc', 'sas', 'nvme']),
        allow_none=True,
    )
    r""" The connection_type field of the shelf.

Valid choices:

* unknown
* fc
* sas
* nvme"""

    current_sensors = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.shelf_current_sensors", "ShelfCurrentSensorsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="current_sensors",
                allow_none=True
            )
    r""" The current_sensors field of the shelf."""

    disk_count = Size(
        data_key="disk_count",
        allow_none=True,
    )
    r""" The disk_count field of the shelf.

Example: 12"""

    drawers = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.shelf_drawers", "ShelfDrawersSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="drawers",
                allow_none=True
            )
    r""" The drawers field of the shelf."""

    errors = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.shelf_errors", "ShelfErrorsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="errors",
                allow_none=True
            )
    r""" The errors field of the shelf."""

    fans = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.shelf_fans", "ShelfFansSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="fans",
                allow_none=True
            )
    r""" The fans field of the shelf."""

    frus = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.shelf_frus", "ShelfFrusSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="frus",
                allow_none=True
            )
    r""" The frus field of the shelf."""

    id = marshmallow_fields.Str(
        data_key="id",
        allow_none=True,
    )
    r""" The id field of the shelf.

Example: 1"""

    internal = marshmallow_fields.Boolean(
        data_key="internal",
        allow_none=True,
    )
    r""" The internal field of the shelf."""

    local = marshmallow_fields.Boolean(
        data_key="local",
        allow_none=True,
    )
    r""" The local field of the shelf."""

    location_led = marshmallow_fields.Str(
        data_key="location_led",
        validate=enum_validation(['off', 'on', 'unsupported']),
        allow_none=True,
    )
    r""" The location_led field of the shelf.

Valid choices:

* off
* on
* unsupported"""

    manufacturer = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.shelf_manufacturer", "ShelfManufacturerSchema"),
                data_key="manufacturer",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The manufacturer field of the shelf."""

    model = marshmallow_fields.Str(
        data_key="model",
        allow_none=True,
    )
    r""" The model field of the shelf.

Example: DS2246"""

    module_type = marshmallow_fields.Str(
        data_key="module_type",
        validate=enum_validation(['unknown', 'iom6', 'iom6e', 'iom12', 'iom12b', 'iom12c', 'iom12e', 'iom12f', 'iom12g', 'nsm100', 'nsm8e', 'nsm16e', 'psm3e', 'nsm100b', 'nsm140']),
        allow_none=True,
    )
    r""" The module_type field of the shelf.

Valid choices:

* unknown
* iom6
* iom6e
* iom12
* iom12b
* iom12c
* iom12e
* iom12f
* iom12g
* nsm100
* nsm8e
* nsm16e
* psm3e
* nsm100b
* nsm140"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name field of the shelf.

Example: 1.1"""

    paths = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.resources.storage_port", "StoragePortSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="paths",
                allow_none=True
            )
    r""" The paths field of the shelf."""

    ports = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.shelf_ports", "ShelfPortsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="ports",
                allow_none=True
            )
    r""" The ports field of the shelf."""

    raw_capacity = Size(
        data_key="raw_capacity",
        allow_none=True,
    )
    r""" Raw capacity of drives in shelf in 4k blocks

Example: 5157308772"""

    serial_number = marshmallow_fields.Str(
        data_key="serial_number",
        allow_none=True,
    )
    r""" The serial_number field of the shelf.

Example: SHFMS1514000895"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['unknown', 'ok', 'error']),
        allow_none=True,
    )
    r""" The state field of the shelf.

Valid choices:

* unknown
* ok
* error"""

    temperature_sensors = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.shelf_temperature_sensors", "ShelfTemperatureSensorsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="temperature_sensors",
                allow_none=True
            )
    r""" The temperature_sensors field of the shelf."""

    uid = marshmallow_fields.Str(
        data_key="uid",
        allow_none=True,
    )
    r""" The uid field of the shelf.

Example: 7777841915827391056"""

    vendor = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.shelf_vendor", "ShelfVendorSchema"),
                data_key="vendor",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The vendor field of the shelf."""

    voltage_sensors = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.shelf_voltage_sensors", "ShelfVoltageSensorsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="voltage_sensors",
                allow_none=True
            )
    r""" The voltage_sensors field of the shelf."""

    @property
    def resource(self):
        return Shelf

    gettable_fields = [
        "acps",
        "bays",
        "connection_type",
        "current_sensors",
        "disk_count",
        "drawers",
        "errors",
        "fans",
        "frus",
        "id",
        "internal",
        "local",
        "location_led",
        "manufacturer",
        "model",
        "module_type",
        "name",
        "paths.links",
        "paths.name",
        "paths.node",
        "ports",
        "raw_capacity",
        "serial_number",
        "state",
        "temperature_sensors",
        "uid",
        "vendor",
        "voltage_sensors",
    ]
    """acps,bays,connection_type,current_sensors,disk_count,drawers,errors,fans,frus,id,internal,local,location_led,manufacturer,model,module_type,name,paths.links,paths.name,paths.node,ports,raw_capacity,serial_number,state,temperature_sensors,uid,vendor,voltage_sensors,"""

    patchable_fields = [
        "location_led",
    ]
    """location_led,"""

    postable_fields = [
    ]
    """"""

class Shelf(Resource):
    """Allows interaction with Shelf objects on the host"""

    _schema = ShelfSchema
    _path = "/api/storage/shelves"
    _keys = ["uid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of shelves.
### Related ONTAP commands
* `storage shelf show`
* `storage shelf port show`
* `storage shelf drawer show`
* `storage shelf drawer show-slot`
* `storage shelf acp show`
### Learn more
* [`DOC /storage/shelves`](#docs-storage-storage_shelves)
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
        """Returns a count of all Shelf resources that match the provided query"""
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
        """Returns a list of RawResources that represent Shelf resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Shelf"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a shelf location LED.
### Related ONTAP commands
* `storage shelf location-led modify`
### Learn more
* [`DOC /storage/shelves`](#docs-storage-storage_shelves)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of shelves.
### Related ONTAP commands
* `storage shelf show`
* `storage shelf port show`
* `storage shelf drawer show`
* `storage shelf drawer show-slot`
* `storage shelf acp show`
### Learn more
* [`DOC /storage/shelves`](#docs-storage-storage_shelves)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific shelf.
### Related ONTAP commands
* `storage shelf show`
* `storage shelf port show`
* `storage shelf drawer show`
* `storage shelf drawer show-slot`
* `storage shelf acp show`
### Learn more
* [`DOC /storage/shelves`](#docs-storage-storage_shelves)
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
        r"""Updates a shelf location LED.
### Related ONTAP commands
* `storage shelf location-led modify`
### Learn more
* [`DOC /storage/shelves`](#docs-storage-storage_shelves)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



