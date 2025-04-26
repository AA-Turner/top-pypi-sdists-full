r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NodeUuid", "NodeUuidSchema"]
__pdoc__ = {
    "NodeUuidSchema.resource": False,
    "NodeUuidSchema.opts": False,
    "NodeUuid": False,
}


class NodeUuidSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NodeUuid object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the node_uuid. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The uuid field of the node_uuid.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NodeUuid

    gettable_fields = [
        "links",
        "uuid",
    ]
    """links,uuid,"""

    patchable_fields = [
        "uuid",
    ]
    """uuid,"""

    postable_fields = [
        "uuid",
    ]
    """uuid,"""


class NodeUuid(Resource):

    _schema = NodeUuidSchema
