# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""`run_regression_tests` refuses an EU connection before it reads it from the public API."""

from __future__ import annotations

import logging
from typing import Any, Callable, NamedTuple, cast
from unittest.mock import patch

import pytest
from fastmcp import Context

from airbyte_ops_mcp.cloud_admin.version_overrides import ResolvedCloudAuth
from airbyte_ops_mcp.github_actions import WorkflowDispatchResult
from airbyte_ops_mcp.mcp import connector_qa
from airbyte_ops_mcp.mcp.connector_qa import (
    ConnectorRepo,
    RunRegressionTestsResponse,
    TestRunStatus,
    run_regression_tests,
)

pytestmark = pytest.mark.unit

CONNECTION_ID = "11111111-1111-1111-1111-111111111111"
WORKSPACE_ID = "22222222-2222-2222-2222-222222222222"

Lookup = Callable[[list[str]], list[dict[str, Any]]]


def _row(dataplane_name: str | None) -> dict[str, Any]:
    """One `query_connection_workspace_details` row, as the Prod DB returns it."""
    return {
        "connection_id": CONNECTION_ID,
        "workspace_id": WORKSPACE_ID,
        "organization_id": "33333333-3333-3333-3333-333333333333",
        "dataplane_group_id": "44444444-4444-4444-4444-444444444444",
        "dataplane_name": dataplane_name,
    }


class Outcome(NamedTuple):
    response: RunRegressionTestsResponse
    dispatched: list[dict[str, str]]
    """The inputs of every workflow dispatch that happened."""
    validated: list[tuple[str, str]]
    """The `(connection_id, workspace_id)` of every workspace validation that happened."""


def _unreachable(_ids: list[str]) -> list[dict[str, Any]]:
    raise RuntimeError("replica unreachable")


def _run(lookup: Lookup, **kwargs: Any) -> Outcome:
    """Run the tool with the dispatch and the workspace validation stubbed.

    The data-plane lookup is replaced by `lookup`.
    """
    dispatched: list[dict[str, str]] = []
    validated: list[tuple[str, str]] = []

    def _fake_dispatch(
        *, inputs: dict[str, str], **_kwargs: Any
    ) -> WorkflowDispatchResult:
        dispatched.append(inputs)
        return WorkflowDispatchResult(workflow_url="https://example.com/workflow")

    def _fake_validate(
        connection_id: str, workspace_id: str, _auth: ResolvedCloudAuth
    ) -> None:
        validated.append((connection_id, workspace_id))

    with patch.object(
        connector_qa, "trigger_workflow_dispatch", _fake_dispatch
    ), patch.object(
        connector_qa, "resolve_ci_trigger_github_token", lambda: "token"
    ), patch.object(
        connector_qa,
        "resolve_cloud_auth",
        lambda _ctx: ResolvedCloudAuth(bearer_token="caller-token"),
    ), patch.object(
        connector_qa, "validate_connection_workspace", _fake_validate
    ), patch.object(connector_qa, "query_connection_workspace_details", lookup):
        response = run_regression_tests(
            connector_name="source-pokeapi",
            pr=1,
            repo=ConnectorRepo.AIRBYTE,
            ctx=cast(Context, object()),
            **kwargs,
        )

    return Outcome(response, dispatched, validated)


def test_an_eu_connection_with_unset_mode_dispatches_masked() -> None:
    outcome = _run(lambda _ids: [_row("EU")], connection_id=CONNECTION_ID)

    assert outcome.response.status is TestRunStatus.QUEUED
    assert outcome.dispatched[0]["output_mode"] == "masked"


def test_raw_eu_request_is_refused_before_workspace_validation() -> None:
    outcome = _run(
        lambda _ids: [_row("EU")],
        connection_id=CONNECTION_ID,
        workspace_id=WORKSPACE_ID,
        output_mode="raw",
    )

    assert outcome.response.status is TestRunStatus.FAILED
    assert outcome.response.message == (
        "EU-resident connections always run masked; raw output is refused."
    )
    assert not outcome.validated
    assert not outcome.dispatched


def test_a_us_connection_with_unset_mode_uses_the_cli_masked_default() -> None:
    outcome = _run(
        lambda _ids: [_row("US")],
        connection_id=CONNECTION_ID,
        workspace_id=WORKSPACE_ID,
    )

    assert outcome.response.status is TestRunStatus.QUEUED
    assert outcome.validated == [(CONNECTION_ID, WORKSPACE_ID)]
    assert len(outcome.dispatched) == 1
    assert "output_mode" not in outcome.dispatched[0]


