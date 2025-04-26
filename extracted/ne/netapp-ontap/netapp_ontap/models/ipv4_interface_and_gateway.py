r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Ipv4InterfaceAndGateway", "Ipv4InterfaceAndGatewaySchema"]
__pdoc__ = {
    "Ipv4InterfaceAndGatewaySchema.resource": False,
    "Ipv4InterfaceAndGatewaySchema.opts": False,
    "Ipv4InterfaceAndGateway": False,
}


class Ipv4InterfaceAndGatewaySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Ipv4InterfaceAndGateway object"""

    address = marshmallow_fields.Str(data_key="address", allow_none=True)
    r""" IPv4 address

Example: 10.10.10.7 """

    gateway = marshmallow_fields.Str(data_key="gateway", allow_none=True)
    r""" The IPv4 address of the default router.

Example: 10.1.1.1 """

    netmask = marshmallow_fields.Str(data_key="netmask", allow_none=True)
    r""" Input as IPv4 mask (255.255.0.0). Output is always the netmask length.

Example: 255.255.0.0 """

    @property
    def resource(self):
        return Ipv4InterfaceAndGateway

    gettable_fields = [
        "address",
        "gateway",
        "netmask",
    ]
    """address,gateway,netmask,"""

    patchable_fields = [
        "address",
        "gateway",
        "netmask",
    ]
    """address,gateway,netmask,"""

    postable_fields = [
        "address",
        "gateway",
        "netmask",
    ]
    """address,gateway,netmask,"""


class Ipv4InterfaceAndGateway(Resource):

    _schema = Ipv4InterfaceAndGatewaySchema
