r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketLifecycleObjectFilter", "S3BucketLifecycleObjectFilterSchema"]
__pdoc__ = {
    "S3BucketLifecycleObjectFilterSchema.resource": False,
    "S3BucketLifecycleObjectFilterSchema.opts": False,
    "S3BucketLifecycleObjectFilter": False,
}


class S3BucketLifecycleObjectFilterSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketLifecycleObjectFilter object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the s3_bucket_lifecycle_object_filter. """

    prefix = marshmallow_fields.Str(data_key="prefix", allow_none=True)
    r""" A prefix that is matched against object-names within a bucket.

Example: /logs """

    size_greater_than = Size(data_key="size_greater_than", allow_none=True)
    r""" Size of the object greater than specified for which the corresponding lifecycle rule is to be applied.

Example: 10240 """

    size_less_than = Size(data_key="size_less_than", allow_none=True)
    r""" Size of the object smaller than specified for which the corresponding lifecycle rule is to be applied.

Example: 10485760 """

    tags = marshmallow_fields.List(marshmallow_fields.Str, data_key="tags", allow_none=True)
    r""" An array of key-value paired tags of the form <tag> or <tag=value>.


Example: ["project1=projA","project2=projB"] """

    @property
    def resource(self):
        return S3BucketLifecycleObjectFilter

    gettable_fields = [
        "links",
        "prefix",
        "size_greater_than",
        "size_less_than",
        "tags",
    ]
    """links,prefix,size_greater_than,size_less_than,tags,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "prefix",
        "size_greater_than",
        "size_less_than",
        "tags",
    ]
    """prefix,size_greater_than,size_less_than,tags,"""


class S3BucketLifecycleObjectFilter(Resource):

    _schema = S3BucketLifecycleObjectFilterSchema
