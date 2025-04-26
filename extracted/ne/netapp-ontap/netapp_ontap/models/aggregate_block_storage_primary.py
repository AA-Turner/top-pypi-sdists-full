r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateBlockStoragePrimary", "AggregateBlockStoragePrimarySchema"]
__pdoc__ = {
    "AggregateBlockStoragePrimarySchema.resource": False,
    "AggregateBlockStoragePrimarySchema.opts": False,
    "AggregateBlockStoragePrimary": False,
}


class AggregateBlockStoragePrimarySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateBlockStoragePrimary object"""

    checksum_style = marshmallow_fields.Str(data_key="checksum_style", allow_none=True)
    r""" The checksum style used by the aggregate.

Valid choices:

* block
* advanced_zoned
* mixed """

    disk_class = marshmallow_fields.Str(data_key="disk_class", allow_none=True)
    r""" The class of disks being used by the aggregate.

Valid choices:

* capacity
* performance
* archive
* solid_state
* array
* virtual
* data_center
* capacity_flash """

    disk_count = Size(data_key="disk_count", allow_none=True)
    r""" Number of disks used in the aggregate. This includes parity disks, but excludes disks in the hybrid cache.

Example: 8 """

    disk_type = marshmallow_fields.Str(data_key="disk_type", allow_none=True)
    r""" The type of disk being used by the aggregate.

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

    raid_size = Size(data_key="raid_size", allow_none=True)
    r""" Option to specify the maximum number of disks that can be included in a RAID group.

Example: 16 """

    raid_type = marshmallow_fields.Str(data_key="raid_type", allow_none=True)
    r""" RAID type of the aggregate.

Valid choices:

* raid_dp
* raid_tec
* raid0
* raid4
* mixed_raid_type """

    simulated_raid_groups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.aggregate_block_storage_primary_simulated_raid_groups.AggregateBlockStoragePrimarySimulatedRaidGroupsSchema", unknown=EXCLUDE, allow_none=True), data_key="simulated_raid_groups", allow_none=True)
    r""" The simulated_raid_groups field of the aggregate_block_storage_primary. """

    @property
    def resource(self):
        return AggregateBlockStoragePrimary

    gettable_fields = [
        "checksum_style",
        "disk_class",
        "disk_count",
        "disk_type",
        "raid_size",
        "raid_type",
        "simulated_raid_groups",
    ]
    """checksum_style,disk_class,disk_count,disk_type,raid_size,raid_type,simulated_raid_groups,"""

    patchable_fields = [
        "disk_count",
        "raid_size",
        "raid_type",
        "simulated_raid_groups",
    ]
    """disk_count,raid_size,raid_type,simulated_raid_groups,"""

    postable_fields = [
        "checksum_style",
        "disk_class",
        "disk_count",
        "raid_size",
        "raid_type",
        "simulated_raid_groups",
    ]
    """checksum_style,disk_class,disk_count,raid_size,raid_type,simulated_raid_groups,"""


class AggregateBlockStoragePrimary(Resource):

    _schema = AggregateBlockStoragePrimarySchema
