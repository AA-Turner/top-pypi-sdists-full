r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["OracleRacOnNfsOracleCrs", "OracleRacOnNfsOracleCrsSchema"]
__pdoc__ = {
    "OracleRacOnNfsOracleCrsSchema.resource": False,
    "OracleRacOnNfsOracleCrsSchema.opts": False,
    "OracleRacOnNfsOracleCrs": False,
}


class OracleRacOnNfsOracleCrsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the OracleRacOnNfsOracleCrs object"""

    copies = Size(data_key="copies", allow_none=True)
    r""" The number of CRS volumes. """

    size = Size(data_key="size", allow_none=True)
    r""" The size of the Oracle CRS/voting storage volume. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.oracle_rac_on_nfs_oracle_crs_storage_service.OracleRacOnNfsOracleCrsStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the oracle_rac_on_nfs_oracle_crs. """

    @property
    def resource(self):
        return OracleRacOnNfsOracleCrs

    gettable_fields = [
        "copies",
        "size",
        "storage_service",
    ]
    """copies,size,storage_service,"""

    patchable_fields = [
        "storage_service",
    ]
    """storage_service,"""

    postable_fields = [
        "copies",
        "size",
        "storage_service",
    ]
    """copies,size,storage_service,"""


class OracleRacOnNfsOracleCrs(Resource):

    _schema = OracleRacOnNfsOracleCrsSchema
