r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CifsDomainPasswordSchedule", "CifsDomainPasswordScheduleSchema"]
__pdoc__ = {
    "CifsDomainPasswordScheduleSchema.resource": False,
    "CifsDomainPasswordScheduleSchema.opts": False,
    "CifsDomainPasswordSchedule": False,
}


class CifsDomainPasswordScheduleSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsDomainPasswordSchedule object"""

    schedule_day_of_week = marshmallow_fields.Str(data_key="schedule_day_of_week", allow_none=True)
    r""" Day of the week for password change schedule.

Example: Sunday """

    schedule_description = marshmallow_fields.Str(data_key="schedule_description", allow_none=True)
    r""" Schedule description. """

    schedule_enabled = marshmallow_fields.Boolean(data_key="schedule_enabled", allow_none=True)
    r""" Is password schedule enabled. """

    schedule_last_changed_time = ImpreciseDateTime(data_key="schedule_last_changed_time", allow_none=True)
    r""" Last successful password change time. """

    schedule_randomized_minute = Size(data_key="schedule_randomized_minute", allow_none=True)
    r""" Minutes within which schedule start can be randomized. """

    schedule_time_of_day = marshmallow_fields.Str(data_key="schedule_time_of_day", allow_none=True)
    r""" Start time for password change schedule.

Example: 36900 """

    schedule_warn_message = marshmallow_fields.Str(data_key="schedule_warn_message", allow_none=True)
    r""" Warning message in case job is deleted. """

    schedule_weekly_interval = Size(data_key="schedule_weekly_interval", allow_none=True)
    r""" Interval in weeks for password change schedule. """

    @property
    def resource(self):
        return CifsDomainPasswordSchedule

    gettable_fields = [
        "schedule_description",
        "schedule_enabled",
        "schedule_last_changed_time",
        "schedule_randomized_minute",
        "schedule_warn_message",
        "schedule_weekly_interval",
    ]
    """schedule_description,schedule_enabled,schedule_last_changed_time,schedule_randomized_minute,schedule_warn_message,schedule_weekly_interval,"""

    patchable_fields = [
        "schedule_day_of_week",
        "schedule_enabled",
        "schedule_randomized_minute",
        "schedule_time_of_day",
        "schedule_weekly_interval",
    ]
    """schedule_day_of_week,schedule_enabled,schedule_randomized_minute,schedule_time_of_day,schedule_weekly_interval,"""

    postable_fields = [
        "schedule_enabled",
        "schedule_randomized_minute",
        "schedule_weekly_interval",
    ]
    """schedule_enabled,schedule_randomized_minute,schedule_weekly_interval,"""


class CifsDomainPasswordSchedule(Resource):

    _schema = CifsDomainPasswordScheduleSchema
