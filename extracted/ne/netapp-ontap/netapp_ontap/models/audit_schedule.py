r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AuditSchedule", "AuditScheduleSchema"]
__pdoc__ = {
    "AuditScheduleSchema.resource": False,
    "AuditScheduleSchema.opts": False,
    "AuditSchedule": False,
}


class AuditScheduleSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AuditSchedule object"""

    days = marshmallow_fields.List(Size, data_key="days", allow_none=True)
    r""" Specifies the day of the month schedule to rotate audit log. Leave empty for all. """

    hours = marshmallow_fields.List(Size, data_key="hours", allow_none=True)
    r""" Specifies the hourly schedule to rotate audit log. Leave empty for all. """

    minutes = marshmallow_fields.List(Size, data_key="minutes", allow_none=True)
    r""" Specifies the minutes schedule to rotate the audit log. """

    months = marshmallow_fields.List(Size, data_key="months", allow_none=True)
    r""" Specifies the months schedule to rotate audit log. Leave empty for all. """

    weekdays = marshmallow_fields.List(Size, data_key="weekdays", allow_none=True)
    r""" Specifies the weekdays schedule to rotate audit log. Leave empty for all. """

    @property
    def resource(self):
        return AuditSchedule

    gettable_fields = [
        "days",
        "hours",
        "minutes",
        "months",
        "weekdays",
    ]
    """days,hours,minutes,months,weekdays,"""

    patchable_fields = [
        "days",
        "hours",
        "minutes",
        "months",
        "weekdays",
    ]
    """days,hours,minutes,months,weekdays,"""

    postable_fields = [
        "days",
        "hours",
        "minutes",
        "months",
        "weekdays",
    ]
    """days,hours,minutes,months,weekdays,"""


class AuditSchedule(Resource):

    _schema = AuditScheduleSchema
