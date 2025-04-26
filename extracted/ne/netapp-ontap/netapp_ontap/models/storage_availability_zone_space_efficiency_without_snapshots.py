r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageAvailabilityZoneSpaceEfficiencyWithoutSnapshots", "StorageAvailabilityZoneSpaceEfficiencyWithoutSnapshotsSchema"]
__pdoc__ = {
    "StorageAvailabilityZoneSpaceEfficiencyWithoutSnapshotsSchema.resource": False,
    "StorageAvailabilityZoneSpaceEfficiencyWithoutSnapshotsSchema.opts": False,
    "StorageAvailabilityZoneSpaceEfficiencyWithoutSnapshots": False,
}


class StorageAvailabilityZoneSpaceEfficiencyWithoutSnapshotsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageAvailabilityZoneSpaceEfficiencyWithoutSnapshots object"""

    ratio = marshmallow_fields.Number(data_key="ratio", allow_none=True)
    r""" Data reduction ratio (logical_used_without_snapshot / physical_used_without_snapshot) """

    savings = Size(data_key="savings", allow_none=True)
    r""" Space saved by storage efficiencies (logical_used_without_snapshot - physical_used_without_snapshot) """

    @property
    def resource(self):
        return StorageAvailabilityZoneSpaceEfficiencyWithoutSnapshots

    gettable_fields = [
        "ratio",
        "savings",
    ]
    """ratio,savings,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class StorageAvailabilityZoneSpaceEfficiencyWithoutSnapshots(Resource):

    _schema = StorageAvailabilityZoneSpaceEfficiencyWithoutSnapshotsSchema
