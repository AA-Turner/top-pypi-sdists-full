# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for connector regression tests.

This module provides MCP tools for triggering regression tests on Airbyte Cloud
connections via GitHub Actions workflows. Regression tests can run in two modes:
- Single version mode: Tests a connector version against a connection config
- Comparison mode: Compares a target version against a control (baseline) version

Tests run asynchronously in GitHub Actions and results can be polled via workflow status.

Note: The term "regression tests" encompasses all connector validation testing.
The term "live tests" is reserved for scenarios where actual Cloud connections
are pinned to pre-release versions for real-world validation.

## MCP reference

.. include:: ../../../docs/mcp-generated/regression_tests.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

import uuid
from datetime import datetime
from enum import Enum
from typing import Annotated, Any

import requests
from airbyte.cloud import CloudWorkspace
from airbyte.cloud.auth import resolve_cloud_client_id, resolve_cloud_client_secret
from airbyte.exceptions import (
    AirbyteMissingResourceError,
    AirbyteWorkspaceMismatchError,
)
from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.constants import WorkspaceAliasEnum
from airbyte_ops_mcp.github_actions import (
    resolve_default_workflow_branch,
    trigger_workflow_dispatch,
)
from airbyte_ops_mcp.github_api import (
    GITHUB_API_BASE,
    resolve_ci_trigger_github_token,
)
from airbyte_ops_mcp.mcp.prerelease import ConnectorRepo

# =============================================================================
# GitHub Workflow Configuration
# =============================================================================

REGRESSION_TEST_REPO_OWNER = "airbytehq"
REGRESSION_TEST_REPO_NAME = "airbyte-ops-mcp"
REGRESSION_TEST_DEFAULT_BRANCH = "main"
# Unified regression test workflow (handles both single-version and comparison modes)
REGRESSION_TEST_WORKFLOW_FILE = "connector-regression-test.yml"


# =============================================================================
# Workspace Validation Helpers
# =============================================================================


def validate_connection_workspace(
    connection_id: str,
    workspace_id: str,
) -> None:
    """Validate that a connection belongs to the expected workspace.

    Uses PyAirbyte's CloudConnection.check_is_valid() method to verify that
    the connection exists and belongs to the specified workspace.

    Raises:
        ValueError: If Airbyte Cloud credentials are missing.
        AirbyteWorkspaceMismatchError: If connection belongs to a different workspace.
        AirbyteMissingResourceError: If connection is not found.
    """
    client_id = resolve_cloud_client_id()
    client_secret = resolve_cloud_client_secret()
    if not client_id or not client_secret:
        raise ValueError(
            "Missing Airbyte Cloud credentials. "
            "Set AIRBYTE_CLOUD_CLIENT_ID and AIRBYTE_CLOUD_CLIENT_SECRET env vars."
        )

    workspace = CloudWorkspace(
        workspace_id=workspace_id,
        client_id=client_id,
        client_secret=client_secret,
    )
    connection = workspace.get_connection(connection_id)
    connection.check_is_valid()


