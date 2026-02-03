r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["WhoamiPrivileges", "WhoamiPrivilegesSchema"]
__pdoc__ = {
    "WhoamiPrivilegesSchema.resource": False,
    "WhoamiPrivilegesSchema.opts": False,
    "WhoamiPrivileges": False,
}

class WhoamiPrivilegesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WhoamiPrivileges object"""

    access = marshmallow_fields.Str(data_key="access", allow_none=True)
    r""" The access field of the whoami_privileges. """

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" Either of REST URI/endpoint OR command/command directory path.

Example: security login """

    query = marshmallow_fields.Str(data_key="query", allow_none=True)
    r""" Query

Example: -username 'tom' """

    @property
    def resource(self):
        return WhoamiPrivileges

    gettable_fields = [
        "access",
        "path",
        "query",
    ]
    """access,path,query,"""

    patchable_fields = [
        "access",
        "path",
        "query",
    ]
    """access,path,query,"""

    postable_fields = [
        "access",
        "path",
        "query",
    ]
    """access,path,query,"""


class WhoamiPrivileges(Resource):

    _schema = WhoamiPrivilegesSchema
