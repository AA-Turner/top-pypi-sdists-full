r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ContainerResponseRecordsVolumesS3BucketPolicyStatements", "ContainerResponseRecordsVolumesS3BucketPolicyStatementsSchema"]
__pdoc__ = {
    "ContainerResponseRecordsVolumesS3BucketPolicyStatementsSchema.resource": False,
    "ContainerResponseRecordsVolumesS3BucketPolicyStatementsSchema.opts": False,
    "ContainerResponseRecordsVolumesS3BucketPolicyStatements": False,
}


class ContainerResponseRecordsVolumesS3BucketPolicyStatementsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerResponseRecordsVolumesS3BucketPolicyStatements object"""

    actions = marshmallow_fields.List(marshmallow_fields.Str, data_key="actions", allow_none=True)
    r""" The actions field of the container_response_records_volumes_s3_bucket_policy_statements.

Example: ["GetObject","PutObject","DeleteObject","ListBucket"] """

    conditions = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_policy_condition.S3BucketPolicyConditionSchema", unknown=EXCLUDE, allow_none=True), data_key="conditions", allow_none=True)
    r""" Specifies bucket policy conditions. """

    effect = marshmallow_fields.Str(data_key="effect", allow_none=True)
    r""" Specifies whether access is allowed or denied when a user requests the specific action. If access (to allow) is not granted explicitly to a resource, access is implicitly denied. Access can also be denied explicitly to a resource, in order to make sure that a user cannot access it, even if a different policy grants access.

Valid choices:

* allow
* deny """

    principals = marshmallow_fields.List(marshmallow_fields.Str, data_key="principals", allow_none=True)
    r""" The principals field of the container_response_records_volumes_s3_bucket_policy_statements.

Example: ["user1","group/grp1","nasgroup/group1"] """

    resources = marshmallow_fields.List(marshmallow_fields.Str, data_key="resources", allow_none=True)
    r""" The resources field of the container_response_records_volumes_s3_bucket_policy_statements.

Example: ["bucket1","bucket1/*"] """

    sid = marshmallow_fields.Str(data_key="sid", allow_none=True)
    r""" Specifies the statement identifier used to differentiate between statements. The sid length can range from 1 to 256 characters and can only contain the following combination of characters 0-9, A-Z, and a-z. Special characters are not valid.

Example: FullAccessToUser1 """

    @property
    def resource(self):
        return ContainerResponseRecordsVolumesS3BucketPolicyStatements

    gettable_fields = [
        "actions",
        "conditions",
        "effect",
        "principals",
        "resources",
        "sid",
    ]
    """actions,conditions,effect,principals,resources,sid,"""

    patchable_fields = [
        "actions",
        "conditions",
        "effect",
        "principals",
        "resources",
        "sid",
    ]
    """actions,conditions,effect,principals,resources,sid,"""

    postable_fields = [
        "actions",
        "conditions",
        "effect",
        "principals",
        "resources",
        "sid",
    ]
    """actions,conditions,effect,principals,resources,sid,"""


class ContainerResponseRecordsVolumesS3BucketPolicyStatements(Resource):

    _schema = ContainerResponseRecordsVolumesS3BucketPolicyStatementsSchema
