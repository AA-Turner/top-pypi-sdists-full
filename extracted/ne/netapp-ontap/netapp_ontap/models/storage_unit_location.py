r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitLocation", "StorageUnitLocationSchema"]
__pdoc__ = {
    "StorageUnitLocationSchema.resource": False,
    "StorageUnitLocationSchema.opts": False,
    "StorageUnitLocation": False,
}


class StorageUnitLocationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitLocation object"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the storage_unit_location. """

    storage_availability_zone = marshmallow_fields.Nested("netapp_ontap.resources.storage_availability_zone.StorageAvailabilityZoneSchema", unknown=EXCLUDE, data_key="storage_availability_zone", allow_none=True)
    r""" The storage_availability_zone field of the storage_unit_location. """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the storage_unit_location. """

    @property
    def resource(self):
        return StorageUnitLocation

    gettable_fields = [
        "node.links",
        "node.name",
        "node.uuid",
        "storage_availability_zone.links",
        "storage_availability_zone.name",
        "storage_availability_zone.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """node.links,node.name,node.uuid,storage_availability_zone.links,storage_availability_zone.name,storage_availability_zone.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "storage_availability_zone.name",
        "storage_availability_zone.uuid",
    ]
    """storage_availability_zone.name,storage_availability_zone.uuid,"""

    postable_fields = [
    ]
    """"""


class StorageUnitLocation(Resource):

    _schema = StorageUnitLocationSchema
