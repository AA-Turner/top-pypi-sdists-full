r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ShelfVoltageSensors", "ShelfVoltageSensorsSchema"]
__pdoc__ = {
    "ShelfVoltageSensorsSchema.resource": False,
    "ShelfVoltageSensorsSchema.opts": False,
    "ShelfVoltageSensors": False,
}


class ShelfVoltageSensorsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShelfVoltageSensors object"""

    id = Size(data_key="id", allow_none=True)
    r""" The id field of the shelf_voltage_sensors.

Example: 1 """

    installed = marshmallow_fields.Boolean(data_key="installed", allow_none=True)
    r""" The installed field of the shelf_voltage_sensors.

Example: true """

    location = marshmallow_fields.Str(data_key="location", allow_none=True)
    r""" The location field of the shelf_voltage_sensors.

Example: rear of the shelf on the lower left power supply """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the shelf_voltage_sensors.

Valid choices:

* ok
* error """

    voltage = marshmallow_fields.Number(data_key="voltage", allow_none=True)
    r""" Voltage, in volts

Example: 12.18 """

    @property
    def resource(self):
        return ShelfVoltageSensors

    gettable_fields = [
        "id",
        "installed",
        "location",
        "state",
        "voltage",
    ]
    """id,installed,location,state,voltage,"""

    patchable_fields = [
        "id",
        "installed",
        "location",
        "state",
        "voltage",
    ]
    """id,installed,location,state,voltage,"""

    postable_fields = [
        "id",
        "installed",
        "location",
        "state",
        "voltage",
    ]
    """id,installed,location,state,voltage,"""


class ShelfVoltageSensors(Resource):

    _schema = ShelfVoltageSensorsSchema
