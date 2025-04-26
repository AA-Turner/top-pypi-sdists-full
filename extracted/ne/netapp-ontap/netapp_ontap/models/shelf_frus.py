r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ShelfFrus", "ShelfFrusSchema"]
__pdoc__ = {
    "ShelfFrusSchema.resource": False,
    "ShelfFrusSchema.opts": False,
    "ShelfFrus": False,
}


class ShelfFrusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShelfFrus object"""

    firmware_version = marshmallow_fields.Str(data_key="firmware_version", allow_none=True)
    r""" The firmware_version field of the shelf_frus.

Example: 191.0 """

    id = Size(data_key="id", allow_none=True)
    r""" The id field of the shelf_frus. """

    installed = marshmallow_fields.Boolean(data_key="installed", allow_none=True)
    r""" The installed field of the shelf_frus.

Example: true """

    part_number = marshmallow_fields.Str(data_key="part_number", allow_none=True)
    r""" The part_number field of the shelf_frus.

Example: 111-00690+A2 """

    psu = marshmallow_fields.Nested("netapp_ontap.models.shelf_frus_psu.ShelfFrusPsuSchema", unknown=EXCLUDE, data_key="psu", allow_none=True)
    r""" The psu field of the shelf_frus. """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" The serial_number field of the shelf_frus.

Example: 8000166294 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the shelf_frus.

Valid choices:

* ok
* error """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type field of the shelf_frus.

Valid choices:

* module
* psu """

    @property
    def resource(self):
        return ShelfFrus

    gettable_fields = [
        "firmware_version",
        "id",
        "installed",
        "part_number",
        "psu",
        "serial_number",
        "state",
        "type",
    ]
    """firmware_version,id,installed,part_number,psu,serial_number,state,type,"""

    patchable_fields = [
        "firmware_version",
        "id",
        "installed",
        "part_number",
        "psu",
        "serial_number",
        "state",
        "type",
    ]
    """firmware_version,id,installed,part_number,psu,serial_number,state,type,"""

    postable_fields = [
        "firmware_version",
        "id",
        "installed",
        "part_number",
        "psu",
        "serial_number",
        "state",
        "type",
    ]
    """firmware_version,id,installed,part_number,psu,serial_number,state,type,"""


class ShelfFrus(Resource):

    _schema = ShelfFrusSchema
