r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SoftwareNode", "SoftwareNodeSchema"]
__pdoc__ = {
    "SoftwareNodeSchema.resource": False,
    "SoftwareNodeSchema.opts": False,
    "SoftwareNode": False,
}


class SoftwareNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwareNode object"""

    firmware = marshmallow_fields.Nested("netapp_ontap.models.firmware.FirmwareSchema", unknown=EXCLUDE, data_key="firmware", allow_none=True)
    r""" The firmware field of the software_node. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the node.

Example: node1 """

    software_images = marshmallow_fields.List(marshmallow_fields.Str, data_key="software_images", allow_none=True)
    r""" The software_images field of the software_node. """

    version = marshmallow_fields.Str(data_key="version", allow_none=True)
    r""" ONTAP version of the node.

Example: ONTAP_X """

    @property
    def resource(self):
        return SoftwareNode

    gettable_fields = [
        "firmware",
        "name",
        "software_images",
        "version",
    ]
    """firmware,name,software_images,version,"""

    patchable_fields = [
        "software_images",
    ]
    """software_images,"""

    postable_fields = [
        "software_images",
    ]
    """software_images,"""


class SoftwareNode(Resource):

    _schema = SoftwareNodeSchema
