r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnaplockRetentionPolicyOperation", "SnaplockRetentionPolicyOperationSchema"]
__pdoc__ = {
    "SnaplockRetentionPolicyOperationSchema.resource": False,
    "SnaplockRetentionPolicyOperationSchema.opts": False,
    "SnaplockRetentionPolicyOperation": False,
}


class SnaplockRetentionPolicyOperationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockRetentionPolicyOperation object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the snaplock_retention_policy_operation. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Specifies the EBR policy name """

    retention_period = marshmallow_fields.Str(data_key="retention_period", allow_none=True)
    r""" Specifies the retention period of an event based retention policy. The retention period value represents a duration and must be specified in the ISO-8601 duration format. The retention period can be in years, months, days, hours or minutes. A period specified for years, months and days is represented in the ISO-8601 format as "P<num>Y", "P<num>M", "P<num>D" respectively. For example "P10Y" represents a duration of 10 years. Similarly, a duration in hours, minutes is represented by "PT<num>H", "PT<num>M" respectively. The period string must contain only a single time element i.e. either years, months, days, hours or minutes. A duration which combines different periods is not supported, example "P1Y10M" is not supported. Apart from the duration specified in the ISO-8601 format, the retention period field also accepts the strings "infinite" and "unspecified".

Example: P30M """

    @property
    def resource(self):
        return SnaplockRetentionPolicyOperation

    gettable_fields = [
        "links",
        "name",
        "retention_period",
    ]
    """links,name,retention_period,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class SnaplockRetentionPolicyOperation(Resource):

    _schema = SnaplockRetentionPolicyOperationSchema
