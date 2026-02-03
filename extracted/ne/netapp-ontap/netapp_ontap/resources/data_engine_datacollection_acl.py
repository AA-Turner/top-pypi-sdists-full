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


__all__ = ["DataEngineDatacollectionAcl", "DataEngineDatacollectionAclSchema"]
__pdoc__ = {
    "DataEngineDatacollectionAclSchema.resource": False,
    "DataEngineDatacollectionAclSchema.opts": False,
}

class DataEngineDatacollectionAclSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineDatacollectionAcl object"""

    data_collection = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.datacollection", "DatacollectionSchema"),
                data_key="data_collection",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Data collection containing the ACL."""

    user_or_group = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_datacollection_acl_user_or_group", "DataEngineDatacollectionAclUserOrGroupSchema"),
                data_key="user_or_group",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" User or group information."""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.workspace", "WorkspaceSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Workspace containing the ACL."""

    @property
    def resource(self):
        return DataEngineDatacollectionAcl

    gettable_fields = [
        "data_collection.links",
        "data_collection.name",
        "data_collection.uuid",
        "user_or_group",
        "workspace.links",
        "workspace.name",
        "workspace.uuid",
    ]
    """data_collection.links,data_collection.name,data_collection.uuid,user_or_group,workspace.links,workspace.name,workspace.uuid,"""

    patchable_fields = [
        "user_or_group",
    ]
    """user_or_group,"""

    postable_fields = [
        "user_or_group",
    ]
    """user_or_group,"""

class DataEngineDatacollectionAcl(Resource):
    r""" Defines the structure of the data engine Access Control List (ACL) for data collections. """

    _schema = DataEngineDatacollectionAclSchema
    _path = "/api/data-engine/workspaces/{workspace[uuid]}/data-collections/{datacollection[uuid]}/acls"
    _keys = ["workspace.uuid", "datacollection.uuid", "user_or_group.name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of ACLs for the data collection.
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
        """Returns a count of all DataEngineDatacollectionAcl resources that match the provided query"""
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
        """Returns a list of RawResources that represent DataEngineDatacollectionAcl resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["DataEngineDatacollectionAcl"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["DataEngineDatacollectionAcl"], NetAppResponse]:
        r"""Access to data collections in a workspace is controlled by configuring ACLs (Access Control Lists) on the data collection.
In order to call a REST API on the data collection, the user must be using a role that has access to the REST API.
In addition, users that do not have the "admin" role must be listed in the ACL to be allowed access.
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
        records: Iterable["DataEngineDatacollectionAcl"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the ACL for the data collection.
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of ACLs for the data collection.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an ACL for the data collection.
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
        r"""Access to data collections in a workspace is controlled by configuring ACLs (Access Control Lists) on the data collection.
In order to call a REST API on the data collection, the user must be using a role that has access to the REST API.
In addition, users that do not have the "admin" role must be listed in the ACL to be allowed access.
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
        r"""Deletes the ACL for the data collection.
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


