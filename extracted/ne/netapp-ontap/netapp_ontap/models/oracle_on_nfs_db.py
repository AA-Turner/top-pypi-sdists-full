r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["OracleOnNfsDb", "OracleOnNfsDbSchema"]
__pdoc__ = {
    "OracleOnNfsDbSchema.resource": False,
    "OracleOnNfsDbSchema.opts": False,
    "OracleOnNfsDb": False,
}


class OracleOnNfsDbSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the OracleOnNfsDb object"""

    size = Size(data_key="size", allow_none=True)
    r""" The size of the database. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_dataset_storage_service.MongoDbOnSanDatasetStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the oracle_on_nfs_db. """

    @property
    def resource(self):
        return OracleOnNfsDb

    gettable_fields = [
        "size",
        "storage_service",
    ]
    """size,storage_service,"""

    patchable_fields = [
        "size",
        "storage_service",
    ]
    """size,storage_service,"""

    postable_fields = [
        "size",
        "storage_service",
    ]
    """size,storage_service,"""


class OracleOnNfsDb(Resource):

    _schema = OracleOnNfsDbSchema
