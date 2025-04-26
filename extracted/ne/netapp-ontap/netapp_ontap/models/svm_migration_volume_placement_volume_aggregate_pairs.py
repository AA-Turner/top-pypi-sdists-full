r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmMigrationVolumePlacementVolumeAggregatePairs", "SvmMigrationVolumePlacementVolumeAggregatePairsSchema"]
__pdoc__ = {
    "SvmMigrationVolumePlacementVolumeAggregatePairsSchema.resource": False,
    "SvmMigrationVolumePlacementVolumeAggregatePairsSchema.opts": False,
    "SvmMigrationVolumePlacementVolumeAggregatePairs": False,
}


class SvmMigrationVolumePlacementVolumeAggregatePairsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationVolumePlacementVolumeAggregatePairs object"""

    aggregate = marshmallow_fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", unknown=EXCLUDE, data_key="aggregate", allow_none=True)
    r""" The aggregate field of the svm_migration_volume_placement_volume_aggregate_pairs. """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the svm_migration_volume_placement_volume_aggregate_pairs. """

    @property
    def resource(self):
        return SvmMigrationVolumePlacementVolumeAggregatePairs

    gettable_fields = [
        "aggregate.links",
        "aggregate.name",
        "aggregate.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """aggregate.links,aggregate.name,aggregate.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "aggregate.name",
        "aggregate.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """aggregate.name,aggregate.uuid,volume.name,volume.uuid,"""

    postable_fields = [
        "aggregate.name",
        "aggregate.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """aggregate.name,aggregate.uuid,volume.name,volume.uuid,"""


class SvmMigrationVolumePlacementVolumeAggregatePairs(Resource):

    _schema = SvmMigrationVolumePlacementVolumeAggregatePairsSchema
