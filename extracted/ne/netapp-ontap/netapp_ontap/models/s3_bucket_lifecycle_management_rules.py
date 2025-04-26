r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketLifecycleManagementRules", "S3BucketLifecycleManagementRulesSchema"]
__pdoc__ = {
    "S3BucketLifecycleManagementRulesSchema.resource": False,
    "S3BucketLifecycleManagementRulesSchema.opts": False,
    "S3BucketLifecycleManagementRules": False,
}


class S3BucketLifecycleManagementRulesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketLifecycleManagementRules object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the s3_bucket_lifecycle_management_rules. """

    abort_incomplete_multipart_upload = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_lifecycle_abort_incomplete_multipart_upload.S3BucketLifecycleAbortIncompleteMultipartUploadSchema", unknown=EXCLUDE, data_key="abort_incomplete_multipart_upload", allow_none=True)
    r""" Information about the abort-incomplete-multipart-upload lifecycle management action. """

    bucket_name = marshmallow_fields.Str(data_key="bucket_name", allow_none=True)
    r""" Specifies the name of the bucket. Bucket name is a string that can only contain the following combination of ASCII-range alphanumeric characters 0-9, a-z, ".", and "-".

Example: bucket1 """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether or not the associated rule is enabled. """

    expiration = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_lifecycle_expiration.S3BucketLifecycleExpirationSchema", unknown=EXCLUDE, data_key="expiration", allow_none=True)
    r""" Information about the expiration lifecycle management action. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Bucket lifecycle management rule identifier. The length of the name can range from 0 to 256 characters. """

    non_current_version_expiration = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_lifecycle_non_current_version_expiration.S3BucketLifecycleNonCurrentVersionExpirationSchema", unknown=EXCLUDE, data_key="non_current_version_expiration", allow_none=True)
    r""" Information about the non-current-version-expiration lifecycle management action. """

    object_filter = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_lifecycle_object_filter.S3BucketLifecycleObjectFilterSchema", unknown=EXCLUDE, data_key="object_filter", allow_none=True)
    r""" Information about the lifecycle management rule of a bucket. """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the s3_bucket_lifecycle_management_rules. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Specifies the unique identifier of the bucket.

Example: 414b29a1-3b26-11e9-bd58-0050568ea055 """

    @property
    def resource(self):
        return S3BucketLifecycleManagementRules

    gettable_fields = [
        "links",
        "abort_incomplete_multipart_upload",
        "bucket_name",
        "enabled",
        "expiration",
        "name",
        "non_current_version_expiration",
        "object_filter",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,abort_incomplete_multipart_upload,bucket_name,enabled,expiration,name,non_current_version_expiration,object_filter,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "abort_incomplete_multipart_upload",
        "enabled",
        "expiration",
        "non_current_version_expiration",
    ]
    """abort_incomplete_multipart_upload,enabled,expiration,non_current_version_expiration,"""

    postable_fields = [
        "abort_incomplete_multipart_upload",
        "bucket_name",
        "enabled",
        "expiration",
        "name",
        "non_current_version_expiration",
        "object_filter",
    ]
    """abort_incomplete_multipart_upload,bucket_name,enabled,expiration,name,non_current_version_expiration,object_filter,"""


class S3BucketLifecycleManagementRules(Resource):

    _schema = S3BucketLifecycleManagementRulesSchema
