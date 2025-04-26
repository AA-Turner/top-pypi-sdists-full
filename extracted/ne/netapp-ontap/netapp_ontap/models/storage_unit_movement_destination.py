r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitMovementDestination", "StorageUnitMovementDestinationSchema"]
__pdoc__ = {
    "StorageUnitMovementDestinationSchema.resource": False,
    "StorageUnitMovementDestinationSchema.opts": False,
    "StorageUnitMovementDestination": False,
}


class StorageUnitMovementDestinationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitMovementDestination object"""

    storage_availability_zone = marshmallow_fields.Nested("netapp_ontap.resources.storage_availability_zone.StorageAvailabilityZoneSchema", unknown=EXCLUDE, data_key="storage_availability_zone", allow_none=True)
    r""" The storage_availability_zone field of the storage_unit_movement_destination. """

    @property
    def resource(self):
        return StorageUnitMovementDestination

    gettable_fields = [
        "storage_availability_zone.links",
        "storage_availability_zone.name",
        "storage_availability_zone.uuid",
    ]
    """storage_availability_zone.links,storage_availability_zone.name,storage_availability_zone.uuid,"""

    patchable_fields = [
        "storage_availability_zone.name",
        "storage_availability_zone.uuid",
    ]
    """storage_availability_zone.name,storage_availability_zone.uuid,"""

    postable_fields = [
        "storage_availability_zone.name",
        "storage_availability_zone.uuid",
    ]
    """storage_availability_zone.name,storage_availability_zone.uuid,"""


class StorageUnitMovementDestination(Resource):

    _schema = StorageUnitMovementDestinationSchema
