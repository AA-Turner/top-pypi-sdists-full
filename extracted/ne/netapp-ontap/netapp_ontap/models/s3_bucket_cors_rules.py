r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketCorsRules", "S3BucketCorsRulesSchema"]
__pdoc__ = {
    "S3BucketCorsRulesSchema.resource": False,
    "S3BucketCorsRulesSchema.opts": False,
    "S3BucketCorsRules": False,
}


class S3BucketCorsRulesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketCorsRules object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the s3_bucket_cors_rules. """

    allowed_headers = marshmallow_fields.List(marshmallow_fields.Str, data_key="allowed_headers", allow_none=True)
    r""" An array of HTTP headers allowed in the cross-origin requests.


Example: ["x-amz-request-id"] """

    allowed_methods = marshmallow_fields.List(marshmallow_fields.Str, data_key="allowed_methods", allow_none=True)
    r""" An array of HTTP methods allowed in the cross-origin requests.


Example: ["PUT","DELETE"] """

    allowed_origins = marshmallow_fields.List(marshmallow_fields.Str, data_key="allowed_origins", allow_none=True)
    r""" List of origins from where a cross-origin request is allowed to originate from for the S3 bucket.


Example: ["http://www.example.com"] """

    expose_headers = marshmallow_fields.List(marshmallow_fields.Str, data_key="expose_headers", allow_none=True)
    r""" List of extra headers sent in the response that customers can access from their applications.


Example: ["x-amz-date"] """

    id = marshmallow_fields.Str(data_key="id", allow_none=True)
    r""" Bucket CORS rule identifier. The length of the name can range from 0 to 256 characters. """

    max_age_seconds = Size(data_key="max_age_seconds", allow_none=True)
    r""" The time in seconds for your browser to cache the preflight response for the specified resource.

Example: 1024 """

    @property
    def resource(self):
        return S3BucketCorsRules

    gettable_fields = [
        "links",
        "allowed_headers",
        "allowed_methods",
        "allowed_origins",
        "expose_headers",
        "id",
        "max_age_seconds",
    ]
    """links,allowed_headers,allowed_methods,allowed_origins,expose_headers,id,max_age_seconds,"""

    patchable_fields = [
        "allowed_headers",
        "allowed_methods",
        "allowed_origins",
        "expose_headers",
        "id",
        "max_age_seconds",
    ]
    """allowed_headers,allowed_methods,allowed_origins,expose_headers,id,max_age_seconds,"""

    postable_fields = [
        "allowed_headers",
        "allowed_methods",
        "allowed_origins",
        "expose_headers",
        "id",
        "max_age_seconds",
    ]
    """allowed_headers,allowed_methods,allowed_origins,expose_headers,id,max_age_seconds,"""


class S3BucketCorsRules(Resource):

    _schema = S3BucketCorsRulesSchema
