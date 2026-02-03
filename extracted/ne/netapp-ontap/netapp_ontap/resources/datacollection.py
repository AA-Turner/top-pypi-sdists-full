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


__all__ = ["Datacollection", "DatacollectionSchema"]
__pdoc__ = {
    "DatacollectionSchema.resource": False,
    "DatacollectionSchema.opts": False,
}

class DatacollectionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Datacollection object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the datacollection."""

    acls = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.resources.data_engine_datacollection_acl", "DataEngineDatacollectionAclSchema"),
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
    r""" The creation time of the data collection. This field is generated when the data collection is created.

Example: 2018-06-04T19:00:00.000+0000"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" Description of the data collection.

Example: This is an example data collection."""

    embedding = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_embedding", "DatacollectionEmbeddingSchema"),
                data_key="embedding",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Vectorization settings for the data collection."""

    entities = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.datacollection_entities", "DatacollectionEntitiesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="entities",
                allow_none=True
            )
    r""" List of entities."""

    entity_count = Size(
        data_key="entity_count",
        allow_none=True,
    )
    r""" The count of entities in a data collection.

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
    r""" The errors field of the datacollection."""

    last_refresh_time = ImpreciseDateTime(
        data_key="last_refresh_time",
        allow_none=True,
    )
    r""" The last refresh time of the data collection. This field is generated when the data collection is refreshed.

Example: 2018-06-04T19:00:00.000+0000"""

    message = marshmallow_fields.Str(
        data_key="message",
        allow_none=True,
    )
    r""" The message associated with the current state of the data collection.

Example: creating data collection"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the data collection.

Example: Example Data Collection"""

    owner = marshmallow_fields.Str(
        data_key="owner",
        allow_none=True,
    )
    r""" The owner of the data collection.

Example: Eva"""

    query = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_query", "DatacollectionQuerySchema"),
                data_key="query",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The query selector associated with the data collection."""

    rag = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_rag", "DatacollectionRagSchema"),
                data_key="rag",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The rag field of the datacollection."""

    size = Size(
        data_key="size",
        allow_none=True,
    )
    r""" The size of the data collection, in bytes.

Example: 1000"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['draft', 'processing', 'published', 'failed', 'outdated']),
        allow_none=True,
    )
    r""" State of the data collection:

* <i>draft</i> - The data collection is in draft.
* <i>processing</i> - The data collection is being processed.
* <i>published</i> - The data collection is published.
* <i>failed</i> - The data collection has a failure.
* <i>outdated</i> - The data collection is outdated.
* Valid in GET requests.


Valid choices:

* draft
* processing
* published
* failed
* outdated"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['manual', 'dynamic']),
        allow_none=True,
    )
    r""" The type of the data collection.

* <i>manual</i> - The data collection is created by providing an entities list.
* <i>dynamic</i> - The data collection is created with a query selector.


Valid choices:

* manual
* dynamic"""

    update_time = ImpreciseDateTime(
        data_key="update_time",
        allow_none=True,
    )
    r""" The update time of the data collection. This field is generated when the data collection is updated.

Example: 2018-06-04T19:00:00.000+0000"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the data collection.

Example: 123e4567-e89b-12d3-a456-426614174000"""

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version1", "DatacollectionVersion1Schema"),
                data_key="version",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The version field of the datacollection."""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.entity_workspace_version", "EntityWorkspaceVersionSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Workspace containing the data collection."""

    @property
    def resource(self):
        return Datacollection

    gettable_fields = [
        "links",
        "create_time",
        "description",
        "embedding",
        "entities",
        "entity_count",
        "errors",
        "last_refresh_time",
        "message",
        "name",
        "owner",
        "query",
        "rag",
        "size",
        "state",
        "type",
        "update_time",
        "uuid",
        "version",
        "workspace",
    ]
    """links,create_time,description,embedding,entities,entity_count,errors,last_refresh_time,message,name,owner,query,rag,size,state,type,update_time,uuid,version,workspace,"""

    patchable_fields = [
        "acls",
        "description",
        "embedding",
        "name",
    ]
    """acls,description,embedding,name,"""

    postable_fields = [
        "acls",
        "description",
        "embedding",
        "entities",
        "name",
        "query",
        "type",
    ]
    """acls,description,embedding,entities,name,query,type,"""

class Datacollection(Resource):
    r""" Data collection information. """

    _schema = DatacollectionSchema
    _path = "/api/data-engine/workspaces/{workspace[uuid]}/data-collections"
    _keys = ["workspace.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all data collections in a workspace.
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
        """Returns a count of all Datacollection resources that match the provided query"""
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
        """Returns a list of RawResources that represent Datacollection resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Datacollection"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a data collection in a workspace.
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Datacollection"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Datacollection"], NetAppResponse]:
        r"""Creates a data collection in a workspace.
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
        records: Iterable["Datacollection"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a data collection in a workspace.
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all data collections in a workspace.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a data collection in a workspace.
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
        r"""Creates a data collection in a workspace.
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
        r"""Updates a data collection in a workspace.
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
        r"""Deletes a data collection in a workspace.
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


