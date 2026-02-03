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


__all__ = ["DataEngineGovernanceFilePreviewJob", "DataEngineGovernanceFilePreviewJobSchema"]
__pdoc__ = {
    "DataEngineGovernanceFilePreviewJobSchema.resource": False,
    "DataEngineGovernanceFilePreviewJobSchema.opts": False,
}

class DataEngineGovernanceFilePreviewJobSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernanceFilePreviewJob object"""

    file = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_file_preview_file_content_request_file", "DataEngineGovernanceFilePreviewFileContentRequestFileSchema"),
                data_key="file",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The file field of the data_engine_governance_file_preview_job."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['new', 'queued', 'in_progress', 'completed', 'warning', 'failed', 'timed_out', 'canceling', 'canceled']),
        allow_none=True,
    )
    r""" Status of the job. Possible values are:

* <i>new</i>: Job is newly created.
* <i>queued</i>: Job is queued for processing.
* <i>in_progress</i>: Job is currently being processed.
* <i>completed</i>: Job completed successfully.
* <i>warning</i>: Job completed with warnings.
* <i>failed</i>: Job failed.
* <i>timed_out</i>: Job timed out.
* <i>canceling</i>: Job is being canceled.
* <i>canceled</i>: Job was canceled.


Valid choices:

* new
* queued
* in_progress
* completed
* warning
* failed
* timed_out
* canceling
* canceled"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the file preview job.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_file_preview_file_content_request_workspace", "DataEngineGovernanceFilePreviewFileContentRequestWorkspaceSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The workspace field of the data_engine_governance_file_preview_job."""

    @property
    def resource(self):
        return DataEngineGovernanceFilePreviewJob

    gettable_fields = [
        "file",
        "state",
        "uuid",
        "workspace",
    ]
    """file,state,uuid,workspace,"""

    patchable_fields = [
        "file",
        "uuid",
        "workspace",
    ]
    """file,uuid,workspace,"""

    postable_fields = [
        "file",
        "uuid",
        "workspace",
    ]
    """file,uuid,workspace,"""

class DataEngineGovernanceFilePreviewJob(Resource):
    r""" File preview job. """

    _schema = DataEngineGovernanceFilePreviewJobSchema
    _path = "/api/data-engine/governance/file-preview/jobs"
    _keys = ["uuid"]



    @classmethod
    def post_collection(
        cls,
        records: Iterable["DataEngineGovernanceFilePreviewJob"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["DataEngineGovernanceFilePreviewJob"], NetAppResponse]:
        r"""Creates a job for retrieving file information.
### Required properties
* `file.uuid`: UUID of the entity.
* `file.path`: Path of the entity.
* `file.format`: Format of the entity.
* `workspace.uuid`: UUID of the workspace in which the entity is present.
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)



    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves information about a file preview job by its UUID.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates a job for retrieving file information.
### Required properties
* `file.uuid`: UUID of the entity.
* `file.path`: Path of the entity.
* `file.format`: Format of the entity.
* `workspace.uuid`: UUID of the workspace in which the entity is present.
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)




