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


__all__ = ["DataEngineGovernanceAuditImpactedFiles", "DataEngineGovernanceAuditImpactedFilesSchema"]
__pdoc__ = {
    "DataEngineGovernanceAuditImpactedFilesSchema.resource": False,
    "DataEngineGovernanceAuditImpactedFilesSchema.opts": False,
}

class DataEngineGovernanceAuditImpactedFilesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernanceAuditImpactedFiles object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the data_engine_governance_audit_impacted_files."""

    actions = marshmallow_fields.List(marshmallow_fields.Str, data_key="actions", allow_none=True)
    r""" List of actions taken on the file."""

    conditions_met = marshmallow_fields.List(marshmallow_fields.Str, data_key="conditions_met", allow_none=True)
    r""" List of conditions that were met during the governance audit."""

    data_collection = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_audit_impacted_files_data_collection", "DataEngineGovernanceAuditImpactedFilesDataCollectionSchema"),
                data_key="data_collection",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The data_collection field of the data_engine_governance_audit_impacted_files."""

    file = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_audit_impacted_files_file", "DataEngineGovernanceAuditImpactedFilesFileSchema"),
                data_key="file",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The file field of the data_engine_governance_audit_impacted_files."""

    guardrail_policy = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.guardrail_policy", "GuardrailPolicySchema"),
                data_key="guardrail_policy",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Guardrail policy."""

    timestamp = ImpreciseDateTime(
        data_key="timestamp",
        allow_none=True,
    )
    r""" Timestamp of the governance audit event.

Example: 2023-10-01T12:00:00.000+0000"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" UUID of the audit.

Example: 4bc7a442-86d1-11e0-ae1c-123478563499"""

    workspace = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_governance_audit_count_workspace", "DataEngineGovernanceAuditCountWorkspaceSchema"),
                data_key="workspace",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The workspace field of the data_engine_governance_audit_impacted_files."""

    @property
    def resource(self):
        return DataEngineGovernanceAuditImpactedFiles

    gettable_fields = [
        "links",
        "actions",
        "conditions_met",
        "data_collection",
        "file",
        "guardrail_policy",
        "timestamp",
        "uuid",
        "workspace",
    ]
    """links,actions,conditions_met,data_collection,file,guardrail_policy,timestamp,uuid,workspace,"""

    patchable_fields = [
        "actions",
        "conditions_met",
        "data_collection",
        "file",
        "guardrail_policy",
        "workspace",
    ]
    """actions,conditions_met,data_collection,file,guardrail_policy,workspace,"""

    postable_fields = [
        "actions",
        "conditions_met",
        "data_collection",
        "file",
        "guardrail_policy",
        "workspace",
    ]
    """actions,conditions_met,data_collection,file,guardrail_policy,workspace,"""

class DataEngineGovernanceAuditImpactedFiles(Resource):
    r""" Governance audit information. """

    _schema = DataEngineGovernanceAuditImpactedFilesSchema
    _path = "/api/data-engine/governance/audit/files"

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves governance audit information for impacted files associated with a specific guardrail policy within a workspace.
**Usage:**
To retrieve audit information for impacted files, use the following endpoint format:
`/data-engine/governance/audit/files/{workspace.uuid}/{guardrail_policy.uuid}`
* `{workspace.uuid}`: The unique identifier of the workspace.
* `{guardrail_policy.uuid}`: The unique identifier of the guardrail policy.
This endpoint provides detailed audit data, including which files have been impacted by governance actions under the specified guardrail policy. It supports query parameters for filtering, ordering, and limiting results, making it suitable for integration into compliance monitoring, reporting, or automation workflows.
**Key Features:**
* Returns audit details for files affected by a particular guardrail policy in a workspace.
* Supports filtering, ordering, and pagination through standard query parameters.
* Useful for compliance, audit tracking, and governance reporting.
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
        """Returns a count of all DataEngineGovernanceAuditImpactedFiles resources that match the provided query"""
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
        """Returns a list of RawResources that represent DataEngineGovernanceAuditImpactedFiles resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves governance audit information for impacted files associated with a specific guardrail policy within a workspace.
**Usage:**
To retrieve audit information for impacted files, use the following endpoint format:
`/data-engine/governance/audit/files/{workspace.uuid}/{guardrail_policy.uuid}`
* `{workspace.uuid}`: The unique identifier of the workspace.
* `{guardrail_policy.uuid}`: The unique identifier of the guardrail policy.
This endpoint provides detailed audit data, including which files have been impacted by governance actions under the specified guardrail policy. It supports query parameters for filtering, ordering, and limiting results, making it suitable for integration into compliance monitoring, reporting, or automation workflows.
**Key Features:**
* Returns audit details for files affected by a particular guardrail policy in a workspace.
* Supports filtering, ordering, and pagination through standard query parameters.
* Useful for compliance, audit tracking, and governance reporting.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






