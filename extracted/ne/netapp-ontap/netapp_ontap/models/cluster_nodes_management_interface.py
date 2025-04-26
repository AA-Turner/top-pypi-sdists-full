r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesManagementInterface", "ClusterNodesManagementInterfaceSchema"]
__pdoc__ = {
    "ClusterNodesManagementInterfaceSchema.resource": False,
    "ClusterNodesManagementInterfaceSchema.opts": False,
    "ClusterNodesManagementInterface": False,
}


class ClusterNodesManagementInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesManagementInterface object"""

    ip = marshmallow_fields.Nested("netapp_ontap.models.node_setup_ip.NodeSetupIpSchema", unknown=EXCLUDE, data_key="ip", allow_none=True)
    r""" The IP configuration for cluster setup. """

    @property
    def resource(self):
        return ClusterNodesManagementInterface

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "ip",
    ]
    """ip,"""


class ClusterNodesManagementInterface(Resource):

    _schema = ClusterNodesManagementInterfaceSchema
