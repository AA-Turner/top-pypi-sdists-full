r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineEventJob", "DataEngineEventJobSchema"]
__pdoc__ = {
    "DataEngineEventJobSchema.resource": False,
    "DataEngineEventJobSchema.opts": False,
    "DataEngineEventJob": False,
}

class DataEngineEventJobSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineEventJob object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the job.

Example: workspace create """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state of the data engine job:

* <i>queued</i> - The job is queued for execution.
* <i>running</i> - The job is currently in execution.
* <i>success</i> - The job has been completed successfully.
* <i>failure</i> - The job has failed.


Valid choices:

* queued
* running
* success
* failure """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type of the job.

Valid choices:

* workspace_create
* workspace_update
* workspace_delete
* workspace_refresh
* workspace_content_processing
* workspace_versioning
* data_collection_update
* data_collection_delete
* data_collection_refresh
* data_collection_content_processing
* data_source_create
* data_source_update
* data_source_delete
* data_source_refresh
* policy_enforcement
* cleanup
* entity_preview
* entity_cache_cleanup
* workspace_version_diff
* data_collection_version_diff """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the job.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return DataEngineEventJob

    gettable_fields = [
        "name",
        "state",
        "type",
        "uuid",
    ]
    """name,state,type,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DataEngineEventJob(Resource):

    _schema = DataEngineEventJobSchema
