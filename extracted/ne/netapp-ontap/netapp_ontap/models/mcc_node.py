r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MccNode", "MccNodeSchema"]
__pdoc__ = {
    "MccNodeSchema.resource": False,
    "MccNodeSchema.opts": False,
    "MccNode": False,
}


class MccNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MccNode object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the mcc_node. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the mcc_node.

Example: node1 """

    system_id = marshmallow_fields.Str(data_key="system_id", allow_none=True)
    r""" The system_id field of the mcc_node. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The uuid field of the mcc_node.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return MccNode

    gettable_fields = [
        "links",
        "name",
        "system_id",
        "uuid",
    ]
    """links,name,system_id,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class MccNode(Resource):

    _schema = MccNodeSchema
