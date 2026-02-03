r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["StoragePoolDisk", "StoragePoolDiskSchema"]
__pdoc__ = {
    "StoragePoolDiskSchema.resource": False,
    "StoragePoolDiskSchema.opts": False,
    "StoragePoolDisk": False,
}

class StoragePoolDiskSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StoragePoolDisk object"""

    disk = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.disk", "DiskSchema"),
                unknown=EXCLUDE,
                data_key="disk",
                allow_none=True
            )
    r""" The disk field of the storage_pool_disk. """

    total_size = Size(data_key="total_size", allow_none=True)
    r""" Raw capacity of the disk, in bytes. """

    usable_size = Size(data_key="usable_size", allow_none=True)
    r""" Usable capacity of this disk, in bytes. """

    @property
    def resource(self):
        return StoragePoolDisk

    gettable_fields = [
        "disk.links",
        "disk.name",
        "total_size",
        "usable_size",
    ]
    """disk.links,disk.name,total_size,usable_size,"""

    patchable_fields = [
        "disk.name",
    ]
    """disk.name,"""

    postable_fields = [
        "disk.name",
    ]
    """disk.name,"""


class StoragePoolDisk(Resource):

    _schema = StoragePoolDiskSchema
