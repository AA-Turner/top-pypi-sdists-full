r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapshotPolicyCopies", "SnapshotPolicyCopiesSchema"]
__pdoc__ = {
    "SnapshotPolicyCopiesSchema.resource": False,
    "SnapshotPolicyCopiesSchema.opts": False,
    "SnapshotPolicyCopies": False,
}


class SnapshotPolicyCopiesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapshotPolicyCopies object"""

    count = Size(data_key="count", allow_none=True)
    r""" The number of snapshots to maintain for this schedule. """

    prefix = marshmallow_fields.Str(data_key="prefix", allow_none=True)
    r""" The prefix to use while creating snapshots at regular intervals. """

    retention_period = marshmallow_fields.Str(data_key="retention_period", allow_none=True)
    r""" The retention period of snapshots for this schedule. The retention period value represents a duration and must be specified in the ISO-8601 duration format. The retention period can be in years, months, days, hours, and minutes. A period specified for years, months, and days is represented in the ISO-8601 format as "P<num>Y", "P<num>M", "P<num>D" respectively, for example "P10Y" represents a duration of 10 years. A duration in hours and minutes is represented by "PT<num>H" and "PT<num>M" respectively. The period string must contain only a single time element that is, either years, months, days, hours, or minutes. A duration which combines different periods is not supported, for example "P1Y10M" is not supported. """

    schedule = marshmallow_fields.Nested("netapp_ontap.resources.schedule.ScheduleSchema", unknown=EXCLUDE, data_key="schedule", allow_none=True)
    r""" The schedule field of the snapshot_policy_copies. """

    snapmirror_label = marshmallow_fields.Str(data_key="snapmirror_label", allow_none=True)
    r""" Label for SnapMirror operations """

    @property
    def resource(self):
        return SnapshotPolicyCopies

    gettable_fields = [
        "count",
        "prefix",
        "retention_period",
        "schedule.links",
        "schedule.name",
        "schedule.uuid",
        "snapmirror_label",
    ]
    """count,prefix,retention_period,schedule.links,schedule.name,schedule.uuid,snapmirror_label,"""

    patchable_fields = [
        "count",
        "prefix",
        "retention_period",
        "schedule.name",
        "schedule.uuid",
        "snapmirror_label",
    ]
    """count,prefix,retention_period,schedule.name,schedule.uuid,snapmirror_label,"""

    postable_fields = [
        "count",
        "prefix",
        "retention_period",
        "schedule.name",
        "schedule.uuid",
        "snapmirror_label",
    ]
    """count,prefix,retention_period,schedule.name,schedule.uuid,snapmirror_label,"""


class SnapshotPolicyCopies(Resource):

    _schema = SnapshotPolicyCopiesSchema
