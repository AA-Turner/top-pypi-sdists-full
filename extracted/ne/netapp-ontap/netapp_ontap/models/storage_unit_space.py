r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitSpace", "StorageUnitSpaceSchema"]
__pdoc__ = {
    "StorageUnitSpaceSchema.resource": False,
    "StorageUnitSpaceSchema.opts": False,
    "StorageUnitSpace": False,
}


class StorageUnitSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitSpace object"""

    efficiency_ratio = marshmallow_fields.Number(data_key="efficiency_ratio", allow_none=True)
    r""" The storage efficiency ratio of the storage unit without snapshots. (Logical Used / Used)


Example: 2.5 """

    physical_used = Size(data_key="physical_used", allow_none=True)
    r""" The number of bytes consumed on the disk by the storage unit, excluding snapshots.


Example: 1073741824 """

    physical_used_by_snapshots = Size(data_key="physical_used_by_snapshots", allow_none=True)
    r""" The number of bytes consumed on the disk by the storage unit's snapshots.


Example: 1073741824 """

    size = Size(data_key="size", allow_none=True)
    r""" The total provisioned size of the storage unit. The storage unit size can be increased but not decreased using the /api/storage/luns or /api/storage/namespaces endpoints.<br/>
The maximum and minimum sizes listed here are the absolute maximum and absolute minimum sizes, in bytes. The actual minimum and maximum sizes vary depending on the ONTAP version, ONTAP platform and the available space.<br/>
For more information, see _Size properties_ in the _docs_ section of the ONTAP REST API documentation.


Example: 1073741824 """

    used = Size(data_key="used", allow_none=True)
    r""" The amount of space consumed by the main data stream of the storage unit.<br/>
This value is the total space consumed, including filesystem overhead, but excluding prefix and suffix streams. Due to internal filesystem overhead and the many ways SAN filesystems and applications utilize blocks within a LUN or namespace, this value does not necessarily reflect actual consumption/availability from the perspective of the filesystem or application. Without specific knowledge of how the LUN or namespace blocks are utilized outside of ONTAP, this property should not be used as an indicator for an out-of-space condition.<br/>
For more information, see _Size properties_ in the _docs_ section of the ONTAP REST API documentation. """

    @property
    def resource(self):
        return StorageUnitSpace

    gettable_fields = [
        "efficiency_ratio",
        "physical_used",
        "physical_used_by_snapshots",
        "size",
        "used",
    ]
    """efficiency_ratio,physical_used,physical_used_by_snapshots,size,used,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class StorageUnitSpace(Resource):

    _schema = StorageUnitSpaceSchema
