r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesExternalCacheBypass", "ClusterNodesExternalCacheBypassSchema"]
__pdoc__ = {
    "ClusterNodesExternalCacheBypassSchema.resource": False,
    "ClusterNodesExternalCacheBypassSchema.opts": False,
    "ClusterNodesExternalCacheBypass": False,
}


class ClusterNodesExternalCacheBypassSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesExternalCacheBypass object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether external cache bypass is enabled.

Example: true """

    large_read_ops_allow_percent = Size(data_key="large_read_ops_allow_percent", allow_none=True)
    r""" External cache bypass allowed operations percentage for large reads.

Example: 100 """

    reset = marshmallow_fields.Boolean(data_key="reset", allow_none=True)
    r""" Initiates an external cache bypass threshold reset action.

Example: true """

    @property
    def resource(self):
        return ClusterNodesExternalCacheBypass

    gettable_fields = [
        "enabled",
        "large_read_ops_allow_percent",
    ]
    """enabled,large_read_ops_allow_percent,"""

    patchable_fields = [
        "enabled",
        "large_read_ops_allow_percent",
        "reset",
    ]
    """enabled,large_read_ops_allow_percent,reset,"""

    postable_fields = [
        "enabled",
        "large_read_ops_allow_percent",
    ]
    """enabled,large_read_ops_allow_percent,"""


class ClusterNodesExternalCacheBypass(Resource):

    _schema = ClusterNodesExternalCacheBypassSchema
