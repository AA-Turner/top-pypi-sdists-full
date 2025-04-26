r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitCloneSource", "StorageUnitCloneSourceSchema"]
__pdoc__ = {
    "StorageUnitCloneSourceSchema.resource": False,
    "StorageUnitCloneSourceSchema.opts": False,
    "StorageUnitCloneSource": False,
}


class StorageUnitCloneSourceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitCloneSource object"""

    snapshot = marshmallow_fields.Nested("netapp_ontap.resources.snapshot.SnapshotSchema", unknown=EXCLUDE, data_key="snapshot", allow_none=True)
    r""" The snapshot field of the storage_unit_clone_source. """

    storage_unit = marshmallow_fields.Nested("netapp_ontap.resources.storage_unit.StorageUnitSchema", unknown=EXCLUDE, data_key="storage_unit", allow_none=True)
    r""" The storage_unit field of the storage_unit_clone_source. """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the storage_unit_clone_source. """

    @property
    def resource(self):
        return StorageUnitCloneSource

    gettable_fields = [
        "snapshot.links",
        "snapshot.name",
        "snapshot.uuid",
        "storage_unit.links",
        "storage_unit.name",
        "storage_unit.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """snapshot.links,snapshot.name,snapshot.uuid,storage_unit.links,storage_unit.name,storage_unit.uuid,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "snapshot.name",
        "snapshot.uuid",
        "storage_unit.name",
        "storage_unit.uuid",
        "svm.name",
        "svm.uuid",
    ]
    """snapshot.name,snapshot.uuid,storage_unit.name,storage_unit.uuid,svm.name,svm.uuid,"""


class StorageUnitCloneSource(Resource):

    _schema = StorageUnitCloneSourceSchema
