r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ShelfFans", "ShelfFansSchema"]
__pdoc__ = {
    "ShelfFansSchema.resource": False,
    "ShelfFansSchema.opts": False,
    "ShelfFans": False,
}


class ShelfFansSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShelfFans object"""

    id = Size(data_key="id", allow_none=True)
    r""" The id field of the shelf_fans.

Example: 1 """

    installed = marshmallow_fields.Boolean(data_key="installed", allow_none=True)
    r""" The installed field of the shelf_fans.

Example: true """

    location = marshmallow_fields.Str(data_key="location", allow_none=True)
    r""" The location field of the shelf_fans.

Example: rear of the shelf on the lower left power supply """

    rpm = Size(data_key="rpm", allow_none=True)
    r""" The rpm field of the shelf_fans.

Example: 3020 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the shelf_fans.

Valid choices:

* ok
* error """

    @property
    def resource(self):
        return ShelfFans

    gettable_fields = [
        "id",
        "installed",
        "location",
        "rpm",
        "state",
    ]
    """id,installed,location,rpm,state,"""

    patchable_fields = [
        "id",
        "installed",
        "location",
        "rpm",
        "state",
    ]
    """id,installed,location,rpm,state,"""

    postable_fields = [
        "id",
        "installed",
        "location",
        "rpm",
        "state",
    ]
    """id,installed,location,rpm,state,"""


class ShelfFans(Resource):

    _schema = ShelfFansSchema
