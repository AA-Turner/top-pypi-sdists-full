r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Retrieving storage bridge information
The storage bridge GET API retrieves all of the bridges in the cluster.
<br/>
---
## Examples
### 1) Retrieves a list of bridges from the cluster
#### The following example shows the response with a list of bridges from the cluster:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageBridge

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(StorageBridge.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    StorageBridge({"name": "ATTO_2000001086a18100", "wwn": "2000001086a18100"}),
    StorageBridge({"name": "ATTO_2000001086a18380", "wwn": "2000001086a18380"}),
]

```
</div>
</div>

---
### 2) Retrieves a specific bridge from the cluster
#### The following example shows the response of the requested bridge. If there is no bridge with the requested wwn, an error is returned.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageBridge

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageBridge(wwn="2000001086a18100")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
StorageBridge(
    {
        "last_reboot": {
            "reason": {
                "message": 'Reason: "FirmwareRestart Command".',
                "code": "39321683",
            },
            "time": "2020-12-09T00:47:58-05:00",
        },
        "name": "ATTO_2000001086a18100",
        "fc_ports": [
            {
                "configured_data_rate": 8.0,
                "peer_wwn": "0000000000000000",
                "negotiated_data_rate": 8.0,
                "state": "online",
                "enabled": True,
                "sfp": {
                    "serial_number": "UW106SA",
                    "vendor": "FINISAR CORP.",
                    "part_number": "FTLF8529P3BCV",
                    "data_rate_capability": 16.0,
                },
                "id": 1,
                "data_rate_capability": 16.0,
                "wwn": "2100001086a18100",
            },
            {
                "configured_data_rate": 16.0,
                "peer_wwn": "0000000000000000",
                "negotiated_data_rate": 16.0,
                "state": "online",
                "enabled": True,
                "sfp": {
                    "serial_number": "UW1072B",
                    "vendor": "FINISAR CORP.",
                    "part_number": "FTLF8529P3BCV",
                    "data_rate_capability": 16.0,
                },
                "id": 2,
                "data_rate_capability": 16.0,
                "wwn": "2200001086a18100",
            },
        ],
        "managed_by": "in_band",
        "monitoring_enabled": True,
        "sas_ports": [
            {
                "phy_3": {"state": "online"},
                "negotiated_data_rate": 6.0,
                "state": "online",
                "phy_2": {"state": "online"},
                "enabled": True,
                "phy_4": {"state": "online"},
                "id": 1,
                "data_rate_capability": 12.0,
                "cable": {
                    "serial_number": "618130935",
                    "part_number": "112-00431",
                    "vendor": "Molex Inc.",
                    "technology": "Passive Copper 5m ID:00",
                },
                "wwn": "5001086000a18100",
                "phy_1": {"state": "online"},
            },
            {
                "phy_3": {"state": "offline"},
                "negotiated_data_rate": 0.0,
                "state": "offline",
                "phy_2": {"state": "offline"},
                "enabled": False,
                "phy_4": {"state": "offline"},
                "data_rate_capability": 12.0,
                "wwn": "5001086000a18104",
                "phy_1": {"state": "offline"},
            },
            {
                "phy_3": {"state": "offline"},
                "negotiated_data_rate": 0.0,
                "state": "offline",
                "phy_2": {"state": "offline"},
                "enabled": False,
                "phy_4": {"state": "offline"},
                "data_rate_capability": 12.0,
                "wwn": "5001086000a18108",
                "phy_1": {"state": "offline"},
            },
            {
                "phy_3": {"state": "offline"},
                "negotiated_data_rate": 0.0,
                "state": "offline",
                "phy_2": {"state": "offline"},
                "enabled": False,
                "phy_4": {"state": "offline"},
                "data_rate_capability": 12.0,
                "wwn": "5001086000a1810c",
                "phy_1": {"state": "offline"},
            },
        ],
        "temperature_sensor": {
            "minimum": 0,
            "name": "Chassis Temperature Sensor",
            "maximum": 90,
            "state": "ok",
            "reading": 54,
        },
        "security_enabled": False,
        "firmware_version": "3.10 007A",
        "chassis_throughput_state": "ok",
        "dram_single_bit_error_count": 0,
        "model": "FibreBridge 7500N",
        "power_supply_units": [
            {"name": "A", "state": "ok"},
            {"name": "B", "state": "ok"},
        ],
        "state": "ok",
        "symbolic_name": "RTP-FCSAS02-41KK10",
        "wwn": "2000001086a18100",
        "serial_number": "FB7500N102450",
        "ip_address": "10.226.57.178",
        "vendor": "atto",
        "paths": [
            {
                "target_port": {"wwn": "2100001086a18380"},
                "name": "0e",
                "node": {
                    "name": "sti8080mcc-htp-005",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/ecc3d992-3a86-11eb-9fab-00a0985a6024"
                        }
                    },
                    "uuid": "ecc3d992-3a86-11eb-9fab-00a0985a6024",
                },
            }
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


__all__ = ["StorageBridge", "StorageBridgeSchema"]
__pdoc__ = {
    "StorageBridgeSchema.resource": False,
    "StorageBridgeSchema.opts": False,
}


class StorageBridgeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageBridge object"""

    chassis_throughput_state = marshmallow_fields.Str(
        data_key="chassis_throughput_state",
        validate=enum_validation(['ok', 'warning']),
        allow_none=True,
    )
    r""" Chassis throughput status

Valid choices:

* ok
* warning"""

    dram_single_bit_error_count = Size(
        data_key="dram_single_bit_error_count",
        allow_none=True,
    )
    r""" The dram_single_bit_error_count field of the storage_bridge."""

    errors = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_errors.StorageBridgeErrorsSchema", unknown=EXCLUDE, allow_none=True), data_key="errors", allow_none=True)
    r""" The errors field of the storage_bridge."""

    fc_ports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_fc_ports.StorageBridgeFcPortsSchema", unknown=EXCLUDE, allow_none=True), data_key="fc_ports", allow_none=True)
    r""" The fc_ports field of the storage_bridge."""

    firmware_version = marshmallow_fields.Str(
        data_key="firmware_version",
        allow_none=True,
    )
    r""" Bridge firmware version

Example: 4.10 007A"""

    ip_address = marshmallow_fields.Str(
        data_key="ip_address",
        allow_none=True,
    )
    r""" IP Address"""

    last_reboot = marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_last_reboot.StorageBridgeLastRebootSchema", data_key="last_reboot", unknown=EXCLUDE, allow_none=True)
    r""" The last_reboot field of the storage_bridge."""

    managed_by = marshmallow_fields.Str(
        data_key="managed_by",
        validate=enum_validation(['snmp', 'in_band']),
        allow_none=True,
    )
    r""" The managed_by field of the storage_bridge.

Valid choices:

* snmp
* in_band"""

    model = marshmallow_fields.Str(
        data_key="model",
        allow_none=True,
    )
    r""" Bridge model

Example: FibreBridge6500N"""

    monitoring_enabled = marshmallow_fields.Boolean(
        data_key="monitoring_enabled",
        allow_none=True,
    )
    r""" Indicates whether monitoring is enabled for the bridge."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Bridge name

Example: ATTO_FibreBridge6500N_1"""

    paths = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_paths.StorageBridgePathsSchema", unknown=EXCLUDE, allow_none=True), data_key="paths", allow_none=True)
    r""" The paths field of the storage_bridge."""

    power_supply_units = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_power_supply_units.StorageBridgePowerSupplyUnitsSchema", unknown=EXCLUDE, allow_none=True), data_key="power_supply_units", allow_none=True)
    r""" The power_supply_units field of the storage_bridge."""

    sas_ports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_sas_ports.StorageBridgeSasPortsSchema", unknown=EXCLUDE, allow_none=True), data_key="sas_ports", allow_none=True)
    r""" The sas_ports field of the storage_bridge."""

    security_enabled = marshmallow_fields.Boolean(
        data_key="security_enabled",
        allow_none=True,
    )
    r""" Indicates whether security is enabled for the bridge."""

    serial_number = marshmallow_fields.Str(
        data_key="serial_number",
        allow_none=True,
    )
    r""" Bridge serial number

Example: FB7600N100004"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['unknown', 'ok', 'error']),
        allow_none=True,
    )
    r""" Bridge state

Valid choices:

* unknown
* ok
* error"""

    symbolic_name = marshmallow_fields.Str(
        data_key="symbolic_name",
        allow_none=True,
    )
    r""" Bridge symbolic name

Example: rtp-fcsas03-41kk11"""

    temperature_sensor = marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_temperature_sensor.StorageBridgeTemperatureSensorSchema", data_key="temperature_sensor", unknown=EXCLUDE, allow_none=True)
    r""" The temperature_sensor field of the storage_bridge."""

    vendor = marshmallow_fields.Str(
        data_key="vendor",
        validate=enum_validation(['unknown', 'atto']),
        allow_none=True,
    )
    r""" Bridge vendor

Valid choices:

* unknown
* atto"""

    wwn = marshmallow_fields.Str(
        data_key="wwn",
        allow_none=True,
    )
    r""" Bridge world wide name

Example: 2000001086600476"""

    @property
    def resource(self):
        return StorageBridge

    gettable_fields = [
        "chassis_throughput_state",
        "dram_single_bit_error_count",
        "errors",
        "fc_ports",
        "firmware_version",
        "ip_address",
        "last_reboot",
        "managed_by",
        "model",
        "monitoring_enabled",
        "name",
        "paths",
        "power_supply_units",
        "sas_ports",
        "security_enabled",
        "serial_number",
        "state",
        "symbolic_name",
        "temperature_sensor",
        "vendor",
        "wwn",
    ]
    """chassis_throughput_state,dram_single_bit_error_count,errors,fc_ports,firmware_version,ip_address,last_reboot,managed_by,model,monitoring_enabled,name,paths,power_supply_units,sas_ports,security_enabled,serial_number,state,symbolic_name,temperature_sensor,vendor,wwn,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class StorageBridge(Resource):
    """Allows interaction with StorageBridge objects on the host"""

    _schema = StorageBridgeSchema
    _path = "/api/storage/bridges"
    _keys = ["wwn"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of bridges.
### Related ONTAP commands
* `storage bridge show`
### Learn more
* [`DOC /storage/bridges`](#docs-storage-storage_bridges)
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
        """Returns a count of all StorageBridge resources that match the provided query"""
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
        """Returns a list of RawResources that represent StorageBridge resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of bridges.
### Related ONTAP commands
* `storage bridge show`
### Learn more
* [`DOC /storage/bridges`](#docs-storage-storage_bridges)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific bridge
### Related ONTAP commands
* `storage bridge show`
### Learn more
* [`DOC /storage/bridges`](#docs-storage-storage_bridges)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