@pytest.mark.parametrize("dataplane_name", ["US", "US-Central"])
def test_a_non_eu_connection_dispatches_as_before(dataplane_name: str) -> None:
    outcome = _run(
        lambda _ids: [_row(dataplane_name)],
        connection_id=CONNECTION_ID,
    )

    assert outcome.response.status is TestRunStatus.QUEUED
    assert [inputs["connection_id"] for inputs in outcome.dispatched] == [CONNECTION_ID]
    assert "EU data-plane check skipped" not in outcome.response.message


def test_a_failed_lookup_fails_closed_for_an_explicit_raw_run(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Unknown residency cannot dispatch an unmasked run."""

    with caplog.at_level(logging.WARNING, logger=connector_qa.__name__):
        outcome = _run(_unreachable, connection_id=CONNECTION_ID, output_mode="raw")

    assert outcome.response.status is TestRunStatus.FAILED
    assert outcome.response.message == (
        f"Could not confirm connection {CONNECTION_ID}'s residency "
        "(the Prod DB replica lookup failed (RuntimeError)); "
        "pass output_mode='masked' to run it."
    )
    assert not outcome.dispatched
    assert any(
        CONNECTION_ID in record.getMessage()
        and "replica unreachable" in record.getMessage()
        for record in caplog.records
    )


def test_a_failed_lookup_uses_the_masked_connection_default(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING, logger=connector_qa.__name__):
        outcome = _run(_unreachable, connection_id=CONNECTION_ID)

    assert outcome.response.status is TestRunStatus.QUEUED
    assert len(outcome.dispatched) == 1
    assert "output_mode" not in outcome.dispatched[0]
    assert outcome.response.message.endswith(
        "EU data-plane check skipped: the Prod DB replica lookup failed (RuntimeError)."
    )
    assert any(
        CONNECTION_ID in record.getMessage()
        and "replica unreachable" in record.getMessage()
        for record in caplog.records
    )


@pytest.mark.parametrize(
    "dataplane_name", [None, "", "  "], ids=["null", "empty", "blank"]
)
def test_a_workspace_without_a_named_data_plane_group_uses_masked_default(
    dataplane_name: str | None,
) -> None:
    """Unknown residency may use the masked connection default."""

    outcome = _run(lambda _ids: [_row(dataplane_name)], connection_id=CONNECTION_ID)

    assert outcome.response.status is TestRunStatus.QUEUED
    assert len(outcome.dispatched) == 1
    assert "output_mode" not in outcome.dispatched[0]
    assert outcome.response.message.endswith(
        "EU data-plane check skipped: the workspace has no named dataplane "
        "group in the Prod DB replica."
    )


def test_an_unresolved_data_plane_group_fails_closed_for_raw() -> None:
    outcome = _run(
        lambda _ids: [_row(None)],
        connection_id=CONNECTION_ID,
        output_mode="raw",
    )

    assert outcome.response.status is TestRunStatus.FAILED
    assert outcome.response.message.endswith("pass output_mode='masked' to run it.")
    assert not outcome.dispatched


def test_an_unknown_connection_can_dispatch_when_masked(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING, logger=connector_qa.__name__):
        outcome = _run(
            lambda _ids: [],
            connection_id=CONNECTION_ID,
            output_mode="masked",
        )

    assert outcome.response.status is TestRunStatus.QUEUED
    assert len(outcome.dispatched) == 1
    assert outcome.dispatched[0]["output_mode"] == "masked"
    assert outcome.response.message.endswith(
        "EU data-plane check skipped: the connection is not in the Prod DB "
        "replica (unknown ID, or a tombstoned source or workspace)."
    )


def test_the_gsm_path_never_looks_up_a_data_plane() -> None:
    def _must_not_be_called(_ids: list[str]) -> list[dict[str, Any]]:
        raise AssertionError("the GSM path has no connection to look up")

    outcome = _run(_must_not_be_called)

    assert outcome.response.status is TestRunStatus.QUEUED
    assert "connection_id" not in outcome.dispatched[0]
    assert "EU data-plane check skipped" not in outcome.response.message
