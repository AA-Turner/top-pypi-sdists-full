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


__all__ = ["DatacollectionVersion", "DatacollectionVersionSchema"]
__pdoc__ = {
    "DatacollectionVersionSchema.resource": False,
    "DatacollectionVersionSchema.opts": False,
}

class DatacollectionVersionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionVersion object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the datacollection_version."""

    data_collection = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version_data_collection", "DatacollectionVersionDataCollectionSchema"),
                data_key="data_collection",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The data_collection field of the datacollection_version."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the data collection version.


Example: 02c9e252-41be-11e9-81d5-00a0986138f7"""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.datacollection_version_workspace", "DatacollectionVersionWorkspaceSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The workspace field of the datacollection_version."""

    @property
    def resource(self):
        return DatacollectionVersion

    gettable_fields = [
        "links",
        "data_collection",
        "uuid",
        "workspace",
    ]
    """links,data_collection,uuid,workspace,"""

    patchable_fields = [
        "data_collection",
        "workspace",
    ]
    """data_collection,workspace,"""

    postable_fields = [
        "data_collection",
        "workspace",
    ]
    """data_collection,workspace,"""

class DatacollectionVersion(Resource):
    r""" Data collection version. """

    _schema = DatacollectionVersionSchema
    _path = "/api/data-engine/workspaces/{workspace[uuid]}/data-collections/{datacollection[uuid]}/versions"
    _keys = ["workspace.uuid", "datacollection.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all versions of a data collection in a workspace.
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
        """Returns a count of all DatacollectionVersion resources that match the provided query"""
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
        """Returns a list of RawResources that represent DatacollectionVersion resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all versions of a data collection in a workspace.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a data collection version in a workspace.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





