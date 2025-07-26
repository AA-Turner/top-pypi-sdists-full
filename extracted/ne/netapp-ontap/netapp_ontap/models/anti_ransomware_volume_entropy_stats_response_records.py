r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AntiRansomwareVolumeEntropyStatsResponseRecords", "AntiRansomwareVolumeEntropyStatsResponseRecordsSchema"]
__pdoc__ = {
    "AntiRansomwareVolumeEntropyStatsResponseRecordsSchema.resource": False,
    "AntiRansomwareVolumeEntropyStatsResponseRecordsSchema.opts": False,
    "AntiRansomwareVolumeEntropyStatsResponseRecords": False,
}


class AntiRansomwareVolumeEntropyStatsResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareVolumeEntropyStatsResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the anti_ransomware_volume_entropy_stats_response_records. """

    data_written_in_bytes = Size(data_key="data_written_in_bytes", allow_none=True)
    r""" The amount of data written. """

    duration = marshmallow_fields.Str(data_key="duration", allow_none=True)
    r""" The duration of the interval associated with this statistic. The duration is represented in ISO-8601 standard format.

Example: PT15M """

    encryption_percentage = Size(data_key="encryption_percentage", allow_none=True)
    r""" The percentage of data that is encrypted. """

    entropy_stats_type = marshmallow_fields.Str(data_key="entropy_stats_type", allow_none=True)
    r""" Volume metrics are retrieved based on this statistic type.

Valid choices:

* sub_hourly
* hourly
* daily
* high_enc_pct """

    timestamp = ImpreciseDateTime(data_key="timestamp", allow_none=True)
    r""" Start time in date-time format. """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the anti_ransomware_volume_entropy_stats_response_records. """

    @property
    def resource(self):
        return AntiRansomwareVolumeEntropyStatsResponseRecords

    gettable_fields = [
        "links",
        "data_written_in_bytes",
        "duration",
        "encryption_percentage",
        "entropy_stats_type",
        "timestamp",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,data_written_in_bytes,duration,encryption_percentage,entropy_stats_type,timestamp,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "entropy_stats_type",
        "timestamp",
        "volume.name",
        "volume.uuid",
    ]
    """entropy_stats_type,timestamp,volume.name,volume.uuid,"""

    postable_fields = [
        "entropy_stats_type",
        "timestamp",
        "volume.name",
        "volume.uuid",
    ]
    """entropy_stats_type,timestamp,volume.name,volume.uuid,"""


class AntiRansomwareVolumeEntropyStatsResponseRecords(Resource):

    _schema = AntiRansomwareVolumeEntropyStatsResponseRecordsSchema
