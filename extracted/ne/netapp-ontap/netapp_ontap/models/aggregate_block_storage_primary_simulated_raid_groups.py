r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateBlockStoragePrimarySimulatedRaidGroups", "AggregateBlockStoragePrimarySimulatedRaidGroupsSchema"]
__pdoc__ = {
    "AggregateBlockStoragePrimarySimulatedRaidGroupsSchema.resource": False,
    "AggregateBlockStoragePrimarySimulatedRaidGroupsSchema.opts": False,
    "AggregateBlockStoragePrimarySimulatedRaidGroups": False,
}


class AggregateBlockStoragePrimarySimulatedRaidGroupsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateBlockStoragePrimarySimulatedRaidGroups object"""

    added_data_disk_count = Size(data_key="added_data_disk_count", allow_none=True)
    r""" Number of added data disks in RAID group. """

    added_parity_disk_count = Size(data_key="added_parity_disk_count", allow_none=True)
    r""" Number of added parity disks in RAID group. """

    data_disk_count = Size(data_key="data_disk_count", allow_none=True)
    r""" Number of data disks in RAID group. """

    existing_data_disk_count = Size(data_key="existing_data_disk_count", allow_none=True)
    r""" Number of existing data disks in the RAID group. """

    existing_parity_disk_count = Size(data_key="existing_parity_disk_count", allow_none=True)
    r""" Number of existing parity disks in the RAID group. """

    is_partition = marshmallow_fields.Boolean(data_key="is_partition", allow_none=True)
    r""" Indicates whether the disk is partitioned (true) or whole (false). """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the raid group. """

    parity_disk_count = Size(data_key="parity_disk_count", allow_none=True)
    r""" Number of parity disks in RAID group. """

    raid_type = marshmallow_fields.Str(data_key="raid_type", allow_none=True)
    r""" RAID type of the aggregate.

Valid choices:

* raid_dp
* raid_tec
* raid0
* raid4 """

    usable_size = Size(data_key="usable_size", allow_none=True)
    r""" Usable size of each disk, in bytes. """

    @property
    def resource(self):
        return AggregateBlockStoragePrimarySimulatedRaidGroups

    gettable_fields = [
        "added_data_disk_count",
        "added_parity_disk_count",
        "data_disk_count",
        "existing_data_disk_count",
        "existing_parity_disk_count",
        "is_partition",
        "name",
        "parity_disk_count",
        "raid_type",
        "usable_size",
    ]
    """added_data_disk_count,added_parity_disk_count,data_disk_count,existing_data_disk_count,existing_parity_disk_count,is_partition,name,parity_disk_count,raid_type,usable_size,"""

    patchable_fields = [
        "added_data_disk_count",
        "added_parity_disk_count",
        "data_disk_count",
        "existing_data_disk_count",
        "existing_parity_disk_count",
        "is_partition",
        "name",
        "parity_disk_count",
        "raid_type",
        "usable_size",
    ]
    """added_data_disk_count,added_parity_disk_count,data_disk_count,existing_data_disk_count,existing_parity_disk_count,is_partition,name,parity_disk_count,raid_type,usable_size,"""

    postable_fields = [
        "added_data_disk_count",
        "added_parity_disk_count",
        "data_disk_count",
        "existing_data_disk_count",
        "existing_parity_disk_count",
        "is_partition",
        "name",
        "parity_disk_count",
        "raid_type",
        "usable_size",
    ]
    """added_data_disk_count,added_parity_disk_count,data_disk_count,existing_data_disk_count,existing_parity_disk_count,is_partition,name,parity_disk_count,raid_type,usable_size,"""


class AggregateBlockStoragePrimarySimulatedRaidGroups(Resource):

    _schema = AggregateBlockStoragePrimarySimulatedRaidGroupsSchema
