r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunMapLunNode", "LunMapLunNodeSchema"]
__pdoc__ = {
    "LunMapLunNodeSchema.resource": False,
    "LunMapLunNodeSchema.opts": False,
    "LunMapLunNode": False,
}


class LunMapLunNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunMapLunNode object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the lun_map_lun_node. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the LUN's node.


Example: node1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the LUN node.


Example: 1cf8aa42-8cd1-12e0-a11c-423468563412 """

    @property
    def resource(self):
        return LunMapLunNode

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class LunMapLunNode(Resource):

    _schema = LunMapLunNodeSchema
