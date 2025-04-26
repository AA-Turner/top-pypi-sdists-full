r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FpolicyConnectionDisconnectedReason", "FpolicyConnectionDisconnectedReasonSchema"]
__pdoc__ = {
    "FpolicyConnectionDisconnectedReasonSchema.resource": False,
    "FpolicyConnectionDisconnectedReasonSchema.opts": False,
    "FpolicyConnectionDisconnectedReason": False,
}


class FpolicyConnectionDisconnectedReasonSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyConnectionDisconnectedReason object"""

    code = Size(data_key="code", allow_none=True)
    r""" Reason ID for the FPolicy Server disconnection.

Example: 9307 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" FPolicy server reason for disconnection message.

Example: TCP Connection to FPolicy server failed. """

    @property
    def resource(self):
        return FpolicyConnectionDisconnectedReason

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


class FpolicyConnectionDisconnectedReason(Resource):

    _schema = FpolicyConnectionDisconnectedReasonSchema
