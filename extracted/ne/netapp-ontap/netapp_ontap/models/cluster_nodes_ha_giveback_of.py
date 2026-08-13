r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ClusterNodesHaGivebackOf", "ClusterNodesHaGivebackOfSchema"]
__pdoc__ = {
    "ClusterNodesHaGivebackOfSchema.resource": False,
    "ClusterNodesHaGivebackOfSchema.opts": False,
    "ClusterNodesHaGivebackOf": False,
}

class ClusterNodesHaGivebackOfSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesHaGivebackOf object"""

    failure = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.cluster_nodes_ha_giveback_of_failure", "ClusterNodesHaGivebackOfFailureSchema"),
                unknown=EXCLUDE,
                data_key="failure",
                allow_none=True
            )
    r""" Indicates the failure code and message. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the cluster_nodes_ha_giveback_of.

Valid choices:

* nothing_to_giveback
* not_attempted
* in_progress
* failed """

    @property
    def resource(self):
        return ClusterNodesHaGivebackOf

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


class ClusterNodesHaGivebackOf(Resource):

    _schema = ClusterNodesHaGivebackOfSchema
