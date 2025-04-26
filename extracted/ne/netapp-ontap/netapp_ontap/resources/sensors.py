r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

# Overview
You can use this API to retrieve the details of all platform environment sensors
## Examples
### Retrieving values of a single sensor
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Sensors

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Sensors(index="{index}", **{"node.uuid": "{node.uuid}"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Sensors(
    {
        "value_units": "mV",
        "value": 831,
        "critical_high_threshold": 1683,
        "critical_low_threshold": 297,
        "name": "PVCCSA CPU FD",
        "node": {
            "name": "node1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/19ec0b4a-4a4d-11ec-9036-d039ea4a991a"
                }
            },
            "uuid": "19ec0b4a-4a4d-11ec-9036-d039ea4a991a",
        },
        "warning_high_threshold": 1485,
        "_links": {
            "self": {
                "href": "/api/cluster/sensors/19ec0b4a-4a4d-11ec-9036-d039ea4a991a/1"
            }
        },
        "threshold_state": "normal",
        "index": 1,
        "warning_low_threshold": 396,
        "type": "voltage",
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


__all__ = ["Sensors", "SensorsSchema"]
__pdoc__ = {
    "SensorsSchema.resource": False,
    "SensorsSchema.opts": False,
}


class SensorsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Sensors object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the sensors."""

    critical_high_threshold = Size(
        data_key="critical_high_threshold",
        allow_none=True,
    )
    r""" Value above which the sensor goes into a critically high state."""

    critical_low_threshold = Size(
        data_key="critical_low_threshold",
        allow_none=True,
    )
    r""" Value below which the sensor goes into a critically low state."""

    discrete_state = marshmallow_fields.Str(
        data_key="discrete_state",
        validate=enum_validation(['bad', 'crit_high', 'crit_low', 'disabled', 'failed', 'fault', 'ignored', 'init_failed', 'invalid', 'normal', 'not_available', 'not_present', 'retry', 'uninitialized', 'unknown', 'warn_high', 'warn_low']),
        allow_none=True,
    )
    r""" Used to determine whether the sensor is in a normal state or any other failed state based on the value of "discrete_value" field. This field is only applicable for discrete sensors.

Valid choices:

* bad
* crit_high
* crit_low
* disabled
* failed
* fault
* ignored
* init_failed
* invalid
* normal
* not_available
* not_present
* retry
* uninitialized
* unknown
* warn_high
* warn_low"""

    discrete_value = marshmallow_fields.Str(
        data_key="discrete_value",
        allow_none=True,
    )
    r""" Applies to discrete sensors which do not have an integer value. It can have values like on, off, good, bad, ok.

Example: ok"""

    index = Size(
        data_key="index",
        allow_none=True,
    )
    r""" Provides the sensor ID."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the sensor.

Example: PVCCSA CPU FD"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the sensors."""

    threshold_state = marshmallow_fields.Str(
        data_key="threshold_state",
        validate=enum_validation(['bad', 'crit_high', 'crit_low', 'disabled', 'failed', 'fault', 'ignored', 'init_failed', 'invalid', 'normal', 'not_available', 'not_present', 'retry', 'uninitialized', 'unknown', 'warn_high', 'warn_low']),
        allow_none=True,
    )
    r""" Used to determine whether the sensor is in a normal state or any other failed state.

Valid choices:

* bad
* crit_high
* crit_low
* disabled
* failed
* fault
* ignored
* init_failed
* invalid
* normal
* not_available
* not_present
* retry
* uninitialized
* unknown
* warn_high
* warn_low"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['agent', 'battery_life', 'counter', 'current', 'discrete', 'fan', 'fru', 'minutes', 'nvmem', 'percent', 'thermal', 'unknown', 'voltage']),
        allow_none=True,
    )
    r""" Used to determine the type of the sensor.

Valid choices:

* agent
* battery_life
* counter
* current
* discrete
* fan
* fru
* minutes
* nvmem
* percent
* thermal
* unknown
* voltage"""

    value = Size(
        data_key="value",
        allow_none=True,
    )
    r""" Provides the sensor reading.

Example: 831"""

    value_units = marshmallow_fields.Str(
        data_key="value_units",
        allow_none=True,
    )
    r""" Units in which the "value" is measured. Some examples of units are mV, mW*hr, C, RPM.

Example: mV"""

    warning_high_threshold = Size(
        data_key="warning_high_threshold",
        allow_none=True,
    )
    r""" Value above which the sensor goes into a warning high state."""

    warning_low_threshold = Size(
        data_key="warning_low_threshold",
        allow_none=True,
    )
    r""" Value below which the sensor goes into a warning low state."""

    @property
    def resource(self):
        return Sensors

    gettable_fields = [
        "links",
        "critical_high_threshold",
        "critical_low_threshold",
        "discrete_state",
        "discrete_value",
        "index",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "threshold_state",
        "type",
        "value",
        "value_units",
        "warning_high_threshold",
        "warning_low_threshold",
    ]
    """links,critical_high_threshold,critical_low_threshold,discrete_state,discrete_value,index,name,node.links,node.name,node.uuid,threshold_state,type,value,value_units,warning_high_threshold,warning_low_threshold,"""

    patchable_fields = [
        "node.name",
        "node.uuid",
    ]
    """node.name,node.uuid,"""

    postable_fields = [
        "node.name",
        "node.uuid",
    ]
    """node.name,node.uuid,"""

class Sensors(Resource):
    r""" Environment Sensors """

    _schema = SensorsSchema
    _path = "/api/cluster/sensors"
    _keys = ["node.uuid", "index"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves Environment Sensors
### Related ONTAP commands
* `system node environment sensors show`
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
        """Returns a count of all Sensors resources that match the provided query"""
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
        """Returns a list of RawResources that represent Sensors resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves Environment Sensors
### Related ONTAP commands
* `system node environment sensors show`
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieve Environment Sensors
### Learn more
* [`DOC /cluster/sensors/{node.uuid}/{index}`](#docs-cluster-cluster_sensors_{node.uuid}_{index})"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





