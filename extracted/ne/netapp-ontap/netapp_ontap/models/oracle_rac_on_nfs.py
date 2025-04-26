r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["OracleRacOnNfs", "OracleRacOnNfsSchema"]
__pdoc__ = {
    "OracleRacOnNfsSchema.resource": False,
    "OracleRacOnNfsSchema.opts": False,
    "OracleRacOnNfs": False,
}


class OracleRacOnNfsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the OracleRacOnNfs object"""

    archive_log = marshmallow_fields.Nested("netapp_ontap.models.oracle_on_nfs_archive_log.OracleOnNfsArchiveLogSchema", unknown=EXCLUDE, data_key="archive_log", allow_none=True)
    r""" The archive_log field of the oracle_rac_on_nfs. """

    db = marshmallow_fields.Nested("netapp_ontap.models.oracle_on_nfs_db.OracleOnNfsDbSchema", unknown=EXCLUDE, data_key="db", allow_none=True)
    r""" The db field of the oracle_rac_on_nfs. """

    grid_binary = marshmallow_fields.Nested("netapp_ontap.models.oracle_rac_on_nfs_grid_binary.OracleRacOnNfsGridBinarySchema", unknown=EXCLUDE, data_key="grid_binary", allow_none=True)
    r""" The grid_binary field of the oracle_rac_on_nfs. """

    nfs_access = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.app_nfs_access.AppNfsAccessSchema", unknown=EXCLUDE, allow_none=True), data_key="nfs_access", allow_none=True)
    r""" The list of NFS access controls. You must provide either 'host' or 'access' to enable NFS access. """

    ora_home = marshmallow_fields.Nested("netapp_ontap.models.oracle_on_nfs_ora_home.OracleOnNfsOraHomeSchema", unknown=EXCLUDE, data_key="ora_home", allow_none=True)
    r""" The ora_home field of the oracle_rac_on_nfs. """

    oracle_crs = marshmallow_fields.Nested("netapp_ontap.models.oracle_rac_on_nfs_oracle_crs.OracleRacOnNfsOracleCrsSchema", unknown=EXCLUDE, data_key="oracle_crs", allow_none=True)
    r""" The oracle_crs field of the oracle_rac_on_nfs. """

    protection_type = marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_protection_type.MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE, data_key="protection_type", allow_none=True)
    r""" The protection_type field of the oracle_rac_on_nfs. """

    redo_log = marshmallow_fields.Nested("netapp_ontap.models.oracle_on_nfs_redo_log.OracleOnNfsRedoLogSchema", unknown=EXCLUDE, data_key="redo_log", allow_none=True)
    r""" The redo_log field of the oracle_rac_on_nfs. """

    @property
    def resource(self):
        return OracleRacOnNfs

    gettable_fields = [
        "archive_log",
        "db",
        "grid_binary",
        "nfs_access",
        "ora_home",
        "oracle_crs",
        "protection_type",
        "redo_log",
    ]
    """archive_log,db,grid_binary,nfs_access,ora_home,oracle_crs,protection_type,redo_log,"""

    patchable_fields = [
        "archive_log",
        "db",
        "grid_binary",
        "ora_home",
        "oracle_crs",
        "protection_type",
        "redo_log",
    ]
    """archive_log,db,grid_binary,ora_home,oracle_crs,protection_type,redo_log,"""

    postable_fields = [
        "archive_log",
        "db",
        "grid_binary",
        "nfs_access",
        "ora_home",
        "oracle_crs",
        "protection_type",
        "redo_log",
    ]
    """archive_log,db,grid_binary,nfs_access,ora_home,oracle_crs,protection_type,redo_log,"""


class OracleRacOnNfs(Resource):

    _schema = OracleRacOnNfsSchema
