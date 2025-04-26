r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketProtectionStatus", "S3BucketProtectionStatusSchema"]
__pdoc__ = {
    "S3BucketProtectionStatusSchema.resource": False,
    "S3BucketProtectionStatusSchema.opts": False,
    "S3BucketProtectionStatus": False,
}


class S3BucketProtectionStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketProtectionStatus object"""

    destination = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_protection_status_destination.S3BucketProtectionStatusDestinationSchema", unknown=EXCLUDE, data_key="destination", allow_none=True)
    r""" The destination field of the s3_bucket_protection_status. """

    is_protected = marshmallow_fields.Boolean(data_key="is_protected", allow_none=True)
    r""" Specifies whether a bucket is a source and if it is protected within ONTAP and/or an external cloud. This field cannot be specified using a POST method. """

    @property
    def resource(self):
        return S3BucketProtectionStatus

    gettable_fields = [
        "destination",
        "is_protected",
    ]
    """destination,is_protected,"""

    patchable_fields = [
        "destination",
    ]
    """destination,"""

    postable_fields = [
        "destination",
    ]
    """destination,"""


class S3BucketProtectionStatus(Resource):

    _schema = S3BucketProtectionStatusSchema
