r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketSnapshotPolicy", "S3BucketSnapshotPolicySchema"]
__pdoc__ = {
    "S3BucketSnapshotPolicySchema.resource": False,
    "S3BucketSnapshotPolicySchema.opts": False,
    "S3BucketSnapshotPolicy": False,
}


class S3BucketSnapshotPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketSnapshotPolicy object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Specifies the name of the snapshot policy.

Example: default-1weekly """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Specifies the unique identifier of the snapshot policy.

Example: 3675af31-431c-12fa-114a-20675afebc12 """

    @property
    def resource(self):
        return S3BucketSnapshotPolicy

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class S3BucketSnapshotPolicy(Resource):

    _schema = S3BucketSnapshotPolicySchema
