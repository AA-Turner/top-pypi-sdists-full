r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DatacollectionVersionDiffDataCollection", "DatacollectionVersionDiffDataCollectionSchema"]
__pdoc__ = {
    "DatacollectionVersionDiffDataCollectionSchema.resource": False,
    "DatacollectionVersionDiffDataCollectionSchema.opts": False,
    "DatacollectionVersionDiffDataCollection": False,
}

class DatacollectionVersionDiffDataCollectionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionVersionDiffDataCollection object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the data collection.

Example: Data Collection 1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the data collection.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version_diff_data_collection_version", "DatacollectionVersionDiffDataCollectionVersionSchema"),
                unknown=EXCLUDE,
                data_key="version",
                allow_none=True
            )
    r""" The version information of a data collection. """

    @property
    def resource(self):
        return DatacollectionVersionDiffDataCollection

    gettable_fields = [
        "name",
        "uuid",
        "version",
    ]
    """name,uuid,version,"""

    patchable_fields = [
        "name",
        "uuid",
        "version",
    ]
    """name,uuid,version,"""

    postable_fields = [
        "name",
        "uuid",
        "version",
    ]
    """name,uuid,version,"""


class DatacollectionVersionDiffDataCollection(Resource):

    _schema = DatacollectionVersionDiffDataCollectionSchema
