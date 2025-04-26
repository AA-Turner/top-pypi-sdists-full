r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["OracleOnNfsRedoLog", "OracleOnNfsRedoLogSchema"]
__pdoc__ = {
    "OracleOnNfsRedoLogSchema.resource": False,
    "OracleOnNfsRedoLogSchema.opts": False,
    "OracleOnNfsRedoLog": False,
}


class OracleOnNfsRedoLogSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the OracleOnNfsRedoLog object"""

    mirrored = marshmallow_fields.Boolean(data_key="mirrored", allow_none=True)
    r""" Specifies whether the redo log group should be mirrored. """

    size = Size(data_key="size", allow_none=True)
    r""" The size of the redo log group. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.oracle_on_nfs_redo_log_storage_service.OracleOnNfsRedoLogStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the oracle_on_nfs_redo_log. """

    @property
    def resource(self):
        return OracleOnNfsRedoLog

    gettable_fields = [
        "mirrored",
        "size",
        "storage_service",
    ]
    """mirrored,size,storage_service,"""

    patchable_fields = [
        "size",
        "storage_service",
    ]
    """size,storage_service,"""

    postable_fields = [
        "mirrored",
        "size",
        "storage_service",
    ]
    """mirrored,size,storage_service,"""


class OracleOnNfsRedoLog(Resource):

    _schema = OracleOnNfsRedoLogSchema
