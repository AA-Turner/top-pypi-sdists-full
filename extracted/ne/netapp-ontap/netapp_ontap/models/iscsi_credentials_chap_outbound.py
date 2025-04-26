r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IscsiCredentialsChapOutbound", "IscsiCredentialsChapOutboundSchema"]
__pdoc__ = {
    "IscsiCredentialsChapOutboundSchema.resource": False,
    "IscsiCredentialsChapOutboundSchema.opts": False,
    "IscsiCredentialsChapOutbound": False,
}


class IscsiCredentialsChapOutboundSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IscsiCredentialsChapOutbound object"""

    password = marshmallow_fields.Str(data_key="password", allow_none=True)
    r""" The outbound CHAP password. Write-only; optional in POST and PATCH. """

    user = marshmallow_fields.Str(data_key="user", allow_none=True)
    r""" The outbound CHAP user name. Optional in POST and PATCH.</br>
To clear previously set outbound CHAP credentials, set this property to an empty string in PATCH. """

    @property
    def resource(self):
        return IscsiCredentialsChapOutbound

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


class IscsiCredentialsChapOutbound(Resource):

    _schema = IscsiCredentialsChapOutboundSchema
