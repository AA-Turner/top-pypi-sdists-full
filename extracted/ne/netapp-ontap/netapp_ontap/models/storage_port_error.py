r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StoragePortError", "StoragePortErrorSchema"]
__pdoc__ = {
    "StoragePortErrorSchema.resource": False,
    "StoragePortErrorSchema.opts": False,
    "StoragePortError": False,
}


class StoragePortErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StoragePortError object"""

    corrective_action = marshmallow_fields.Str(data_key="corrective_action", allow_none=True)
    r""" Error corrective action """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Error message """

    @property
    def resource(self):
        return StoragePortError

    gettable_fields = [
        "corrective_action",
        "message",
    ]
    """corrective_action,message,"""

    patchable_fields = [
        "corrective_action",
        "message",
    ]
    """corrective_action,message,"""

    postable_fields = [
        "corrective_action",
        "message",
    ]
    """corrective_action,message,"""


class StoragePortError(Resource):

    _schema = StoragePortErrorSchema
