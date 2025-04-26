r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappS3BucketApplicationComponentsAccessPolicies", "ZappS3BucketApplicationComponentsAccessPoliciesSchema"]
__pdoc__ = {
    "ZappS3BucketApplicationComponentsAccessPoliciesSchema.resource": False,
    "ZappS3BucketApplicationComponentsAccessPoliciesSchema.opts": False,
    "ZappS3BucketApplicationComponentsAccessPolicies": False,
}


class ZappS3BucketApplicationComponentsAccessPoliciesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappS3BucketApplicationComponentsAccessPolicies object"""

    actions = marshmallow_fields.List(marshmallow_fields.Str, data_key="actions", allow_none=True)
    r""" The actions field of the zapp_s3_bucket_application_components_access_policies. """

    conditions = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.zapp_s3_bucket_application_components_access_policies_conditions.ZappS3BucketApplicationComponentsAccessPoliciesConditionsSchema", unknown=EXCLUDE, allow_none=True), data_key="conditions", allow_none=True)
    r""" conditions. """

    effect = marshmallow_fields.Str(data_key="effect", allow_none=True)
    r""" Allow or Deny Access.

Valid choices:

* allow
* deny """

    principals = marshmallow_fields.List(marshmallow_fields.Str, data_key="principals", allow_none=True)
    r""" The principals field of the zapp_s3_bucket_application_components_access_policies. """

    resources = marshmallow_fields.List(marshmallow_fields.Str, data_key="resources", allow_none=True)
    r""" The resources field of the zapp_s3_bucket_application_components_access_policies. """

    sid = marshmallow_fields.Str(data_key="sid", allow_none=True)
    r""" Statement Identifier Usage: &lt;(size 1..256)&gt; """

    @property
    def resource(self):
        return ZappS3BucketApplicationComponentsAccessPolicies

    gettable_fields = [
        "actions",
        "conditions",
        "effect",
        "principals",
        "resources",
        "sid",
    ]
    """actions,conditions,effect,principals,resources,sid,"""

    patchable_fields = [
        "actions",
        "principals",
        "resources",
    ]
    """actions,principals,resources,"""

    postable_fields = [
        "actions",
        "conditions",
        "effect",
        "principals",
        "resources",
        "sid",
    ]
    """actions,conditions,effect,principals,resources,sid,"""


class ZappS3BucketApplicationComponentsAccessPolicies(Resource):

    _schema = ZappS3BucketApplicationComponentsAccessPoliciesSchema