def _get_workflow_run_status(
    owner: str,
    repo: str,
    run_id: int,
    token: str,
) -> dict[str, Any]:
    """Get workflow run details from GitHub API.

    Args:
        owner: Repository owner (e.g., "airbytehq")
        repo: Repository name (e.g., "airbyte-ops-mcp")
        run_id: Workflow run ID
        token: GitHub API token

    Returns:
        Workflow run data dictionary.

    Raises:
        ValueError: If workflow run not found.
        requests.HTTPError: If API request fails.
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 404:
        raise ValueError(f"Workflow run {owner}/{repo}/actions/runs/{run_id} not found")
    response.raise_for_status()

    return response.json()


# =============================================================================
# Pydantic Models for Test Results
# =============================================================================


class TestRunStatus(str, Enum):
    """Status of a test run."""

    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class TestOutcome(str, Enum):
    """Outcome of a test (execution or comparison)."""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ValidationResultModel(BaseModel):
    """Result of a single validation check."""

    name: str = Field(description="Name of the validation check")
    passed: bool = Field(description="Whether the validation passed")
    message: str = Field(description="Human-readable result message")
    errors: list[str] = Field(
        default_factory=list,
        description="List of error messages if validation failed",
    )


class StreamComparisonResultModel(BaseModel):
    """Result of comparing a single stream between control and target."""

    stream_name: str = Field(description="Name of the stream")
    passed: bool = Field(description="Whether all comparisons passed")
    control_record_count: int = Field(description="Number of records in control")
    target_record_count: int = Field(description="Number of records in target")
    missing_pks: list[str] = Field(
        default_factory=list,
        description="Primary keys present in control but missing in target",
    )
    differing_records: int = Field(
        default=0,
        description="Number of records that differ between control and target",
    )
    message: str = Field(description="Human-readable comparison summary")


class RegressionTestExecutionResult(BaseModel):
    """Results from executing the connector (validations and record counts)."""

    outcome: TestOutcome = Field(description="Outcome of the execution")
    catalog_validations: list[ValidationResultModel] = Field(
        default_factory=list,
        description="Results of catalog validation checks",
    )
    record_validations: list[ValidationResultModel] = Field(
        default_factory=list,
        description="Results of record validation checks",
    )
    record_count: int = Field(
        default=0,
        description="Total number of records read",
    )
    error_message: str | None = Field(
        default=None,
        description="Error message if the execution failed",
    )


class RegressionTestComparisonResult(BaseModel):
    """Results from comparing target vs control connector versions."""

    outcome: TestOutcome = Field(description="Outcome of the comparison")
    baseline_version: str | None = Field(
        default=None,
        description="Version of the baseline (control) connector",
    )
    stream_comparisons: list[StreamComparisonResultModel] = Field(
        default_factory=list,
        description="Per-stream comparison results",
    )
    error_message: str | None = Field(
        default=None,
        description="Error message if the comparison failed",
    )


class RegressionTestResult(BaseModel):
    """Complete result of a regression test run."""

    run_id: str = Field(description="Unique identifier for this test run")
    connection_id: str = Field(description="The connection being tested")
    workspace_id: str = Field(description="The workspace containing the connection")
    status: TestRunStatus = Field(description="Overall status of the test run")
    target_version: str | None = Field(
        default=None,
        description="Version of the target connector being tested",
    )
    baseline_version: str | None = Field(
        default=None,
        description="Version of the baseline connector (if comparison mode)",
    )
    evaluation_mode: str = Field(
        default="diagnostic",
        description="Evaluation mode used (diagnostic or strict)",
    )
    compare_versions: bool = Field(
        default=False,
        description="Whether comparison mode was used (target vs control)",
    )
    execution_result: RegressionTestExecutionResult | None = Field(
        default=None,
        description="Results from executing the connector (validations and record counts)",
    )
    comparison_result: RegressionTestComparisonResult | None = Field(
        default=None,
        description="Results from comparing target vs control connector versions",
    )
    artifacts: dict[str, str] = Field(
        default_factory=dict,
        description="Paths to generated artifacts (JSONL, DuckDB, HAR files)",
    )
    human_summary: str = Field(
        default="",
        description="Human-readable summary of the test results",
    )
    started_at: datetime | None = Field(
        default=None,
        description="When the test run started",
    )
    completed_at: datetime | None = Field(
        default=None,
        description="When the test run completed",
    )
    test_description: str | None = Field(
        default=None,
        description="Optional description/context for this test run",
    )


class RunRegressionTestsResponse(BaseModel):
    """Response from starting a regression test via GitHub Actions workflow."""

    run_id: str = Field(
        description="Unique identifier for the test run (internal tracking ID)"
    )
    status: TestRunStatus = Field(description="Initial status of the test run")
    message: str = Field(description="Human-readable status message")
    workflow_url: str | None = Field(
        default=None,
        description="URL to view the GitHub Actions workflow file",
    )
    github_run_id: int | None = Field(
        default=None,
        description="GitHub Actions workflow run ID (use with check_ci_workflow_status)",
    )
    github_run_url: str | None = Field(
        default=None,
        description="Direct URL to the GitHub Actions workflow run",
    )


# =============================================================================
# MCP Tools
# =============================================================================


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def run_regression_tests(
    connector_name: Annotated[
        str,
        "Connector name to build from source (e.g., 'source-pokeapi'). Required.",
    ],
    pr: Annotated[
        int,
        "PR number to checkout and build from (e.g., 70847). Required. "
        "The PR must be from the repository specified by the 'repo' parameter.",
    ],
    repo: Annotated[
        ConnectorRepo,
        "Repository where the connector PR is located. "
        "Use 'airbyte' for OSS connectors (default) or 'airbyte-enterprise' for enterprise connectors.",
    ],
    connection_id: Annotated[
        str | None,
        "Airbyte Cloud connection ID to fetch config/catalog from. "
        "If not provided, uses GSM integration test secrets.",
    ] = None,
    skip_compare: Annotated[
        bool,
        "If True, skip comparison and run single-version tests only. "
        "If False (default), run comparison tests (target vs control versions).",
    ] = False,
    skip_read_action: Annotated[
        bool,
        "If True, skip the read action (run only spec, check, discover). "
        "If False (default), run all verbs including read.",
    ] = False,
    override_test_image: Annotated[
        str | None,
        "Override test connector image with tag (e.g., 'airbyte/source-github:1.0.0'). "
        "Ignored if skip_compare=False.",
    ] = None,
    override_control_image: Annotated[
        str | None,
        "Override control connector image (baseline version) with tag. "
        "Ignored if skip_compare=True.",
    ] = None,
    workspace_id: Annotated[
        str | WorkspaceAliasEnum | None,
        "Optional Airbyte Cloud workspace ID (UUID) or alias. If provided with connection_id, "
        "validates that the connection belongs to this workspace before triggering tests. "
        "Accepts '@devin-ai-sandbox' as an alias for the Devin AI sandbox workspace.",
    ] = None,
    selected_streams: Annotated[
        list[str] | None,
        "List of stream names to include in the read. Only these streams will be included "
        "in the configured catalog. This is useful to limit data volume by testing only "
        "specific streams. If not provided, all streams are tested.",
    ] = None,
    enable_debug_logs: Annotated[
        bool,
        "Enable debug-level logging for regression test output. "
        "Also passed as `LOG_LEVEL=DEBUG` to the connector Docker container.",
    ] = False,
    with_state: Annotated[
        bool | None,
        "Fetch and pass the connection's current state to the read command, "
        "producing a warm read instead of a cold read. Defaults to `True` when "
        "`connection_id` is provided, `False` otherwise. Has no effect unless "
        "the command is `read`.",
    ] = None,
) -> RunRegressionTestsResponse:
    """Start a regression test run via GitHub Actions workflow.

    This tool triggers the regression test workflow which builds the connector
    from the specified PR and runs tests against it.

    Supports both OSS connectors (from airbytehq/airbyte) and enterprise connectors
    (from airbytehq/airbyte-enterprise). Use the 'repo' parameter to specify which
    repository contains the connector PR.

    - skip_compare=False (default): Comparison mode - compares the PR version
      against the baseline (control) version.
    - skip_compare=True: Single-version mode - runs tests without comparison.

    If connection_id is provided, config/catalog are fetched from Airbyte Cloud.
    Otherwise, GSM integration test secrets are used.

    Returns immediately with a run_id and workflow URL. Check the workflow URL
    to monitor progress and view results.

    Requires GITHUB_CI_WORKFLOW_TRIGGER_PAT or GITHUB_TOKEN environment variable
    with 'actions:write' permission.
    """
    # Resolve workspace ID alias
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)

    # Generate a unique run ID for tracking
    run_id = str(uuid.uuid4())

    # Get GitHub token
    try:
        token = resolve_ci_trigger_github_token()
    except ValueError as e:
        return RunRegressionTestsResponse(
            run_id=run_id,
            status=TestRunStatus.FAILED,
            message=str(e),
            workflow_url=None,
        )

    # Validate workspace membership if workspace_id and connection_id are provided
    if resolved_workspace_id and connection_id:
        try:
            validate_connection_workspace(connection_id, resolved_workspace_id)
        except (
            ValueError,
            AirbyteWorkspaceMismatchError,
            AirbyteMissingResourceError,
        ) as e:
            return RunRegressionTestsResponse(
                run_id=run_id,
                status=TestRunStatus.FAILED,
                message=str(e),
                workflow_url=None,
            )

    # Build workflow inputs - connector_name, pr, and repo are required
    workflow_inputs: dict[str, str] = {
        "connector_name": connector_name,
        "pr": str(pr),
        "repo": repo,
    }

    # Add optional inputs
    if connection_id:
        workflow_inputs["connection_id"] = connection_id
    if skip_compare:
        workflow_inputs["skip_compare"] = "true"
    if skip_read_action:
        workflow_inputs["skip_read_action"] = "true"
    if override_test_image:
        workflow_inputs["override_test_image"] = override_test_image
    if override_control_image:
        workflow_inputs["override_control_image"] = override_control_image
    if selected_streams:
        workflow_inputs["selected_streams"] = ",".join(selected_streams)
    if enable_debug_logs:
        workflow_inputs["enable_debug_logs"] = "true"
    if with_state is True:
        workflow_inputs["with_state"] = "true"
    elif with_state is False:
        workflow_inputs["with_state"] = "false"

    mode_description = "single-version" if skip_compare else "comparison"

    dispatch_result = trigger_workflow_dispatch(
        owner=REGRESSION_TEST_REPO_OWNER,
        repo=REGRESSION_TEST_REPO_NAME,
        workflow_file=REGRESSION_TEST_WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(REGRESSION_TEST_DEFAULT_BRANCH),
        inputs=workflow_inputs,
        token=token,
    )

    view_url = dispatch_result.run_url or dispatch_result.workflow_url
    connection_info = f" for connection {connection_id}" if connection_id else ""
    repo_info = f" from {repo}" if repo != ConnectorRepo.AIRBYTE else ""
    return RunRegressionTestsResponse(
        run_id=run_id,
        status=TestRunStatus.QUEUED,
        message=(
            f"{mode_description.capitalize()} regression test workflow triggered "
            f"for {connector_name} (PR #{pr}{repo_info}){connection_info}. View progress at: {view_url}"
        ),
        workflow_url=dispatch_result.workflow_url,
        github_run_id=dispatch_result.run_id,
        github_run_url=dispatch_result.run_url,
    )


# =============================================================================
# Registration
# =============================================================================


def register_regression_tests_tools(app: FastMCP) -> None:
    """Register regression tests tools with the FastMCP app.

    Args:
        app: FastMCP application instance
    """
    register_mcp_tools(app, mcp_module=__name__)
