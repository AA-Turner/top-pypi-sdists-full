r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterManagementInterface", "ClusterManagementInterfaceSchema"]
__pdoc__ = {
    "ClusterManagementInterfaceSchema.resource": False,
    "ClusterManagementInterfaceSchema.opts": False,
    "ClusterManagementInterface": False,
}


class ClusterManagementInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterManagementInterface object"""

    ip = marshmallow_fields.Nested("netapp_ontap.models.ip_interface_and_gateway.IpInterfaceAndGatewaySchema", unknown=EXCLUDE, data_key="ip", allow_none=True)
    r""" Object to setup an interface along with its default router. """

    @property
    def resource(self):
        return ClusterManagementInterface

    gettable_fields = [
        "ip",
    ]
    """ip,"""

    patchable_fields = [
        "ip",
    ]
    """ip,"""

    postable_fields = [
        "ip",
    ]
    """ip,"""


class ClusterManagementInterface(Resource):

    _schema = ClusterManagementInterfaceSchema
