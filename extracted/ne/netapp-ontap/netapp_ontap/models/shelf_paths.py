r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ShelfPaths", "ShelfPathsSchema"]
__pdoc__ = {
    "ShelfPathsSchema.resource": False,
    "ShelfPathsSchema.opts": False,
    "ShelfPaths": False,
}


class ShelfPathsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShelfPaths object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the shelf_paths. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the shelf_paths.

Example: 2a """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the shelf_paths. """

    @property
    def resource(self):
        return ShelfPaths

    gettable_fields = [
        "links",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
    ]
    """links,name,node.links,node.name,node.uuid,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class ShelfPaths(Resource):

    _schema = ShelfPathsSchema
