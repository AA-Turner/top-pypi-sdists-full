r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IscsiCredentialsChapInbound", "IscsiCredentialsChapInboundSchema"]
__pdoc__ = {
    "IscsiCredentialsChapInboundSchema.resource": False,
    "IscsiCredentialsChapInboundSchema.opts": False,
    "IscsiCredentialsChapInbound": False,
}


class IscsiCredentialsChapInboundSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IscsiCredentialsChapInbound object"""

    password = marshmallow_fields.Str(data_key="password", allow_none=True)
    r""" The inbound CHAP password. Write-only; optional in POST and PATCH. """

    user = marshmallow_fields.Str(data_key="user", allow_none=True)
    r""" The inbound CHAP user name. Optional in POST and PATCH. """

    @property
    def resource(self):
        return IscsiCredentialsChapInbound

    gettable_fields = [
        "user",
    ]
    """user,"""

    patchable_fields = [
        "password",
        "user",
    ]
    """password,user,"""

    postable_fields = [
        "password",
        "user",
    ]
    """password,user,"""


class IscsiCredentialsChapInbound(Resource):

    _schema = IscsiCredentialsChapInboundSchema
