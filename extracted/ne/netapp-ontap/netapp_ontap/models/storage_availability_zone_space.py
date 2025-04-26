r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageAvailabilityZoneSpace", "StorageAvailabilityZoneSpaceSchema"]
__pdoc__ = {
    "StorageAvailabilityZoneSpaceSchema.resource": False,
    "StorageAvailabilityZoneSpaceSchema.opts": False,
    "StorageAvailabilityZoneSpace": False,
}


class StorageAvailabilityZoneSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageAvailabilityZoneSpace object"""

    available = Size(data_key="available", allow_none=True)
    r""" Available space in the availability zone. """

    delayed_frees = Size(data_key="delayed_frees", allow_none=True)
    r""" Total space used by the delayed frees in the availability zone. """

    efficiency_without_snapshots = marshmallow_fields.Nested("netapp_ontap.models.storage_availability_zone_space_efficiency_without_snapshots.StorageAvailabilityZoneSpaceEfficiencyWithoutSnapshotsSchema", unknown=EXCLUDE, data_key="efficiency_without_snapshots", allow_none=True)
    r""" Storage efficiency that does not include the savings provided by snapshots for the availability zone. """

    full_threshold_percent = Size(data_key="full_threshold_percent", allow_none=True)
    r""" The availability zone full threshold percentage that triggers an EMS error. """

    inactive_data = Size(data_key="inactive_data", allow_none=True)
    r""" Inactive data in the availability zone. """

    logical_user_data_without_snapshots = Size(data_key="logical_user_data_without_snapshots", allow_none=True)
    r""" The logical space used by user data excluding snapshots in the availability zone. """

    nearly_full_threshold_percent = Size(data_key="nearly_full_threshold_percent", allow_none=True)
    r""" The availability zone nearly full threshold percentage that triggers an EMS warning. """

    physical_used = Size(data_key="physical_used", allow_none=True)
    r""" Total physical used space in the availability zone. """

    physical_used_percent = Size(data_key="physical_used_percent", allow_none=True)
    r""" The physical space used percentage in the availability zone. """

    physical_user_data_without_snapshots = Size(data_key="physical_user_data_without_snapshots", allow_none=True)
    r""" The physical space used by user data excluding snapshots in the availability zone. """

    size = Size(data_key="size", allow_none=True)
    r""" Total space in the availability zone. """

    total_metadata_used = Size(data_key="total_metadata_used", allow_none=True)
    r""" Total metadata used in the availability zone. """

    unusable = Size(data_key="unusable", allow_none=True)
    r""" Total unusable space in the availability zone due to an aggregate being unavailable. """

    @property
    def resource(self):
        return StorageAvailabilityZoneSpace

    gettable_fields = [
        "available",
        "delayed_frees",
        "efficiency_without_snapshots",
        "full_threshold_percent",
        "inactive_data",
        "logical_user_data_without_snapshots",
        "nearly_full_threshold_percent",
        "physical_used",
        "physical_used_percent",
        "physical_user_data_without_snapshots",
        "size",
        "total_metadata_used",
        "unusable",
    ]
    """available,delayed_frees,efficiency_without_snapshots,full_threshold_percent,inactive_data,logical_user_data_without_snapshots,nearly_full_threshold_percent,physical_used,physical_used_percent,physical_user_data_without_snapshots,size,total_metadata_used,unusable,"""

    patchable_fields = [
        "full_threshold_percent",
        "nearly_full_threshold_percent",
    ]
    """full_threshold_percent,nearly_full_threshold_percent,"""

    postable_fields = [
    ]
    """"""


class StorageAvailabilityZoneSpace(Resource):

    _schema = StorageAvailabilityZoneSpaceSchema
