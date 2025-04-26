r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SqlOnSan", "SqlOnSanSchema"]
__pdoc__ = {
    "SqlOnSanSchema.resource": False,
    "SqlOnSanSchema.opts": False,
    "SqlOnSan": False,
}


class SqlOnSanSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SqlOnSan object"""

    db = marshmallow_fields.Nested("netapp_ontap.models.sql_on_san_db.SqlOnSanDbSchema", unknown=EXCLUDE, data_key="db", allow_none=True)
    r""" The db field of the sql_on_san. """

    igroup_name = marshmallow_fields.Str(data_key="igroup_name", allow_none=True)
    r""" The name of the initiator group through which the contents of this application will be accessed. Modification of this parameter is a disruptive operation. All LUNs in the application component will be unmapped from the current igroup and re-mapped to the new igroup. """

    log = marshmallow_fields.Nested("netapp_ontap.models.sql_on_san_log.SqlOnSanLogSchema", unknown=EXCLUDE, data_key="log", allow_none=True)
    r""" The log field of the sql_on_san. """

    new_igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.sql_on_san_new_igroups.SqlOnSanNewIgroupsSchema", unknown=EXCLUDE, allow_none=True), data_key="new_igroups", allow_none=True)
    r""" The list of initiator groups to create. """

    os_type = marshmallow_fields.Str(data_key="os_type", allow_none=True)
    r""" The name of the host OS running the application.

Valid choices:

* windows
* windows_2008
* windows_gpt """

    protection_type = marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_protection_type.MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE, data_key="protection_type", allow_none=True)
    r""" The protection_type field of the sql_on_san. """

    server_cores_count = Size(data_key="server_cores_count", allow_none=True)
    r""" The number of server cores for the DB. """

    temp_db = marshmallow_fields.Nested("netapp_ontap.models.sql_on_san_temp_db.SqlOnSanTempDbSchema", unknown=EXCLUDE, data_key="temp_db", allow_none=True)
    r""" The temp_db field of the sql_on_san. """

    @property
    def resource(self):
        return SqlOnSan

    gettable_fields = [
        "db",
        "igroup_name",
        "log",
        "os_type",
        "protection_type",
        "server_cores_count",
        "temp_db",
    ]
    """db,igroup_name,log,os_type,protection_type,server_cores_count,temp_db,"""

    patchable_fields = [
        "db",
        "igroup_name",
        "log",
        "new_igroups",
        "protection_type",
        "temp_db",
    ]
    """db,igroup_name,log,new_igroups,protection_type,temp_db,"""

    postable_fields = [
        "db",
        "igroup_name",
        "log",
        "new_igroups",
        "os_type",
        "protection_type",
        "server_cores_count",
        "temp_db",
    ]
    """db,igroup_name,log,new_igroups,os_type,protection_type,server_cores_count,temp_db,"""


class SqlOnSan(Resource):

    _schema = SqlOnSanSchema
