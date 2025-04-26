r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MccipPortL3Config", "MccipPortL3ConfigSchema"]
__pdoc__ = {
    "MccipPortL3ConfigSchema.resource": False,
    "MccipPortL3ConfigSchema.opts": False,
    "MccipPortL3Config": False,
}


class MccipPortL3ConfigSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MccipPortL3Config object"""

    ipv4_interface = marshmallow_fields.Nested("netapp_ontap.models.ip_interface_and_gateway.IpInterfaceAndGatewaySchema", unknown=EXCLUDE, data_key="ipv4_interface", allow_none=True)
    r""" Object to setup an interface along with its default router. """

    @property
    def resource(self):
        return MccipPortL3Config

    gettable_fields = [
        "ipv4_interface",
    ]
    """ipv4_interface,"""

    patchable_fields = [
        "ipv4_interface",
    ]
    """ipv4_interface,"""

    postable_fields = [
        "ipv4_interface",
    ]
    """ipv4_interface,"""


class MccipPortL3Config(Resource):

    _schema = MccipPortL3ConfigSchema
