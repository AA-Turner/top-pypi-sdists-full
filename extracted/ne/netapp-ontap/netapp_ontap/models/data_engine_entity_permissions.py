r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineEntityPermissions", "DataEngineEntityPermissionsSchema"]
__pdoc__ = {
    "DataEngineEntityPermissionsSchema.resource": False,
    "DataEngineEntityPermissionsSchema.opts": False,
    "DataEngineEntityPermissions": False,
}

class DataEngineEntityPermissionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineEntityPermissions object"""

    key = marshmallow_fields.Str(data_key="key", allow_none=True)
    r""" The key field of the data_engine_entity_permissions.

Example: owner """

    value = marshmallow_fields.Str(data_key="value", allow_none=True)
    r""" The value field of the data_engine_entity_permissions.

Example: rwx """

    @property
    def resource(self):
        return DataEngineEntityPermissions

    gettable_fields = [
        "key",
        "value",
    ]
    """key,value,"""

    patchable_fields = [
        "key",
        "value",
    ]
    """key,value,"""

    postable_fields = [
        "key",
        "value",
    ]
    """key,value,"""


class DataEngineEntityPermissions(Resource):

    _schema = DataEngineEntityPermissionsSchema
