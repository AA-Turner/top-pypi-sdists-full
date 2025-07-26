r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MediatorPingErrorError", "MediatorPingErrorErrorSchema"]
__pdoc__ = {
    "MediatorPingErrorErrorSchema.resource": False,
    "MediatorPingErrorErrorSchema.opts": False,
    "MediatorPingErrorError": False,
}


class MediatorPingErrorErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MediatorPingErrorError object"""

    code = Size(data_key="code", allow_none=True)
    r""" Error code. """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Error message string. """

    @property
    def resource(self):
        return MediatorPingErrorError

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    postable_fields = [
        "code",
        "message",
    ]
    """code,message,"""


class MediatorPingErrorError(Resource):

    _schema = MediatorPingErrorErrorSchema
