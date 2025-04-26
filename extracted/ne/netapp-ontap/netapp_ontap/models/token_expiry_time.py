r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TokenExpiryTime", "TokenExpiryTimeSchema"]
__pdoc__ = {
    "TokenExpiryTimeSchema.resource": False,
    "TokenExpiryTimeSchema.opts": False,
    "TokenExpiryTime": False,
}


class TokenExpiryTimeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TokenExpiryTime object"""

    left = marshmallow_fields.Str(data_key="left", allow_none=True)
    r""" Specifies the time remaining before the given token expires in ISO-8601 format. """

    limit = marshmallow_fields.Str(data_key="limit", allow_none=True)
    r""" Specifies when the given token expires in ISO-8601 format. """

    @property
    def resource(self):
        return TokenExpiryTime

    gettable_fields = [
        "left",
        "limit",
    ]
    """left,limit,"""

    patchable_fields = [
        "limit",
    ]
    """limit,"""

    postable_fields = [
        "limit",
    ]
    """limit,"""


class TokenExpiryTime(Resource):

    _schema = TokenExpiryTimeSchema
