r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["BindingStatus", "BindingStatusSchema"]
__pdoc__ = {
    "BindingStatusSchema.resource": False,
    "BindingStatusSchema.opts": False,
    "BindingStatus": False,
}


class BindingStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the BindingStatus object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Code corresponding to the server's binding status. """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Detailed description of the server's binding status. """

    @property
    def resource(self):
        return BindingStatus

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


class BindingStatus(Resource):

    _schema = BindingStatusSchema
