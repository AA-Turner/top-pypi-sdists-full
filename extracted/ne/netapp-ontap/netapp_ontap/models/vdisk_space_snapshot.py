r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["VdiskSpaceSnapshot", "VdiskSpaceSnapshotSchema"]
__pdoc__ = {
    "VdiskSpaceSnapshotSchema.resource": False,
    "VdiskSpaceSnapshotSchema.opts": False,
    "VdiskSpaceSnapshot": False,
}

class VdiskSpaceSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VdiskSpaceSnapshot object"""

    autodelete = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.vdisk_space_snapshot_autodelete", "VdiskSpaceSnapshotAutodeleteSchema"),
                unknown=EXCLUDE,
                data_key="autodelete",
                allow_none=True
            )
    r""" The autodelete field of the vdisk_space_snapshot. """

    reserve_available = Size(data_key="reserve_available", allow_none=True)
    r""" Size available for snapshots within the snapshot reserve, in bytes. """

    reserve_percent = Size(data_key="reserve_percent", allow_none=True)
    r""" The space that has been reserved for snapshot usage, in percent. """

    reserve_size = Size(data_key="reserve_size", allow_none=True)
    r""" Size that has been reserved for snapshot usage, in bytes. """

    space_used_percent = Size(data_key="space_used_percent", allow_none=True)
    r""" Percentage of snapshot reserve size that has been used. """

    used = Size(data_key="used", allow_none=True)
    r""" The total space used by snapshots, in bytes. """

    @property
    def resource(self):
        return VdiskSpaceSnapshot

    gettable_fields = [
        "autodelete",
        "reserve_available",
        "reserve_percent",
        "reserve_size",
        "space_used_percent",
        "used",
    ]
    """autodelete,reserve_available,reserve_percent,reserve_size,space_used_percent,used,"""

    patchable_fields = [
        "autodelete",
        "reserve_percent",
    ]
    """autodelete,reserve_percent,"""

    postable_fields = [
        "autodelete",
        "reserve_percent",
    ]
    """autodelete,reserve_percent,"""


class VdiskSpaceSnapshot(Resource):

    _schema = VdiskSpaceSnapshotSchema
