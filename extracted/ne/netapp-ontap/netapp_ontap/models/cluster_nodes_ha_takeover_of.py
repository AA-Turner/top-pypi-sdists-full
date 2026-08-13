r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ClusterNodesHaTakeoverOf", "ClusterNodesHaTakeoverOfSchema"]
__pdoc__ = {
    "ClusterNodesHaTakeoverOfSchema.resource": False,
    "ClusterNodesHaTakeoverOfSchema.opts": False,
    "ClusterNodesHaTakeoverOf": False,
}

class ClusterNodesHaTakeoverOfSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesHaTakeoverOf object"""

    failure = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_takeover_of_failure", "ClusterNodesHaTakeoverOfFailureSchema"),
                unknown=EXCLUDE,
                data_key="failure",
                allow_none=True
            )
    r""" Indicates the failure code and message. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the cluster_nodes_ha_takeover_of.

Valid choices:

* not_possible
* not_attempted
* taken_over
* in_progress
* failed """

    @property
    def resource(self):
        return ClusterNodesHaTakeoverOf

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


class ClusterNodesHaTakeoverOf(Resource):

    _schema = ClusterNodesHaTakeoverOfSchema
