r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineSubJob", "DataEngineSubJobSchema"]
__pdoc__ = {
    "DataEngineSubJobSchema.resource": False,
    "DataEngineSubJobSchema.opts": False,
    "DataEngineSubJob": False,
}

class DataEngineSubJobSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineSubJob object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                unknown=EXCLUDE,
                data_key="_links",
                allow_none=True
            )
    r""" The links field of the data_engine_sub_job. """

    create_time = ImpreciseDateTime(data_key="create_time", allow_none=True)
    r""" The creation time of the job.

Example: 2018-06-04T19:00:00.000+0000 """

    description = marshmallow_fields.Str(data_key="description", allow_none=True)
    r""" The description of the job.

Example: Workspace Create Job """

    end_time = ImpreciseDateTime(data_key="end_time", allow_none=True)
    r""" The end time of the job.

Example: 2018-06-04T19:00:00.000+0000 """

    error = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_common_error", "DcnCommonErrorSchema"),
                unknown=EXCLUDE,
                data_key="error",
                allow_none=True
            )
    r""" DCN ONTAP related error information. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the job.

Example: workspace create """

    parent_job = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_job_parent_job", "DataEngineJobParentJobSchema"),
                unknown=EXCLUDE,
                data_key="parent_job",
                allow_none=True
            )
    r""" The parent job reference of the job. """

    percent_complete = Size(data_key="percent_complete", allow_none=True)
    r""" The percentage of the job that is completed.

Example: 5 """

    resource = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_job_resource", "DataEngineJobResourceSchema"),
                unknown=EXCLUDE,
                data_key="resource",
                allow_none=True
            )
    r""" The data engine resource for which the job has been created. """

    start_time = ImpreciseDateTime(data_key="start_time", allow_none=True)
    r""" The start time of the job.

Example: 2018-06-04T19:00:00.000+0000 """

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

    tags = marshmallow_fields.List(marshmallow_fields.Str, data_key="tags", allow_none=True)
    r""" Job tags in string format. """

    timeout = Size(data_key="timeout", allow_none=True)
    r""" The timeout period of the job in minutes.

Example: 30 """

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

    update_time = ImpreciseDateTime(data_key="update_time", allow_none=True)
    r""" The update time of the job.

Example: 2018-06-04T19:00:00.000+0000 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the job.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return DataEngineSubJob

    gettable_fields = [
        "links",
        "create_time",
        "description",
        "end_time",
        "error",
        "name",
        "parent_job",
        "percent_complete",
        "resource",
        "start_time",
        "state",
        "tags",
        "timeout",
        "type",
        "update_time",
        "uuid",
    ]
    """links,create_time,description,end_time,error,name,parent_job,percent_complete,resource,start_time,state,tags,timeout,type,update_time,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DataEngineSubJob(Resource):

    _schema = DataEngineSubJobSchema
