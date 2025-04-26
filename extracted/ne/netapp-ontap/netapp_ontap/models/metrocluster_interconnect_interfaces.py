r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MetroclusterInterconnectInterfaces", "MetroclusterInterconnectInterfacesSchema"]
__pdoc__ = {
    "MetroclusterInterconnectInterfacesSchema.resource": False,
    "MetroclusterInterconnectInterfacesSchema.opts": False,
    "MetroclusterInterconnectInterfaces": False,
}


class MetroclusterInterconnectInterfacesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterInterconnectInterfaces object"""

    address = marshmallow_fields.Str(data_key="address", allow_none=True)
    r""" IPv4 or IPv6 address

Example: 10.10.10.7 """

    gateway = marshmallow_fields.Str(data_key="gateway", allow_none=True)
    r""" The IPv4 or IPv6 address of the default router.

Example: 10.1.1.1 """

    netmask = marshmallow_fields.Str(data_key="netmask", allow_none=True)
    r""" The netmask field of the metrocluster_interconnect_interfaces. """

    @property
    def resource(self):
        return MetroclusterInterconnectInterfaces

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


class MetroclusterInterconnectInterfaces(Resource):

    _schema = MetroclusterInterconnectInterfacesSchema
