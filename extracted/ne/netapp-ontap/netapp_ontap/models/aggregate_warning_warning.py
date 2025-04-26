r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateWarningWarning", "AggregateWarningWarningSchema"]
__pdoc__ = {
    "AggregateWarningWarningSchema.resource": False,
    "AggregateWarningWarningSchema.opts": False,
    "AggregateWarningWarning": False,
}


class AggregateWarningWarningSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateWarningWarning object"""

    arguments = marshmallow_fields.List(marshmallow_fields.Str, data_key="arguments", allow_none=True)
    r""" Arguments present in the warning message encountered. """

    code = Size(data_key="code", allow_none=True)
    r""" Warning code of the warning encountered. """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Details of the warning encountered by the aggregate simulate query. """

    @property
    def resource(self):
        return AggregateWarningWarning

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


class AggregateWarningWarning(Resource):

    _schema = AggregateWarningWarningSchema
