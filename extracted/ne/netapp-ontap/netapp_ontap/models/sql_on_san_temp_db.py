r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SqlOnSanTempDb", "SqlOnSanTempDbSchema"]
__pdoc__ = {
    "SqlOnSanTempDbSchema.resource": False,
    "SqlOnSanTempDbSchema.opts": False,
    "SqlOnSanTempDb": False,
}


class SqlOnSanTempDbSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SqlOnSanTempDb object"""

    size = Size(data_key="size", allow_none=True)
    r""" The size of the temp DB. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.sql_on_san_temp_db_storage_service.SqlOnSanTempDbStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the sql_on_san_temp_db. """

    @property
    def resource(self):
        return SqlOnSanTempDb

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


class SqlOnSanTempDb(Resource):

    _schema = SqlOnSanTempDbSchema
