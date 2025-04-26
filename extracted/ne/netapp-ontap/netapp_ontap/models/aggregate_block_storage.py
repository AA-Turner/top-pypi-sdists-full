r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateBlockStorage", "AggregateBlockStorageSchema"]
__pdoc__ = {
    "AggregateBlockStorageSchema.resource": False,
    "AggregateBlockStorageSchema.opts": False,
    "AggregateBlockStorage": False,
}


class AggregateBlockStorageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateBlockStorage object"""

    hybrid_cache = marshmallow_fields.Nested("netapp_ontap.models.aggregate_block_storage_hybrid_cache.AggregateBlockStorageHybridCacheSchema", unknown=EXCLUDE, data_key="hybrid_cache", allow_none=True)
    r""" Contains the configuration for the hybrid cache. The hybrid cache is made up of either whole SSDs or storage pool SSDs. """

    mirror = marshmallow_fields.Nested("netapp_ontap.models.aggregate_block_storage_mirror.AggregateBlockStorageMirrorSchema", unknown=EXCLUDE, data_key="mirror", allow_none=True)
    r""" The mirror field of the aggregate_block_storage. """

    plexes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.plex.PlexSchema", unknown=EXCLUDE, allow_none=True), data_key="plexes", allow_none=True)
    r""" Plex reference for each plex in the aggregate. """

    primary = marshmallow_fields.Nested("netapp_ontap.models.aggregate_block_storage_primary.AggregateBlockStoragePrimarySchema", unknown=EXCLUDE, data_key="primary", allow_none=True)
    r""" Configuration information for the primary storage portion of the aggregate. This excludes the hybrid cache details. """

    storage_type = marshmallow_fields.Str(data_key="storage_type", allow_none=True)
    r""" Type of aggregate.

Valid choices:

* hdd
* hybrid
* lun
* ssd
* vmdisk """

    uses_partitions = marshmallow_fields.Boolean(data_key="uses_partitions", allow_none=True)
    r""" If true, aggregate is using shared disks. """

    @property
    def resource(self):
        return AggregateBlockStorage

    gettable_fields = [
        "hybrid_cache",
        "mirror",
        "plexes",
        "primary",
        "storage_type",
        "uses_partitions",
    ]
    """hybrid_cache,mirror,plexes,primary,storage_type,uses_partitions,"""

    patchable_fields = [
        "mirror",
        "primary",
    ]
    """mirror,primary,"""

    postable_fields = [
        "mirror",
        "primary",
    ]
    """mirror,primary,"""


class AggregateBlockStorage(Resource):

    _schema = AggregateBlockStorageSchema
