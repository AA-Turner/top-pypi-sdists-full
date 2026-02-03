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


__all__ = ["DataEngineGovernanceAuditCount", "DataEngineGovernanceAuditCountSchema"]
__pdoc__ = {
    "DataEngineGovernanceAuditCountSchema.resource": False,
    "DataEngineGovernanceAuditCountSchema.opts": False,
}

class DataEngineGovernanceAuditCountSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernanceAuditCount object"""

    anonymized_count = Size(
        data_key="anonymized_count",
        allow_none=True,
    )
    r""" Total count of anonymized files.

Example: 1024"""

    excluded_count = Size(
        data_key="excluded_count",
        allow_none=True,
    )
    r""" Total count of excluded files.

Example: 1024"""

    guardrail_policy = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.guardrail_policy", "GuardrailPolicySchema"),
                data_key="guardrail_policy",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Guardrail policy."""

    total_count = Size(
        data_key="total_count",
        allow_none=True,
    )
    r""" Total count of files impacted by the guardrail.

Example: 1024"""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_audit_count_workspace", "DataEngineGovernanceAuditCountWorkspaceSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The workspace field of the data_engine_governance_audit_count."""

    @property
    def resource(self):
        return DataEngineGovernanceAuditCount

    gettable_fields = [
        "anonymized_count",
        "excluded_count",
        "guardrail_policy",
        "total_count",
        "workspace",
    ]
    """anonymized_count,excluded_count,guardrail_policy,total_count,workspace,"""

    patchable_fields = [
        "guardrail_policy",
        "workspace",
    ]
    """guardrail_policy,workspace,"""

    postable_fields = [
        "guardrail_policy",
        "workspace",
    ]
    """guardrail_policy,workspace,"""

class DataEngineGovernanceAuditCount(Resource):
    r""" Governance audit count information. """

    _schema = DataEngineGovernanceAuditCountSchema
    _path = "/api/data-engine/governance/audit/policies"
    _keys = ["workspace.uuid", "guardrail_policy.uuid"]






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the governance audit impacted files count.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





