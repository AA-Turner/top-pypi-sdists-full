r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AntiRansomwareVolumeSurgeUsage", "AntiRansomwareVolumeSurgeUsageSchema"]
__pdoc__ = {
    "AntiRansomwareVolumeSurgeUsageSchema.resource": False,
    "AntiRansomwareVolumeSurgeUsageSchema.opts": False,
    "AntiRansomwareVolumeSurgeUsage": False,
}


class AntiRansomwareVolumeSurgeUsageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareVolumeSurgeUsage object"""

    file_create_peak_rate_per_minute = Size(data_key="file_create_peak_rate_per_minute", allow_none=True)
    r""" Peak rate of file creates per minute in the workload of the volume during surge.

Example: 10 """

    file_delete_peak_rate_per_minute = Size(data_key="file_delete_peak_rate_per_minute", allow_none=True)
    r""" Peak rate of file deletes per minute in the workload of the volume during surge.

Example: 50 """

    file_rename_peak_rate_per_minute = Size(data_key="file_rename_peak_rate_per_minute", allow_none=True)
    r""" Peak rate of file renames per minute in the workload of the volume during surge.

Example: 30 """

    high_entropy_data_write_peak_percent = Size(data_key="high_entropy_data_write_peak_percent", allow_none=True)
    r""" Peak percentage of high entropy data writes in the volume during surge.

Example: 30 """

    high_entropy_data_write_peak_rate_kb_per_minute = Size(data_key="high_entropy_data_write_peak_rate_kb_per_minute", allow_none=True)
    r""" Peak high entropy data write rate in the volume during surge, in KBs per minute.

Example: 2500 """

    time = ImpreciseDateTime(data_key="time", allow_none=True)
    r""" Timestamp at which the first surge in the volume's workload is observed.

Example: 2021-12-01T17:46:20.000+0000 """

    @property
    def resource(self):
        return AntiRansomwareVolumeSurgeUsage

    gettable_fields = [
        "file_create_peak_rate_per_minute",
        "file_delete_peak_rate_per_minute",
        "file_rename_peak_rate_per_minute",
        "high_entropy_data_write_peak_percent",
        "high_entropy_data_write_peak_rate_kb_per_minute",
        "time",
    ]
    """file_create_peak_rate_per_minute,file_delete_peak_rate_per_minute,file_rename_peak_rate_per_minute,high_entropy_data_write_peak_percent,high_entropy_data_write_peak_rate_kb_per_minute,time,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class AntiRansomwareVolumeSurgeUsage(Resource):

    _schema = AntiRansomwareVolumeSurgeUsageSchema
