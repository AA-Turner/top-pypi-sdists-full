r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitMapsLunMap", "StorageUnitMapsLunMapSchema"]
__pdoc__ = {
    "StorageUnitMapsLunMapSchema.resource": False,
    "StorageUnitMapsLunMapSchema.opts": False,
    "StorageUnitMapsLunMap": False,
}


class StorageUnitMapsLunMapSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitMapsLunMap object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the storage_unit_maps_lun_map. """

    igroup = marshmallow_fields.Nested("netapp_ontap.resources.igroup.IgroupSchema", unknown=EXCLUDE, data_key="igroup", allow_none=True)
    r""" The igroup field of the storage_unit_maps_lun_map. """

    logical_unit_number = Size(data_key="logical_unit_number", allow_none=True)
    r""" The logical unit number assigned to the LUN when mapped to the specified initiator group. The number is used to identify the LUN to initiators in the initiator group when communicating through Fibre Channel Protocol or iSCSI.


Example: 1 """

    @property
    def resource(self):
        return StorageUnitMapsLunMap

    gettable_fields = [
        "links",
        "igroup.links",
        "igroup.name",
        "igroup.uuid",
        "logical_unit_number",
    ]
    """links,igroup.links,igroup.name,igroup.uuid,logical_unit_number,"""

    patchable_fields = [
        "igroup.name",
        "igroup.uuid",
    ]
    """igroup.name,igroup.uuid,"""

    postable_fields = [
        "igroup.name",
        "igroup.uuid",
    ]
    """igroup.name,igroup.uuid,"""


class StorageUnitMapsLunMap(Resource):

    _schema = StorageUnitMapsLunMapSchema
