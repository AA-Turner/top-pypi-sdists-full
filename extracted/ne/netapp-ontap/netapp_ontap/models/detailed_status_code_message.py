r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["DetailedStatusCodeMessage", "DetailedStatusCodeMessageSchema"]
__pdoc__ = {
    "DetailedStatusCodeMessageSchema.resource": False,
    "DetailedStatusCodeMessageSchema.opts": False,
    "DetailedStatusCodeMessage": False,
}


class DetailedStatusCodeMessageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DetailedStatusCodeMessage object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Code corresponding to the import status failure.


Example: 6684732 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Detailed description of the import status. """

    @property
    def resource(self):
        return DetailedStatusCodeMessage

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DetailedStatusCodeMessage(Resource):

    _schema = DetailedStatusCodeMessageSchema
