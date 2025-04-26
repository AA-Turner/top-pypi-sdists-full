r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapmirrorError", "SnapmirrorErrorSchema"]
__pdoc__ = {
    "SnapmirrorErrorSchema.resource": False,
    "SnapmirrorErrorSchema.opts": False,
    "SnapmirrorError": False,
}


class SnapmirrorErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorError object"""

    arguments = marshmallow_fields.List(marshmallow_fields.Str, data_key="arguments", allow_none=True)
    r""" Arguments present in the error message encountered. """

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Error code """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Error message """

    @property
    def resource(self):
        return SnapmirrorError

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


class SnapmirrorError(Resource):

    _schema = SnapmirrorErrorSchema
