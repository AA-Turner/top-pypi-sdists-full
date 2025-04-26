r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Ipv6Interface", "Ipv6InterfaceSchema"]
__pdoc__ = {
    "Ipv6InterfaceSchema.resource": False,
    "Ipv6InterfaceSchema.opts": False,
    "Ipv6Interface": False,
}


class Ipv6InterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Ipv6Interface object"""

    address = marshmallow_fields.Str(data_key="address", allow_none=True)
    r""" IPv6 address

Example: fd20:8b1e:b255:5011:10:141:4:97 """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether the IPv6 interfaces is enabled. It expects values for address, netmask and gateway when set to "true". """

    gateway = marshmallow_fields.Str(data_key="gateway", allow_none=True)
    r""" The IPv6 address of the default router.

Example: fd20:8b1e:b255:5011:10::1 """

    is_ipv6_ra_enabled = marshmallow_fields.Boolean(data_key="is_ipv6_ra_enabled", allow_none=True)
    r""" Indicates whether IPv6 RA is enabled. """

    link_local_ip = marshmallow_fields.Str(data_key="link_local_ip", allow_none=True)
    r""" Link local IP address.

Example: FE80::/10 """

    netmask = Size(data_key="netmask", allow_none=True)
    r""" The IPv6 netmask/prefix length. The default value is 64 with a valid range of 1 to 127.

Example: 64 """

    router_ip = marshmallow_fields.Str(data_key="router_ip", allow_none=True)
    r""" Router assigned IP address.

Example: 2001:0db8:85a3:0000:0000:8a2e:0370:7334 """

    setup_state = marshmallow_fields.Str(data_key="setup_state", allow_none=True)
    r""" Indicates the setup state of the interface.

Valid choices:

* not_setup
* succeeded
* in_progress
* failed """

    @property
    def resource(self):
        return Ipv6Interface

    gettable_fields = [
        "address",
        "enabled",
        "gateway",
        "is_ipv6_ra_enabled",
        "link_local_ip",
        "netmask",
        "router_ip",
        "setup_state",
    ]
    """address,enabled,gateway,is_ipv6_ra_enabled,link_local_ip,netmask,router_ip,setup_state,"""

    patchable_fields = [
        "address",
        "enabled",
        "gateway",
        "is_ipv6_ra_enabled",
        "link_local_ip",
        "netmask",
        "router_ip",
    ]
    """address,enabled,gateway,is_ipv6_ra_enabled,link_local_ip,netmask,router_ip,"""

    postable_fields = [
    ]
    """"""


class Ipv6Interface(Resource):

    _schema = Ipv6InterfaceSchema
