r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageSwitchPathsPort", "StorageSwitchPathsPortSchema"]
__pdoc__ = {
    "StorageSwitchPathsPortSchema.resource": False,
    "StorageSwitchPathsPortSchema.opts": False,
    "StorageSwitchPathsPort": False,
}


class StorageSwitchPathsPortSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitchPathsPort object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Storage switch port name """

    speed = Size(data_key="speed", allow_none=True)
    r""" Storage switch port speed, in Gbps """

    @property
    def resource(self):
        return StorageSwitchPathsPort

    gettable_fields = [
        "name",
        "speed",
    ]
    """name,speed,"""

    patchable_fields = [
        "name",
        "speed",
    ]
    """name,speed,"""

    postable_fields = [
        "name",
        "speed",
    ]
    """name,speed,"""


class StorageSwitchPathsPort(Resource):

    _schema = StorageSwitchPathsPortSchema
