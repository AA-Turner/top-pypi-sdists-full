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


__all__ = ["DatacollectionEntity", "DatacollectionEntitySchema"]
__pdoc__ = {
    "DatacollectionEntitySchema.resource": False,
    "DatacollectionEntitySchema.opts": False,
}

class DatacollectionEntitySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionEntity object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the datacollection_entity."""

    access_time = ImpreciseDateTime(
        data_key="access_time",
        allow_none=True,
    )
    r""" The last access time of the entity.

Example: 2018-06-04T19:00:00.000+0000"""

    attributes = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_entity_attributes", "DatacollectionEntityAttributesSchema"),
                data_key="attributes",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The attributes field of the datacollection_entity."""

    can_preview = marshmallow_fields.Boolean(
        data_key="can_preview",
        allow_none=True,
    )
    r""" Indicates if the entity can be previewed.

Example: true"""

    content_hash = marshmallow_fields.Str(
        data_key="content_hash",
        allow_none=True,
    )
    r""" The hash of the entity content."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The create time of the entity.

Example: 2018-06-04T19:00:00.000+0000"""

    datacollection = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.datacollection", "DatacollectionSchema"),
                data_key="datacollection",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The datacollection field of the datacollection_entity."""

    datasource = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_source_version", "DataSourceVersionSchema"),
                data_key="datasource",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Data source version."""

    errors = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_entity_errors", "DataEngineEntityErrorsSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="errors",
                allow_none=True
            )
    r""" The errors field of the datacollection_entity."""

    extension = marshmallow_fields.Str(
        data_key="extension",
        allow_none=True,
    )
    r""" The extension of the entity."""

    format = marshmallow_fields.Str(
        data_key="format",
        allow_none=True,
    )
    r""" The format of the entity (e.g. pdf document, jpeg image, mp4 video, zip).

Example: pdf"""

    has_pii = marshmallow_fields.Boolean(
        data_key="has_pii",
        allow_none=True,
    )
    r""" Indicates if the entity has PII.

Example: false"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name of the entity."""

    permissions = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_entity_permissions", "DataEngineEntityPermissionsSchema"),
                data_key="permissions",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The permissions of the entity."""

    size = Size(
        data_key="size",
        allow_none=True,
    )
    r""" The size of the entity in bytes.

Example: 100"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['file', 'object']),
        allow_none=True,
    )
    r""" Type of the entity:

* <i>file</i> - The entity is a file.
* <i>object</i> - The entity is an object.


Valid choices:

* file
* object"""

    update_time = ImpreciseDateTime(
        data_key="update_time",
        allow_none=True,
    )
    r""" The last update time of the entity.

Example: 2018-06-04T19:00:00.000+0000"""

    uri = marshmallow_fields.Str(
        data_key="uri",
        allow_none=True,
    )
    r""" The URI of the entity."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier for the entity.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.entity_workspace_version", "EntityWorkspaceVersionSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Workspace version."""

    @property
    def resource(self):
        return DatacollectionEntity

    gettable_fields = [
        "links",
        "access_time",
        "attributes",
        "can_preview",
        "content_hash",
        "create_time",
        "datacollection.links",
        "datacollection.name",
        "datacollection.uuid",
        "datasource",
        "errors",
        "extension",
        "format",
        "has_pii",
        "name",
        "permissions",
        "size",
        "type",
        "update_time",
        "uri",
        "uuid",
        "workspace",
    ]
    """links,access_time,attributes,can_preview,content_hash,create_time,datacollection.links,datacollection.name,datacollection.uuid,datasource,errors,extension,format,has_pii,name,permissions,size,type,update_time,uri,uuid,workspace,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "uuid",
    ]
    """uuid,"""

class DatacollectionEntity(Resource):
    r""" Entity attributes. """

    _schema = DatacollectionEntitySchema
    _path = "/api/data-engine/workspaces/{workspace[uuid]}/data-collections/{datacollection[uuid]}/entities"
    _keys = ["workspace.uuid", "datacollection.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all entities in a data collection.
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
        """Returns a count of all DatacollectionEntity resources that match the provided query"""
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
        """Returns a list of RawResources that represent DatacollectionEntity resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["DatacollectionEntity"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["DatacollectionEntity"], NetAppResponse]:
        r"""Creates a new entity in a data collection.
### Required properties
* type `uuid` - Unique identifier of the entity
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
        records: Iterable["DatacollectionEntity"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an entity in a data collection.
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all entities in a data collection.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an entity in a data collection.
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
        r"""Creates a new entity in a data collection.
### Required properties
* type `uuid` - Unique identifier of the entity
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)


    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an entity in a data collection.
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


