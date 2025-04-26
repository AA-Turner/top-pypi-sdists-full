r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AntiRansomwareVolumeWorkload", "AntiRansomwareVolumeWorkloadSchema"]
__pdoc__ = {
    "AntiRansomwareVolumeWorkloadSchema.resource": False,
    "AntiRansomwareVolumeWorkloadSchema.opts": False,
    "AntiRansomwareVolumeWorkload": False,
}


class AntiRansomwareVolumeWorkloadSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareVolumeWorkload object"""

    file_extension_types_count = Size(data_key="file_extension_types_count", allow_none=True)
    r""" Count of types of file extensions observed in the volume.

Example: 3 """

    file_extensions_observed = marshmallow_fields.List(marshmallow_fields.Str, data_key="file_extensions_observed", allow_none=True)
    r""" File extensions observed in the volume.

Example: ["pdf","jpeg","txt"] """

    historical_statistics = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_workload_historical_statistics.AntiRansomwareVolumeWorkloadHistoricalStatisticsSchema", unknown=EXCLUDE, data_key="historical_statistics", allow_none=True)
    r""" Typical usage values of volume workload. """

    newly_observed_file_extensions = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_workload_newly_observed_file_extensions.AntiRansomwareVolumeWorkloadNewlyObservedFileExtensionsSchema", unknown=EXCLUDE, allow_none=True), data_key="newly_observed_file_extensions", allow_none=True)
    r""" New file extensions observed in the volume during surge. """

    surge_statistics = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_workload_surge_statistics.AntiRansomwareVolumeWorkloadSurgeStatisticsSchema", unknown=EXCLUDE, data_key="surge_statistics", allow_none=True)
    r""" Usage values of the volume's workload during surge. """

    surge_usage = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_workload_surge_usage.AntiRansomwareVolumeWorkloadSurgeUsageSchema", unknown=EXCLUDE, data_key="surge_usage", allow_none=True)
    r""" Usage values of the volume's workload during surge. This object is no longer supported use surge_statistics instead. """

    typical_usage = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_typical_usage.AntiRansomwareVolumeTypicalUsageSchema", unknown=EXCLUDE, data_key="typical_usage", allow_none=True)
    r""" Typical usage values of volume workload. This object is no longer supported use historical_statistics instead. """

    @property
    def resource(self):
        return AntiRansomwareVolumeWorkload

    gettable_fields = [
        "file_extension_types_count",
        "file_extensions_observed",
        "historical_statistics",
        "newly_observed_file_extensions",
        "surge_statistics",
        "surge_usage",
        "typical_usage",
    ]
    """file_extension_types_count,file_extensions_observed,historical_statistics,newly_observed_file_extensions,surge_statistics,surge_usage,typical_usage,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class AntiRansomwareVolumeWorkload(Resource):

    _schema = AntiRansomwareVolumeWorkloadSchema
