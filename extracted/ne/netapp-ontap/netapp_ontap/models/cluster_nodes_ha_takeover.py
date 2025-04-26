r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesHaTakeover", "ClusterNodesHaTakeoverSchema"]
__pdoc__ = {
    "ClusterNodesHaTakeoverSchema.resource": False,
    "ClusterNodesHaTakeoverSchema.opts": False,
    "ClusterNodesHaTakeover": False,
}


class ClusterNodesHaTakeoverSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesHaTakeover object"""

    failure = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_ha_takeover_failure.ClusterNodesHaTakeoverFailureSchema", unknown=EXCLUDE, data_key="failure", allow_none=True)
    r""" Indicates the failure code and message. This property is not supported on the ASA r2 platform. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the cluster_nodes_ha_takeover.

Valid choices:

* not_possible
* not_attempted
* in_takeover
* in_progress
* failed """

    @property
    def resource(self):
        return ClusterNodesHaTakeover

    gettable_fields = [
        "failure",
        "state",
    ]
    """failure,state,"""

    patchable_fields = [
        "failure",
        "state",
    ]
    """failure,state,"""

    postable_fields = [
        "failure",
        "state",
    ]
    """failure,state,"""


class ClusterNodesHaTakeover(Resource):

    _schema = ClusterNodesHaTakeoverSchema
