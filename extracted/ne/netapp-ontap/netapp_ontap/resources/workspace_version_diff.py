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


__all__ = ["WorkspaceVersionDiff", "WorkspaceVersionDiffSchema"]
__pdoc__ = {
    "WorkspaceVersionDiffSchema.resource": False,
    "WorkspaceVersionDiffSchema.opts": False,
}

class WorkspaceVersionDiffSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WorkspaceVersionDiff object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the workspace_version_diff."""

    change_type = marshmallow_fields.Str(
        data_key="change_type",
        validate=enum_validation(['added', 'modified', 'deleted', 'renamed', 'identical']),
        allow_none=True,
    )
    r""" The type of change for the entities.

Valid choices:

* added
* modified
* deleted
* renamed
* identical"""

    data_source = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.workspace_version_diff_data_source", "WorkspaceVersionDiffDataSourceSchema"),
                data_key="data_source",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The data_source field of the workspace_version_diff."""

    entities = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.workspace_version_diff_entities", "WorkspaceVersionDiffEntitiesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="entities",
                allow_none=True
            )
    r""" The entities field of the workspace_version_diff."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the diff.

Example: 123e4567-e89b-12d3-a456-426614174000"""

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version_diff_version", "DatacollectionVersionDiffVersionSchema"),
                data_key="version",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The version field of the workspace_version_diff."""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.workspace", "WorkspaceSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Workspace containing the query."""

    @property
    def resource(self):
        return WorkspaceVersionDiff

    gettable_fields = [
        "links",
        "change_type",
        "data_source",
        "entities",
        "uuid",
        "version",
        "workspace.links",
        "workspace.name",
        "workspace.uuid",
    ]
    """links,change_type,data_source,entities,uuid,version,workspace.links,workspace.name,workspace.uuid,"""

    patchable_fields = [
        "version",
    ]
    """version,"""

    postable_fields = [
        "version",
    ]
    """version,"""

class WorkspaceVersionDiff(Resource):
    r""" Workspace version diff. """

    _schema = WorkspaceVersionDiffSchema
    _path = "/api/data-engine/workspaces/{workspace[uuid]}/versions/{workspace_version[uuid]}/diffs"
    _keys = ["workspace.uuid", "workspace_version.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all workspace version diffs.
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
        """Returns a count of all WorkspaceVersionDiff resources that match the provided query"""
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
        """Returns a list of RawResources that represent WorkspaceVersionDiff resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["WorkspaceVersionDiff"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["WorkspaceVersionDiff"], NetAppResponse]:
        r"""Creates a workspace version diff.
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)


    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all workspace version diffs.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)


    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates a workspace version diff.
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)




