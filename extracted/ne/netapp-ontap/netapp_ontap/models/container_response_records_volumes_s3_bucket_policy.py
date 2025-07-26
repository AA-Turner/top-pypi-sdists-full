r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ContainerResponseRecordsVolumesS3BucketPolicy", "ContainerResponseRecordsVolumesS3BucketPolicySchema"]
__pdoc__ = {
    "ContainerResponseRecordsVolumesS3BucketPolicySchema.resource": False,
    "ContainerResponseRecordsVolumesS3BucketPolicySchema.opts": False,
    "ContainerResponseRecordsVolumesS3BucketPolicy": False,
}


class ContainerResponseRecordsVolumesS3BucketPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerResponseRecordsVolumesS3BucketPolicy object"""

    statements = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.container_volumes_s3_bucket_policy_statements.ContainerVolumesS3BucketPolicyStatementsSchema", unknown=EXCLUDE, allow_none=True), data_key="statements", allow_none=True)
    r""" Specifies the bucket access policy statement. """

    @property
    def resource(self):
        return ContainerResponseRecordsVolumesS3BucketPolicy

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


class ContainerResponseRecordsVolumesS3BucketPolicy(Resource):

    _schema = ContainerResponseRecordsVolumesS3BucketPolicySchema
