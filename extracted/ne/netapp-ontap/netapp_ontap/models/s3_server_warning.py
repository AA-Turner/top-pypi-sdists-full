r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3ServerWarning", "S3ServerWarningSchema"]
__pdoc__ = {
    "S3ServerWarningSchema.resource": False,
    "S3ServerWarningSchema.opts": False,
    "S3ServerWarning": False,
}


class S3ServerWarningSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3ServerWarning object"""

    code = Size(data_key="code", allow_none=True)
    r""" Warning code of the warning encountered. """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Details of the warning sent from the S3 server. """

    @property
    def resource(self):
        return S3ServerWarning

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


class S3ServerWarning(Resource):

    _schema = S3ServerWarningSchema
