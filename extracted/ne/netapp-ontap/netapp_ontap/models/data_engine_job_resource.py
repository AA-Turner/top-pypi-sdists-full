r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineJobResource", "DataEngineJobResourceSchema"]
__pdoc__ = {
    "DataEngineJobResourceSchema.resource": False,
    "DataEngineJobResourceSchema.opts": False,
    "DataEngineJobResource": False,
}

class DataEngineJobResourceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineJobResource object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the data engine resource.

Example: workspace_1 """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type of the data engine resource.

Valid choices:

* workspace
* data_source
* data_collection
* policy
* entity """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the data engine resource.

Example: 123e4567-e89b-12d3-a456-426614173000 """

    @property
    def resource(self):
        return DataEngineJobResource

    gettable_fields = [
        "name",
        "type",
        "uuid",
    ]
    """name,type,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DataEngineJobResource(Resource):

    _schema = DataEngineJobResourceSchema
