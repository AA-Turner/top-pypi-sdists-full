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


__all__ = ["DataEngineGovernanceFilePreviewFileContentRequest", "DataEngineGovernanceFilePreviewFileContentRequestSchema"]
__pdoc__ = {
    "DataEngineGovernanceFilePreviewFileContentRequestSchema.resource": False,
    "DataEngineGovernanceFilePreviewFileContentRequestSchema.opts": False,
}

class DataEngineGovernanceFilePreviewFileContentRequestSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernanceFilePreviewFileContentRequest object"""

    file = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_file_preview_file_content_request_file", "DataEngineGovernanceFilePreviewFileContentRequestFileSchema"),
                data_key="file",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The file field of the data_engine_governance_file_preview_file_content_request."""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_file_preview_file_content_request_workspace", "DataEngineGovernanceFilePreviewFileContentRequestWorkspaceSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The workspace field of the data_engine_governance_file_preview_file_content_request."""

    @property
    def resource(self):
        return DataEngineGovernanceFilePreviewFileContentRequest

    gettable_fields = [
        "file",
        "workspace",
    ]
    """file,workspace,"""

    patchable_fields = [
        "file",
        "workspace",
    ]
    """file,workspace,"""

    postable_fields = [
        "file",
        "workspace",
    ]
    """file,workspace,"""

class DataEngineGovernanceFilePreviewFileContentRequest(Resource):
    r""" Request body for retrieving anonymized file content. """

    _schema = DataEngineGovernanceFilePreviewFileContentRequestSchema
    _path = "/api/data-engine/governance/file-preview/file-content"



    @classmethod
    def post_collection(
        cls,
        records: Iterable["DataEngineGovernanceFilePreviewFileContentRequest"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["DataEngineGovernanceFilePreviewFileContentRequest"], NetAppResponse]:
        r"""Retrieves the anonymized content of a file.
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




    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Retrieves the anonymized content of a file.
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




