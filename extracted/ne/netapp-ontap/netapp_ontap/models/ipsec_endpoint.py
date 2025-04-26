r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IpsecEndpoint", "IpsecEndpointSchema"]
__pdoc__ = {
    "IpsecEndpointSchema.resource": False,
    "IpsecEndpointSchema.opts": False,
    "IpsecEndpoint": False,
}


class IpsecEndpointSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IpsecEndpoint object"""

    address = marshmallow_fields.Str(data_key="address", allow_none=True)
    r""" The address field of the ipsec_endpoint. """

    family = marshmallow_fields.Str(data_key="family", allow_none=True)
    r""" The family field of the ipsec_endpoint. """

    netmask = marshmallow_fields.Str(data_key="netmask", allow_none=True)
    r""" The netmask field of the ipsec_endpoint. """

    port = marshmallow_fields.Str(data_key="port", allow_none=True)
    r""" Application port to be covered by the IPsec policy

Example: 23 """

    @property
    def resource(self):
        return IpsecEndpoint

    gettable_fields = [
        "address",
        "family",
        "netmask",
        "port",
    ]
    """address,family,netmask,port,"""

    patchable_fields = [
        "address",
        "family",
        "netmask",
        "port",
    ]
    """address,family,netmask,port,"""

    postable_fields = [
        "address",
        "family",
        "netmask",
        "port",
    ]
    """address,family,netmask,port,"""


class IpsecEndpoint(Resource):

    _schema = IpsecEndpointSchema
