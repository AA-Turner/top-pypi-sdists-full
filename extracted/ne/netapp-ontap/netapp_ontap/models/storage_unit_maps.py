r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitMaps", "StorageUnitMapsSchema"]
__pdoc__ = {
    "StorageUnitMapsSchema.resource": False,
    "StorageUnitMapsSchema.opts": False,
    "StorageUnitMaps": False,
}


class StorageUnitMapsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitMaps object"""

    host_group = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_maps_host_group.StorageUnitMapsHostGroupSchema", unknown=EXCLUDE, data_key="host_group", allow_none=True)
    r""" A host group mapped to the storage unit. A host group is either an initiator group or an NVMe subsystem. """

    lun_map = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_maps_lun_map.StorageUnitMapsLunMapSchema", unknown=EXCLUDE, data_key="lun_map", allow_none=True)
    r""" A map between the storage unit and an initiator group. """

    subsystem_map = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_maps_subsystem_map.StorageUnitMapsSubsystemMapSchema", unknown=EXCLUDE, data_key="subsystem_map", allow_none=True)
    r""" A map between the storage unit and an NVMe subsystem. """

    @property
    def resource(self):
        return StorageUnitMaps

    gettable_fields = [
        "host_group",
        "lun_map",
        "subsystem_map",
    ]
    """host_group,lun_map,subsystem_map,"""

    patchable_fields = [
        "host_group",
        "lun_map",
        "subsystem_map",
    ]
    """host_group,lun_map,subsystem_map,"""

    postable_fields = [
        "host_group",
        "lun_map",
        "subsystem_map",
    ]
    """host_group,lun_map,subsystem_map,"""


class StorageUnitMaps(Resource):

    _schema = StorageUnitMapsSchema
