r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineEventResource", "DataEngineEventResourceSchema"]
__pdoc__ = {
    "DataEngineEventResourceSchema.resource": False,
    "DataEngineEventResourceSchema.opts": False,
    "DataEngineEventResource": False,
}

class DataEngineEventResourceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineEventResource object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the resource.

Example: Workspace 1 """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type of the data engine resource.

Valid choices:

* workspace
* data_source
* data_collection
* policy
* custom """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the resource.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return DataEngineEventResource

    gettable_fields = [
        "name",
        "type",
        "uuid",
    ]
    """name,type,uuid,"""

    patchable_fields = [
        "name",
        "type",
        "uuid",
    ]
    """name,type,uuid,"""

    postable_fields = [
        "name",
        "type",
        "uuid",
    ]
    """name,type,uuid,"""


class DataEngineEventResource(Resource):

    _schema = DataEngineEventResourceSchema
