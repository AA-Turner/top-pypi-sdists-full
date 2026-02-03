r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineEventOwner", "DataEngineEventOwnerSchema"]
__pdoc__ = {
    "DataEngineEventOwnerSchema.resource": False,
    "DataEngineEventOwnerSchema.opts": False,
    "DataEngineEventOwner": False,
}

class DataEngineEventOwnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineEventOwner object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the user or group.

Example: noah """

    @property
    def resource(self):
        return DataEngineEventOwner

    gettable_fields = [
        "name",
    ]
    """name,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class DataEngineEventOwner(Resource):

    _schema = DataEngineEventOwnerSchema
