r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ClusterNodesHaPeering", "ClusterNodesHaPeeringSchema"]
__pdoc__ = {
    "ClusterNodesHaPeeringSchema.resource": False,
    "ClusterNodesHaPeeringSchema.opts": False,
    "ClusterNodesHaPeering": False,
}

class ClusterNodesHaPeeringSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesHaPeering object"""

    dst_peer_node1 = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_peering_dst_peer_node1", "ClusterNodesHaPeeringDstPeerNode1Schema"),
                unknown=EXCLUDE,
                data_key="dst_peer_node1",
                allow_none=True
            )
    r""" The dst_peer_node1 field of the cluster_nodes_ha_peering. """

    dst_peer_node2 = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_peering_dst_peer_node2", "ClusterNodesHaPeeringDstPeerNode2Schema"),
                unknown=EXCLUDE,
                data_key="dst_peer_node2",
                allow_none=True
            )
    r""" The dst_peer_node2 field of the cluster_nodes_ha_peering. """

    dst_peer_node3 = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_peering_dst_peer_node3", "ClusterNodesHaPeeringDstPeerNode3Schema"),
                unknown=EXCLUDE,
                data_key="dst_peer_node3",
                allow_none=True
            )
    r""" The dst_peer_node3 field of the cluster_nodes_ha_peering. """

    ineligible = marshmallow_fields.Boolean(data_key="ineligible", allow_none=True)
    r""" Indicates if the node is ineligible for peering.

Example: true """

    node_protection_level = Size(data_key="node_protection_level", allow_none=True)
    r""" The protection level of the node.

Example: 1 """

    @property
    def resource(self):
        return ClusterNodesHaPeering

    gettable_fields = [
        "dst_peer_node1",
        "dst_peer_node2",
        "dst_peer_node3",
        "ineligible",
        "node_protection_level",
    ]
    """dst_peer_node1,dst_peer_node2,dst_peer_node3,ineligible,node_protection_level,"""

    patchable_fields = [
        "dst_peer_node1",
        "dst_peer_node2",
        "dst_peer_node3",
        "ineligible",
        "node_protection_level",
    ]
    """dst_peer_node1,dst_peer_node2,dst_peer_node3,ineligible,node_protection_level,"""

    postable_fields = [
        "dst_peer_node1",
        "dst_peer_node2",
        "dst_peer_node3",
        "ineligible",
        "node_protection_level",
    ]
    """dst_peer_node1,dst_peer_node2,dst_peer_node3,ineligible,node_protection_level,"""


class ClusterNodesHaPeering(Resource):

    _schema = ClusterNodesHaPeeringSchema
