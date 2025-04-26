r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Ipv4Interface", "Ipv4InterfaceSchema"]
__pdoc__ = {
    "Ipv4InterfaceSchema.resource": False,
    "Ipv4InterfaceSchema.opts": False,
    "Ipv4Interface": False,
}


class Ipv4InterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Ipv4Interface object"""

    address = marshmallow_fields.Str(data_key="address", allow_none=True)
    r""" IPv4 address

Example: 10.10.10.7 """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether the IPv4 interfaces is enabled. It expects dhcp_enabled as "true" or values for address, netmask and gateway when set to "true". """

    gateway = marshmallow_fields.Str(data_key="gateway", allow_none=True)
    r""" The IPv4 address of the default router.

Example: 10.1.1.1 """

    netmask = marshmallow_fields.Str(data_key="netmask", allow_none=True)
    r""" Input as IPv4 mask (255.255.0.0). Output is always the netmask length.

Example: 255.255.0.0 """

    setup_state = marshmallow_fields.Str(data_key="setup_state", allow_none=True)
    r""" Indicates the setup state of the interface.

Valid choices:

* not_setup
* succeeded
* in_progress
* failed """

    @property
    def resource(self):
        return Ipv4Interface

    gettable_fields = [
        "address",
        "enabled",
        "gateway",
        "netmask",
        "setup_state",
    ]
    """address,enabled,gateway,netmask,setup_state,"""

    patchable_fields = [
        "address",
        "enabled",
        "gateway",
        "netmask",
    ]
    """address,enabled,gateway,netmask,"""

    postable_fields = [
        "address",
        "enabled",
        "gateway",
        "netmask",
    ]
    """address,enabled,gateway,netmask,"""


class Ipv4Interface(Resource):

    _schema = Ipv4InterfaceSchema
