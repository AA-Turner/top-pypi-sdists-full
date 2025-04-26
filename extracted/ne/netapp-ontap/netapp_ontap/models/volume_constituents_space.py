r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeConstituentsSpace", "VolumeConstituentsSpaceSchema"]
__pdoc__ = {
    "VolumeConstituentsSpaceSchema.resource": False,
    "VolumeConstituentsSpaceSchema.opts": False,
    "VolumeConstituentsSpace": False,
}


class VolumeConstituentsSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeConstituentsSpace object"""

    afs_total = Size(data_key="afs_total", allow_none=True)
    r""" Total size of AFS, excluding snap-reserve, in bytes. """

    available = Size(data_key="available", allow_none=True)
    r""" The available space, in bytes. """

    available_percent = Size(data_key="available_percent", allow_none=True)
    r""" The space available, as a percent. """

    block_storage_inactive_user_data = Size(data_key="block_storage_inactive_user_data", allow_none=True)
    r""" The size that is physically used in the block storage of the volume and has a cold temperature. In bytes. This parameter is only supported if the volume is in an aggregate that is either attached to a cloud store or could be attached to a cloud store. """

    capacity_tier_footprint = Size(data_key="capacity_tier_footprint", allow_none=True)
    r""" Space used by capacity tier for this volume in the FabricPool aggregate, in bytes. """

    footprint = Size(data_key="footprint", allow_none=True)
    r""" Data used for this volume in the aggregate, in bytes. """

    large_size_enabled = marshmallow_fields.Boolean(data_key="large_size_enabled", allow_none=True)
    r""" Specifies whether the support for large volumes and large files is enabled on the volume. """

    local_tier_footprint = Size(data_key="local_tier_footprint", allow_none=True)
    r""" Space used by the local tier for this volume in the aggregate, in bytes. """

    logical_space = marshmallow_fields.Nested("netapp_ontap.models.volume_constituents_space_logical_space.VolumeConstituentsSpaceLogicalSpaceSchema", unknown=EXCLUDE, data_key="logical_space", allow_none=True)
    r""" The logical_space field of the volume_constituents_space. """

    max_size = marshmallow_fields.Str(data_key="max_size", allow_none=True)
    r""" Indicates the maximum size supported for each constituent of the FlexGroup volume.

Valid choices:

* 100T
* 300T
* 600T """

    metadata = Size(data_key="metadata", allow_none=True)
    r""" Space used by the volume metadata in the aggregate, in bytes. """

    over_provisioned = Size(data_key="over_provisioned", allow_none=True)
    r""" The amount of space not available for this volume in the aggregate, in bytes. """

    performance_tier_footprint = Size(data_key="performance_tier_footprint", allow_none=True)
    r""" Space used by the performance tier for this volume in the FabricPool aggregate, in bytes. """

    size = Size(data_key="size", allow_none=True)
    r""" Total provisioned size. The default size is equal to the minimum size of 20MB, in bytes. """

    snapshot = marshmallow_fields.Nested("netapp_ontap.models.volume_constituents_space_snapshot.VolumeConstituentsSpaceSnapshotSchema", unknown=EXCLUDE, data_key="snapshot", allow_none=True)
    r""" The snapshot field of the volume_constituents_space. """

    total_footprint = Size(data_key="total_footprint", allow_none=True)
    r""" Data and metadata used for this volume in the aggregate, in bytes. """

    total_metadata = Size(data_key="total_metadata", allow_none=True)
    r""" Space used by the total metadata in the volume, in bytes. """

    total_metadata_footprint = Size(data_key="total_metadata_footprint", allow_none=True)
    r""" Space used by the volume metadata footprint in the aggregate, in bytes. """

    used = Size(data_key="used", allow_none=True)
    r""" The virtual space used (includes volume reserves) before storage efficiency, in bytes. """

    used_by_afs = Size(data_key="used_by_afs", allow_none=True)
    r""" The space used by Active Filesystem, in bytes. """

    used_percent = Size(data_key="used_percent", allow_none=True)
    r""" The virtual space used (includes volume reserves) before storage efficiency, as a percent. """

    @property
    def resource(self):
        return VolumeConstituentsSpace

    gettable_fields = [
        "afs_total",
        "available",
        "available_percent",
        "block_storage_inactive_user_data",
        "capacity_tier_footprint",
        "footprint",
        "large_size_enabled",
        "local_tier_footprint",
        "logical_space",
        "max_size",
        "metadata",
        "over_provisioned",
        "performance_tier_footprint",
        "size",
        "snapshot",
        "total_footprint",
        "total_metadata",
        "total_metadata_footprint",
        "used",
        "used_by_afs",
        "used_percent",
    ]
    """afs_total,available,available_percent,block_storage_inactive_user_data,capacity_tier_footprint,footprint,large_size_enabled,local_tier_footprint,logical_space,max_size,metadata,over_provisioned,performance_tier_footprint,size,snapshot,total_footprint,total_metadata,total_metadata_footprint,used,used_by_afs,used_percent,"""

    patchable_fields = [
        "afs_total",
        "available_percent",
        "large_size_enabled",
        "logical_space",
        "max_size",
        "size",
        "snapshot",
        "used_by_afs",
        "used_percent",
    ]
    """afs_total,available_percent,large_size_enabled,logical_space,max_size,size,snapshot,used_by_afs,used_percent,"""

    postable_fields = [
        "afs_total",
        "available_percent",
        "large_size_enabled",
        "logical_space",
        "max_size",
        "size",
        "snapshot",
        "used_by_afs",
        "used_percent",
    ]
    """afs_total,available_percent,large_size_enabled,logical_space,max_size,size,snapshot,used_by_afs,used_percent,"""


class VolumeConstituentsSpace(Resource):

    _schema = VolumeConstituentsSpaceSchema
