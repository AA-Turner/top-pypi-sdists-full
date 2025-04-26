r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeSpaceSnapshotAutodelete", "VolumeSpaceSnapshotAutodeleteSchema"]
__pdoc__ = {
    "VolumeSpaceSnapshotAutodeleteSchema.resource": False,
    "VolumeSpaceSnapshotAutodeleteSchema.opts": False,
    "VolumeSpaceSnapshotAutodelete": False,
}


class VolumeSpaceSnapshotAutodeleteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeSpaceSnapshotAutodelete object"""

    commitment = marshmallow_fields.Str(data_key="commitment", allow_none=True)
    r""" By default, snapshot autodelete does not delete snapshots locked by Snapmirror, clones of a volume, a LUN, an NVMe namespace, or a file.  Deletion of snapshots locked by these applications is specified using this option. The default value is try.

Valid choices:

* try
* disrupt
* destroy """

    defer_delete = marshmallow_fields.Str(data_key="defer_delete", allow_none=True)
    r""" Allows the user to inform snapshot autodelete to defer the deletion of a specified snapshot until the end. The default value is user_created.

Valid choices:

* scheduled
* user_created
* prefix
* none """

    delete_order = marshmallow_fields.Str(data_key="delete_order", allow_none=True)
    r""" Specifies the order in which snapshot autodelete occurs. Ordering is done using the date and time the snapshot is created. The default value is oldest_first.

Valid choices:

* newest_first
* oldest_first """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether snapshot autodelete is currently enabled on this volume. """

    prefix = marshmallow_fields.Str(data_key="prefix", allow_none=True)
    r""" Specifies the prefix of the snapshot which if matched, is deleted last. Used with autodelete_defer_delete when used with a prefix value. """

    target_free_space = Size(data_key="target_free_space", allow_none=True)
    r""" Snapshots are deleted, one at a time, until the used volume space reaches the value specified. The default is 20% free space or 80% utilized. """

    trigger = marshmallow_fields.Str(data_key="trigger", allow_none=True)
    r""" Specifies when the system should trigger an autodelete of snapshots. When set to _volume_, autodelete is triggered based on volume fullness. When set to _snap_reserve_, autodelete is triggered based on snapshot reserve fullness. The default value is _volume_.

Valid choices:

* volume
* snap_reserve """

    @property
    def resource(self):
        return VolumeSpaceSnapshotAutodelete

    gettable_fields = [
        "commitment",
        "defer_delete",
        "delete_order",
        "prefix",
        "target_free_space",
        "trigger",
    ]
    """commitment,defer_delete,delete_order,prefix,target_free_space,trigger,"""

    patchable_fields = [
        "commitment",
        "defer_delete",
        "delete_order",
        "enabled",
        "prefix",
        "target_free_space",
        "trigger",
    ]
    """commitment,defer_delete,delete_order,enabled,prefix,target_free_space,trigger,"""

    postable_fields = [
    ]
    """"""


class VolumeSpaceSnapshotAutodelete(Resource):

    _schema = VolumeSpaceSnapshotAutodeleteSchema
