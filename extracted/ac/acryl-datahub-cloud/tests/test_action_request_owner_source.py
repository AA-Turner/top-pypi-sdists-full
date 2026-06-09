from typing import Any, Dict, cast
from unittest.mock import MagicMock

import pytest

from acryl_datahub_cloud.action_request.action_request_owner_source import (
    ActionRequestOwnerSource,
    ActionRequestOwnerSourceConfig,
)
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.graph.client import DataHubGraph
from datahub.metadata.schema_classes import ActionRequestInfoClass

WF_URN = "urn:li:actionRequest:wf-1"
TAG_URN = "urn:li:actionRequest:tag-1"
DATASET = "urn:li:dataset:(urn:li:dataPlatform:snowflake,db.t,PROD)"


def _request(urn: str, action_type: str) -> Dict[str, Any]:
    return {
        "urn": urn,
        "type": action_type,
        "entity": {"urn": DATASET},
        "subResource": None,
        "subResourceType": None,
        "assignedUsers": ["urn:li:corpuser:alice"],
        "assignedGroups": [],
        "assignedRoles": [],
    }


@pytest.fixture
def source() -> ActionRequestOwnerSource:
    ctx = MagicMock(spec=PipelineContext)
    ctx.require_graph.return_value = MagicMock(spec=DataHubGraph)
    src = ActionRequestOwnerSource(ActionRequestOwnerSourceConfig(), ctx)
    src.graph = cast(DataHubGraph, ctx.require_graph())
    return src


def test_owner_sync_overwrites_proposals_but_skips_workflow_requests(
    source: ActionRequestOwnerSource,
) -> None:
    """Owner-sync overwrites assignees for ownership-based proposals but must never touch
    WORKFLOW_FORM_REQUESTs, whose assignees are owned by the workflow step definition.

    Regression test for CAT-2218: getActionRequestAssignee returns [] for workflow
    requests, so without the skip the source wiped their workflow-resolved assignees.
    The batch below mixes both types; only the proposal should yield an overwrite MCP.
    """
    graph = cast(MagicMock, source.graph)

    def fake_graphql(query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        if "listActionRequests" in query:
            return {
                "listActionRequests": {
                    "total": 2,
                    "actionRequests": [
                        _request(WF_URN, "WORKFLOW_FORM_REQUEST"),
                        _request(TAG_URN, "TAG_ASSOCIATION"),
                    ],
                    "nextScrollId": None,
                }
            }
        if "getActionRequestAssignee" in query:
            # The proposal's computed owners differ from the stored ["alice"], forcing a rewrite.
            return {"getActionRequestAssignee": ["urn:li:corpuser:bob"]}
        raise AssertionError(f"unexpected query: {query}")

    graph.execute_graphql.side_effect = fake_graphql
    graph.get_aspect_v2.return_value = ActionRequestInfoClass(
        type="TAG_ASSOCIATION",
        assignedUsers=["urn:li:corpuser:alice"],
        assignedGroups=[],
        created=0,
        createdBy="urn:li:corpuser:alice",
    )

    overwritten = [
        cast(MetadataChangeProposalWrapper, wu.metadata).entityUrn
        for wu in source.get_workunits()
    ]

    assert overwritten == [TAG_URN]  # workflow request produced no MCP
    assert source.report.skipped_workflow_requests == 1
    assert source.report.incorrect_proposal_owners == 1
