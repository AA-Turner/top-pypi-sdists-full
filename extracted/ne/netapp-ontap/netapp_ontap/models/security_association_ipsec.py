r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SecurityAssociationIpsec", "SecurityAssociationIpsecSchema"]
__pdoc__ = {
    "SecurityAssociationIpsecSchema.resource": False,
    "SecurityAssociationIpsecSchema.opts": False,
    "SecurityAssociationIpsec": False,
}


class SecurityAssociationIpsecSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityAssociationIpsec object"""

    action = marshmallow_fields.Str(data_key="action", allow_none=True)
    r""" Action for the IPsec security association.

Valid choices:

* bypass
* discard
* esp_transport """

    inbound = marshmallow_fields.Nested("netapp_ontap.models.security_association_ipsec_inbound.SecurityAssociationIpsecInboundSchema", unknown=EXCLUDE, data_key="inbound", allow_none=True)
    r""" Status for inbound parameters for the IPsec security association. """

    outbound = marshmallow_fields.Nested("netapp_ontap.models.security_association_ipsec_outbound.SecurityAssociationIpsecOutboundSchema", unknown=EXCLUDE, data_key="outbound", allow_none=True)
    r""" Status for outbound parameters for the IPsec security association. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" State of the IPsec security association. """

    @property
    def resource(self):
        return SecurityAssociationIpsec

    gettable_fields = [
        "action",
        "inbound",
        "outbound",
        "state",
    ]
    """action,inbound,outbound,state,"""

    patchable_fields = [
        "action",
        "inbound",
        "outbound",
        "state",
    ]
    """action,inbound,outbound,state,"""

    postable_fields = [
        "action",
        "inbound",
        "outbound",
        "state",
    ]
    """action,inbound,outbound,state,"""


class SecurityAssociationIpsec(Resource):

    _schema = SecurityAssociationIpsecSchema
