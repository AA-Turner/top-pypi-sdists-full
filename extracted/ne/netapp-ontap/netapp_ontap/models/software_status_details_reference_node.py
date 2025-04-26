r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SoftwareStatusDetailsReferenceNode", "SoftwareStatusDetailsReferenceNodeSchema"]
__pdoc__ = {
    "SoftwareStatusDetailsReferenceNodeSchema.resource": False,
    "SoftwareStatusDetailsReferenceNodeSchema.opts": False,
    "SoftwareStatusDetailsReferenceNode": False,
}


class SoftwareStatusDetailsReferenceNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwareStatusDetailsReferenceNode object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the node to be retrieved for status details.

Example: node1 """

    @property
    def resource(self):
        return SoftwareStatusDetailsReferenceNode

    gettable_fields = [
        "name",
    ]
    """name,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SoftwareStatusDetailsReferenceNode(Resource):

    _schema = SoftwareStatusDetailsReferenceNodeSchema
