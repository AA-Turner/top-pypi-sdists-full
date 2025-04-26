r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageBridgePaths", "StorageBridgePathsSchema"]
__pdoc__ = {
    "StorageBridgePathsSchema.resource": False,
    "StorageBridgePathsSchema.opts": False,
    "StorageBridgePaths": False,
}


class StorageBridgePathsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageBridgePaths object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the storage_bridge_paths.

Example: 2c """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the storage_bridge_paths. """

    source_port = marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_paths_source_port.StorageBridgePathsSourcePortSchema", unknown=EXCLUDE, data_key="source_port", allow_none=True)
    r""" The source_port field of the storage_bridge_paths. """

    target_port = marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_paths_target_port.StorageBridgePathsTargetPortSchema", unknown=EXCLUDE, data_key="target_port", allow_none=True)
    r""" The target_port field of the storage_bridge_paths. """

    @property
    def resource(self):
        return StorageBridgePaths

    gettable_fields = [
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "source_port",
        "target_port",
    ]
    """name,node.links,node.name,node.uuid,source_port,target_port,"""

    patchable_fields = [
        "name",
        "node.name",
        "node.uuid",
        "source_port",
        "target_port",
    ]
    """name,node.name,node.uuid,source_port,target_port,"""

    postable_fields = [
        "name",
        "node.name",
        "node.uuid",
        "source_port",
        "target_port",
    ]
    """name,node.name,node.uuid,source_port,target_port,"""


class StorageBridgePaths(Resource):

    _schema = StorageBridgePathsSchema
