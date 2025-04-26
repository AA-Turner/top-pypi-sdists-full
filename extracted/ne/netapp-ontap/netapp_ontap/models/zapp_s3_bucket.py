r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappS3Bucket", "ZappS3BucketSchema"]
__pdoc__ = {
    "ZappS3BucketSchema.resource": False,
    "ZappS3BucketSchema.opts": False,
    "ZappS3Bucket": False,
}


class ZappS3BucketSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappS3Bucket object"""

    application_components = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.zapp_s3_bucket_application_components.ZappS3BucketApplicationComponentsSchema", unknown=EXCLUDE, allow_none=True), data_key="application_components", allow_none=True)
    r""" The list of application components to be created. """

    protection_type = marshmallow_fields.Nested("netapp_ontap.models.zapp_s3_bucket_protection_type.ZappS3BucketProtectionTypeSchema", unknown=EXCLUDE, data_key="protection_type", allow_none=True)
    r""" The protection_type field of the zapp_s3_bucket. """

    @property
    def resource(self):
        return ZappS3Bucket

    gettable_fields = [
        "application_components",
        "protection_type",
    ]
    """application_components,protection_type,"""

    patchable_fields = [
        "application_components",
    ]
    """application_components,"""

    postable_fields = [
        "application_components",
        "protection_type",
    ]
    """application_components,protection_type,"""


class ZappS3Bucket(Resource):

    _schema = ZappS3BucketSchema
