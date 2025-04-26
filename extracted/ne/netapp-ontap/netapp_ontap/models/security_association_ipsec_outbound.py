r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SecurityAssociationIpsecOutbound", "SecurityAssociationIpsecOutboundSchema"]
__pdoc__ = {
    "SecurityAssociationIpsecOutboundSchema.resource": False,
    "SecurityAssociationIpsecOutboundSchema.opts": False,
    "SecurityAssociationIpsecOutbound": False,
}


class SecurityAssociationIpsecOutboundSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityAssociationIpsecOutbound object"""

    bytes = Size(data_key="bytes", allow_none=True)
    r""" Number of outbound bytes for the IPsec security association. """

    offload_bytes = Size(data_key="offload_bytes", allow_none=True)
    r""" Number of outbound bytes processed by offload for the IPsec security association. """

    offload_packets = Size(data_key="offload_packets", allow_none=True)
    r""" Number of outbound packets processed by offload for the IPsec security association. """

    packets = Size(data_key="packets", allow_none=True)
    r""" Number of outbound packets for the IPsec security association. """

    security_parameter_index = marshmallow_fields.Str(data_key="security_parameter_index", allow_none=True)
    r""" Outbound security parameter index for the IPSec security association. """

    @property
    def resource(self):
        return SecurityAssociationIpsecOutbound

    gettable_fields = [
        "bytes",
        "offload_bytes",
        "offload_packets",
        "packets",
        "security_parameter_index",
    ]
    """bytes,offload_bytes,offload_packets,packets,security_parameter_index,"""

    patchable_fields = [
        "bytes",
        "offload_bytes",
        "offload_packets",
        "packets",
        "security_parameter_index",
    ]
    """bytes,offload_bytes,offload_packets,packets,security_parameter_index,"""

    postable_fields = [
        "bytes",
        "offload_bytes",
        "offload_packets",
        "packets",
        "security_parameter_index",
    ]
    """bytes,offload_bytes,offload_packets,packets,security_parameter_index,"""


class SecurityAssociationIpsecOutbound(Resource):

    _schema = SecurityAssociationIpsecOutboundSchema
