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


__all__ = ["DataEngineGovernanceAuditDatacollectionCount", "DataEngineGovernanceAuditDatacollectionCountSchema"]
__pdoc__ = {
    "DataEngineGovernanceAuditDatacollectionCountSchema.resource": False,
    "DataEngineGovernanceAuditDatacollectionCountSchema.opts": False,
}

class DataEngineGovernanceAuditDatacollectionCountSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernanceAuditDatacollectionCount object"""

    anonymized_count = Size(
        data_key="anonymized_count",
        allow_none=True,
    )
    r""" Total count of anonymized files for the data collection.

Example: 1024"""

    data_collection = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_audit_datacollection_count_data_collection", "DataEngineGovernanceAuditDatacollectionCountDataCollectionSchema"),
                data_key="data_collection",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The data_collection field of the data_engine_governance_audit_datacollection_count."""

    excluded_count = Size(
        data_key="excluded_count",
        allow_none=True,
    )
    r""" Total count of excluded files for the data collection.

Example: 1024"""

    total_count = Size(
        data_key="total_count",
        allow_none=True,
    )
    r""" Total count of files impacted in the data collection.

Example: 1024"""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_audit_datacollection_count_workspace", "DataEngineGovernanceAuditDatacollectionCountWorkspaceSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The workspace field of the data_engine_governance_audit_datacollection_count."""

    @property
    def resource(self):
        return DataEngineGovernanceAuditDatacollectionCount

    gettable_fields = [
        "anonymized_count",
        "data_collection",
        "excluded_count",
        "total_count",
        "workspace",
    ]
    """anonymized_count,data_collection,excluded_count,total_count,workspace,"""

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

class DataEngineGovernanceAuditDatacollectionCount(Resource):
    r""" Governance audit count information for a data collection. """

    _schema = DataEngineGovernanceAuditDatacollectionCountSchema
    _path = "/api/data-engine/governance/audit/data-collections"
    _keys = ["workspace.uuid", "data_collection.uuid"]






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the governance audit impacted files count for a data collection.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





