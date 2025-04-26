r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeSpace", "VolumeSpaceSchema"]
__pdoc__ = {
    "VolumeSpaceSchema.resource": False,
    "VolumeSpaceSchema.opts": False,
    "VolumeSpace": False,
}


class VolumeSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeSpace object"""

    afs_total = Size(data_key="afs_total", allow_none=True)
    r""" Total size of AFS, excluding snap-reserve, in bytes. """

    auto_adaptive_compression_footprint_data_reduction = Size(data_key="auto_adaptive_compression_footprint_data_reduction", allow_none=True)
    r""" Savings achieved due to Auto Adaptive Compression, in bytes. """

    available = Size(data_key="available", allow_none=True)
    r""" The available space, in bytes. """

    available_percent = Size(data_key="available_percent", allow_none=True)
    r""" The space available, as a percent. """

    block_storage_inactive_user_data = Size(data_key="block_storage_inactive_user_data", allow_none=True)
    r""" The size that is physically used in the block storage of the volume and has a cold temperature. In bytes. This parameter is only supported if the volume is in an aggregate that is either attached to a cloud store or could be attached to a cloud store. """

    block_storage_inactive_user_data_percent = Size(data_key="block_storage_inactive_user_data_percent", allow_none=True)
    r""" Percentage of size that is physically used in the performance tier of the volume. """

    capacity_tier_footprint = Size(data_key="capacity_tier_footprint", allow_none=True)
    r""" Space used by capacity tier for this volume in the FabricPool aggregate, in bytes. """

    capacity_tier_footprint_data_reduction = Size(data_key="capacity_tier_footprint_data_reduction", allow_none=True)
    r""" Savings achieved in the space used by the capacity tier for this volume in the FabricPool aggregate, in bytes. """

    compaction_footprint_data_reduction = Size(data_key="compaction_footprint_data_reduction", allow_none=True)
    r""" Savings achieved due to Data Compaction, in bytes. """

    cross_volume_dedupe_metafiles_footprint = Size(data_key="cross_volume_dedupe_metafiles_footprint", allow_none=True)
    r""" Cross volume deduplication metadata footprint, in bytes. """

    cross_volume_dedupe_metafiles_temporary_footprint = Size(data_key="cross_volume_dedupe_metafiles_temporary_footprint", allow_none=True)
    r""" Cross volume temporary deduplication metadata footprint, in bytes. """

    dedupe_metafiles_footprint = Size(data_key="dedupe_metafiles_footprint", allow_none=True)
    r""" Deduplication metadata footprint, in bytes. """

    dedupe_metafiles_temporary_footprint = Size(data_key="dedupe_metafiles_temporary_footprint", allow_none=True)
    r""" Temporary deduplication metadata footprint, in bytes. """

    delayed_free_footprint = Size(data_key="delayed_free_footprint", allow_none=True)
    r""" Delayed free blocks footprint, in bytes. """

    effective_total_footprint = Size(data_key="effective_total_footprint", allow_none=True)
    r""" Volume footprint after efficiency savings, in bytes. effective total footprint represents total footprint after deducting auto adaptive compression and compaction savings. effective-footprint includes aggregate metadata used by volume. """

    expected_available = Size(data_key="expected_available", allow_none=True)
    r""" Size that should be available for the volume, irrespective of available size in the aggregate, in bytes. """

    file_operation_metadata = Size(data_key="file_operation_metadata", allow_none=True)
    r""" File operation metadata footprint, in bytes. """

    filesystem_size = Size(data_key="filesystem_size", allow_none=True)
    r""" Total usable size of the volume, in bytes. """

    filesystem_size_fixed = marshmallow_fields.Boolean(data_key="filesystem_size_fixed", allow_none=True)
    r""" Specifies whether the file system is to remain of the same size when set to true or to grow when set to false. This option is automatically set to true when a volume becomes SnapMirrored. """

    footprint = Size(data_key="footprint", allow_none=True)
    r""" Data used for this volume in the aggregate, in bytes. """

    fractional_reserve = Size(data_key="fractional_reserve", allow_none=True)
    r""" Used to change the amount of space reserved for overwrites of reserved objects in a volume. """

    full_threshold_percent = Size(data_key="full_threshold_percent", allow_none=True)
    r""" Volume full threshold percentage at which EMS warnings can be sent. """

    is_used_stale = marshmallow_fields.Boolean(data_key="is_used_stale", allow_none=True)
    r""" Specifies if the virtual space used is stale. """

    large_size_enabled = marshmallow_fields.Boolean(data_key="large_size_enabled", allow_none=True)
    r""" Indicates if the support for large FlexVol volumes and large files is enabled on this volume. When configured to true, FlexVol volume size can reach up to 300TB and single file size can reach 128TB. """

    local_tier_footprint = Size(data_key="local_tier_footprint", allow_none=True)
    r""" Space used by the local tier for this volume in the aggregate, in bytes. """

    logical_space = marshmallow_fields.Nested("netapp_ontap.models.volume_space_logical_space.VolumeSpaceLogicalSpaceSchema", unknown=EXCLUDE, data_key="logical_space", allow_none=True)
    r""" The logical_space field of the volume_space. """

    max_size = marshmallow_fields.Str(data_key="max_size", allow_none=True)
    r""" Indicates the maximum size supported for the FlexVol volume or for each constituent of the FlexGroup volume.

