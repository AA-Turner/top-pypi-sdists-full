r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketSvmEncryption", "S3BucketSvmEncryptionSchema"]
__pdoc__ = {
    "S3BucketSvmEncryptionSchema.resource": False,
    "S3BucketSvmEncryptionSchema.opts": False,
    "S3BucketSvmEncryption": False,
}


class S3BucketSvmEncryptionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketSvmEncryption object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether encryption is enabled on the bucket. By default, encryption is disabled on a bucket. This field cannot be set in a POST or PATCH method. """

    @property
    def resource(self):
        return S3BucketSvmEncryption

    gettable_fields = [
        "enabled",
    ]
    """enabled,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "enabled",
    ]
    """enabled,"""


class S3BucketSvmEncryption(Resource):

    _schema = S3BucketSvmEncryptionSchema
