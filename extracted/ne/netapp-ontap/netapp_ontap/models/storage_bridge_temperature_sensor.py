r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageBridgeTemperatureSensor", "StorageBridgeTemperatureSensorSchema"]
__pdoc__ = {
    "StorageBridgeTemperatureSensorSchema.resource": False,
    "StorageBridgeTemperatureSensorSchema.opts": False,
    "StorageBridgeTemperatureSensor": False,
}


class StorageBridgeTemperatureSensorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageBridgeTemperatureSensor object"""

    maximum = Size(data_key="maximum", allow_none=True)
    r""" Maximum safe operating temperature, in degrees Celsius. """

    minimum = Size(data_key="minimum", allow_none=True)
    r""" Minimum safe operating temperature, in degrees Celsius. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Temperature sensor name

Example: Chassis temperature sensor """

    reading = Size(data_key="reading", allow_none=True)
    r""" Chassis temperature sensor reading, in degrees Celsius. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the storage_bridge_temperature_sensor.

Valid choices:

* ok
* warning
* error """

    @property
    def resource(self):
        return StorageBridgeTemperatureSensor

    gettable_fields = [
        "maximum",
        "minimum",
        "name",
        "reading",
        "state",
    ]
    """maximum,minimum,name,reading,state,"""

    patchable_fields = [
        "maximum",
        "minimum",
        "name",
        "reading",
        "state",
    ]
    """maximum,minimum,name,reading,state,"""

    postable_fields = [
        "maximum",
        "minimum",
        "name",
        "reading",
        "state",
    ]
    """maximum,minimum,name,reading,state,"""


class StorageBridgeTemperatureSensor(Resource):

    _schema = StorageBridgeTemperatureSensorSchema
