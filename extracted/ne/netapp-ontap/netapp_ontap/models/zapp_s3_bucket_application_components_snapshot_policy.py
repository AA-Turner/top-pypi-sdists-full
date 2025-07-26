r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappS3BucketApplicationComponentsSnapshotPolicy", "ZappS3BucketApplicationComponentsSnapshotPolicySchema"]
__pdoc__ = {
    "ZappS3BucketApplicationComponentsSnapshotPolicySchema.resource": False,
    "ZappS3BucketApplicationComponentsSnapshotPolicySchema.opts": False,
    "ZappS3BucketApplicationComponentsSnapshotPolicy": False,
}


class ZappS3BucketApplicationComponentsSnapshotPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappS3BucketApplicationComponentsSnapshotPolicy object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the snapshot policy that is used for the S3 bucket. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The UUID of the snapshot policy that is used for the S3 bucket. Usage: &lt;UUID&gt; """

    @property
    def resource(self):
        return ZappS3BucketApplicationComponentsSnapshotPolicy

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class ZappS3BucketApplicationComponentsSnapshotPolicy(Resource):

    _schema = ZappS3BucketApplicationComponentsSnapshotPolicySchema
