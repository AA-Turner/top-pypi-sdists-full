r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappS3BucketApplicationComponents", "ZappS3BucketApplicationComponentsSchema"]
__pdoc__ = {
    "ZappS3BucketApplicationComponentsSchema.resource": False,
    "ZappS3BucketApplicationComponentsSchema.opts": False,
    "ZappS3BucketApplicationComponents": False,
}


class ZappS3BucketApplicationComponentsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappS3BucketApplicationComponents object"""

    access_policies = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.zapp_s3_bucket_application_components_access_policies.ZappS3BucketApplicationComponentsAccessPoliciesSchema", unknown=EXCLUDE, allow_none=True), data_key="access_policies", allow_none=True)
    r""" The list of S3 objectstore policies to be created. """

    bucket_endpoint_type = marshmallow_fields.Str(data_key="bucket_endpoint_type", allow_none=True)
    r""" The type of bucket.

Valid choices:

* nas
* s3 """

    capacity_tier = marshmallow_fields.Boolean(data_key="capacity_tier", allow_none=True)
    r""" Prefer lower latency storage under similar media costs. """

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" Object Store Server Bucket Description Usage: &lt;(size 1..256)&gt; """

    default_retention_period = marshmallow_fields.Str(data_key="default_retention_period", allow_none=True)
    r""" Specifies the default retention period that is applied to objects while committing them to the WORM state without an associated retention period. The retention period can be in years, or days. The retention period value represents a duration and must be specified in the ISO-8601 duration format. A period specified for years and days is represented in the ISO-8601 format as quot;Plt;num&gt;Y&quot; and quot;Plt;num&gt;D&quot; respectively, for example &quot;P10Y&quot; represents a duration of 10 years. The period string must contain only a single time element that is, either years, or days. A duration which combines different periods is not supported, for example &quot;P1Y10D&quot; is not supported. Usage: {{&lt;integer&gt; days|years} | none} """

    exclude_aggregates = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.nas_exclude_aggregates.NasExcludeAggregatesSchema", unknown=EXCLUDE, allow_none=True), data_key="exclude_aggregates", allow_none=True)
    r""" The exclude_aggregates field of the zapp_s3_bucket_application_components. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the application component. """

    nas_path = marshmallow_fields.Str(data_key="nas_path", allow_none=True)
    r""" The path to which the bucket corresponds to. """

    qos = marshmallow_fields.Nested("netapp_ontap.models.nas_application_components_qos.NasApplicationComponentsQosSchema", unknown=EXCLUDE, data_key="qos", allow_none=True)
    r""" The qos field of the zapp_s3_bucket_application_components. """

    retention_mode = marshmallow_fields.Str(data_key="retention_mode", allow_none=True)
    r""" The lock mode of the bucket. &lt;br&gt;compliance &dash; A SnapLock Compliance (SLC) bucket provides the highest level of WORM protection and an administrator cannot destroy a compliance bucket if it contains unexpired WORM objects. &lt;br&gt; governance &dash; An administrator can delete a Governance bucket.&lt;br&gt; no_lock &dash; Indicates the bucket does not support object locking. For s3 type buckets, the default value is no_lock.

Valid choices:

* compliance
* governance
* no_lock """

    size = Size(data_key="size", allow_none=True)
    r""" The total size of the S3 Bucket, split across the member components. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.nas_application_components_storage_service.NasApplicationComponentsStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the zapp_s3_bucket_application_components. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Object Store Server Bucket UUID Usage: &lt;UUID&gt; """

    versioning_state = marshmallow_fields.Str(data_key="versioning_state", allow_none=True)
    r""" Bucket Versioning State. For nas type buckets, this field is not set. For s3 type buckets, the default value is disabled.

Valid choices:

* disabled
* enabled
* suspended """

    @property
    def resource(self):
        return ZappS3BucketApplicationComponents

    gettable_fields = [
        "access_policies",
        "bucket_endpoint_type",
        "capacity_tier",
        "comment",
        "default_retention_period",
        "exclude_aggregates",
        "name",
        "nas_path",
        "qos",
        "retention_mode",
        "size",
        "storage_service",
        "uuid",
        "versioning_state",
    ]
    """access_policies,bucket_endpoint_type,capacity_tier,comment,default_retention_period,exclude_aggregates,name,nas_path,qos,retention_mode,size,storage_service,uuid,versioning_state,"""

    patchable_fields = [
        "name",
        "size",
        "storage_service",
    ]
    """name,size,storage_service,"""

    postable_fields = [
        "access_policies",
        "bucket_endpoint_type",
        "capacity_tier",
        "comment",
        "default_retention_period",
        "exclude_aggregates",
        "name",
        "nas_path",
        "qos",
        "retention_mode",
        "size",
        "storage_service",
        "versioning_state",
    ]
    """access_policies,bucket_endpoint_type,capacity_tier,comment,default_retention_period,exclude_aggregates,name,nas_path,qos,retention_mode,size,storage_service,versioning_state,"""


class ZappS3BucketApplicationComponents(Resource):

    _schema = ZappS3BucketApplicationComponentsSchema
