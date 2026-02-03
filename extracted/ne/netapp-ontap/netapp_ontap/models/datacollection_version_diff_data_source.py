r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DatacollectionVersionDiffDataSource", "DatacollectionVersionDiffDataSourceSchema"]
__pdoc__ = {
    "DatacollectionVersionDiffDataSourceSchema.resource": False,
    "DatacollectionVersionDiffDataSourceSchema.opts": False,
    "DatacollectionVersionDiffDataSource": False,
}

class DatacollectionVersionDiffDataSourceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionVersionDiffDataSource object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the data source.

Example: volume 1 """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type of the data source.

Valid choices:

* volume
* bucket """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the data source.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return DatacollectionVersionDiffDataSource

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


class DatacollectionVersionDiffDataSource(Resource):

    _schema = DatacollectionVersionDiffDataSourceSchema
