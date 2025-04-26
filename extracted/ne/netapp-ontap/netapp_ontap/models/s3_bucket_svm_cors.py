r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketSvmCors", "S3BucketSvmCorsSchema"]
__pdoc__ = {
    "S3BucketSvmCorsSchema.resource": False,
    "S3BucketSvmCorsSchema.opts": False,
    "S3BucketSvmCors": False,
}


class S3BucketSvmCorsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketSvmCors object"""

    rules = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_cors_rules.S3BucketCorsRulesSchema", unknown=EXCLUDE, allow_none=True), data_key="rules", allow_none=True)
    r""" Specifies an object store bucket CORS rule. """

    @property
    def resource(self):
        return S3BucketSvmCors

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


class S3BucketSvmCors(Resource):

    _schema = S3BucketSvmCorsSchema
