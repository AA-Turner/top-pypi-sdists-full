r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DatacollectionVersionDataCollectionVersion", "DatacollectionVersionDataCollectionVersionSchema"]
__pdoc__ = {
    "DatacollectionVersionDataCollectionVersionSchema.resource": False,
    "DatacollectionVersionDataCollectionVersionSchema.opts": False,
    "DatacollectionVersionDataCollectionVersion": False,
}

class DatacollectionVersionDataCollectionVersionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionVersionDataCollectionVersion object"""

    job = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_version_job", "DataEngineVersionJobSchema"),
                unknown=EXCLUDE,
                data_key="job",
                allow_none=True
            )
    r""" The version job details. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the version.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return DatacollectionVersionDataCollectionVersion

    gettable_fields = [
        "job",
        "uuid",
    ]
    """job,uuid,"""

    patchable_fields = [
        "uuid",
    ]
    """uuid,"""

    postable_fields = [
        "uuid",
    ]
    """uuid,"""


class DatacollectionVersionDataCollectionVersion(Resource):

    _schema = DatacollectionVersionDataCollectionVersionSchema
