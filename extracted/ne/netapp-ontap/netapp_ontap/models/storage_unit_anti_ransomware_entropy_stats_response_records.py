r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitAntiRansomwareEntropyStatsResponseRecords", "StorageUnitAntiRansomwareEntropyStatsResponseRecordsSchema"]
__pdoc__ = {
    "StorageUnitAntiRansomwareEntropyStatsResponseRecordsSchema.resource": False,
    "StorageUnitAntiRansomwareEntropyStatsResponseRecordsSchema.opts": False,
    "StorageUnitAntiRansomwareEntropyStatsResponseRecords": False,
}


class StorageUnitAntiRansomwareEntropyStatsResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitAntiRansomwareEntropyStatsResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the storage_unit_anti_ransomware_entropy_stats_response_records. """

    data_written_in_bytes = Size(data_key="data_written_in_bytes", allow_none=True)
    r""" The amount of data written. """

    duration = marshmallow_fields.Str(data_key="duration", allow_none=True)
    r""" The duration of the interval associated with this statistic. The duration is represented in ISO-8601 standard format.

Example: PT15M """

    encryption_percentage = Size(data_key="encryption_percentage", allow_none=True)
    r""" The percentage of data that is encrypted. """

    entropy_stats_type = marshmallow_fields.Str(data_key="entropy_stats_type", allow_none=True)
    r""" Storage unit metrics are retrieved based on this statistic type.

Valid choices:

* sub_hourly
* hourly
* daily
* high_enc_pct """

    storage_unit = marshmallow_fields.Nested("netapp_ontap.resources.storage_unit.StorageUnitSchema", unknown=EXCLUDE, data_key="storage_unit", allow_none=True)
    r""" The storage_unit field of the storage_unit_anti_ransomware_entropy_stats_response_records. """

    timestamp = ImpreciseDateTime(data_key="timestamp", allow_none=True)
    r""" Start time in date-time format. """

    @property
    def resource(self):
        return StorageUnitAntiRansomwareEntropyStatsResponseRecords

    gettable_fields = [
        "links",
        "data_written_in_bytes",
        "duration",
        "encryption_percentage",
        "entropy_stats_type",
        "storage_unit.links",
        "storage_unit.name",
        "storage_unit.uuid",
        "timestamp",
    ]
    """links,data_written_in_bytes,duration,encryption_percentage,entropy_stats_type,storage_unit.links,storage_unit.name,storage_unit.uuid,timestamp,"""

    patchable_fields = [
        "entropy_stats_type",
        "storage_unit.name",
        "storage_unit.uuid",
        "timestamp",
    ]
    """entropy_stats_type,storage_unit.name,storage_unit.uuid,timestamp,"""

    postable_fields = [
        "entropy_stats_type",
        "storage_unit.name",
        "storage_unit.uuid",
        "timestamp",
    ]
    """entropy_stats_type,storage_unit.name,storage_unit.uuid,timestamp,"""


class StorageUnitAntiRansomwareEntropyStatsResponseRecords(Resource):

    _schema = StorageUnitAntiRansomwareEntropyStatsResponseRecordsSchema
