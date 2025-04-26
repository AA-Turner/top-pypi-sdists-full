r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Retrieving storage switch information
The storage switch GET API retrieves all of the switches in the cluster.
<br/>
---
## Examples
### 1) Retrieves a list of storage switches from the cluster
#### The following example shows the response with a list of storage switches in the cluster:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageSwitch

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(StorageSwitch.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    StorageSwitch({"name": "Brocade_10.226.57.206"}),
    StorageSwitch({"name": "Brocade_10.226.57.207"}),
    StorageSwitch({"name": "Brocade_10.226.57.208"}),
    StorageSwitch({"name": "Brocade_10.226.57.209"}),
]

```
</div>
</div>

---
### 2) Retrieves a specific storage switch from the cluster
#### The following example shows the response of the requested storage switch. If there is no storage switch with the requested name, an error is returned.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageSwitch

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageSwitch(name="Brocade_10.226.57.206")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
StorageSwitch(
    {
        "name": "Brocade_10.226.57.206",
        "monitoring_enabled": True,
        "connections": [
            {
                "peer_port": {
                    "connection": "sti8020mcc-htp-006:fcvi_device_1",
                    "unique_id": "38993dc0-4ea1-11eb-9331-00a0985bd455",
                    "wwn": "2100000e1e30ac5f",
                    "type": "fcvi_adapter",
                },
                "source_port": {
                    "mode": "f_port",
                    "name": "FC port 0/0",
                    "wwn": "200050eb1a236efd",
                },
            },
            {
                "peer_port": {
                    "connection": "sti8020mcc-htp-006:2b",
                    "unique_id": "38993dc0-4ea1-11eb-9331-00a0985bd455",
                    "wwn": "21000024ff72c0c9",
                    "type": "fcp_adapter",
                },
                "source_port": {
                    "mode": "f_port",
                    "name": "FC port 0/1",
                    "wwn": "200150eb1a236efd",
                },
            },
            {
                "peer_port": {
                    "connection": "sti8020mcc-htp-006:2d",
                    "unique_id": "38993dc0-4ea1-11eb-9331-00a0985bd455",
                    "wwn": "21000024ff72c0cb",
                    "type": "fcp_adapter",
                },
                "source_port": {
                    "mode": "f_port",
                    "name": "FC port 0/2",
                    "wwn": "200250eb1a236efd",
                },
            },
        ],
        "ports": [
            {
                "name": "FC port 0/0",
                "speed": 16,
                "state": "online",
                "enabled": True,
                "sfp": {
                    "type": "small_form_factor",
                    "transmitter_type": "short_wave_laser",
                    "serial_number": "HAA2140310058E5",
                },
                "mode": "f_port",
                "wwn": "200050eb1a1ef7d7",
            },
            {
                "name": "FC port 0/1",
                "speed": 16,
                "state": "online",
                "enabled": True,
                "sfp": {
                    "type": "small_form_factor",
                    "transmitter_type": "short_wave_laser",
                    "serial_number": "HAA2140310058E5",
                },
                "mode": "f_port",
                "wwn": "200050eb1a1ef2d7",
            },
            {
                "name": "FC port 0/2",
                "speed": 16,
                "state": "online",
                "enabled": True,
                "sfp": {
                    "type": "small_form_factor",
                    "transmitter_type": "short_wave_laser",
                    "serial_number": "HAA2140310058E5",
                },
                "mode": "f_port",
                "wwn": "200050eb1a1ef7d0",
            },
            {
                "name": "FC port 0/3",
                "speed": 16,
                "state": "online",
                "enabled": True,
                "sfp": {
                    "type": "small_form_factor",
                    "transmitter_type": "short_wave_laser",
                    "serial_number": "HAA2140310058E5",
                },
                "mode": "f_port",
                "wwn": "200050eb1a1ef7d7",
            },
            {
                "name": "FC port 0/4",
                "speed": 16,
                "state": "online",
                "enabled": True,
                "sfp": {
                    "type": "small_form_factor",
                    "transmitter_type": "short_wave_laser",
                    "serial_number": "HAA2140310058E5",
                },
                "mode": "f_port",
                "wwn": "200050eb1a1ef2d7",
            },
            {
                "name": "FC port 0/5",
                "speed": 16,
                "state": "online",
                "enabled": True,
                "sfp": {
                    "type": "small_form_factor",
                    "transmitter_type": "short_wave_laser",
                    "serial_number": "HAA2140310058E5",
                },
                "mode": "f_port",
                "wwn": "200050eb1a1ef7d0",
            },
        ],
        "fans": [
            {"name": "FAN #1", "speed": 7336, "state": "ok"},
            {"name": "FAN #2", "speed": 7336, "state": "ok"},
        ],
        "model": "Brocade6510",
        "power_supply_units": [
            {"name": "Power Supply #1", "state": "ok"},
            {"name": "Power Supply #2", "state": "ok"},
        ],
        "state": "ok",
        "role": "subordinate",
        "symbolic_name": "rtp-fc01-41kk11",
        "local": False,
        "wwn": "100050eb1a1ef7d7",
        "ip_address": "10.226.57.206",
        "vendor": "brocade",
        "domain_id": 5,
        "paths": [
            {
                "adapter": {
                    "type": "fcp_initiator",
                    "name": "2a",
                    "wwn": "21000024ff6c4bc0",
                },
                "port": {"name": "FC port 0/4", "speed": 8},
                "node": {
                    "name": "sti8020mcc-htp-005",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/382cb083-4416-11eb-ad1d-00a0985bd455"
                        }
                    },
                    "uuid": "382cb083-4416-11eb-ad1d-00a0985bd455",
                },
            },
            {
                "adapter": {
                    "type": "fcp_initiator",
                    "name": "2c",
                    "wwn": "21000024ff6c4bc2",
                },
                "port": {"name": "FC port 0/5", "speed": 8},
                "node": {
                    "name": "sti8020mcc-htp-005",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/382cb083-4416-11eb-ad1d-00a0985bd455"
                        }
                    },
                    "uuid": "382cb083-4416-11eb-ad1d-00a0985bd455",
                },
            },
            {
                "adapter": {
                    "type": "fc_vi",
                    "name": "fcvi_device_0",
                    "wwn": "2100000e1e09d5d2",
                },
                "port": {"name": "FC port 0/3", "speed": 16},
                "node": {
                    "name": "sti8020mcc-htp-005",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/382cb083-4416-11eb-ad1d-00a0985bd455"
                        }
                    },
                    "uuid": "382cb083-4416-11eb-ad1d-00a0985bd455",
                },
            },
            {
                "adapter": {
                    "type": "fcp_initiator",
                    "name": "2a",
                    "wwn": "21000024ff72c0c8",
                },
                "port": {"name": "FC port 0/1", "speed": 8},
                "node": {
                    "name": "sti8020mcc-htp-006",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/364fbba8-4416-11eb-8e72-00a098431045"
                        }
                    },
                    "uuid": "364fbba8-4416-11eb-8e72-00a098431045",
                },
            },
            {
                "adapter": {
                    "type": "fcp_initiator",
                    "name": "2c",
                    "wwn": "21000024ff72c0ca",
                },
                "port": {"name": "FC port 0/2", "speed": 8},
                "node": {
                    "name": "sti8020mcc-htp-006",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/364fbba8-4416-11eb-8e72-00a098431045"
                        }
                    },
                    "uuid": "364fbba8-4416-11eb-8e72-00a098431045",
                },
            },
        ],
        "temperature_sensors": [
            {"state": "ok", "name": "SLOT #0: TEMP #1", "reading": 52}
        ],
    }
)

```
</div>
</div>

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


