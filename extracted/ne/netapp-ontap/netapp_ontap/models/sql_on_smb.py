r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SqlOnSmb", "SqlOnSmbSchema"]
__pdoc__ = {
    "SqlOnSmbSchema.resource": False,
    "SqlOnSmbSchema.opts": False,
    "SqlOnSmb": False,
}


class SqlOnSmbSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SqlOnSmb object"""

    access = marshmallow_fields.Nested("netapp_ontap.models.sql_on_smb_access.SqlOnSmbAccessSchema", unknown=EXCLUDE, data_key="access", allow_none=True)
    r""" The access field of the sql_on_smb. """

    db = marshmallow_fields.Nested("netapp_ontap.models.sql_on_san_db.SqlOnSanDbSchema", unknown=EXCLUDE, data_key="db", allow_none=True)
    r""" The db field of the sql_on_smb. """

    log = marshmallow_fields.Nested("netapp_ontap.models.sql_on_san_log.SqlOnSanLogSchema", unknown=EXCLUDE, data_key="log", allow_none=True)
    r""" The log field of the sql_on_smb. """

    protection_type = marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_protection_type.MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE, data_key="protection_type", allow_none=True)
    r""" The protection_type field of the sql_on_smb. """

    server_cores_count = Size(data_key="server_cores_count", allow_none=True)
    r""" The number of server cores for the DB. """

    temp_db = marshmallow_fields.Nested("netapp_ontap.models.sql_on_san_temp_db.SqlOnSanTempDbSchema", unknown=EXCLUDE, data_key="temp_db", allow_none=True)
    r""" The temp_db field of the sql_on_smb. """

    @property
    def resource(self):
        return SqlOnSmb

    gettable_fields = [
        "access",
        "db",
        "log",
        "protection_type",
        "server_cores_count",
        "temp_db",
    ]
    """access,db,log,protection_type,server_cores_count,temp_db,"""

    patchable_fields = [
        "db",
        "log",
        "protection_type",
        "temp_db",
    ]
    """db,log,protection_type,temp_db,"""

    postable_fields = [
        "access",
        "db",
        "log",
        "protection_type",
        "server_cores_count",
        "temp_db",
    ]
    """access,db,log,protection_type,server_cores_count,temp_db,"""


class SqlOnSmb(Resource):

    _schema = SqlOnSmbSchema
