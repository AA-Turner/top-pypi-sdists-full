r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["RaidGroup", "RaidGroupSchema"]
__pdoc__ = {
    "RaidGroupSchema.resource": False,
    "RaidGroupSchema.opts": False,
    "RaidGroup": False,
}


class RaidGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the RaidGroup object"""

    cache_tier = marshmallow_fields.Boolean(data_key="cache_tier", allow_none=True)
    r""" RAID group is a cache tier """

    degraded = marshmallow_fields.Boolean(data_key="degraded", allow_none=True)
    r""" RAID group is degraded. A RAID group is degraded when at least one disk from that group has failed or is offline. """

    disks = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.raid_group_disk.RaidGroupDiskSchema", unknown=EXCLUDE, allow_none=True), data_key="disks", allow_none=True)
    r""" The disks field of the raid_group. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" RAID group name

Example: rg0 """

    raid_type = marshmallow_fields.Str(data_key="raid_type", allow_none=True)
    r""" RAID type of the raid group.

Valid choices:

* raid_dp
* raid_tec
* raid0
* raid4 """

    recomputing_parity = marshmallow_fields.Nested("netapp_ontap.models.raid_group_recomputing_parity.RaidGroupRecomputingParitySchema", unknown=EXCLUDE, data_key="recomputing_parity", allow_none=True)
    r""" The recomputing_parity field of the raid_group. """

    reconstruct = marshmallow_fields.Nested("netapp_ontap.models.raid_group_reconstruct.RaidGroupReconstructSchema", unknown=EXCLUDE, data_key="reconstruct", allow_none=True)
    r""" The reconstruct field of the raid_group. """

    @property
    def resource(self):
        return RaidGroup

    gettable_fields = [
        "cache_tier",
        "degraded",
        "disks",
        "name",
        "raid_type",
        "recomputing_parity",
        "reconstruct",
    ]
    """cache_tier,degraded,disks,name,raid_type,recomputing_parity,reconstruct,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class RaidGroup(Resource):

    _schema = RaidGroupSchema
