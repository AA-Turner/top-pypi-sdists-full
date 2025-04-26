r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["RaidGroupDisk", "RaidGroupDiskSchema"]
__pdoc__ = {
    "RaidGroupDiskSchema.resource": False,
    "RaidGroupDiskSchema.opts": False,
    "RaidGroupDisk": False,
}


class RaidGroupDiskSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the RaidGroupDisk object"""

    disk = marshmallow_fields.Nested("netapp_ontap.resources.disk.DiskSchema", unknown=EXCLUDE, data_key="disk", allow_none=True)
    r""" The disk field of the raid_group_disk. """

    position = marshmallow_fields.Str(data_key="position", allow_none=True)
    r""" The position of the disk within the RAID group.

Valid choices:

* data
* parity
* dparity
* tparity
* copy """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state of the disk within the RAID group.

Valid choices:

* normal
* failed
* zeroing
* copy
* replacing
* evacuating
* prefail
* offline
* reconstructing """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Disk interface type

Valid choices:

* ata
* bsas
* fcal
* fsas
* lun
* sas
* msata
* ssd
* vmdisk
* unknown
* ssd_cap
* ssd_nvm
* ssd_zns """

    usable_size = Size(data_key="usable_size", allow_none=True)
    r""" Size in bytes that is usable by the aggregate.

Example: 947912704 """

    @property
    def resource(self):
        return RaidGroupDisk

    gettable_fields = [
        "disk.links",
        "disk.name",
        "position",
        "state",
        "type",
        "usable_size",
    ]
    """disk.links,disk.name,position,state,type,usable_size,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class RaidGroupDisk(Resource):

    _schema = RaidGroupDiskSchema
