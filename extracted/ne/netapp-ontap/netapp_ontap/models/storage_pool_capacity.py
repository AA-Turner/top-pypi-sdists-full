r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StoragePoolCapacity", "StoragePoolCapacitySchema"]
__pdoc__ = {
    "StoragePoolCapacitySchema.resource": False,
    "StoragePoolCapacitySchema.opts": False,
    "StoragePoolCapacity": False,
}


class StoragePoolCapacitySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StoragePoolCapacity object"""

    disk_count = Size(data_key="disk_count", allow_none=True)
    r""" The number of disks in the storage pool. """

    disks = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_pool_disk.StoragePoolDiskSchema", unknown=EXCLUDE, allow_none=True), data_key="disks", allow_none=True)
    r""" Properties of each disk used in the shared storage pool. """

    remaining = Size(data_key="remaining", allow_none=True)
    r""" Remaining usable capacity in the flash pool, in bytes. """

    spare_allocation_units = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_pool_spare_allocation_unit.StoragePoolSpareAllocationUnitSchema", unknown=EXCLUDE, allow_none=True), data_key="spare_allocation_units", allow_none=True)
    r""" Properties of spare allocation units. """

    total = Size(data_key="total", allow_none=True)
    r""" Total size of the flash pool, in bytes. """

    used_allocation_units = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_pool_used_allocation_unit.StoragePoolUsedAllocationUnitSchema", unknown=EXCLUDE, allow_none=True), data_key="used_allocation_units", allow_none=True)
    r""" Information about the storage pool allocation units participating in the cache tier of an aggregate. """

    @property
    def resource(self):
        return StoragePoolCapacity

    gettable_fields = [
        "disk_count",
        "disks",
        "remaining",
        "spare_allocation_units",
        "total",
        "used_allocation_units",
    ]
    """disk_count,disks,remaining,spare_allocation_units,total,used_allocation_units,"""

    patchable_fields = [
        "disk_count",
        "disks",
        "spare_allocation_units",
    ]
    """disk_count,disks,spare_allocation_units,"""

    postable_fields = [
        "disk_count",
        "disks",
        "spare_allocation_units",
    ]
    """disk_count,disks,spare_allocation_units,"""


class StoragePoolCapacity(Resource):

    _schema = StoragePoolCapacitySchema
