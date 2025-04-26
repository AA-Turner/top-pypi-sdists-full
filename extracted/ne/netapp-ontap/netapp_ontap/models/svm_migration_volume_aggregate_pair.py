r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmMigrationVolumeAggregatePair", "SvmMigrationVolumeAggregatePairSchema"]
__pdoc__ = {
    "SvmMigrationVolumeAggregatePairSchema.resource": False,
    "SvmMigrationVolumeAggregatePairSchema.opts": False,
    "SvmMigrationVolumeAggregatePair": False,
}


class SvmMigrationVolumeAggregatePairSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationVolumeAggregatePair object"""

    aggregate = marshmallow_fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", unknown=EXCLUDE, data_key="aggregate", allow_none=True)
    r""" The aggregate field of the svm_migration_volume_aggregate_pair. """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the svm_migration_volume_aggregate_pair. """

    @property
    def resource(self):
        return SvmMigrationVolumeAggregatePair

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


class SvmMigrationVolumeAggregatePair(Resource):

    _schema = SvmMigrationVolumeAggregatePairSchema
