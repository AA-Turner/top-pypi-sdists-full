r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["OracleRacOnNfsGridBinary", "OracleRacOnNfsGridBinarySchema"]
__pdoc__ = {
    "OracleRacOnNfsGridBinarySchema.resource": False,
    "OracleRacOnNfsGridBinarySchema.opts": False,
    "OracleRacOnNfsGridBinary": False,
}


class OracleRacOnNfsGridBinarySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the OracleRacOnNfsGridBinary object"""

    size = Size(data_key="size", allow_none=True)
    r""" The size of the Oracle grid binary storage volume. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.oracle_rac_on_nfs_grid_binary_storage_service.OracleRacOnNfsGridBinaryStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the oracle_rac_on_nfs_grid_binary. """

    @property
    def resource(self):
        return OracleRacOnNfsGridBinary

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


class OracleRacOnNfsGridBinary(Resource):

    _schema = OracleRacOnNfsGridBinarySchema