__all__ = ["StorageSwitch", "StorageSwitchSchema"]
__pdoc__ = {
    "StorageSwitchSchema.resource": False,
    "StorageSwitchSchema.opts": False,
}


class StorageSwitchSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitch object"""

    connections = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_switch_connections.StorageSwitchConnectionsSchema", unknown=EXCLUDE, allow_none=True), data_key="connections", allow_none=True)
    r""" The connections field of the storage_switch."""

    director_class = marshmallow_fields.Boolean(
        data_key="director_class",
        allow_none=True,
    )
    r""" The director_class field of the storage_switch."""

    domain_id = Size(
        data_key="domain_id",
        allow_none=True,
    )
    r""" Domain ID"""

    errors = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_switch_errors.StorageSwitchErrorsSchema", unknown=EXCLUDE, allow_none=True), data_key="errors", allow_none=True)
    r""" The errors field of the storage_switch."""

    fabric_name = marshmallow_fields.Str(
        data_key="fabric_name",
        allow_none=True,
    )
    r""" Storage switch fabric name"""

    fans = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_switch_fans.StorageSwitchFansSchema", unknown=EXCLUDE, allow_none=True), data_key="fans", allow_none=True)
    r""" The fans field of the storage_switch."""

    firmware_version = marshmallow_fields.Str(
        data_key="firmware_version",
        allow_none=True,
    )
    r""" Storage switch firmware version"""

    ip_address = marshmallow_fields.Str(
        data_key="ip_address",
        allow_none=True,
    )
    r""" IP Address"""

    local = marshmallow_fields.Boolean(
        data_key="local",
        allow_none=True,
    )
    r""" Indicates whether the storage switch is directly connected to the reporting cluster."""

    model = marshmallow_fields.Str(
        data_key="model",
        allow_none=True,
    )
    r""" Storage switch model."""

    monitored_blades = marshmallow_fields.List(Size, data_key="monitored_blades", allow_none=True)
    r""" Indicates the blades that are being monitored for a director-class switch."""

    monitoring_enabled = marshmallow_fields.Boolean(
        data_key="monitoring_enabled",
        allow_none=True,
    )
    r""" Indicates whether monitoring is enabled for the storage switch."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Storage switch name"""

    paths = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_switch_paths.StorageSwitchPathsSchema", unknown=EXCLUDE, allow_none=True), data_key="paths", allow_none=True)
    r""" The paths field of the storage_switch."""

    ports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_switch_ports.StorageSwitchPortsSchema", unknown=EXCLUDE, allow_none=True), data_key="ports", allow_none=True)
    r""" The ports field of the storage_switch."""

    power_supply_units = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_power_supply_units.StorageBridgePowerSupplyUnitsSchema", unknown=EXCLUDE, allow_none=True), data_key="power_supply_units", allow_none=True)
    r""" The power_supply_units field of the storage_switch."""

    role = marshmallow_fields.Str(
        data_key="role",
        validate=enum_validation(['unknown', 'primary', 'subordinate']),
        allow_none=True,
    )
    r""" Storage switch role in fabric.

Valid choices:

* unknown
* primary
* subordinate"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['ok', 'error']),
        allow_none=True,
    )
    r""" Storage switch state

