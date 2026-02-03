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


__all__ = ["DataEngine", "DataEngineSchema"]
__pdoc__ = {
    "DataEngineSchema.resource": False,
    "DataEngineSchema.opts": False,
}

class DataEngineSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngine object"""

    data_collection_metrics = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_collection_metrics", "DataCollectionMetricsSchema"),
                data_key="data_collection_metrics",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The aggregated metrics of all data collections."""

    top_cpu_operations = marshmallow_fields.List(marshmallow_fields.Str, data_key="top_cpu_operations", allow_none=True)
    r""" Top CPU consuming operations."""

    top_gpu_operations = marshmallow_fields.List(marshmallow_fields.Str, data_key="top_gpu_operations", allow_none=True)
    r""" Top GPU consuming operations."""

    workspace_metrics = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.workspace_metrics", "WorkspaceMetricsSchema"),
                data_key="workspace_metrics",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The aggregated metrics of all workspaces."""

    @property
    def resource(self):
        return DataEngine

    gettable_fields = [
        "data_collection_metrics",
        "top_cpu_operations",
        "top_gpu_operations",
        "workspace_metrics",
    ]
    """data_collection_metrics,top_cpu_operations,top_gpu_operations,workspace_metrics,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class DataEngine(Resource):
    """Allows interaction with DataEngine objects on the host"""

    _schema = DataEngineSchema
    _path = "/api/data-engine"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves data engine information and cluster level metrics.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





