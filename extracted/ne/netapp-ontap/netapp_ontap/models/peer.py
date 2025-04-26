r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Peer", "PeerSchema"]
__pdoc__ = {
    "PeerSchema.resource": False,
    "PeerSchema.opts": False,
    "Peer": False,
}


class PeerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Peer object"""

    cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster_peer.ClusterPeerSchema", unknown=EXCLUDE, data_key="cluster", allow_none=True)
    r""" The cluster field of the peer. """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the peer. """

    @property
    def resource(self):
        return Peer

    gettable_fields = [
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """cluster.links,cluster.name,cluster.uuid,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "cluster.name",
        "cluster.uuid",
        "svm.name",
        "svm.uuid",
    ]
    """cluster.name,cluster.uuid,svm.name,svm.uuid,"""

    postable_fields = [
        "cluster.name",
        "cluster.uuid",
        "svm.name",
        "svm.uuid",
    ]
    """cluster.name,cluster.uuid,svm.name,svm.uuid,"""


class Peer(Resource):

    _schema = PeerSchema
