r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ContainerVolumesSpaceSnapshot", "ContainerVolumesSpaceSnapshotSchema"]
__pdoc__ = {
    "ContainerVolumesSpaceSnapshotSchema.resource": False,
    "ContainerVolumesSpaceSnapshotSchema.opts": False,
    "ContainerVolumesSpaceSnapshot": False,
}

class ContainerVolumesSpaceSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumesSpaceSnapshot object"""

    reserve_percent = Size(data_key="reserve_percent", allow_none=True)
    r""" The space that has been set aside as a reserve for snapshot usage, in percent. """

    @property
    def resource(self):
        return ContainerVolumesSpaceSnapshot

    gettable_fields = [
        "reserve_percent",
    ]
    """reserve_percent,"""

    patchable_fields = [
        "reserve_percent",
    ]
    """reserve_percent,"""

    postable_fields = [
        "reserve_percent",
    ]
    """reserve_percent,"""


class ContainerVolumesSpaceSnapshot(Resource):

    _schema = ContainerVolumesSpaceSnapshotSchema
