r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["DrNode", "DrNodeSchema"]
__pdoc__ = {
    "DrNodeSchema.resource": False,
    "DrNodeSchema.opts": False,
    "DrNode": False,
}


class DrNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DrNode object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the dr_node.

Example: node1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The uuid field of the dr_node.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return DrNode

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DrNode(Resource):

    _schema = DrNodeSchema
