r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketSvmProtectionStatusDestination", "S3BucketSvmProtectionStatusDestinationSchema"]
__pdoc__ = {
    "S3BucketSvmProtectionStatusDestinationSchema.resource": False,
    "S3BucketSvmProtectionStatusDestinationSchema.opts": False,
    "S3BucketSvmProtectionStatusDestination": False,
}


class S3BucketSvmProtectionStatusDestinationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketSvmProtectionStatusDestination object"""

    is_cloud = marshmallow_fields.Boolean(data_key="is_cloud", allow_none=True)
    r""" Specifies whether a bucket is protected within the Cloud. """

    is_external_cloud = marshmallow_fields.Boolean(data_key="is_external_cloud", allow_none=True)
    r""" Specifies whether a bucket is protected on external Cloud providers. """

    is_ontap = marshmallow_fields.Boolean(data_key="is_ontap", allow_none=True)
    r""" Specifies whether a bucket is protected within ONTAP. """

    @property
    def resource(self):
        return S3BucketSvmProtectionStatusDestination

    gettable_fields = [
        "is_cloud",
        "is_external_cloud",
        "is_ontap",
    ]
    """is_cloud,is_external_cloud,is_ontap,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class S3BucketSvmProtectionStatusDestination(Resource):

    _schema = S3BucketSvmProtectionStatusDestinationSchema
