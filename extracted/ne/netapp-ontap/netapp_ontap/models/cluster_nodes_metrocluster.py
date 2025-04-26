r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesMetrocluster", "ClusterNodesMetroclusterSchema"]
__pdoc__ = {
    "ClusterNodesMetroclusterSchema.resource": False,
    "ClusterNodesMetroclusterSchema.opts": False,
    "ClusterNodesMetrocluster": False,
}


class ClusterNodesMetroclusterSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesMetrocluster object"""

    custom_vlan_capable = marshmallow_fields.Boolean(data_key="custom_vlan_capable", allow_none=True)
    r""" Indicates whether the MetroCluster over IP platform supports custom VLAN IDs. """

    ports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_metrocluster_ports.ClusterNodesMetroclusterPortsSchema", unknown=EXCLUDE, allow_none=True), data_key="ports", allow_none=True)
    r""" MetroCluster over IP ports. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The Metrocluster configuration type

Valid choices:

* fc
* fc_2_node
* ip """

    @property
    def resource(self):
        return ClusterNodesMetrocluster

    gettable_fields = [
        "custom_vlan_capable",
        "ports",
        "type",
    ]
    """custom_vlan_capable,ports,type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ClusterNodesMetrocluster(Resource):

    _schema = ClusterNodesMetroclusterSchema
