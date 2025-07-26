r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ContainerVolumesS3BucketPolicy", "ContainerVolumesS3BucketPolicySchema"]
__pdoc__ = {
    "ContainerVolumesS3BucketPolicySchema.resource": False,
    "ContainerVolumesS3BucketPolicySchema.opts": False,
    "ContainerVolumesS3BucketPolicy": False,
}


class ContainerVolumesS3BucketPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumesS3BucketPolicy object"""

    statements = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_policy_statement.S3BucketPolicyStatementSchema", unknown=EXCLUDE, allow_none=True), data_key="statements", allow_none=True)
    r""" Specifies the bucket access policy statement. """

    @property
    def resource(self):
        return ContainerVolumesS3BucketPolicy

    gettable_fields = [
        "statements",
    ]
    """statements,"""

    patchable_fields = [
        "statements",
    ]
    """statements,"""

    postable_fields = [
        "statements",
    ]
    """statements,"""


class ContainerVolumesS3BucketPolicy(Resource):

    _schema = ContainerVolumesS3BucketPolicySchema
