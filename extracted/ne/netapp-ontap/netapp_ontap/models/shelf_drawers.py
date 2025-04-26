r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ShelfDrawers", "ShelfDrawersSchema"]
__pdoc__ = {
    "ShelfDrawersSchema.resource": False,
    "ShelfDrawersSchema.opts": False,
    "ShelfDrawers": False,
}


class ShelfDrawersSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShelfDrawers object"""

    closed = marshmallow_fields.Boolean(data_key="closed", allow_none=True)
    r""" The closed field of the shelf_drawers. """

    disk_count = Size(data_key="disk_count", allow_none=True)
    r""" The disk_count field of the shelf_drawers.

Example: 12 """

    error = marshmallow_fields.Str(data_key="error", allow_none=True)
    r""" The error field of the shelf_drawers. """

    id = Size(data_key="id", allow_none=True)
    r""" The id field of the shelf_drawers. """

    part_number = marshmallow_fields.Str(data_key="part_number", allow_none=True)
    r""" The part_number field of the shelf_drawers.

Example: 111-03071 """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" The serial_number field of the shelf_drawers.

Example: 2.1604008263E10 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the shelf_drawers.

Valid choices:

* ok
* error """

    @property
    def resource(self):
        return ShelfDrawers

    gettable_fields = [
        "closed",
        "disk_count",
        "error",
        "id",
        "part_number",
        "serial_number",
        "state",
    ]
    """closed,disk_count,error,id,part_number,serial_number,state,"""

    patchable_fields = [
        "closed",
        "disk_count",
        "error",
        "id",
        "part_number",
        "serial_number",
        "state",
    ]
    """closed,disk_count,error,id,part_number,serial_number,state,"""

    postable_fields = [
        "closed",
        "disk_count",
        "error",
        "id",
        "part_number",
        "serial_number",
        "state",
    ]
    """closed,disk_count,error,id,part_number,serial_number,state,"""


class ShelfDrawers(Resource):

    _schema = ShelfDrawersSchema
