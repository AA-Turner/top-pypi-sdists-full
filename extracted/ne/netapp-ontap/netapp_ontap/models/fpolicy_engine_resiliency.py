r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FpolicyEngineResiliency", "FpolicyEngineResiliencySchema"]
__pdoc__ = {
    "FpolicyEngineResiliencySchema.resource": False,
    "FpolicyEngineResiliencySchema.opts": False,
    "FpolicyEngineResiliency": False,
}


class FpolicyEngineResiliencySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyEngineResiliency object"""

    directory_path = marshmallow_fields.Str(data_key="directory_path", allow_none=True)
    r""" Specifies the directory path under the SVM namespace,
where notifications are stored in the files whenever a network outage happens.


Example: /dir1 """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether the resiliency feature is enabled or not.
Default is false. """

    retention_duration = marshmallow_fields.Str(data_key="retention_duration", allow_none=True)
    r""" Specifies the ISO-8601 duration, for which the notifications are written
to files inside the storage controller during a network outage. The value for
this field must be between 0 and 600 seconds. Default is 180 seconds.


Example: PT3M """

    @property
    def resource(self):
        return FpolicyEngineResiliency

    gettable_fields = [
        "directory_path",
        "enabled",
        "retention_duration",
    ]
    """directory_path,enabled,retention_duration,"""

    patchable_fields = [
        "directory_path",
        "enabled",
        "retention_duration",
    ]
    """directory_path,enabled,retention_duration,"""

    postable_fields = [
        "directory_path",
        "enabled",
        "retention_duration",
    ]
    """directory_path,enabled,retention_duration,"""


class FpolicyEngineResiliency(Resource):

    _schema = FpolicyEngineResiliencySchema
