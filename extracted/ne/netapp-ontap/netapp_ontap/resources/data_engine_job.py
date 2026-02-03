r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union
from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["DataEngineJob", "DataEngineJobSchema"]
__pdoc__ = {
    "DataEngineJobSchema.resource": False,
    "DataEngineJobSchema.opts": False,
}

class DataEngineJobSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineJob object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the data_engine_job."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The creation time of the job.

Example: 2018-06-04T19:00:00.000+0000"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" The description of the job.

Example: Workspace Create Job"""

    end_time = ImpreciseDateTime(
        data_key="end_time",
        allow_none=True,
    )
    r""" The end time of the job.

Example: 2018-06-04T19:00:00.000+0000"""

    error = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_common_error", "DcnCommonErrorSchema"),
                data_key="error",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" DCN ONTAP related error information."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name of the job.

Example: workspace create"""

    parent_job = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_job_parent_job", "DataEngineJobParentJobSchema"),
                data_key="parent_job",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The parent job reference of the job."""

    percent_complete = Size(
        data_key="percent_complete",
        validate=integer_validation(minimum=0, maximum=100),
        allow_none=True,
    )
    r""" The percentage of the job that is completed.

Example: 5"""

    resource = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_job_resource", "DataEngineJobResourceSchema"),
                data_key="resource",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The data engine resource for which the job has been created."""

    start_time = ImpreciseDateTime(
        data_key="start_time",
        allow_none=True,
    )
    r""" The start time of the job.

Example: 2018-06-04T19:00:00.000+0000"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['queued', 'running', 'success', 'failure']),
        allow_none=True,
    )
    r""" The state of the data engine job:

* <i>queued</i> - The job is queued for execution.
* <i>running</i> - The job is currently in execution.
* <i>success</i> - The job has been completed successfully.
* <i>failure</i> - The job has failed.


Valid choices:

* queued
* running
* success
* failure"""

    sub_jobs = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_sub_job", "DataEngineSubJobSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="sub_jobs",
                allow_none=True
            )
    r""" The list of direct children of the job."""

    tags = marshmallow_fields.List(marshmallow_fields.Str, data_key="tags", allow_none=True)
    r""" Job tags in string format."""

    timeout = Size(
        data_key="timeout",
        allow_none=True,
    )
    r""" The timeout period of the job in minutes.

Example: 30"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['workspace_create', 'workspace_update', 'workspace_delete', 'workspace_refresh', 'workspace_content_processing', 'workspace_versioning', 'data_collection_update', 'data_collection_delete', 'data_collection_refresh', 'data_collection_content_processing', 'data_source_create', 'data_source_update', 'data_source_delete', 'data_source_refresh', 'policy_enforcement', 'cleanup', 'entity_preview', 'entity_cache_cleanup', 'workspace_version_diff', 'data_collection_version_diff']),
        allow_none=True,
    )
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
* data_collection_version_diff"""

    update_time = ImpreciseDateTime(
        data_key="update_time",
        allow_none=True,
    )
    r""" The update time of the job.

Example: 2018-06-04T19:00:00.000+0000"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the job.

Example: 123e4567-e89b-12d3-a456-426614174000"""

    @property
    def resource(self):
        return DataEngineJob

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
        "sub_jobs",
        "tags",
        "timeout",
        "type",
        "update_time",
        "uuid",
    ]
    """links,create_time,description,end_time,error,name,parent_job,percent_complete,resource,start_time,state,sub_jobs,tags,timeout,type,update_time,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class DataEngineJob(Resource):
    r""" Data engine job related information. """

    _schema = DataEngineJobSchema
    _path = "/api/data-engine/jobs"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of DCN jobs.
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all DataEngineJob resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent DataEngineJob resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of DCN jobs.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of a specific DCN job.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





