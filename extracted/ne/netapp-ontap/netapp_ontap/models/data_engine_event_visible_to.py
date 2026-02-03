r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineEventVisibleTo", "DataEngineEventVisibleToSchema"]
__pdoc__ = {
    "DataEngineEventVisibleToSchema.resource": False,
    "DataEngineEventVisibleToSchema.opts": False,
    "DataEngineEventVisibleTo": False,
}

class DataEngineEventVisibleToSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineEventVisibleTo object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the user, group, or role.

Example: admin """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Specifies the visibility of the event to a user, group or role.

Valid choices:

* role
* user
* group """

    @property
    def resource(self):
        return DataEngineEventVisibleTo

    gettable_fields = [
        "name",
        "type",
    ]
    """name,type,"""

    patchable_fields = [
        "name",
        "type",
    ]
    """name,type,"""

    postable_fields = [
        "name",
        "type",
    ]
    """name,type,"""


class DataEngineEventVisibleTo(Resource):

    _schema = DataEngineEventVisibleToSchema
