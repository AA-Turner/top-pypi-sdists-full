r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CapacityPoolNode", "CapacityPoolNodeSchema"]
__pdoc__ = {
    "CapacityPoolNodeSchema.resource": False,
    "CapacityPoolNodeSchema.opts": False,
    "CapacityPoolNode": False,
}


class CapacityPoolNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CapacityPoolNode object"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the capacity_pool_node. """

    used_size = Size(data_key="used_size", allow_none=True)
    r""" Capacity, in bytes, that is currently used by the node. """

    @property
    def resource(self):
        return CapacityPoolNode

    gettable_fields = [
        "node.links",
        "node.name",
        "node.uuid",
        "used_size",
    ]
    """node.links,node.name,node.uuid,used_size,"""

    patchable_fields = [
        "node.name",
        "node.uuid",
    ]
    """node.name,node.uuid,"""

    postable_fields = [
        "node.name",
        "node.uuid",
    ]
    """node.name,node.uuid,"""


class CapacityPoolNode(Resource):

    _schema = CapacityPoolNodeSchema
