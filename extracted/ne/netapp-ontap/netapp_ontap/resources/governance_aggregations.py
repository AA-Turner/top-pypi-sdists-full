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


__all__ = ["GovernanceAggregations", "GovernanceAggregationsSchema"]
__pdoc__ = {
    "GovernanceAggregationsSchema.resource": False,
    "GovernanceAggregationsSchema.opts": False,
}

class GovernanceAggregationsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GovernanceAggregations object"""

    classifier_category_count = Size(
        data_key="classifier_category_count",
        allow_none=True,
    )
    r""" Total number of classifier categories across all workspaces.

Example: 4"""

    classifier_matched_in_last30_days_count = Size(
        data_key="classifier_matched_in_last30_days_count",
        allow_none=True,
    )
    r""" Number of classifiers matched in the last 30 days.

Example: 4"""

    data_collection_count = Size(
        data_key="data_collection_count",
        allow_none=True,
    )
    r""" Total number of data collections across all workspaces.

Example: 7"""

    data_container_count = Size(
        data_key="data_container_count",
        allow_none=True,
    )
    r""" Total number of data containers across all workspaces.

Example: 8"""

    enabled_classifier_count = Size(
        data_key="enabled_classifier_count",
        allow_none=True,
    )
    r""" Total number of enabled classifiers across all workspaces.

Example: 6"""

    enabled_guardrail_count = Size(
        data_key="enabled_guardrail_count",
        allow_none=True,
    )
    r""" Total number of enabled guardrails across all workspaces.

Example: 3"""

    guardrail_with_disabled_classifier_count = Size(
        data_key="guardrail_with_disabled_classifier_count",
        allow_none=True,
    )
    r""" Number of guardrails that have disabled classifiers.

Example: 5"""

    guardrail_workspace_count = Size(
        data_key="guardrail_workspace_count",
        allow_none=True,
    )
    r""" Number of workspaces with guardrails.

Example: 2"""

    impacted_entities_by_guardrails_count = Size(
        data_key="impacted_entities_by_guardrails_count",
        allow_none=True,
    )
    r""" Total number of entities impacted by guardrails across all workspaces.

Example: 2"""

    non_guardrail_workspace_count = Size(
        data_key="non_guardrail_workspace_count",
        allow_none=True,
    )
    r""" Number of workspaces without guardrails.

Example: 4"""

    recent_workspaces = marshmallow_fields.List(marshmallow_fields.Str, data_key="recent_workspaces", allow_none=True)
    r""" The recent_workspaces field of the governance_aggregations."""

    scanned_content_size = Size(
        data_key="scanned_content_size",
        allow_none=True,
    )
    r""" Total scanned content size across all workspaces.

Example: 8776552"""

    simulated_guardrail_count = Size(
        data_key="simulated_guardrail_count",
        allow_none=True,
    )
    r""" Number of guardrails that are in testing.

Example: 2"""

    workspace_count = Size(
        data_key="workspace_count",
        allow_none=True,
    )
    r""" Total number of workspaces.

Example: 2"""

    @property
    def resource(self):
        return GovernanceAggregations

    gettable_fields = [
        "classifier_category_count",
        "classifier_matched_in_last30_days_count",
        "data_collection_count",
        "data_container_count",
        "enabled_classifier_count",
        "enabled_guardrail_count",
        "guardrail_with_disabled_classifier_count",
        "guardrail_workspace_count",
        "impacted_entities_by_guardrails_count",
        "non_guardrail_workspace_count",
        "recent_workspaces",
        "scanned_content_size",
        "simulated_guardrail_count",
        "workspace_count",
    ]
    """classifier_category_count,classifier_matched_in_last30_days_count,data_collection_count,data_container_count,enabled_classifier_count,enabled_guardrail_count,guardrail_with_disabled_classifier_count,guardrail_workspace_count,impacted_entities_by_guardrails_count,non_guardrail_workspace_count,recent_workspaces,scanned_content_size,simulated_guardrail_count,workspace_count,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class GovernanceAggregations(Resource):
    """Allows interaction with GovernanceAggregations objects on the host"""

    _schema = GovernanceAggregationsSchema
    _path = "/api/data-engine/governance/aggregation"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves aggregation data across all workspaces.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





