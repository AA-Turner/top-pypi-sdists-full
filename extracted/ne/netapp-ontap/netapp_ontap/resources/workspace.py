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


__all__ = ["Workspace", "WorkspaceSchema"]
__pdoc__ = {
    "WorkspaceSchema.resource": False,
    "WorkspaceSchema.opts": False,
}

class WorkspaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Workspace object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the workspace."""

    acls = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.resources.data_engine_acl", "DataEngineAclSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="acls",
                allow_none=True
            )
    r""" List of users or groups associated with the ACL."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The creation time of the workspace. This field is generated when the workspace is created.

Example: 2018-06-04T19:00:00.000+0000"""

    data_collection_count = Size(
        data_key="data_collection_count",
        allow_none=True,
    )
    r""" The count of data collection in a workspace.

Example: 20"""

    data_sources = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.workspace_data_sources", "WorkspaceDataSourcesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="data_sources",
                allow_none=True
            )
    r""" The data sources to be added to the workspace. Required in a POST request."""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" Description of the workspace.

Example: Example workspace"""

    entity_count = Size(
        data_key="entity_count",
        allow_none=True,
    )
    r""" The count of entities in a workspace.

Example: 1000"""

    errors = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_entity_errors", "DataEngineEntityErrorsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="errors",
                allow_none=True
            )
    r""" The errors field of the workspace."""

    last_refresh_time = ImpreciseDateTime(
        data_key="last_refresh_time",
        allow_none=True,
    )
    r""" The last refresh time of the workspace. This field is generated when the workspace is refreshed.

Example: 2018-06-04T19:00:00.000+0000"""

    message = marshmallow_fields.Str(
        data_key="message",
        allow_none=True,
    )
    r""" The message associated with the current state of the workspace.

Example: creating workspace"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name for the workspace. Required for POST requests.

Example: Doc workspace"""

    owner = marshmallow_fields.Str(
        data_key="owner",
        allow_none=True,
    )
    r""" The owner of the workspace.

Example: SAL"""

    policies = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.workspace_policies", "WorkspacePoliciesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="policies",
                allow_none=True
            )
    r""" The policies field of the workspace."""

    refresh_interval = marshmallow_fields.Str(
        data_key="refresh_interval",
        allow_none=True,
    )
    r""" The workspace refresh time interval in ISO-8601 format. Optional in POST requests. If not supplied, this value defaults to PT1H.

Example: PT1H"""

    space = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.workspace_space", "WorkspaceSpaceSchema"),
                data_key="space",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The space field of the workspace."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['processing', 'ready', 'failed', 'outdated']),
        allow_none=True,
    )
    r""" State of the workspace:

* <i>processing</i> - The workspace is being processed after creation.
* <i>ready</i> - The workspace is ready for use.
* <i>failed</i> - The workspace has a failure.
* <i>outdated</i> - The workspace is outdated.
* Valid in GET.


Valid choices:

* processing
* ready
* failed
* outdated"""

    update_time = ImpreciseDateTime(
        data_key="update_time",
        allow_none=True,
    )
    r""" The time of update of the workspace. This field is generated when the workspace is updated.

Example: 2018-06-04T19:00:00.000+0000"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier for the workspace.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.workspace_version1", "WorkspaceVersion1Schema"),
                data_key="version",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The version field of the workspace."""

    @property
    def resource(self):
        return Workspace

    gettable_fields = [
        "links",
        "create_time",
        "data_collection_count",
        "description",
        "entity_count",
        "errors",
        "last_refresh_time",
        "message",
        "name",
        "owner",
        "policies",
        "refresh_interval",
        "space",
        "state",
        "update_time",
        "uuid",
        "version",
    ]
    """links,create_time,data_collection_count,description,entity_count,errors,last_refresh_time,message,name,owner,policies,refresh_interval,space,state,update_time,uuid,version,"""

    patchable_fields = [
        "acls",
        "description",
        "name",
        "policies",
        "refresh_interval",
    ]
    """acls,description,name,policies,refresh_interval,"""

    postable_fields = [
        "acls",
        "data_sources",
        "description",
        "name",
        "policies",
        "refresh_interval",
    ]
    """acls,data_sources,description,name,policies,refresh_interval,"""

class Workspace(Resource):
    r""" Workspace information """

    _schema = WorkspaceSchema
    _path = "/api/data-engine/workspaces"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of workspaces.
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
        """Returns a count of all Workspace resources that match the provided query"""
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
        """Returns a list of RawResources that represent Workspace resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Workspace"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Modifies a workspace.
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Workspace"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Workspace"], NetAppResponse]:
        r"""Creates a workspace.
 ### Required properties
* `name` - The name for the workspace.
* `data_sources` - The data sources to be added to the workspace.
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["Workspace"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a workspace.
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of workspaces.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a workspace.
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
        r"""Creates a workspace.
 ### Required properties
* `name` - The name for the workspace.
* `data_sources` - The data sources to be added to the workspace.
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Modifies a workspace.
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a workspace.
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


