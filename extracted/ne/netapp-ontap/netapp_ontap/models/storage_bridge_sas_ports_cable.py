r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageBridgeSasPortsCable", "StorageBridgeSasPortsCableSchema"]
__pdoc__ = {
    "StorageBridgeSasPortsCableSchema.resource": False,
    "StorageBridgeSasPortsCableSchema.opts": False,
    "StorageBridgeSasPortsCable": False,
}


class StorageBridgeSasPortsCableSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageBridgeSasPortsCable object"""

    part_number = marshmallow_fields.Str(data_key="part_number", allow_none=True)
    r""" Bridge cable part number """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" Bridge cable serial number """

    technology = marshmallow_fields.Str(data_key="technology", allow_none=True)
    r""" Bridge cable type """

    vendor = marshmallow_fields.Str(data_key="vendor", allow_none=True)
    r""" Bridge cable vendor """

    @property
    def resource(self):
        return StorageBridgeSasPortsCable

    gettable_fields = [
        "part_number",
        "serial_number",
        "technology",
        "vendor",
    ]
    """part_number,serial_number,technology,vendor,"""

    patchable_fields = [
        "part_number",
        "serial_number",
        "technology",
        "vendor",
    ]
    """part_number,serial_number,technology,vendor,"""

    postable_fields = [
        "part_number",
        "serial_number",
        "technology",
        "vendor",
    ]
    """part_number,serial_number,technology,vendor,"""


class StorageBridgeSasPortsCable(Resource):

    _schema = StorageBridgeSasPortsCableSchema
