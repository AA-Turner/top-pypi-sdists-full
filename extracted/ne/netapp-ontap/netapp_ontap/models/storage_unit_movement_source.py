r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitMovementSource", "StorageUnitMovementSourceSchema"]
__pdoc__ = {
    "StorageUnitMovementSourceSchema.resource": False,
    "StorageUnitMovementSourceSchema.opts": False,
    "StorageUnitMovementSource": False,
}


class StorageUnitMovementSourceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitMovementSource object"""

    storage_availability_zone = marshmallow_fields.Nested("netapp_ontap.resources.storage_availability_zone.StorageAvailabilityZoneSchema", unknown=EXCLUDE, data_key="storage_availability_zone", allow_none=True)
    r""" The storage_availability_zone field of the storage_unit_movement_source. """

    @property
    def resource(self):
        return StorageUnitMovementSource

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


class StorageUnitMovementSource(Resource):

    _schema = StorageUnitMovementSourceSchema
