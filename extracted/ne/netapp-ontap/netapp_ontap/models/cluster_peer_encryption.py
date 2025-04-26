r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterPeerEncryption", "ClusterPeerEncryptionSchema"]
__pdoc__ = {
    "ClusterPeerEncryptionSchema.resource": False,
    "ClusterPeerEncryptionSchema.opts": False,
    "ClusterPeerEncryption": False,
}


class ClusterPeerEncryptionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterPeerEncryption object"""

    proposed = marshmallow_fields.Str(data_key="proposed", allow_none=True)
    r""" The proposed field of the cluster_peer_encryption.

Valid choices:

* none
* tls_psk """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the cluster_peer_encryption.

Valid choices:

* none
* tls_psk """

    @property
    def resource(self):
        return ClusterPeerEncryption

    gettable_fields = [
        "proposed",
        "state",
    ]
    """proposed,state,"""

    patchable_fields = [
        "proposed",
    ]
    """proposed,"""

    postable_fields = [
        "proposed",
    ]
    """proposed,"""


class ClusterPeerEncryption(Resource):

    _schema = ClusterPeerEncryptionSchema
