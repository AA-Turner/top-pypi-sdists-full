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


__all__ = ["DataEnginePolicyVersion", "DataEnginePolicyVersionSchema"]
__pdoc__ = {
    "DataEnginePolicyVersionSchema.resource": False,
    "DataEnginePolicyVersionSchema.opts": False,
}

class DataEnginePolicyVersionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEnginePolicyVersion object"""

    policy = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.data_engine_policy", "DataEnginePolicySchema"),
                data_key="policy",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Details of the associated data engine policy."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the data engine policy version.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return DataEnginePolicyVersion

    gettable_fields = [
        "policy",
        "uuid",
    ]
    """policy,uuid,"""

    patchable_fields = [
        "policy",
    ]
    """policy,"""

    postable_fields = [
        "policy",
    ]
    """policy,"""

class DataEnginePolicyVersion(Resource):
    r""" Defines the structure of a data engine policy version. """

    _schema = DataEnginePolicyVersionSchema
    _path = "/api/data-engine/policies/{data_engine_policy[uuid]}/versions"
    _keys = ["data_engine_policy.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all the versions of the specified data engine policy.
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
        """Returns a count of all DataEnginePolicyVersion resources that match the provided query"""
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
        """Returns a list of RawResources that represent DataEnginePolicyVersion resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all the versions of the specified data engine policy.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of the specified version of the data engine policy.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





