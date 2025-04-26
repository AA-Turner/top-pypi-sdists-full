r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesHaTakeoverCheck", "ClusterNodesHaTakeoverCheckSchema"]
__pdoc__ = {
    "ClusterNodesHaTakeoverCheckSchema.resource": False,
    "ClusterNodesHaTakeoverCheckSchema.opts": False,
    "ClusterNodesHaTakeoverCheck": False,
}


class ClusterNodesHaTakeoverCheckSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesHaTakeoverCheck object"""

    reasons = marshmallow_fields.List(marshmallow_fields.Str, data_key="reasons", allow_none=True)
    r""" Reasons why the takeover is not possible. """

    takeover_possible = marshmallow_fields.Boolean(data_key="takeover_possible", allow_none=True)
    r""" Indicates whether the takeover is possible. """

    @property
    def resource(self):
        return ClusterNodesHaTakeoverCheck

    gettable_fields = [
        "reasons",
        "takeover_possible",
    ]
    """reasons,takeover_possible,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ClusterNodesHaTakeoverCheck(Resource):

    _schema = ClusterNodesHaTakeoverCheckSchema
