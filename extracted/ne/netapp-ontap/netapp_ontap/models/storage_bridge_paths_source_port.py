r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageBridgePathsSourcePort", "StorageBridgePathsSourcePortSchema"]
__pdoc__ = {
    "StorageBridgePathsSourcePortSchema.resource": False,
    "StorageBridgePathsSourcePortSchema.opts": False,
    "StorageBridgePathsSourcePort": False,
}


class StorageBridgePathsSourcePortSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageBridgePathsSourcePort object"""

    id = marshmallow_fields.Str(data_key="id", allow_none=True)
    r""" Initiator side switch port id

Example: 100050eb1a238892 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Initiator side switch port name

Example: rtp-fc03-41kk11:1 """

    @property
    def resource(self):
        return StorageBridgePathsSourcePort

    gettable_fields = [
        "id",
        "name",
    ]
    """id,name,"""

    patchable_fields = [
        "id",
        "name",
    ]
    """id,name,"""

    postable_fields = [
        "id",
        "name",
    ]
    """id,name,"""


class StorageBridgePathsSourcePort(Resource):

    _schema = StorageBridgePathsSourcePortSchema
