r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeSpaceSnapshot", "VolumeSpaceSnapshotSchema"]
__pdoc__ = {
    "VolumeSpaceSnapshotSchema.resource": False,
    "VolumeSpaceSnapshotSchema.opts": False,
    "VolumeSpaceSnapshot": False,
}


class VolumeSpaceSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeSpaceSnapshot object"""

    autodelete = marshmallow_fields.Nested("netapp_ontap.models.volume_space_snapshot_autodelete.VolumeSpaceSnapshotAutodeleteSchema", unknown=EXCLUDE, data_key="autodelete", allow_none=True)
    r""" The autodelete field of the volume_space_snapshot. """

    autodelete_enabled = marshmallow_fields.Boolean(data_key="autodelete_enabled", allow_none=True)
    r""" Specifies whether snapshot autodelete is currently enabled on this volume. This field will no longer be supported in a future release. Use autodelete.enabled instead. """

    autodelete_trigger = marshmallow_fields.Str(data_key="autodelete_trigger", allow_none=True)
    r""" Specifies when the system should trigger an autodelete of snapshots. When set to _volume_, autodelete is triggered based on volume fullness. When set to _snap_reserve_, autodelete is triggered based on snapshot reserve fullness. The default value is _volume_. This field will no longer be supported in a future release. Use autodelete.trigger instead.

Valid choices:

* volume
* snap_reserve """

    reserve_available = Size(data_key="reserve_available", allow_none=True)
    r""" Size available for snapshots within the snapshot reserve, in bytes. """

    reserve_percent = Size(data_key="reserve_percent", allow_none=True)
    r""" The space that has been set aside as a reserve for snapshot usage, in percent. """

    reserve_size = Size(data_key="reserve_size", allow_none=True)
    r""" Size in the volume that has been set aside as a reserve for snapshot usage, in bytes. """

    space_used_percent = Size(data_key="space_used_percent", allow_none=True)
    r""" Percentage of snapshot reserve size that has been used. """

    used = Size(data_key="used", allow_none=True)
    r""" The total space used by snapshots in the volume, in bytes. """

    @property
    def resource(self):
        return VolumeSpaceSnapshot

    gettable_fields = [
        "autodelete",
        "autodelete_trigger",
        "reserve_available",
        "reserve_percent",
        "reserve_size",
        "space_used_percent",
        "used",
    ]
    """autodelete,autodelete_trigger,reserve_available,reserve_percent,reserve_size,space_used_percent,used,"""

    patchable_fields = [
        "autodelete",
        "autodelete_enabled",
        "autodelete_trigger",
        "reserve_percent",
    ]
    """autodelete,autodelete_enabled,autodelete_trigger,reserve_percent,"""

    postable_fields = [
        "autodelete",
        "reserve_percent",
    ]
    """autodelete,reserve_percent,"""


class VolumeSpaceSnapshot(Resource):

    _schema = VolumeSpaceSnapshotSchema
