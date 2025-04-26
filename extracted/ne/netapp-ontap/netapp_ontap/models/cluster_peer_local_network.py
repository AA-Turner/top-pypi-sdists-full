r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterPeerLocalNetwork", "ClusterPeerLocalNetworkSchema"]
__pdoc__ = {
    "ClusterPeerLocalNetworkSchema.resource": False,
    "ClusterPeerLocalNetworkSchema.opts": False,
    "ClusterPeerLocalNetwork": False,
}


class ClusterPeerLocalNetworkSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterPeerLocalNetwork object"""

    broadcast_domain = marshmallow_fields.Str(data_key="broadcast_domain", allow_none=True)
    r""" Broadcast domain that is in use within the IPspace.

Example: bd1 """

    gateway = marshmallow_fields.Str(data_key="gateway", allow_none=True)
    r""" The IPv4 or IPv6 address of the default router.

Example: 10.1.1.1 """

    interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cluster_peer_local_network_interfaces.ClusterPeerLocalNetworkInterfacesSchema", unknown=EXCLUDE, allow_none=True), data_key="interfaces", allow_none=True)
    r""" The interfaces field of the cluster_peer_local_network. """

    netmask = marshmallow_fields.Str(data_key="netmask", allow_none=True)
    r""" IPv4 mask or netmask length.

Example: 255.255.0.0 """

    @property
    def resource(self):
        return ClusterPeerLocalNetwork

    gettable_fields = [
        "broadcast_domain",
        "gateway",
        "interfaces",
        "netmask",
    ]
    """broadcast_domain,gateway,interfaces,netmask,"""

    patchable_fields = [
        "broadcast_domain",
        "gateway",
        "interfaces",
        "netmask",
    ]
    """broadcast_domain,gateway,interfaces,netmask,"""

    postable_fields = [
        "broadcast_domain",
        "gateway",
        "interfaces",
        "netmask",
    ]
    """broadcast_domain,gateway,interfaces,netmask,"""


class ClusterPeerLocalNetwork(Resource):

    _schema = ClusterPeerLocalNetworkSchema
