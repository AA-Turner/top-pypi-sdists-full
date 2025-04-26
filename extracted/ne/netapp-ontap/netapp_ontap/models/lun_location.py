r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunLocation", "LunLocationSchema"]
__pdoc__ = {
    "LunLocationSchema.resource": False,
    "LunLocationSchema.opts": False,
    "LunLocation": False,
}


class LunLocationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunLocation object"""

    logical_unit = marshmallow_fields.Str(data_key="logical_unit", allow_none=True)
    r""" * **Unified ONTAP**:
The base name component of the LUN. Valid in POST and PATCH.<br/>
If properties `name` and `location.logical_unit` are specified in the same request, they must refer to the base name.<br/>
A PATCH that modifies the base name of the LUN is considered a rename operation.

* **ASA r2**:
The volume logical unit property is read-only and cannot be set in POST or PATCH. Use the `name` property for POST.


Example: lun1 """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the lun_location. """

    qtree = marshmallow_fields.Nested("netapp_ontap.resources.qtree.QtreeSchema", unknown=EXCLUDE, data_key="qtree", allow_none=True)
    r""" The qtree field of the lun_location. """

    storage_availability_zone = marshmallow_fields.Nested("netapp_ontap.resources.storage_availability_zone.StorageAvailabilityZoneSchema", unknown=EXCLUDE, data_key="storage_availability_zone", allow_none=True)
    r""" The storage_availability_zone field of the lun_location. """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the lun_location. """

    @property
    def resource(self):
        return LunLocation

    gettable_fields = [
        "logical_unit",
        "node.links",
        "node.name",
        "node.uuid",
        "qtree.links",
        "qtree.id",
        "qtree.name",
        "storage_availability_zone.links",
        "storage_availability_zone.name",
        "storage_availability_zone.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """logical_unit,node.links,node.name,node.uuid,qtree.links,qtree.id,qtree.name,storage_availability_zone.links,storage_availability_zone.name,storage_availability_zone.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "logical_unit",
        "qtree.id",
        "qtree.name",
        "volume.name",
        "volume.uuid",
    ]
    """logical_unit,qtree.id,qtree.name,volume.name,volume.uuid,"""

    postable_fields = [
        "logical_unit",
        "qtree.id",
        "qtree.name",
        "storage_availability_zone.name",
        "storage_availability_zone.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """logical_unit,qtree.id,qtree.name,storage_availability_zone.name,storage_availability_zone.uuid,volume.name,volume.uuid,"""


class LunLocation(Resource):

    _schema = LunLocationSchema
