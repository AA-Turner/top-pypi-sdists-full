r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeHostProximity", "NvmeHostProximitySchema"]
__pdoc__ = {
    "NvmeHostProximitySchema.resource": False,
    "NvmeHostProximitySchema.opts": False,
    "NvmeHostProximity": False,
}


class NvmeHostProximitySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeHostProximity object"""

    local_svm = marshmallow_fields.Boolean(data_key="local_svm", allow_none=True)
    r""" A boolean that indicates if the host is proximal to the SVM for which it is configured. """

    peer_svms = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_initiator_no_records_proximity_peer_svms.IgroupInitiatorNoRecordsProximityPeerSvmsSchema", unknown=EXCLUDE, allow_none=True), data_key="peer_svms", allow_none=True)
    r""" An array of remote peer SVMs to which the host is proximal. """

    @property
    def resource(self):
        return NvmeHostProximity

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


class NvmeHostProximity(Resource):

    _schema = NvmeHostProximitySchema
