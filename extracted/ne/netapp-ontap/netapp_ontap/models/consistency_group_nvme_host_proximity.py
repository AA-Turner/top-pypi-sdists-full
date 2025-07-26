r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupNvmeHostProximity", "ConsistencyGroupNvmeHostProximitySchema"]
__pdoc__ = {
    "ConsistencyGroupNvmeHostProximitySchema.resource": False,
    "ConsistencyGroupNvmeHostProximitySchema.opts": False,
    "ConsistencyGroupNvmeHostProximity": False,
}


class ConsistencyGroupNvmeHostProximitySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupNvmeHostProximity object"""

    local_svm = marshmallow_fields.Boolean(data_key="local_svm", allow_none=True)
    r""" A boolean that indicates if the host is proximal to the SVM for which it is configured. """

    peer_svms = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_nvme_host_proximity1_peer_svms.ConsistencyGroupNvmeHostProximity1PeerSvmsSchema", unknown=EXCLUDE, allow_none=True), data_key="peer_svms", allow_none=True)
    r""" An array of remote peer SVMs to which the host is proximal. """

    @property
    def resource(self):
        return ConsistencyGroupNvmeHostProximity

    gettable_fields = [
        "local_svm",
        "peer_svms.links",
        "peer_svms.name",
        "peer_svms.uuid",
    ]
    """local_svm,peer_svms.links,peer_svms.name,peer_svms.uuid,"""

    patchable_fields = [
        "local_svm",
        "peer_svms.name",
        "peer_svms.uuid",
    ]
    """local_svm,peer_svms.name,peer_svms.uuid,"""

    postable_fields = [
        "local_svm",
        "peer_svms.name",
        "peer_svms.uuid",
    ]
    """local_svm,peer_svms.name,peer_svms.uuid,"""


class ConsistencyGroupNvmeHostProximity(Resource):

    _schema = ConsistencyGroupNvmeHostProximitySchema
