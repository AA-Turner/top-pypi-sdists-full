r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeEfficiencyIdcsScanner", "VolumeEfficiencyIdcsScannerSchema"]
__pdoc__ = {
    "VolumeEfficiencyIdcsScannerSchema.resource": False,
    "VolumeEfficiencyIdcsScannerSchema.opts": False,
    "VolumeEfficiencyIdcsScanner": False,
}


class VolumeEfficiencyIdcsScannerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeEfficiencyIdcsScanner object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies the administrative state of the inactive data compression scanner. Disabling inactive data compression is not allowed on Capacity optimized Flash with QAT supported platforms. """

    inactive_days = Size(data_key="inactive_days", allow_none=True)
    r""" Data blocks older than, or equal to, 'inactive_days' are picked up by the inactive data compression scanner. Valid for PATCH only. Only applicable when 'operation_state' set to 'active'. """

    mode = marshmallow_fields.Str(data_key="mode", allow_none=True)
    r""" Specifies the mode of inactive data compression scanner. Valid for PATCH and GET.

Valid choices:

* default
* compute_compression_savings """

    operation_state = marshmallow_fields.Str(data_key="operation_state", allow_none=True)
    r""" Specifies the operational state of the inactive data compression scanner. VALID for PATCH and GET. Valid options for PATCH are "idle" and "active".

Valid choices:

* idle
* active """

    status = marshmallow_fields.Str(data_key="status", allow_none=True)
    r""" Status of last inactive data compression scan on the volume.

Valid choices:

* success
* failure """

    threshold_inactive_time = marshmallow_fields.Str(data_key="threshold_inactive_time", allow_none=True)
    r""" Time interval after which inactive data compression is automatically triggered. The value is in days and is represented in the ISO-8601 format "P<num>D", for example "P3D" represents a duration of 3 days. This field is not supported on QAT supported platforms.

Example: P14D """

    @property
    def resource(self):
        return VolumeEfficiencyIdcsScanner

    gettable_fields = [
        "enabled",
        "mode",
        "operation_state",
        "status",
        "threshold_inactive_time",
    ]
    """enabled,mode,operation_state,status,threshold_inactive_time,"""

    patchable_fields = [
        "inactive_days",
        "mode",
        "operation_state",
    ]
    """inactive_days,mode,operation_state,"""

    postable_fields = [
        "mode",
        "operation_state",
    ]
    """mode,operation_state,"""


class VolumeEfficiencyIdcsScanner(Resource):

    _schema = VolumeEfficiencyIdcsScannerSchema
