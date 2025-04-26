r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapmirrorPolicyRule", "SnapmirrorPolicyRuleSchema"]
__pdoc__ = {
    "SnapmirrorPolicyRuleSchema.resource": False,
    "SnapmirrorPolicyRuleSchema.opts": False,
    "SnapmirrorPolicyRule": False,
}


class SnapmirrorPolicyRuleSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorPolicyRule object"""

    count = Size(data_key="count", allow_none=True)
    r""" Number of snapshots to be kept for retention. Maximum value will differ based on type of relationship and scaling factor.

Example: 7 """

    creation_schedule = marshmallow_fields.Nested("netapp_ontap.resources.schedule.ScheduleSchema", unknown=EXCLUDE, data_key="creation_schedule", allow_none=True)
    r""" The creation_schedule field of the snapmirror_policy_rule. """

    label = marshmallow_fields.Str(data_key="label", allow_none=True)
    r""" Snapshot label

Example: hourly """

    period = marshmallow_fields.Str(data_key="period", allow_none=True)
    r""" Specifies the duration for which the snapshots are locked. The retention period value represents a duration and must be in the ISO-8601 duration format. Years, months, days, hours, minutes, and seconds are represented as "P<num>Y","P<num>M","P<num>D","PT<num>H","PT<num>M" and "PT<num>S". Value "infinite" is also a valid input for Flexvol volumes and FlexGroup volumes. A duration which combines different periods is not supported, for example "P1Y10M" is not supported. The range of supported retention period values is between 1 second to infinite.

Example: P30D """

    prefix = marshmallow_fields.Str(data_key="prefix", allow_none=True)
    r""" Specifies the prefix for the snapshot name to be created as per the schedule. If no value is specified, then the label is used as the prefix. """

    preserve = marshmallow_fields.Boolean(data_key="preserve", allow_none=True)
    r""" Specifies the behavior when the snapshot retention count is reached on the SnapMirror destination for the rule. The default value is false, which means that the oldest snapshot is deleted to make room for new ones but only if the number of snapshots has exceeded the retention count specified in the 'count' property. When set to true and where the snapshots have reached the retention count, an incremental SnapMirror transfer will fail or if the rule has a schedule, snapshots will be no longer be created on the SnapMirror destination.

Example: true """

    warn = Size(data_key="warn", allow_none=True)
    r""" Specifies the warning threshold count for the rule. The default value is zero. When set to a value greater than zero, an event is generated after the number of snapshots (for the particular rule) retained on a SnapMirror destination reaches the specified warning limit. The preserve property for the rule must be true in order to set the warn property to a value greater than zero.

Example: 4 """

    @property
    def resource(self):
        return SnapmirrorPolicyRule

    gettable_fields = [
        "count",
        "creation_schedule.links",
        "creation_schedule.name",
        "creation_schedule.uuid",
        "label",
        "period",
        "prefix",
        "preserve",
        "warn",
    ]
    """count,creation_schedule.links,creation_schedule.name,creation_schedule.uuid,label,period,prefix,preserve,warn,"""

    patchable_fields = [
        "count",
        "creation_schedule.name",
        "creation_schedule.uuid",
        "label",
        "period",
        "prefix",
        "preserve",
        "warn",
    ]
    """count,creation_schedule.name,creation_schedule.uuid,label,period,prefix,preserve,warn,"""

    postable_fields = [
        "count",
        "creation_schedule.name",
        "creation_schedule.uuid",
        "label",
        "period",
        "prefix",
        "preserve",
        "warn",
    ]
    """count,creation_schedule.name,creation_schedule.uuid,label,period,prefix,preserve,warn,"""


class SnapmirrorPolicyRule(Resource):

    _schema = SnapmirrorPolicyRuleSchema