Valid choices:

* 100T
* 300T
* 600T """

    metadata = Size(data_key="metadata", allow_none=True)
    r""" Space used by the volume metadata in the aggregate, in bytes. """

    nearly_full_threshold_percent = Size(data_key="nearly_full_threshold_percent", allow_none=True)
    r""" Volume nearly full threshold percentage at which EMS warnings can be sent. """

    over_provisioned = Size(data_key="over_provisioned", allow_none=True)
    r""" The amount of space not available for this volume in the aggregate, in bytes. """

    overwrite_reserve = Size(data_key="overwrite_reserve", allow_none=True)
    r""" Reserved space for overwrites, in bytes. """

    overwrite_reserve_used = Size(data_key="overwrite_reserve_used", allow_none=True)
    r""" Overwrite logical reserve space used, in bytes. """

    percent_used = Size(data_key="percent_used", allow_none=True)
    r""" Percentage of the volume size that is used. """

    performance_tier_footprint = Size(data_key="performance_tier_footprint", allow_none=True)
    r""" Space used by the performance tier for this volume in the FabricPool aggregate, in bytes. """

    physical_used = Size(data_key="physical_used", allow_none=True)
    r""" Size that is physically used in the volume, in bytes. Physical used is effective total footprint which is equivalent to total footprint after deducting auto adaptive compression and compaction savings. Physical-used also includes aggregate metadata used by volume. """

    physical_used_percent = Size(data_key="physical_used_percent", allow_none=True)
    r""" Size that is physically used in the volume, as a percentage. """

    size = Size(data_key="size", allow_none=True)
    r""" Total provisioned size. The default size is equal to the minimum size of 20MB, in bytes. """

    size_available_for_snapshots = Size(data_key="size_available_for_snapshots", allow_none=True)
    r""" Available space for snapshots from snap-reserve, in bytes. """

    snapmirror_destination_footprint = Size(data_key="snapmirror_destination_footprint", allow_none=True)
    r""" SnapMirror destination footprint, in bytes. """

    snapshot = marshmallow_fields.Nested("netapp_ontap.models.volume_space_snapshot.VolumeSpaceSnapshotSchema", unknown=EXCLUDE, data_key="snapshot", allow_none=True)
    r""" The snapshot field of the volume_space. """

    snapshot_reserve_unusable = Size(data_key="snapshot_reserve_unusable", allow_none=True)
    r""" Snapshot reserve that is not available for snapshot creation, in bytes. """

    snapshot_spill = Size(data_key="snapshot_spill", allow_none=True)
    r""" Space used by the snapshot copies beyond the snap-reserve, in bytes. """

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

    user_data = Size(data_key="user_data", allow_none=True)
    r""" User data, in bytes. """

    volume_guarantee_footprint = Size(data_key="volume_guarantee_footprint", allow_none=True)
    r""" Space reserved for future writes in the volume, in bytes. """

    @property
    def resource(self):
        return VolumeSpace

    gettable_fields = [
        "afs_total",
        "auto_adaptive_compression_footprint_data_reduction",
        "available",
        "available_percent",
        "block_storage_inactive_user_data",
        "block_storage_inactive_user_data_percent",
        "capacity_tier_footprint",
        "capacity_tier_footprint_data_reduction",
        "compaction_footprint_data_reduction",
        "cross_volume_dedupe_metafiles_footprint",
        "cross_volume_dedupe_metafiles_temporary_footprint",
        "dedupe_metafiles_footprint",
        "dedupe_metafiles_temporary_footprint",
        "delayed_free_footprint",
        "effective_total_footprint",
        "expected_available",
        "file_operation_metadata",
        "filesystem_size",
        "filesystem_size_fixed",
        "footprint",
        "fractional_reserve",
        "full_threshold_percent",
        "is_used_stale",
        "large_size_enabled",
        "local_tier_footprint",
        "logical_space",
        "max_size",
        "metadata",
        "nearly_full_threshold_percent",
        "over_provisioned",
        "overwrite_reserve",
        "overwrite_reserve_used",
        "percent_used",
        "performance_tier_footprint",
        "physical_used",
        "physical_used_percent",
        "size",
        "size_available_for_snapshots",
        "snapmirror_destination_footprint",
        "snapshot",
        "snapshot_reserve_unusable",
        "snapshot_spill",
        "total_footprint",
        "total_metadata",
        "total_metadata_footprint",
        "used",
        "used_by_afs",
        "user_data",
        "volume_guarantee_footprint",
    ]
    """afs_total,auto_adaptive_compression_footprint_data_reduction,available,available_percent,block_storage_inactive_user_data,block_storage_inactive_user_data_percent,capacity_tier_footprint,capacity_tier_footprint_data_reduction,compaction_footprint_data_reduction,cross_volume_dedupe_metafiles_footprint,cross_volume_dedupe_metafiles_temporary_footprint,dedupe_metafiles_footprint,dedupe_metafiles_temporary_footprint,delayed_free_footprint,effective_total_footprint,expected_available,file_operation_metadata,filesystem_size,filesystem_size_fixed,footprint,fractional_reserve,full_threshold_percent,is_used_stale,large_size_enabled,local_tier_footprint,logical_space,max_size,metadata,nearly_full_threshold_percent,over_provisioned,overwrite_reserve,overwrite_reserve_used,percent_used,performance_tier_footprint,physical_used,physical_used_percent,size,size_available_for_snapshots,snapmirror_destination_footprint,snapshot,snapshot_reserve_unusable,snapshot_spill,total_footprint,total_metadata,total_metadata_footprint,used,used_by_afs,user_data,volume_guarantee_footprint,"""

    patchable_fields = [
        "afs_total",
        "available_percent",
        "expected_available",
        "filesystem_size_fixed",
        "fractional_reserve",
        "full_threshold_percent",
        "large_size_enabled",
        "logical_space",
        "max_size",
        "nearly_full_threshold_percent",
        "physical_used",
        "physical_used_percent",
        "size",
        "snapshot",
        "used_by_afs",
    ]
    """afs_total,available_percent,expected_available,filesystem_size_fixed,fractional_reserve,full_threshold_percent,large_size_enabled,logical_space,max_size,nearly_full_threshold_percent,physical_used,physical_used_percent,size,snapshot,used_by_afs,"""

    postable_fields = [
        "afs_total",
        "available_percent",
        "expected_available",
        "filesystem_size_fixed",
        "fractional_reserve",
        "full_threshold_percent",
        "large_size_enabled",
        "logical_space",
        "max_size",
        "nearly_full_threshold_percent",
        "physical_used",
        "physical_used_percent",
        "size",
        "snapshot",
        "used_by_afs",
    ]
    """afs_total,available_percent,expected_available,filesystem_size_fixed,fractional_reserve,full_threshold_percent,large_size_enabled,logical_space,max_size,nearly_full_threshold_percent,physical_used,physical_used_percent,size,snapshot,used_by_afs,"""


class VolumeSpace(Resource):

    _schema = VolumeSpaceSchema
