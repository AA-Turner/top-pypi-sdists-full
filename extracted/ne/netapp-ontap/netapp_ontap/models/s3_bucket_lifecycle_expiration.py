r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketLifecycleExpiration", "S3BucketLifecycleExpirationSchema"]
__pdoc__ = {
    "S3BucketLifecycleExpirationSchema.resource": False,
    "S3BucketLifecycleExpirationSchema.opts": False,
    "S3BucketLifecycleExpiration": False,
}


class S3BucketLifecycleExpirationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketLifecycleExpiration object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the s3_bucket_lifecycle_expiration. """

    expired_object_delete_marker = marshmallow_fields.Boolean(data_key="expired_object_delete_marker", allow_none=True)
    r""" Cleanup object delete markers. """

    object_age_days = Size(data_key="object_age_days", allow_none=True)
    r""" Number of days since creation after which objects can be deleted. This cannot be used along with object_expiry_date.

Example: 100 """

    object_expiry_date = ImpreciseDateTime(data_key="object_expiry_date", allow_none=True)
    r""" Specific date from when objects can expire. This cannot be used with object_age_days.

Example: 2039-09-23T00:00:00.000+0000 """

    @property
    def resource(self):
        return S3BucketLifecycleExpiration

    gettable_fields = [
        "links",
        "expired_object_delete_marker",
        "object_age_days",
        "object_expiry_date",
    ]
    """links,expired_object_delete_marker,object_age_days,object_expiry_date,"""

    patchable_fields = [
        "expired_object_delete_marker",
        "object_age_days",
        "object_expiry_date",
    ]
    """expired_object_delete_marker,object_age_days,object_expiry_date,"""

    postable_fields = [
        "expired_object_delete_marker",
        "object_age_days",
        "object_expiry_date",
    ]
    """expired_object_delete_marker,object_age_days,object_expiry_date,"""


class S3BucketLifecycleExpiration(Resource):

    _schema = S3BucketLifecycleExpirationSchema
