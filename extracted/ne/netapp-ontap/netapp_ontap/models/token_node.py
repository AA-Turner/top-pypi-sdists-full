r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TokenNode", "TokenNodeSchema"]
__pdoc__ = {
    "TokenNodeSchema.resource": False,
    "TokenNodeSchema.opts": False,
    "TokenNode": False,
}


class TokenNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TokenNode object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Node name """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Node UUID """

    @property
    def resource(self):
        return TokenNode

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
        "uuid",
    ]
    """uuid,"""

    postable_fields = [
        "uuid",
    ]
    """uuid,"""


class TokenNode(Resource):

    _schema = TokenNodeSchema
