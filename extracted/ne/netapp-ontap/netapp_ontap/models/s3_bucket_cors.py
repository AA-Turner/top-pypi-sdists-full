r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketCors", "S3BucketCorsSchema"]
__pdoc__ = {
    "S3BucketCorsSchema.resource": False,
    "S3BucketCorsSchema.opts": False,
    "S3BucketCors": False,
}


class S3BucketCorsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketCors object"""

    rules = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_cors_rule.S3BucketCorsRuleSchema", unknown=EXCLUDE, allow_none=True), data_key="rules", allow_none=True)
    r""" Specifies an object store bucket CORS rule. """

    @property
    def resource(self):
        return S3BucketCors

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


class S3BucketCors(Resource):

    _schema = S3BucketCorsSchema
