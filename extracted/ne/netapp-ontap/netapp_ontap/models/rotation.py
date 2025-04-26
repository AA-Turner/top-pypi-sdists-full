r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Rotation", "RotationSchema"]
__pdoc__ = {
    "RotationSchema.resource": False,
    "RotationSchema.opts": False,
    "Rotation": False,
}


class RotationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Rotation object"""

    now = marshmallow_fields.Boolean(data_key="now", allow_none=True)
    r""" Manually rotates the audit logs. Optional in PATCH only. Not available in POST. """

    schedule = marshmallow_fields.Nested("netapp_ontap.models.audit_schedule.AuditScheduleSchema", unknown=EXCLUDE, data_key="schedule", allow_none=True)
    r""" Rotates the audit logs based on a schedule by using the time-based rotation parameters in any combination. The rotation schedule is calculated by using all the time-related values. """

    size = Size(data_key="size", allow_none=True)
    r""" Rotates logs based on log size in bytes. """

    @property
    def resource(self):
        return Rotation

    gettable_fields = [
        "schedule",
        "size",
    ]
    """schedule,size,"""

    patchable_fields = [
        "now",
        "schedule",
        "size",
    ]
    """now,schedule,size,"""

    postable_fields = [
        "schedule",
        "size",
    ]
    """schedule,size,"""


class Rotation(Resource):

    _schema = RotationSchema
