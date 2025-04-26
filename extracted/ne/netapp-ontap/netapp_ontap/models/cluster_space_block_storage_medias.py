r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterSpaceBlockStorageMedias", "ClusterSpaceBlockStorageMediasSchema"]
__pdoc__ = {
    "ClusterSpaceBlockStorageMediasSchema.resource": False,
    "ClusterSpaceBlockStorageMediasSchema.opts": False,
    "ClusterSpaceBlockStorageMedias": False,
}


class ClusterSpaceBlockStorageMediasSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterSpaceBlockStorageMedias object"""

    available = Size(data_key="available", allow_none=True)
    r""" Available space across the cluster based on media type. """

    efficiency = marshmallow_fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", unknown=EXCLUDE, data_key="efficiency", allow_none=True)
    r""" The efficiency field of the cluster_space_block_storage_medias. """

    efficiency_without_snapshots = marshmallow_fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", unknown=EXCLUDE, data_key="efficiency_without_snapshots", allow_none=True)
    r""" The efficiency_without_snapshots field of the cluster_space_block_storage_medias. """

    efficiency_without_snapshots_flexclones = marshmallow_fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", unknown=EXCLUDE, data_key="efficiency_without_snapshots_flexclones", allow_none=True)
    r""" The efficiency_without_snapshots_flexclones field of the cluster_space_block_storage_medias. """

    physical_used = Size(data_key="physical_used", allow_none=True)
    r""" Total physical used space across the cluster based on media type. """

    size = Size(data_key="size", allow_none=True)
    r""" Total space across the cluster based on media type. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type of media being used.

Valid choices:

* hdd
* hybrid
* lun
* ssd
* vmdisk """

    used = Size(data_key="used", allow_none=True)
    r""" Used space across the cluster based on media type.
### Platform Specifics

* **Unified ONTAP**: Available for GET requests.
* **ASA r2**: This property is not applicable, it is not available in the REST API and is not reported for GET requests. """

    @property
    def resource(self):
        return ClusterSpaceBlockStorageMedias

    gettable_fields = [
        "available",
        "efficiency",
        "efficiency_without_snapshots",
        "efficiency_without_snapshots_flexclones",
        "physical_used",
        "size",
        "type",
        "used",
    ]
    """available,efficiency,efficiency_without_snapshots,efficiency_without_snapshots_flexclones,physical_used,size,type,used,"""

    patchable_fields = [
        "available",
        "efficiency",
        "efficiency_without_snapshots",
        "efficiency_without_snapshots_flexclones",
        "physical_used",
        "size",
        "type",
        "used",
    ]
    """available,efficiency,efficiency_without_snapshots,efficiency_without_snapshots_flexclones,physical_used,size,type,used,"""

    postable_fields = [
        "available",
        "efficiency",
        "efficiency_without_snapshots",
        "efficiency_without_snapshots_flexclones",
        "physical_used",
        "size",
        "type",
        "used",
    ]
    """available,efficiency,efficiency_without_snapshots,efficiency_without_snapshots_flexclones,physical_used,size,type,used,"""


class ClusterSpaceBlockStorageMedias(Resource):

    _schema = ClusterSpaceBlockStorageMediasSchema
