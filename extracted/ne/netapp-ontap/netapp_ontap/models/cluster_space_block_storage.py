r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterSpaceBlockStorage", "ClusterSpaceBlockStorageSchema"]
__pdoc__ = {
    "ClusterSpaceBlockStorageSchema.resource": False,
    "ClusterSpaceBlockStorageSchema.opts": False,
    "ClusterSpaceBlockStorage": False,
}


class ClusterSpaceBlockStorageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterSpaceBlockStorage object"""

    available = Size(data_key="available", allow_none=True)
    r""" Available space across the cluster. """

    delayed_frees = Size(data_key="delayed_frees", allow_none=True)
    r""" Total delayed free space across the cluster. """

    full_threshold_percent = Size(data_key="full_threshold_percent", allow_none=True)
    r""" The cluster space full threshold percentage that triggers an EMS error. """

    inactive_data = Size(data_key="inactive_data", allow_none=True)
    r""" Inactive data across the cluster. """

    log_and_recovery_metadata = Size(data_key="log_and_recovery_metadata", allow_none=True)
    r""" The total space consumed by system logs and cores in the cluster. """

    medias = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cluster_space_block_storage_medias.ClusterSpaceBlockStorageMediasSchema", unknown=EXCLUDE, allow_none=True), data_key="medias", allow_none=True)
    r""" Configuration information based on type of media. For example, SSD media type information includes the sum of all the SSD storage across the cluster. """

    nearly_full_threshold_percent = Size(data_key="nearly_full_threshold_percent", allow_none=True)
    r""" The cluster space nearly full threshold percentage that triggers an EMS warning. """

    physical_used = Size(data_key="physical_used", allow_none=True)
    r""" Total physical used space across the cluster. """

    physical_used_percent = Size(data_key="physical_used_percent", allow_none=True)
    r""" The Physical space used percentage across the cluster. """

    size = Size(data_key="size", allow_none=True)
    r""" Total space across the cluster. """

    total_metadata_used = Size(data_key="total_metadata_used", allow_none=True)
    r""" The total space consumed by metadata in the cluster, which includes log and recovery metadata, delayed frees along with filesystem metadata and performance metadata. """

    unusable_space = Size(data_key="unusable_space", allow_none=True)
    r""" Total unusable space across the cluster due to some aggregate being unavailable. """

    used = Size(data_key="used", allow_none=True)
    r""" Used space (includes volume reserves) across the cluster. """

    @property
    def resource(self):
        return ClusterSpaceBlockStorage

    gettable_fields = [
        "available",
        "delayed_frees",
        "full_threshold_percent",
        "inactive_data",
        "log_and_recovery_metadata",
        "medias",
        "nearly_full_threshold_percent",
        "physical_used",
        "physical_used_percent",
        "size",
        "total_metadata_used",
        "unusable_space",
        "used",
    ]
    """available,delayed_frees,full_threshold_percent,inactive_data,log_and_recovery_metadata,medias,nearly_full_threshold_percent,physical_used,physical_used_percent,size,total_metadata_used,unusable_space,used,"""

    patchable_fields = [
        "full_threshold_percent",
        "nearly_full_threshold_percent",
    ]
    """full_threshold_percent,nearly_full_threshold_percent,"""

    postable_fields = [
        "full_threshold_percent",
        "nearly_full_threshold_percent",
    ]
    """full_threshold_percent,nearly_full_threshold_percent,"""


class ClusterSpaceBlockStorage(Resource):

    _schema = ClusterSpaceBlockStorageSchema
