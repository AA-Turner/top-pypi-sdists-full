r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["S3BucketSnapshotRestore", "S3BucketSnapshotRestoreSchema"]
__pdoc__ = {
    "S3BucketSnapshotRestoreSchema.resource": False,
    "S3BucketSnapshotRestoreSchema.opts": False,
    "S3BucketSnapshotRestore": False,
}

class S3BucketSnapshotRestoreSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketSnapshotRestore object"""

    objects_remaining = Size(data_key="objects_remaining", allow_none=True)
    r""" Remaining objects to be restored for the bucket """

    progress = Size(data_key="progress", allow_none=True)
    r""" Snapshot restore progress in percent """

    snapshot = marshmallow_fields.Str(data_key="snapshot", allow_none=True)
    r""" Name of the snapshot being restored for the bucket """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Snapshot restore state of the bucket

Valid choices:

* none
* preparing
* restoring
* done """

    @property
    def resource(self):
        return S3BucketSnapshotRestore

    gettable_fields = [
        "objects_remaining",
        "progress",
        "snapshot",
        "state",
    ]
    """objects_remaining,progress,snapshot,state,"""

    patchable_fields = [
        "objects_remaining",
        "progress",
        "snapshot",
        "state",
    ]
    """objects_remaining,progress,snapshot,state,"""

    postable_fields = [
        "objects_remaining",
        "progress",
        "snapshot",
        "state",
    ]
    """objects_remaining,progress,snapshot,state,"""


class S3BucketSnapshotRestore(Resource):

    _schema = S3BucketSnapshotRestoreSchema
