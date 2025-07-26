r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ContainerVolumeS3BucketPolicy", "ContainerVolumeS3BucketPolicySchema"]
__pdoc__ = {
    "ContainerVolumeS3BucketPolicySchema.resource": False,
    "ContainerVolumeS3BucketPolicySchema.opts": False,
    "ContainerVolumeS3BucketPolicy": False,
}


class ContainerVolumeS3BucketPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumeS3BucketPolicy object"""

    statements = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.container_response_records_volumes_s3_bucket_policy_statements.ContainerResponseRecordsVolumesS3BucketPolicyStatementsSchema", unknown=EXCLUDE, allow_none=True), data_key="statements", allow_none=True)
    r""" Specifies the bucket access policy statement. """

    @property
    def resource(self):
        return ContainerVolumeS3BucketPolicy

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


class ContainerVolumeS3BucketPolicy(Resource):

    _schema = ContainerVolumeS3BucketPolicySchema