Valid choices:

* ok
* error"""

    symbolic_name = marshmallow_fields.Str(
        data_key="symbolic_name",
        allow_none=True,
    )
    r""" Storage switch symbolic name"""

    temperature_sensors = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_switch_temperature_sensors.StorageSwitchTemperatureSensorsSchema", unknown=EXCLUDE, allow_none=True), data_key="temperature_sensors", allow_none=True)
    r""" The temperature_sensors field of the storage_switch."""

    vendor = marshmallow_fields.Str(
        data_key="vendor",
        validate=enum_validation(['unknown', 'brocade', 'cisco']),
        allow_none=True,
    )
    r""" Storage switch vendor

Valid choices:

* unknown
* brocade
* cisco"""

    vsans = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_switch_vsans.StorageSwitchVsansSchema", unknown=EXCLUDE, allow_none=True), data_key="vsans", allow_none=True)
    r""" The vsans field of the storage_switch."""

    wwn = marshmallow_fields.Str(
        data_key="wwn",
        allow_none=True,
    )
    r""" Storage switch world wide name"""

    zones = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_switch_zones.StorageSwitchZonesSchema", unknown=EXCLUDE, allow_none=True), data_key="zones", allow_none=True)
    r""" The zones field of the storage_switch."""

    @property
    def resource(self):
        return StorageSwitch

    gettable_fields = [
        "connections",
        "director_class",
        "domain_id",
        "errors",
        "fabric_name",
        "fans",
        "firmware_version",
        "ip_address",
        "local",
        "model",
        "monitored_blades",
        "monitoring_enabled",
        "name",
        "paths",
        "ports",
        "power_supply_units",
        "role",
        "state",
        "symbolic_name",
        "temperature_sensors",
        "vendor",
        "vsans",
        "wwn",
        "zones",
    ]
    """connections,director_class,domain_id,errors,fabric_name,fans,firmware_version,ip_address,local,model,monitored_blades,monitoring_enabled,name,paths,ports,power_supply_units,role,state,symbolic_name,temperature_sensors,vendor,vsans,wwn,zones,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class StorageSwitch(Resource):
    r""" The Storage switch object describes the storage switch properties, features and cabling. """

    _schema = StorageSwitchSchema
    _path = "/api/storage/switches"
    _keys = ["name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of storage switches.
### Related ONTAP commands
* `storage switch show`
### Learn more
* [`DOC /storage/switches`](#docs-storage-storage_switches)
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
        """Returns a count of all StorageSwitch resources that match the provided query"""
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
        """Returns a list of RawResources that represent StorageSwitch resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of storage switches.
### Related ONTAP commands
* `storage switch show`
### Learn more
* [`DOC /storage/switches`](#docs-storage-storage_switches)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific storage switch.
### Related ONTAP commands
* `storage switch show`
### Learn more
* [`DOC /storage/switches`](#docs-storage-storage_switches)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





