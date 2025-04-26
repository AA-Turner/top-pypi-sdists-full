r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateBlockStorageHybridCacheSimulatedRaidGroups", "AggregateBlockStorageHybridCacheSimulatedRaidGroupsSchema"]
__pdoc__ = {
    "AggregateBlockStorageHybridCacheSimulatedRaidGroupsSchema.resource": False,
    "AggregateBlockStorageHybridCacheSimulatedRaidGroupsSchema.opts": False,
    "AggregateBlockStorageHybridCacheSimulatedRaidGroups": False,
}


class AggregateBlockStorageHybridCacheSimulatedRaidGroupsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateBlockStorageHybridCacheSimulatedRaidGroups object"""

    added_data_disk_count = Size(data_key="added_data_disk_count", allow_none=True)
    r""" Number of added data disks in RAID group. """

    added_parity_disk_count = Size(data_key="added_parity_disk_count", allow_none=True)
    r""" Number of added parity disks in RAID group. """

    existing_data_disk_count = Size(data_key="existing_data_disk_count", allow_none=True)
    r""" Number of existing data disks in the RAID group. """

    existing_parity_disk_count = Size(data_key="existing_parity_disk_count", allow_none=True)
    r""" Number of existing parity disks in the RAID group. """

    is_partition = marshmallow_fields.Boolean(data_key="is_partition", allow_none=True)
    r""" Indicates whether the disk is partitioned (true) or whole (false). """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the raid group. """

    usable_size = Size(data_key="usable_size", allow_none=True)
    r""" Usable size of each disk, in bytes. """

    @property
    def resource(self):
        return AggregateBlockStorageHybridCacheSimulatedRaidGroups

    gettable_fields = [
        "added_data_disk_count",
        "added_parity_disk_count",
        "existing_data_disk_count",
        "existing_parity_disk_count",
        "is_partition",
        "name",
        "usable_size",
    ]
    """added_data_disk_count,added_parity_disk_count,existing_data_disk_count,existing_parity_disk_count,is_partition,name,usable_size,"""

    patchable_fields = [
        "added_data_disk_count",
        "added_parity_disk_count",
        "existing_data_disk_count",
        "existing_parity_disk_count",
        "is_partition",
        "name",
        "usable_size",
    ]
    """added_data_disk_count,added_parity_disk_count,existing_data_disk_count,existing_parity_disk_count,is_partition,name,usable_size,"""

    postable_fields = [
        "added_data_disk_count",
        "added_parity_disk_count",
        "existing_data_disk_count",
        "existing_parity_disk_count",
        "is_partition",
        "name",
        "usable_size",
    ]
    """added_data_disk_count,added_parity_disk_count,existing_data_disk_count,existing_parity_disk_count,is_partition,name,usable_size,"""


class AggregateBlockStorageHybridCacheSimulatedRaidGroups(Resource):

    _schema = AggregateBlockStorageHybridCacheSimulatedRaidGroupsSchema
