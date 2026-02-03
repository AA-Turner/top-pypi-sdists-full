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


__all__ = ["GovernanceWorkspaceAggregations", "GovernanceWorkspaceAggregationsSchema"]
__pdoc__ = {
    "GovernanceWorkspaceAggregationsSchema.resource": False,
    "GovernanceWorkspaceAggregationsSchema.opts": False,
}

class GovernanceWorkspaceAggregationsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GovernanceWorkspaceAggregations object"""

    age_of_data = marshmallow_fields.List(marshmallow_fields.Str, data_key="age_of_data", allow_none=True)
    r""" The age_of_data field of the governance_workspace_aggregations."""

    anonymized_entity_count = Size(
        data_key="anonymized_entity_count",
        allow_none=True,
    )
    r""" Number of files anonymized.

Example: 226526256"""

    data_classifier = marshmallow_fields.List(marshmallow_fields.Str, data_key="data_classifier", allow_none=True)
    r""" The data_classifier field of the governance_workspace_aggregations."""

    data_classifier_categories = marshmallow_fields.List(marshmallow_fields.Str, data_key="data_classifier_categories", allow_none=True)
    r""" The data_classifier_categories field of the governance_workspace_aggregations."""

    data_collection_count = Size(
        data_key="data_collection_count",
        allow_none=True,
    )
    r""" Number of data collections in the workspace.

Example: 3"""

    data_collection_entity_count = Size(
        data_key="data_collection_entity_count",
        allow_none=True,
    )
    r""" Number of entities used in data collections.

Example: 100"""

    data_container_count = Size(
        data_key="data_container_count",
        allow_none=True,
    )
    r""" Number of data containers in the workspace.

Example: 5"""

    data_sources = marshmallow_fields.List(marshmallow_fields.Str, data_key="data_sources", allow_none=True)
    r""" The data_sources field of the governance_workspace_aggregations."""

    document_category_count = Size(
        data_key="document_category_count",
        allow_none=True,
    )
    r""" Number of document categories in the workspace.

Example: 2"""

    document_classifier = marshmallow_fields.List(marshmallow_fields.Str, data_key="document_classifier", allow_none=True)
    r""" The document_classifier field of the governance_workspace_aggregations."""

    document_classifier_categories = marshmallow_fields.List(marshmallow_fields.Str, data_key="document_classifier_categories", allow_none=True)
    r""" The document_classifier_categories field of the governance_workspace_aggregations."""

    entity_count = Size(
        data_key="entity_count",
        allow_none=True,
    )
    r""" Total number of entities in the workspace.

Example: 200"""

    excluded_entity_count = Size(
        data_key="excluded_entity_count",
        allow_none=True,
    )
    r""" Number of entities excluded from data collections.

Example: 283863685"""

    guardrail_count = Size(
        data_key="guardrail_count",
        allow_none=True,
    )
    r""" Number of guardrails in the workspace.

Example: 2"""

    guardrail_impacted_entity_count = Size(
        data_key="guardrail_impacted_entity_count",
        allow_none=True,
    )
    r""" Number of entities impacted by guardrails in the workspace.

Example: 3"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the workspace.

Example: gov_workspace"""

    pii_percent = Size(
        data_key="pii_percent",
        allow_none=True,
    )
    r""" PII percentage for the workspace.

Example: 50"""

    scanned_content = Size(
        data_key="scanned_content",
        allow_none=True,
    )
    r""" Total size of scanned content in the workspace.

Example: 1656564"""

    sensitive_entity_count = Size(
        data_key="sensitive_entity_count",
        allow_none=True,
    )
    r""" Sensitive entities count in the workspace.

Example: 50"""

    size_of_data = marshmallow_fields.List(marshmallow_fields.Str, data_key="size_of_data", allow_none=True)
    r""" The size_of_data field of the governance_workspace_aggregations."""

    stale_entity_count = Size(
        data_key="stale_entity_count",
        allow_none=True,
    )
    r""" Number of stale entities in the workspace.

Example: 1"""

    state = marshmallow_fields.Str(
        data_key="state",
        allow_none=True,
    )
    r""" State of the workspace.

Example: Active"""

    top_enforced_guardrails = marshmallow_fields.List(marshmallow_fields.Str, data_key="top_enforced_guardrails", allow_none=True)
    r""" The top_enforced_guardrails field of the governance_workspace_aggregations."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" UUID of the workspace.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return GovernanceWorkspaceAggregations

    gettable_fields = [
        "age_of_data",
        "anonymized_entity_count",
        "data_classifier",
        "data_classifier_categories",
        "data_collection_count",
        "data_collection_entity_count",
        "data_container_count",
        "data_sources",
        "document_category_count",
        "document_classifier",
        "document_classifier_categories",
        "entity_count",
        "excluded_entity_count",
        "guardrail_count",
        "guardrail_impacted_entity_count",
        "name",
        "pii_percent",
        "scanned_content",
        "sensitive_entity_count",
        "size_of_data",
        "stale_entity_count",
        "state",
        "top_enforced_guardrails",
        "uuid",
    ]
    """age_of_data,anonymized_entity_count,data_classifier,data_classifier_categories,data_collection_count,data_collection_entity_count,data_container_count,data_sources,document_category_count,document_classifier,document_classifier_categories,entity_count,excluded_entity_count,guardrail_count,guardrail_impacted_entity_count,name,pii_percent,scanned_content,sensitive_entity_count,size_of_data,stale_entity_count,state,top_enforced_guardrails,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class GovernanceWorkspaceAggregations(Resource):
    """Allows interaction with GovernanceWorkspaceAggregations objects on the host"""

    _schema = GovernanceWorkspaceAggregationsSchema
    _path = "/api/data-engine/governance/aggregation/workspaces"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves aggregation data for workspaces.
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
        """Returns a count of all GovernanceWorkspaceAggregations resources that match the provided query"""
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
        """Returns a list of RawResources that represent GovernanceWorkspaceAggregations resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves aggregation data for workspaces.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves aggregation data for workspaces.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





