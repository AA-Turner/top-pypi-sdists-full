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


__all__ = ["DataSource", "DataSourceSchema"]
__pdoc__ = {
    "DataSourceSchema.resource": False,
    "DataSourceSchema.opts": False,
}

class DataSourceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataSource object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the data_source."""

    errors = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_entity_errors", "DataEngineEntityErrorsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="errors",
                allow_none=True
            )
    r""" The errors field of the data_source."""

    last_refresh_time = ImpreciseDateTime(
        data_key="last_refresh_time",
        allow_none=True,
    )
    r""" The last refresh time of the data source. This field is generated when the data source is refreshed.

Example: 2018-06-04T19:00:00.000+0000"""

    local_storage = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.local_storage", "LocalStorageSchema"),
                data_key="local_storage",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The local storage used for a data source. Required on POST requests."""

    message = marshmallow_fields.Str(
        data_key="message",
        allow_none=True,
    )
    r""" The message associated with the current state of the data source.

Example: refreshing data source"""

    remote_storage = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.remote_storage", "RemoteStorageSchema"),
                data_key="remote_storage",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The remote storage used for a data source. Required on POST requests."""

    space = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_source_space", "DataSourceSpaceSchema"),
                data_key="space",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The space field of the data_source."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['processing', 'ready', 'failed', 'outdated', 'deleted']),
        allow_none=True,
    )
    r""" State of the data source:

* <i>processing</i> - The data source is being processed after creation.
* <i>ready</i> - The data source is ready for use.
* <i>failed</i> - The data source has a failure.
* <i>outdated</i> - The data source is outdated.
* <i>deleted</i> - The data source has been marked for deletion.
* Valid in GET requests.


Valid choices:

* processing
* ready
* failed
* outdated
* deleted"""

    type = marshmallow_fields.Str(
        data_key="type",
        allow_none=True,
    )
    r""" The type of the data source."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier for the data source.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    workspaces = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.resources.workspace", "WorkspaceSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="workspaces",
                allow_none=True
            )
    r""" The list of workspaces that are associated with the data source."""

    @property
    def resource(self):
        return DataSource

    gettable_fields = [
        "links",
        "errors",
        "last_refresh_time",
        "local_storage",
        "message",
        "remote_storage",
        "space",
        "state",
        "type",
        "uuid",
        "workspaces",
    ]
    """links,errors,last_refresh_time,local_storage,message,remote_storage,space,state,type,uuid,workspaces,"""

    patchable_fields = [
        "local_storage",
        "remote_storage",
        "space",
        "type",
    ]
    """local_storage,remote_storage,space,type,"""

    postable_fields = [
        "local_storage",
        "remote_storage",
        "space",
        "type",
    ]
    """local_storage,remote_storage,space,type,"""

class DataSource(Resource):
    r""" Data source information. """

    _schema = DataSourceSchema
    _path = "/api/data-engine/data-sources"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of data sources.
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
        """Returns a count of all DataSource resources that match the provided query"""
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
        """Returns a list of RawResources that represent DataSource resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of data sources.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a data source by UUID.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





