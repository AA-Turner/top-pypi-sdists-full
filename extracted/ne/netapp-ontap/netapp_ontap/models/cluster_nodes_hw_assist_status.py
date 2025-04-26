r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesHwAssistStatus", "ClusterNodesHwAssistStatusSchema"]
__pdoc__ = {
    "ClusterNodesHwAssistStatusSchema.resource": False,
    "ClusterNodesHwAssistStatusSchema.opts": False,
    "ClusterNodesHwAssistStatus": False,
}


class ClusterNodesHwAssistStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesHwAssistStatus object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether hardware assist is enabled on the node. """

    local = marshmallow_fields.Nested("netapp_ontap.models.hw_assist_status.HwAssistStatusSchema", unknown=EXCLUDE, data_key="local", allow_none=True)
    r""" The local field of the cluster_nodes_hw_assist_status. """

    partner = marshmallow_fields.Nested("netapp_ontap.models.hw_assist_status.HwAssistStatusSchema", unknown=EXCLUDE, data_key="partner", allow_none=True)
    r""" The partner field of the cluster_nodes_hw_assist_status. """

    @property
    def resource(self):
        return ClusterNodesHwAssistStatus

    gettable_fields = [
        "enabled",
        "local",
        "partner",
    ]
    """enabled,local,partner,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "enabled",
    ]
    """enabled,"""


class ClusterNodesHwAssistStatus(Resource):

    _schema = ClusterNodesHwAssistStatusSchema
