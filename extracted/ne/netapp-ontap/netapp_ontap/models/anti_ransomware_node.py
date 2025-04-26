r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AntiRansomwareNode", "AntiRansomwareNodeSchema"]
__pdoc__ = {
    "AntiRansomwareNodeSchema.resource": False,
    "AntiRansomwareNodeSchema.opts": False,
    "AntiRansomwareNode": False,
}


class AntiRansomwareNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareNode object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the node.

Example: node1 """

    version = marshmallow_fields.Str(data_key="version", allow_none=True)
    r""" Anti-ransomware version.

Example: 1.0 """

    @property
    def resource(self):
        return AntiRansomwareNode

    gettable_fields = [
        "name",
        "version",
    ]
    """name,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class AntiRansomwareNode(Resource):

    _schema = AntiRansomwareNodeSchema
