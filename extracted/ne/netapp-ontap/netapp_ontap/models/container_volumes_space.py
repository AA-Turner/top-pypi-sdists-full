r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


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

    snapshot = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.container_volumes_space_snapshot", "ContainerVolumesSpaceSnapshotSchema"),
                unknown=EXCLUDE,
                data_key="snapshot",
                allow_none=True
            )
    r""" The snapshot field of the container_volumes_space. """

    @property
    def resource(self):
        return ContainerVolumesSpace

    gettable_fields = [
        "size",
        "snapshot",
    ]
    """size,snapshot,"""

    patchable_fields = [
        "size",
        "snapshot",
    ]
    """size,snapshot,"""

    postable_fields = [
        "size",
        "snapshot",
    ]
    """size,snapshot,"""


class ContainerVolumesSpace(Resource):

    _schema = ContainerVolumesSpaceSchema
