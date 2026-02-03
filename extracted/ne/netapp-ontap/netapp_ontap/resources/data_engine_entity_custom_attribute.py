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


__all__ = ["DataEngineEntityCustomAttribute", "DataEngineEntityCustomAttributeSchema"]
__pdoc__ = {
    "DataEngineEntityCustomAttributeSchema.resource": False,
    "DataEngineEntityCustomAttributeSchema.opts": False,
}

class DataEngineEntityCustomAttributeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineEntityCustomAttribute object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the data_engine_entity_custom_attribute."""

    entity = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.data_engine_entity", "DataEngineEntitySchema"),
                data_key="entity",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The entity field of the data_engine_entity_custom_attribute."""

    key = marshmallow_fields.Str(
        data_key="key",
        allow_none=True,
    )
    r""" The key of the custom attribute.

Example: custom_attribute_1"""

    value = marshmallow_fields.Str(
        data_key="value",
        allow_none=True,
    )
    r""" The value of the custom attribute.

Example: custom_value_1"""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.workspace", "WorkspaceSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The workspace field of the data_engine_entity_custom_attribute."""

    @property
    def resource(self):
        return DataEngineEntityCustomAttribute

    gettable_fields = [
        "links",
        "entity.links",
        "entity.name",
        "entity.uuid",
        "key",
        "value",
        "workspace.links",
        "workspace.name",
        "workspace.uuid",
    ]
    """links,entity.links,entity.name,entity.uuid,key,value,workspace.links,workspace.name,workspace.uuid,"""

    patchable_fields = [
        "key",
        "value",
    ]
    """key,value,"""

    postable_fields = [
        "key",
        "value",
    ]
    """key,value,"""

class DataEngineEntityCustomAttribute(Resource):
    r""" Custom attributes for the entity. """

    _schema = DataEngineEntityCustomAttributeSchema
    _path = "/api/data-engine/workspaces/{workspace[uuid]}/entities/{data_engine_entity[uuid]}/custom-attributes"
    _keys = ["workspace.uuid", "data_engine_entity.uuid", "key"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves custom attributes of an entity in a workspace.
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
        """Returns a count of all DataEngineEntityCustomAttribute resources that match the provided query"""
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
        """Returns a list of RawResources that represent DataEngineEntityCustomAttribute resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["DataEngineEntityCustomAttribute"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["DataEngineEntityCustomAttribute"], NetAppResponse]:
        r"""Adds a custom attribute to an entity in a workspace.
### Required properties
* `key` - The key of the attribute to add.
* `value` - The value of the attribute to add.
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
        records: Iterable["DataEngineEntityCustomAttribute"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a custom attribute of an entity in a workspace.
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves custom attributes of an entity in a workspace.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a custom attribute of an entity in a workspace.
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
        r"""Adds a custom attribute to an entity in a workspace.
### Required properties
* `key` - The key of the attribute to add.
* `value` - The value of the attribute to add.
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
        r"""Deletes a custom attribute of an entity in a workspace.
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


