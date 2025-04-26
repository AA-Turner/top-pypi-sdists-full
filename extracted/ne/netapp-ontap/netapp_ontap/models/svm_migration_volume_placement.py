r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmMigrationVolumePlacement", "SvmMigrationVolumePlacementSchema"]
__pdoc__ = {
    "SvmMigrationVolumePlacementSchema.resource": False,
    "SvmMigrationVolumePlacementSchema.opts": False,
    "SvmMigrationVolumePlacement": False,
}


class SvmMigrationVolumePlacementSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationVolumePlacement object"""

    aggregates = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.svm_migration_destination_volume_placement_aggregates.SvmMigrationDestinationVolumePlacementAggregatesSchema", unknown=EXCLUDE, allow_none=True), data_key="aggregates", allow_none=True)
    r""" Optional property used to specify the list of desired aggregates to use for volume creation in the destination. """

    volume_aggregate_pairs = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.svm_migration_destination_volume_placement_volume_aggregate_pairs.SvmMigrationDestinationVolumePlacementVolumeAggregatePairsSchema", unknown=EXCLUDE, allow_none=True), data_key="volume_aggregate_pairs", allow_none=True)
    r""" Optional property used to specify the list of desired volume-aggregate pairs in the destination. """

    @property
    def resource(self):
        return SvmMigrationVolumePlacement

    gettable_fields = [
        "aggregates.links",
        "aggregates.name",
        "aggregates.uuid",
        "volume_aggregate_pairs",
    ]
    """aggregates.links,aggregates.name,aggregates.uuid,volume_aggregate_pairs,"""

    patchable_fields = [
        "volume_aggregate_pairs",
    ]
    """volume_aggregate_pairs,"""

    postable_fields = [
        "aggregates.name",
        "aggregates.uuid",
        "volume_aggregate_pairs",
    ]
    """aggregates.name,aggregates.uuid,volume_aggregate_pairs,"""


class SvmMigrationVolumePlacement(Resource):

    _schema = SvmMigrationVolumePlacementSchema
