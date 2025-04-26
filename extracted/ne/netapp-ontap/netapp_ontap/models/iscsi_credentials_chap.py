r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IscsiCredentialsChap", "IscsiCredentialsChapSchema"]
__pdoc__ = {
    "IscsiCredentialsChapSchema.resource": False,
    "IscsiCredentialsChapSchema.opts": False,
    "IscsiCredentialsChap": False,
}


class IscsiCredentialsChapSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IscsiCredentialsChap object"""

    inbound = marshmallow_fields.Nested("netapp_ontap.models.iscsi_credentials_chap_inbound.IscsiCredentialsChapInboundSchema", unknown=EXCLUDE, data_key="inbound", allow_none=True)
    r""" Inbound CHAP credentials. """

    outbound = marshmallow_fields.Nested("netapp_ontap.models.iscsi_credentials_chap_outbound.IscsiCredentialsChapOutboundSchema", unknown=EXCLUDE, data_key="outbound", allow_none=True)
    r""" Output CHAP credentials.</br>
To clear previously set outbound CHAP credentials, set property `chap.outbound.user` to an empty string in PATCH. """

    @property
    def resource(self):
        return IscsiCredentialsChap

    gettable_fields = [
        "inbound",
        "outbound",
    ]
    """inbound,outbound,"""

    patchable_fields = [
        "inbound",
        "outbound",
    ]
    """inbound,outbound,"""

    postable_fields = [
        "inbound",
        "outbound",
    ]
    """inbound,outbound,"""


class IscsiCredentialsChap(Resource):

    _schema = IscsiCredentialsChapSchema
