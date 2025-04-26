r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterPeerStatus", "ClusterPeerStatusSchema"]
__pdoc__ = {
    "ClusterPeerStatusSchema.resource": False,
    "ClusterPeerStatusSchema.opts": False,
    "ClusterPeerStatus": False,
}


class ClusterPeerStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterPeerStatus object"""

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the cluster_peer_status.

Valid choices:

* available
* partial
* unavailable
* pending
* unidentified """

    update_time = ImpreciseDateTime(data_key="update_time", allow_none=True)
    r""" The last time the state was updated.

Example: 2017-01-25T11:20:13.000+0000 """

    @property
    def resource(self):
        return ClusterPeerStatus

    gettable_fields = [
        "state",
        "update_time",
    ]
    """state,update_time,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ClusterPeerStatus(Resource):

    _schema = ClusterPeerStatusSchema
