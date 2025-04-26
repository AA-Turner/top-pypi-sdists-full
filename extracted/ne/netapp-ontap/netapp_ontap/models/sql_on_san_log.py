r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SqlOnSanLog", "SqlOnSanLogSchema"]
__pdoc__ = {
    "SqlOnSanLogSchema.resource": False,
    "SqlOnSanLogSchema.opts": False,
    "SqlOnSanLog": False,
}


class SqlOnSanLogSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SqlOnSanLog object"""

    size = Size(data_key="size", allow_none=True)
    r""" The size of the log DB. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.sql_on_san_log_storage_service.SqlOnSanLogStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the sql_on_san_log. """

    @property
    def resource(self):
        return SqlOnSanLog

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


class SqlOnSanLog(Resource):

    _schema = SqlOnSanLogSchema
