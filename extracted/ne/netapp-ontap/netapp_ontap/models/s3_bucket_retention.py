r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketRetention", "S3BucketRetentionSchema"]
__pdoc__ = {
    "S3BucketRetentionSchema.resource": False,
    "S3BucketRetentionSchema.opts": False,
    "S3BucketRetention": False,
}


class S3BucketRetentionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketRetention object"""

    default_period = marshmallow_fields.Str(data_key="default_period", allow_none=True)
    r""" Specifies the default retention period that is applied to objects while committing them to the WORM state without an associated retention period. The retention period can be in years, or days. The retention period value represents a duration and must be specified in the ISO-8601 duration format.  A period specified for years and days is represented in the ISO-8601 format as "P<num>Y" and "P<num>D" respectively, for example "P10Y" represents a duration of 10 years. The period string must contain only a single time element that is, either years, or days. A duration which combines different periods is not supported, for example "P1Y10D" is not supported.

Example: P10Y """

    mode = marshmallow_fields.Str(data_key="mode", allow_none=True)
    r""" The lock mode of the bucket. <br>compliance &dash; A SnapLock Compliance (SLC) bucket provides the highest level of WORM protection and an administrator cannot destroy a compliance bucket if it contains unexpired WORM objects. <br> governance &dash; An administrator can delete a Governance bucket.<br> no_lock &dash; Indicates the bucket does not support object locking.

Valid choices:

* no_lock
* compliance
* governance """

    @property
    def resource(self):
        return S3BucketRetention

    gettable_fields = [
        "default_period",
        "mode",
    ]
    """default_period,mode,"""

    patchable_fields = [
        "default_period",
    ]
    """default_period,"""

    postable_fields = [
        "default_period",
        "mode",
    ]
    """default_period,mode,"""


class S3BucketRetention(Resource):

    _schema = S3BucketRetentionSchema
