r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

Displays the list of files under the specified litigation ID."""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["SnaplockLitigationFile", "SnaplockLitigationFileSchema"]
__pdoc__ = {
    "SnaplockLitigationFileSchema.resource": False,
    "SnaplockLitigationFileSchema.opts": False,
}


class SnaplockLitigationFileSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockLitigationFile object"""

    file = marshmallow_fields.List(marshmallow_fields.Str, data_key="file", allow_none=True)
    r""" Name of the file including the path from the root."""

    sequence_index = Size(
        data_key="sequence_index",
        allow_none=True,
    )
    r""" Sequence index of files path list."""

    @property
    def resource(self):
        return SnaplockLitigationFile

    gettable_fields = [
        "file",
        "sequence_index",
    ]
    """file,sequence_index,"""

    patchable_fields = [
        "file",
        "sequence_index",
    ]
    """file,sequence_index,"""

    postable_fields = [
        "file",
        "sequence_index",
    ]
    """file,sequence_index,"""

class SnaplockLitigationFile(Resource):
    """Allows interaction with SnaplockLitigationFile objects on the host"""

    _schema = SnaplockLitigationFileSchema
    _path = "/api/storage/snaplock/litigations/{litigation[id]}/files"
    _keys = ["litigation.id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Displays the list of files for the specified litigation ID.
### Learn more
* [`DOC /storage/snaplock/litigations/{litigation.id}/files`](#docs-snaplock-storage_snaplock_litigations_{litigation.id}_files)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SnaplockLitigationFile resources that match the provided query"""
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
        """Returns a list of RawResources that represent SnaplockLitigationFile resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Displays the list of files for the specified litigation ID.
### Learn more
* [`DOC /storage/snaplock/litigations/{litigation.id}/files`](#docs-snaplock-storage_snaplock_litigations_{litigation.id}_files)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






