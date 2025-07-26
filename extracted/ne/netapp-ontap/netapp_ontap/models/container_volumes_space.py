r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ContainerVolumesSpace", "ContainerVolumesSpaceSchema"]
__pdoc__ = {
    "ContainerVolumesSpaceSchema.resource": False,
    "ContainerVolumesSpaceSchema.opts": False,
    "ContainerVolumesSpace": False,
}


class ContainerVolumesSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumesSpace object"""

    size = Size(data_key="size", allow_none=True)
    r""" The total provisioned size of the container, in bytes.<br/>


Example: 1073741824 """

    @property
    def resource(self):
        return ContainerVolumesSpace

    gettable_fields = [
        "size",
    ]
    """size,"""

    patchable_fields = [
        "size",
    ]
    """size,"""

    postable_fields = [
        "size",
    ]
    """size,"""


class ContainerVolumesSpace(Resource):

    _schema = ContainerVolumesSpaceSchema
