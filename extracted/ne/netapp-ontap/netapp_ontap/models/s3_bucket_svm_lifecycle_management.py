r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketSvmLifecycleManagement", "S3BucketSvmLifecycleManagementSchema"]
__pdoc__ = {
    "S3BucketSvmLifecycleManagementSchema.resource": False,
    "S3BucketSvmLifecycleManagementSchema.opts": False,
    "S3BucketSvmLifecycleManagement": False,
}


class S3BucketSvmLifecycleManagementSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketSvmLifecycleManagement object"""

    rules = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_lifecycle_management_rules.S3BucketLifecycleManagementRulesSchema", unknown=EXCLUDE, allow_none=True), data_key="rules", allow_none=True)
    r""" Specifies an object store lifecycle management policy. This field cannot be set using the PATCH method. """

    @property
    def resource(self):
        return S3BucketSvmLifecycleManagement

    gettable_fields = [
        "rules",
    ]
    """rules,"""

    patchable_fields = [
        "rules",
    ]
    """rules,"""

    postable_fields = [
        "rules",
    ]
    """rules,"""


class S3BucketSvmLifecycleManagement(Resource):

    _schema = S3BucketSvmLifecycleManagementSchema
