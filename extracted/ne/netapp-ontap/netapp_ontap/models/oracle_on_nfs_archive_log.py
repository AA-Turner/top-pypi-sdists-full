r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["OracleOnNfsArchiveLog", "OracleOnNfsArchiveLogSchema"]
__pdoc__ = {
    "OracleOnNfsArchiveLogSchema.resource": False,
    "OracleOnNfsArchiveLogSchema.opts": False,
    "OracleOnNfsArchiveLog": False,
}


class OracleOnNfsArchiveLogSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the OracleOnNfsArchiveLog object"""

    size = Size(data_key="size", allow_none=True)
    r""" The size of the archive log. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.oracle_on_nfs_archive_log_storage_service.OracleOnNfsArchiveLogStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the oracle_on_nfs_archive_log. """

    @property
    def resource(self):
        return OracleOnNfsArchiveLog

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


class OracleOnNfsArchiveLog(Resource):

    _schema = OracleOnNfsArchiveLogSchema
