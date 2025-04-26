r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageSwitchConnectionsSourcePort", "StorageSwitchConnectionsSourcePortSchema"]
__pdoc__ = {
    "StorageSwitchConnectionsSourcePortSchema.resource": False,
    "StorageSwitchConnectionsSourcePortSchema.opts": False,
    "StorageSwitchConnectionsSourcePort": False,
}


class StorageSwitchConnectionsSourcePortSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitchConnectionsSourcePort object"""

    mode = marshmallow_fields.Str(data_key="mode", allow_none=True)
    r""" Storage switch port operating mode """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Storage switch port name """

    wwn = marshmallow_fields.Str(data_key="wwn", allow_none=True)
    r""" Storage switch peer port world wide name """

    @property
    def resource(self):
        return StorageSwitchConnectionsSourcePort

    gettable_fields = [
        "mode",
        "name",
        "wwn",
    ]
    """mode,name,wwn,"""

    patchable_fields = [
        "mode",
        "name",
        "wwn",
    ]
    """mode,name,wwn,"""

    postable_fields = [
        "mode",
        "name",
        "wwn",
    ]
    """mode,name,wwn,"""


class StorageSwitchConnectionsSourcePort(Resource):

    _schema = StorageSwitchConnectionsSourcePortSchema
