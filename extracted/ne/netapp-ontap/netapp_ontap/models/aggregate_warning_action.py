r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateWarningAction", "AggregateWarningActionSchema"]
__pdoc__ = {
    "AggregateWarningActionSchema.resource": False,
    "AggregateWarningActionSchema.opts": False,
    "AggregateWarningAction": False,
}


class AggregateWarningActionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateWarningAction object"""

    arguments = marshmallow_fields.List(marshmallow_fields.Str, data_key="arguments", allow_none=True)
    r""" Arguments present in the specified action message. """

    code = Size(data_key="code", allow_none=True)
    r""" Corrective action code of the specified action. """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Specifies the corrective action to be taken to resolve the issue. """

    @property
    def resource(self):
        return AggregateWarningAction

    gettable_fields = [
        "arguments",
        "code",
        "message",
    ]
    """arguments,code,message,"""

    patchable_fields = [
        "arguments",
        "code",
        "message",
    ]
    """arguments,code,message,"""

    postable_fields = [
        "arguments",
        "code",
        "message",
    ]
    """arguments,code,message,"""


class AggregateWarningAction(Resource):

    _schema = AggregateWarningActionSchema
