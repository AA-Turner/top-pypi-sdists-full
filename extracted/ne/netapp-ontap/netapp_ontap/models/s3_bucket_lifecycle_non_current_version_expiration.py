r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketLifecycleNonCurrentVersionExpiration", "S3BucketLifecycleNonCurrentVersionExpirationSchema"]
__pdoc__ = {
    "S3BucketLifecycleNonCurrentVersionExpirationSchema.resource": False,
    "S3BucketLifecycleNonCurrentVersionExpirationSchema.opts": False,
    "S3BucketLifecycleNonCurrentVersionExpiration": False,
}


class S3BucketLifecycleNonCurrentVersionExpirationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketLifecycleNonCurrentVersionExpiration object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the s3_bucket_lifecycle_non_current_version_expiration. """

    new_non_current_versions = Size(data_key="new_non_current_versions", allow_none=True)
    r""" Number of latest non-current versions to be retained. """

    non_current_days = Size(data_key="non_current_days", allow_none=True)
    r""" Number of days after which non-current versions can be deleted. """

    @property
    def resource(self):
        return S3BucketLifecycleNonCurrentVersionExpiration

    gettable_fields = [
        "links",
        "new_non_current_versions",
        "non_current_days",
    ]
    """links,new_non_current_versions,non_current_days,"""

    patchable_fields = [
        "new_non_current_versions",
        "non_current_days",
    ]
    """new_non_current_versions,non_current_days,"""

    postable_fields = [
        "new_non_current_versions",
        "non_current_days",
    ]
    """new_non_current_versions,non_current_days,"""


class S3BucketLifecycleNonCurrentVersionExpiration(Resource):

    _schema = S3BucketLifecycleNonCurrentVersionExpirationSchema
