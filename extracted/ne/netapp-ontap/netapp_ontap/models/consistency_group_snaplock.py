r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupSnaplock", "ConsistencyGroupSnaplockSchema"]
__pdoc__ = {
    "ConsistencyGroupSnaplockSchema.resource": False,
    "ConsistencyGroupSnaplockSchema.opts": False,
    "ConsistencyGroupSnaplock": False,
}


class ConsistencyGroupSnaplockSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupSnaplock object"""

    compliance_clock_time = ImpreciseDateTime(data_key="compliance_clock_time", allow_none=True)
    r""" The compliance clock time used to manage the SnapLock objects in the consistency group.

Example: 2018-06-04T19:00:00.000+0000 """

    expiry_time = ImpreciseDateTime(data_key="expiry_time", allow_none=True)
    r""" Expiry time of the consistency group. For consistency group with an infinite SnapLock expiry time, "9999-12-31T23:59:59" is used to denote the time.

Example: 2018-06-04T19:00:00.000+0000 """

    retention = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_snaplock_retention.ConsistencyGroupSnaplockRetentionSchema", unknown=EXCLUDE, data_key="retention", allow_none=True)
    r""" The retention value represents a duration and must be specified in the ISO-8601 duration format. The retention period can be in years, months, days, hours, and minutes. A duration specified for years, months, and days is represented in the ISO-8601 format as "P<num>Y", "P<num>M", "P<num>D" respectively, for example "P10Y" represents a duration of 10 years. A duration in hours and minutes is represented by "PT<num>H" and "PT<num>M" respectively. The retention string must contain only a single time element that is, either years, months, days, hours, or minutes. A duration which combines different periods is not supported, for example "P1Y10M" is not supported. Apart from the duration specified in the ISO-8601 format, the duration field also accepts the string "infinite" to set an infinite retention period and the string "unspecified" to set an unspecified retention period. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The SnapLock type of the consistency group. <br>compliance &dash; A SnapLock Compliance (SLC) consistency group provides the highest level of WORM protection and an administrator cannot destroy an SLC consistency group if it contains unexpired WORM objects. <br> enterprise &dash; An administrator can delete a SnapLock Enterprise (SLE) consistency group.<br> non_snaplock &dash; Indicates the consistency group is non-snaplock.

Valid choices:

* compliance
* enterprise
* non_snaplock """

    @property
    def resource(self):
        return ConsistencyGroupSnaplock

    gettable_fields = [
        "compliance_clock_time",
        "expiry_time",
        "retention",
        "type",
    ]
    """compliance_clock_time,expiry_time,retention,type,"""

    patchable_fields = [
        "retention",
    ]
    """retention,"""

    postable_fields = [
        "retention",
    ]
    """retention,"""


class ConsistencyGroupSnaplock(Resource):

    _schema = ConsistencyGroupSnaplockSchema
