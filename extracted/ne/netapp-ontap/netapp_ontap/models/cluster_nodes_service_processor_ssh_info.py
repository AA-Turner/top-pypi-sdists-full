r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesServiceProcessorSshInfo", "ClusterNodesServiceProcessorSshInfoSchema"]
__pdoc__ = {
    "ClusterNodesServiceProcessorSshInfoSchema.resource": False,
    "ClusterNodesServiceProcessorSshInfoSchema.opts": False,
    "ClusterNodesServiceProcessorSshInfo": False,
}


class ClusterNodesServiceProcessorSshInfoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesServiceProcessorSshInfo object"""

    allowed_addresses = marshmallow_fields.List(marshmallow_fields.Str, data_key="allowed_addresses", allow_none=True)
    r""" Allowed IP addresses """

    @property
    def resource(self):
        return ClusterNodesServiceProcessorSshInfo

    gettable_fields = [
        "allowed_addresses",
    ]
    """allowed_addresses,"""

    patchable_fields = [
        "allowed_addresses",
    ]
    """allowed_addresses,"""

    postable_fields = [
        "allowed_addresses",
    ]
    """allowed_addresses,"""


class ClusterNodesServiceProcessorSshInfo(Resource):

    _schema = ClusterNodesServiceProcessorSshInfoSchema
