r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateBlockStorageHybridCache", "AggregateBlockStorageHybridCacheSchema"]
__pdoc__ = {
    "AggregateBlockStorageHybridCacheSchema.resource": False,
    "AggregateBlockStorageHybridCacheSchema.opts": False,
    "AggregateBlockStorageHybridCache": False,
}


class AggregateBlockStorageHybridCacheSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateBlockStorageHybridCache object"""

    disk_count = Size(data_key="disk_count", allow_none=True)
    r""" Number of disks used in the cache tier of the aggregate. Only provided when hybrid_cache.enabled is 'true'.

Example: 6 """

    disk_type = marshmallow_fields.Str(data_key="disk_type", allow_none=True)
    r""" Type of disk being used by the aggregate's cache tier.

Valid choices:

* fc
* lun
* nl_sas
* nvme_ssd
* sas
* sata
* scsi
* ssd
* ssd_cap
* ssd_zns
* vm_disk """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether the aggregate uses HDDs with SSDs as a cache. """

    raid_size = Size(data_key="raid_size", allow_none=True)
    r""" Option to specify the maximum number of disks that can be included in a RAID group.

Example: 24 """

    raid_type = marshmallow_fields.Str(data_key="raid_type", allow_none=True)
    r""" RAID type for SSD cache of the aggregate. Only provided when hybrid_cache.enabled is 'true'.

Valid choices:

* raid_dp
* raid_tec
* raid4 """

    simulated_raid_groups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.aggregate_block_storage_hybrid_cache_simulated_raid_groups.AggregateBlockStorageHybridCacheSimulatedRaidGroupsSchema", unknown=EXCLUDE, allow_none=True), data_key="simulated_raid_groups", allow_none=True)
    r""" The simulated_raid_groups field of the aggregate_block_storage_hybrid_cache. """

    size = Size(data_key="size", allow_none=True)
    r""" Total usable space in bytes of SSD cache. Only provided when hybrid_cache.enabled is 'true'.

Example: 1612709888 """

    storage_pools = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.aggregate_block_storage_hybrid_cache_storage_pools.AggregateBlockStorageHybridCacheStoragePoolsSchema", unknown=EXCLUDE, allow_none=True), data_key="storage_pools", allow_none=True)
    r""" List of storage pool properties and allocation_units_count for aggregate. """

    used = Size(data_key="used", allow_none=True)
    r""" Space used in bytes of SSD cache. Only provided when hybrid_cache.enabled is 'true'.

Example: 26501122 """

    @property
    def resource(self):
        return AggregateBlockStorageHybridCache

    gettable_fields = [
        "disk_count",
        "disk_type",
        "enabled",
        "raid_size",
        "raid_type",
        "simulated_raid_groups",
        "size",
        "storage_pools",
        "used",
    ]
    """disk_count,disk_type,enabled,raid_size,raid_type,simulated_raid_groups,size,storage_pools,used,"""

    patchable_fields = [
        "disk_count",
        "raid_size",
        "raid_type",
        "simulated_raid_groups",
        "storage_pools",
    ]
    """disk_count,raid_size,raid_type,simulated_raid_groups,storage_pools,"""

    postable_fields = [
        "disk_count",
        "raid_size",
        "raid_type",
        "simulated_raid_groups",
        "storage_pools",
    ]
    """disk_count,raid_size,raid_type,simulated_raid_groups,storage_pools,"""


class AggregateBlockStorageHybridCache(Resource):

    _schema = AggregateBlockStorageHybridCacheSchema
