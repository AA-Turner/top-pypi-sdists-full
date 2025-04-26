r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageSwitchFans", "StorageSwitchFansSchema"]
__pdoc__ = {
    "StorageSwitchFansSchema.resource": False,
    "StorageSwitchFansSchema.opts": False,
    "StorageSwitchFans": False,
}


class StorageSwitchFansSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitchFans object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Storage switch fan name """

    speed = Size(data_key="speed", allow_none=True)
    r""" Storage switch fan speed """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Storage switch fan state

Valid choices:

* ok
* error """

    @property
    def resource(self):
        return StorageSwitchFans

    gettable_fields = [
        "name",
        "speed",
        "state",
    ]
    """name,speed,state,"""

    patchable_fields = [
        "name",
        "speed",
        "state",
    ]
    """name,speed,state,"""

    postable_fields = [
        "name",
        "speed",
        "state",
    ]
    """name,speed,state,"""


class StorageSwitchFans(Resource):

    _schema = StorageSwitchFansSchema
