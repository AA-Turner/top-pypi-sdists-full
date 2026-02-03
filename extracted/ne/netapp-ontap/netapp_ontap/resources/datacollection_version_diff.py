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


__all__ = ["DatacollectionVersionDiff", "DatacollectionVersionDiffSchema"]
__pdoc__ = {
    "DatacollectionVersionDiffSchema.resource": False,
    "DatacollectionVersionDiffSchema.opts": False,
}

class DatacollectionVersionDiffSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionVersionDiff object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the datacollection_version_diff."""

    change_type = marshmallow_fields.Str(
        data_key="change_type",
        validate=enum_validation(['added', 'modified', 'deleted', 'renamed', 'identical']),
        allow_none=True,
    )
    r""" The type of change.

Valid choices:

* added
* modified
* deleted
* renamed
* identical"""

    data_collection = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version_diff_data_collection", "DatacollectionVersionDiffDataCollectionSchema"),
                data_key="data_collection",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The data_collection field of the datacollection_version_diff."""

    data_source = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version_diff_data_source", "DatacollectionVersionDiffDataSourceSchema"),
                data_key="data_source",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Data source information."""

    entities = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.datacollection_version_diff_entities", "DatacollectionVersionDiffEntitiesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="entities",
                allow_none=True
            )
    r""" The list of entities."""

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
    r""" The version field of the datacollection_version_diff."""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version_workspace", "DatacollectionVersionWorkspaceSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The workspace field of the datacollection_version_diff."""

    @property
    def resource(self):
        return DatacollectionVersionDiff

    gettable_fields = [
        "links",
        "change_type",
        "data_collection",
        "data_source",
        "entities",
        "uuid",
        "version",
        "workspace",
    ]
    """links,change_type,data_collection,data_source,entities,uuid,version,workspace,"""

    patchable_fields = [
        "version",
        "workspace",
    ]
    """version,workspace,"""

    postable_fields = [
        "version",
        "workspace",
    ]
    """version,workspace,"""

class DatacollectionVersionDiff(Resource):
    r""" Data collection version diff. """

    _schema = DatacollectionVersionDiffSchema
    _path = "/api/data-engine/workspaces/{workspace[uuid]}/data-collections/{datacollection[uuid]}/versions/{datacollection_version[uuid]}/diffs"
    _keys = ["workspace.uuid", "datacollection.uuid", "datacollection_version.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all data collection version diffs.
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
        """Returns a count of all DatacollectionVersionDiff resources that match the provided query"""
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
        """Returns a list of RawResources that represent DatacollectionVersionDiff resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["DatacollectionVersionDiff"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["DatacollectionVersionDiff"], NetAppResponse]:
        r"""Creates a data collection version diff in a workspace.
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)


    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all data collection version diffs.
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
        r"""Creates a data collection version diff in a workspace.
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)




