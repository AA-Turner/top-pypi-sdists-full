r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitAntiRansomwareSuspectResponseRecords", "StorageUnitAntiRansomwareSuspectResponseRecordsSchema"]
__pdoc__ = {
    "StorageUnitAntiRansomwareSuspectResponseRecordsSchema.resource": False,
    "StorageUnitAntiRansomwareSuspectResponseRecordsSchema.opts": False,
    "StorageUnitAntiRansomwareSuspectResponseRecords": False,
}


class StorageUnitAntiRansomwareSuspectResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitAntiRansomwareSuspectResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the storage_unit_anti_ransomware_suspect_response_records. """

    storage_unit = marshmallow_fields.Nested("netapp_ontap.resources.storage_unit.StorageUnitSchema", unknown=EXCLUDE, data_key="storage_unit", allow_none=True)
    r""" The storage_unit field of the storage_unit_anti_ransomware_suspect_response_records. """

    @property
    def resource(self):
        return StorageUnitAntiRansomwareSuspectResponseRecords

    gettable_fields = [
        "links",
        "storage_unit.links",
        "storage_unit.name",
        "storage_unit.uuid",
    ]
    """links,storage_unit.links,storage_unit.name,storage_unit.uuid,"""

    patchable_fields = [
        "storage_unit.name",
        "storage_unit.uuid",
    ]
    """storage_unit.name,storage_unit.uuid,"""

    postable_fields = [
        "storage_unit.name",
        "storage_unit.uuid",
    ]
    """storage_unit.name,storage_unit.uuid,"""


class StorageUnitAntiRansomwareSuspectResponseRecords(Resource):

    _schema = StorageUnitAntiRansomwareSuspectResponseRecordsSchema
