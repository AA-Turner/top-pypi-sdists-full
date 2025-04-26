r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageSwitchTemperatureSensors", "StorageSwitchTemperatureSensorsSchema"]
__pdoc__ = {
    "StorageSwitchTemperatureSensorsSchema.resource": False,
    "StorageSwitchTemperatureSensorsSchema.opts": False,
    "StorageSwitchTemperatureSensors": False,
}


class StorageSwitchTemperatureSensorsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitchTemperatureSensors object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Temperature sensor name """

    reading = Size(data_key="reading", allow_none=True)
    r""" Temperature sensor reading, in degrees celsius. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Temperature sensor state

Valid choices:

* error
* ok """

    @property
    def resource(self):
        return StorageSwitchTemperatureSensors

    gettable_fields = [
        "name",
        "reading",
        "state",
    ]
    """name,reading,state,"""

    patchable_fields = [
        "name",
        "reading",
        "state",
    ]
    """name,reading,state,"""

    postable_fields = [
        "name",
        "reading",
        "state",
    ]
    """name,reading,state,"""


class StorageSwitchTemperatureSensors(Resource):

    _schema = StorageSwitchTemperatureSensorsSchema
