r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Error", "ErrorSchema"]
__pdoc__ = {
    "ErrorSchema.resource": False,
    "ErrorSchema.opts": False,
    "Error": False,
}


class ErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Error object"""

    arguments = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.error_arguments.ErrorArgumentsSchema", unknown=EXCLUDE, allow_none=True), data_key="arguments", allow_none=True)
    r""" Message arguments """

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Error code

Example: 4 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Error message

Example: entry doesn't exist """

    @property
    def resource(self):
        return Error

    gettable_fields = [
        "arguments",
        "code",
        "message",
    ]
    """arguments,code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class Error(Resource):

    _schema = ErrorSchema
