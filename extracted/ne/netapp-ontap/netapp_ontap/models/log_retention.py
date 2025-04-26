r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LogRetention", "LogRetentionSchema"]
__pdoc__ = {
    "LogRetentionSchema.resource": False,
    "LogRetentionSchema.opts": False,
    "LogRetention": False,
}


class LogRetentionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LogRetention object"""

    count = Size(data_key="count", allow_none=True)
    r""" Determines how many audit log files to retain before
rotating the oldest log file out. This is mutually exclusive with
duration. """

    duration = marshmallow_fields.Str(data_key="duration", allow_none=True)
    r""" Specifies an ISO-8601 format date and time to retain the audit log file. The audit log files are
deleted once they reach the specified date/time. This is mutually exclusive with count.


Example: P4DT12H30M5S """

    @property
    def resource(self):
        return LogRetention

    gettable_fields = [
        "count",
        "duration",
    ]
    """count,duration,"""

    patchable_fields = [
        "count",
        "duration",
    ]
    """count,duration,"""

    postable_fields = [
        "count",
        "duration",
    ]
    """count,duration,"""


class LogRetention(Resource):

    _schema = LogRetentionSchema
