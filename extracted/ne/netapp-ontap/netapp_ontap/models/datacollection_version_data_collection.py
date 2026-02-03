r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DatacollectionVersionDataCollection", "DatacollectionVersionDataCollectionSchema"]
__pdoc__ = {
    "DatacollectionVersionDataCollectionSchema.resource": False,
    "DatacollectionVersionDataCollectionSchema.opts": False,
    "DatacollectionVersionDataCollection": False,
}

class DatacollectionVersionDataCollectionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionVersionDataCollection object"""

    create_time = ImpreciseDateTime(data_key="create_time", allow_none=True)
    r""" The creation time of the data collection version.

Example: 2018-06-04T19:00:00.000+0000 """

    description = marshmallow_fields.Str(data_key="description", allow_none=True)
    r""" Description of the data collection.

Example: This is an example data collection. """

    embedding = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version_data_collection_embedding", "DatacollectionVersionDataCollectionEmbeddingSchema"),
                unknown=EXCLUDE,
                data_key="embedding",
                allow_none=True
            )
    r""" Vectorization settings for the data collection. """

    entities = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.datacollection_entities", "DatacollectionEntitiesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="entities",
                allow_none=True
                )
    r""" List of entities. """

    entity_count = Size(data_key="entity_count", allow_none=True)
    r""" The count of entities in a data collection.

Example: 1000 """

    errors = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_entity_errors", "DataEngineEntityErrorsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="errors",
                allow_none=True
                )
    r""" The errors field of the datacollection_version_data_collection. """

    last_refresh_time = ImpreciseDateTime(data_key="last_refresh_time", allow_none=True)
    r""" The last refresh time of the data collection. This field is generated when the data collection is refreshed.

Example: 2018-06-04T19:00:00.000+0000 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" The message associated with the current state of the data collection.

Example: creating data collection """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the data collection.

Example: Example Data Collection """

    owner = marshmallow_fields.Str(data_key="owner", allow_none=True)
    r""" The owner of the data collection.

Example: Eva """

    query = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_query", "DatacollectionQuerySchema"),
                unknown=EXCLUDE,
                data_key="query",
                allow_none=True
            )
    r""" The query selector associated with the data collection. """

    size = Size(data_key="size", allow_none=True)
    r""" The size of the data collection, in bytes.

Example: 1000 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" State of the data collection version:

* <i>draft</i> - The data collection is in draft.
* <i>processing</i> - The data collection is being processed.
* <i>published</i> - The data collection is published.
* <i>failed</i> - The data collection has a failure.
* <i>outdated</i> - The data collection is outdated.
* Valid in GET requests.


Valid choices:

* draft
* processing
* published
* failed
* outdated """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type of the data collection.

* <i>manual</i> - The data collection is created by providing an entities list.
* <i>dynamic</i> - The data collection is created with a query selector.


Valid choices:

* manual
* dynamic """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier of the data collection.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version_data_collection_version", "DatacollectionVersionDataCollectionVersionSchema"),
                unknown=EXCLUDE,
                data_key="version",
                allow_none=True
            )
    r""" The version information of a data collection. """

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.workspace", "WorkspaceSchema"),
                unknown=EXCLUDE,
                data_key="workspace",
                allow_none=True
            )
    r""" Workspace containing the data collection. """

    @property
    def resource(self):
        return DatacollectionVersionDataCollection

    gettable_fields = [
        "create_time",
        "description",
        "embedding",
        "entities",
        "entity_count",
        "errors",
        "last_refresh_time",
        "message",
        "name",
        "owner",
        "query",
        "size",
        "state",
        "type",
        "uuid",
        "version",
        "workspace.links",
        "workspace.name",
        "workspace.uuid",
    ]
    """create_time,description,embedding,entities,entity_count,errors,last_refresh_time,message,name,owner,query,size,state,type,uuid,version,workspace.links,workspace.name,workspace.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DatacollectionVersionDataCollection(Resource):

    _schema = DatacollectionVersionDataCollectionSchema
