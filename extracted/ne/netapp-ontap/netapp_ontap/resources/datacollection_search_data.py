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


__all__ = ["DatacollectionSearchData", "DatacollectionSearchDataSchema"]
__pdoc__ = {
    "DatacollectionSearchDataSchema.resource": False,
    "DatacollectionSearchDataSchema.opts": False,
}

class DatacollectionSearchDataSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionSearchData object"""

    num_records = Size(
        data_key="num_records",
        allow_none=True,
    )
    r""" The number of records returned.

Example: 1"""

    records = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.datacollection_search", "DatacollectionSearchSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="records",
                allow_none=True
            )
    r""" Search result of a data collection."""

    @property
    def resource(self):
        return DatacollectionSearchData

    gettable_fields = [
        "num_records",
        "records",
    ]
    """num_records,records,"""

    patchable_fields = [
        "records",
    ]
    """records,"""

    postable_fields = [
        "records",
    ]
    """records,"""

class DatacollectionSearchData(Resource):
    """Allows interaction with DatacollectionSearchData objects on the host"""

    _schema = DatacollectionSearchDataSchema
    _path = "/api/data-engine/workspaces/{workspace[uuid]}/data-collections/{datacollection[uuid]}/search"
    _keys = ["workspace.uuid", "datacollection.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Performs a similarity search of the given prompt against the entities in a data collection.
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
        """Returns a count of all DatacollectionSearchData resources that match the provided query"""
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
        """Returns a list of RawResources that represent DatacollectionSearchData resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Performs a similarity search of the given prompt against the entities in a data collection.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






