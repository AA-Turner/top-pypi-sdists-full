# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for connector quality assurance: regression tests and connector release blocking.

## MCP reference

.. include:: ../../../docs/mcp-generated/connector_qa.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

import logging
import uuid
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Literal, NamedTuple
from urllib.parse import quote

import requests
import yaml
from airbyte.cloud import CloudWorkspace
from airbyte.exceptions import (
    AirbyteMissingResourceError,
    AirbyteNoCloudCredentialsError,
    AirbyteWorkspaceMismatchError,
    PyAirbyteSecretNotFoundError,
)
from fastmcp import Context, FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.cloud_admin.auth import CloudAuthError
from airbyte_ops_mcp.cloud_admin.version_overrides import ResolvedCloudAuth
from airbyte_ops_mcp.constants import WorkspaceAliasEnum
from airbyte_ops_mcp.github_actions import (
    resolve_default_workflow_branch,
    trigger_workflow_dispatch,
)
from airbyte_ops_mcp.github_api import (
    GITHUB_API_BASE,
    get_file_contents_at_ref,
    resolve_ci_trigger_github_token,
)
from airbyte_ops_mcp.mcp.cloud_auth import resolve_cloud_auth
from airbyte_ops_mcp.mcp.connector_versions import ConnectorRepo
from airbyte_ops_mcp.prod_db_access.queries import query_connection_workspace_details
from airbyte_ops_mcp.regression_tests.models import OUTPUT_MODES
from airbyte_ops_mcp.regression_tests.read_inputs import READ_TIMEOUT_MINUTES_MAX
from airbyte_ops_mcp.regression_tests.seed_state import (
    SEED_STATE_NEEDS_CONNECTION,
    seed_state_error,
)

logger = logging.getLogger(__name__)

REGRESSION_TEST_REPO_OWNER = "airbytehq"

REGRESSION_TEST_REPO_NAME = "airbyte-ops-mcp"

REGRESSION_TEST_DEFAULT_BRANCH = "main"

REGRESSION_TEST_WORKFLOW_FILE = "connector-regression-test.yml"

_MISSING_CLOUD_AUTH_MESSAGE = (
    "Airbyte Cloud credentials are required for workspace validation. "
    "Provide an Authorization bearer token, both "
    "X-Airbyte-Cloud-Client-Id and X-Airbyte-Cloud-Client-Secret headers, or "
    "AIRBYTE_CLOUD_CLIENT_ID and AIRBYTE_CLOUD_CLIENT_SECRET environment variables."
)


def validate_connection_workspace(
    connection_id: str,
    workspace_id: str,
    auth: ResolvedCloudAuth,
) -> None:
    """Validate that a connection belongs to the expected workspace.

    Uses PyAirbyte's CloudConnection.check_is_valid() method to verify that
    the connection exists and belongs to the specified workspace.

    Raises:
        `AirbyteWorkspaceMismatchError`: If connection belongs to a different workspace.
        `AirbyteMissingResourceError`: If connection is not found.
    """
    workspace = CloudWorkspace(
        workspace_id=workspace_id,
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
    )
    connection = workspace.get_connection(connection_id)
    connection.check_is_valid()


class _EuDataPlaneCheck(NamedTuple):
    """Outcome of the trigger-time EU data-plane lookup.

    `skipped` is the reason the check could not decide, or `None` when it did.
    """

    is_eu: bool
    skipped: str | None = None


def _check_eu_data_plane(connection_id: str) -> _EuDataPlaneCheck:
    """Look up the connection's data plane in the Prod DB replica.

    `is_eu` is True only when the replica returns a row whose dataplane group
    is named exactly `EU`. When the check cannot decide, `is_eu` is False and
    `skipped` says why, so the caller can report the unresolved residency and
    fail closed unless masking was explicitly requested. The lookup exception
    text is kept out of the response because it can contain SQL or connection
    details; the exception class is safe to report.

    A missing row (an unknown ID, or a tombstoned source or workspace), or a
    workspace without a named dataplane group, cannot be treated as US. A NULL
    or empty name counts as unknown, not as US: this is a residency gate,
    unlike `tier_cache`, which defaults a missing group to US for tier lookups.

    This lookup and the secret retriever differ in three cases:

    - a tombstoned source or workspace: no row here, while the retriever
      ignores tombstones and still refuses a deleted EU connection;
    - a workspace with no dataplane group, or a group with an empty name: a
      NULL or empty name here; the retriever refuses the missing group;
    - a custom EU group with a name other than exactly `EU` is not recognized.
    """
    try:
        rows = query_connection_workspace_details([connection_id])
    except Exception as exc:
        return _skip_eu_check(
            connection_id,
            f"the Prod DB replica lookup failed ({type(exc).__name__})",
            detail=f": {exc}",
        )
    if not rows:
        return _skip_eu_check(
            connection_id,
            "the connection is not in the Prod DB replica "
            "(unknown ID, or a tombstoned source or workspace)",
        )
    dataplane_name = rows[0].get("dataplane_name")
    if not dataplane_name or not dataplane_name.strip():
        return _skip_eu_check(
            connection_id,
            "the workspace has no named dataplane group in the Prod DB replica",
        )
    return _EuDataPlaneCheck(is_eu=dataplane_name == "EU")


def _skip_eu_check(
    connection_id: str, reason: str, detail: str = ""
) -> _EuDataPlaneCheck:
    """Fail open with `reason` in the response; `detail` goes to the log only."""
    logger.warning(
        f"EU data-plane check skipped for connection {connection_id}: {reason}{detail}"
    )
    return _EuDataPlaneCheck(is_eu=False, skipped=reason)


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


def _api_error_message(exc: requests.RequestException) -> str:
    """GitHub's own words for a failed request, or the exception's.

    A dispatch whose inputs pass GitHub's 65,535-character limit, which a
    large `state_json` can, comes back as a 422 whose body says so.
    """
    response = exc.response
    if response is not None:
        try:
            body = response.json()
        except ValueError:
            body = None
        message = body.get("message") if isinstance(body, dict) else None
        if message:
            return f"{response.status_code} {message}"
    return str(exc)


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
        "If not provided, prefers the default-config GSM integration-test secret "
        "before trying other connector secrets.",
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
    discover_missing_streams: Annotated[
        bool,
        "Read selected streams the connection does not sync yet, such as a stream "
        "the PR adds. READ discovers them on the PR version and adds them to the "
        "catalog. A stream the control version does not discover has no control "
        "side and is read by the target only; when every selected stream is new, "
        "also select one stream the connection already syncs, so the control reads "
        "something. Needs selected_streams.",
    ] = False,
    injected_sync_mode: Annotated[
        Literal["full_refresh", "incremental"] | None,
        "Sync mode for streams added by discover_missing_streams. Default prefers "
        "full refresh; incremental uses the stream's default cursor.",
    ] = None,
    enable_debug_logs: Annotated[
        bool,
        "Enable debug-level logging for regression test output. "
        "Also passed as `LOG_LEVEL=DEBUG` to the connector Docker container. "
        "Debug logs are off on masked runs for now: with `output_mode='masked'`, "
        "or on a `connection_id` run that leaves `output_mode` unset, the run "
        "goes ahead with them switched off.",
    ] = False,
    disable_http_replay: Annotated[
        bool,
        "Run both connector versions against the live API instead of replaying the "
        "control run's recorded HTTP responses. Replay is on by default and is what "
        "makes a record difference attributable to the version under test rather "
        "than to upstream drift, so only disable it for a connector whose traffic "
        "cannot be replayed faithfully. Comparison mode only.",
    ] = False,
    with_state: Annotated[
        bool | None,
        "Fetch and pass the connection's current state to the read command, "
        "producing a warm read instead of a cold read. Defaults to `True` when "
        "`connection_id` is provided, `False` otherwise. Has no effect unless "
        "the command is `read`.",
    ] = None,
    max_records: Annotated[
        int | None,
        "Stop each side of the read when a RECORD message arrives past this "
        "many in total, across its streams; a side that emits no more than "
        "this many reads in full. Bounds a read of a large connection; a read "
        "the cap stops is a smoke test of the records read before the cap, not "
        "a full regression, and the report says so on each side that stopped "
        "early. The two sides can stop at different records. At least 1. Leave "
        "unset for no cap. Has no effect unless the command is `read`.",
    ] = None,
    state_json: Annotated[
        str | None,
        "Airbyte state to seed the read with, as a JSON string holding a "
        "non-empty list of STREAM state messages (the shape "
        "`get_connection_state` returns; a GLOBAL or LEGACY state is refused). "
        "Both versions then start from these cursors instead of the "
        "connection's stored state, so `with_state` is ignored. Use it to replay "
        "a sync from a chosen point, for example the state a customer's failing "
        "sync started from. Needs `connection_id`: the connection's catalog says "
        "which streams sync incrementally, and without one every stream is read "
        "full_refresh and the seed would be ignored. A connector may clamp a "
        "seed to what its API still serves. The workflow keeps the seed out of "
        "the job log, and the report names the seeded streams but none of its "
        "values. Has no effect unless the command is `read`.",
    ] = None,
    output_mode: Annotated[
        Literal["masked", "raw"] | None,
        "How the connector output is written to the run artifacts. `masked` "
        "masks every record value as a type-and-length token as it is written, "
        "masks primary keys, keeps a cursor readable only when its declared type "
        "is an integer or a date, and keeps only the length of DEBUG, TRACE, "
        "ERROR and FATAL log messages, stack traces, error internals and every "
        "line of the connector's stderr; INFO and WARN log messages, a TRACE "
        "error's message and the CONNECTION_STATUS message stay readable. "
        "`raw` keeps the output as emitted. "
        "Leave unset for the default: `masked` on a `connection_id` run, which "
        "reads a customer's data, and `raw` otherwise. `raw` is an explicit "
        "opt-in for US connections and is refused for EU connections. A raw "
        "request also fails closed when residency cannot be confirmed. Pass "
        "`masked` to mask a GSM run. Debug logs are off on masked runs for now, "
        "so a masked run switches `enable_debug_logs` off.",
    ] = None,
    read_timeout_minutes: Annotated[
        int | None,
        "Minutes the read may take, from its start to its report; in comparison "
        "mode both versions share them. A read still running at the end is "
        "stopped, compared and reported as incomplete. Raise it for a connection "
        "too large to read in the default 170 minutes. From 1 to 300, so the run "
        "stays inside GitHub's six-hour job limit with fifty minutes for the "
        "other steps. Leave unset for the default. Has no effect unless the "
        "command is `read`.",
    ] = None,
    *,
    ctx: Context,
) -> RunRegressionTestsResponse:
    """Start a regression test run via GitHub Actions workflow.

    This tool triggers the regression test workflow which builds the connector
    from the specified PR and runs tests against it.

    Supports both OSS connectors (from airbytehq/airbyte) and enterprise connectors
    (from airbytehq/airbyte-enterprise). Use the 'repo' parameter to specify which
    repository contains the connector PR.

    - skip_compare=False (default): Comparison mode - compares the PR version
      against the baseline (control) version. A read is reported NOT EXERCISED,
      never a pass, when a stream only the target was configured to read
      (typically one the PR adds) returns no records: the comparison could not
      fail it, and the PR's new code path never ran.
    - skip_compare=True: Single-version mode - runs tests without comparison.

    If connection_id is provided, config/catalog are fetched from Airbyte Cloud.
    Otherwise, the default-config GSM integration-test secret is preferred before
    other connector secrets are tried. EU connections always run masked; raw
    output is refused. If residency cannot be confirmed, the run fails closed
    unless output_mode='masked' is explicitly requested.

    Returns immediately with a run_id and workflow URL. Check the workflow URL
    to monitor progress and view results.

    Requires GITHUB_CI_WORKFLOW_TRIGGER_PAT or GITHUB_TOKEN environment variable
    with 'actions:write' permission.
    """
    # Resolve workspace ID alias
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)

    # Generate a unique run ID for tracking
    run_id = str(uuid.uuid4())

    if max_records is not None and max_records < 1:
        return RunRegressionTestsResponse(
            run_id=run_id,
            status=TestRunStatus.FAILED,
            message=f"max_records must be at least 1, got {max_records}",
            workflow_url=None,
        )

    if output_mode is not None and output_mode not in OUTPUT_MODES:
        return RunRegressionTestsResponse(
            run_id=run_id,
            status=TestRunStatus.FAILED,
            message=(
                f"output_mode must be one of {', '.join(OUTPUT_MODES)}, "
                f"got {output_mode!r}"
            ),
            workflow_url=None,
        )

    if read_timeout_minutes is not None and not (
        1 <= read_timeout_minutes <= READ_TIMEOUT_MINUTES_MAX
    ):
        return RunRegressionTestsResponse(
            run_id=run_id,
            status=TestRunStatus.FAILED,
            message=(
                "read_timeout_minutes must be from 1 to "
                f"{READ_TIMEOUT_MINUTES_MAX}, got {read_timeout_minutes}"
            ),
            workflow_url=None,
        )

    # A seed is judged here, where a mistake costs a message rather than a
    # build; the workflow judges it again before SPEC, by the same rules, for
    # a direct dispatch.
    if state_json is not None:
        seed_error = (
            SEED_STATE_NEEDS_CONNECTION
            if not connection_id
            else seed_state_error(state_json)
        )
        if seed_error:
            return RunRegressionTestsResponse(
                run_id=run_id,
                status=TestRunStatus.FAILED,
                message=seed_error,
                workflow_url=None,
            )

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

    effective_output_mode = output_mode or ("masked" if connection_id else "raw")

    # Resolve residency before dispatch or workspace validation.
    eu_check: _EuDataPlaneCheck | None = None
    if connection_id:
        eu_check = _check_eu_data_plane(connection_id)
        if eu_check.skipped and effective_output_mode != "masked":
            return RunRegressionTestsResponse(
                run_id=run_id,
                status=TestRunStatus.FAILED,
                message=(
                    f"Could not confirm connection {connection_id}'s residency "
                    f"({eu_check.skipped}); pass output_mode='masked' to run it."
                ),
                workflow_url=None,
            )
        if eu_check.is_eu and output_mode == "raw":
            return RunRegressionTestsResponse(
                run_id=run_id,
                status=TestRunStatus.FAILED,
                message="EU-resident connections always run masked; "
                "raw output is refused.",
                workflow_url=None,
            )
        if eu_check.is_eu and output_mode is None:
            output_mode = "masked"

    # Validate workspace membership if workspace_id and connection_id are provided
    if resolved_workspace_id and connection_id:
        try:
            auth = resolve_cloud_auth(ctx)
            if not (auth.bearer_token or (auth.client_id and auth.client_secret)):
                raise CloudAuthError(_MISSING_CLOUD_AUTH_MESSAGE)
            validate_connection_workspace(connection_id, resolved_workspace_id, auth)
        except PyAirbyteSecretNotFoundError:
            return RunRegressionTestsResponse(
                run_id=run_id,
                status=TestRunStatus.FAILED,
                message=_MISSING_CLOUD_AUTH_MESSAGE,
                workflow_url=None,
            )
        except (
            ValueError,
            CloudAuthError,
            AirbyteNoCloudCredentialsError,
            AirbyteWorkspaceMismatchError,
            AirbyteMissingResourceError,
        ) as e:
            return RunRegressionTestsResponse(
                run_id=run_id,
                status=TestRunStatus.FAILED,
                message=str(e),
                workflow_url=None,
            )

    if discover_missing_streams and not selected_streams:
        return RunRegressionTestsResponse(
            run_id=run_id,
            status=TestRunStatus.FAILED,
            message="discover_missing_streams needs selected_streams naming the "
            "streams to add to the catalog.",
            workflow_url=None,
        )

    if injected_sync_mode and not discover_missing_streams:
        return RunRegressionTestsResponse(
            run_id=run_id,
            status=TestRunStatus.FAILED,
            message="injected_sync_mode only applies with discover_missing_streams.",
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
    if discover_missing_streams:
        workflow_inputs["discover_missing_streams"] = "true"
    if injected_sync_mode:
        workflow_inputs["injected_sync_mode"] = injected_sync_mode
    if enable_debug_logs:
        workflow_inputs["enable_debug_logs"] = "true"
    if disable_http_replay:
        workflow_inputs["disable_http_replay"] = "true"
    if with_state is True:
        workflow_inputs["with_state"] = "true"
    elif with_state is False:
        workflow_inputs["with_state"] = "false"
    if max_records is not None:
        workflow_inputs["max_records"] = str(max_records)
    if state_json is not None:
        workflow_inputs["state_json"] = state_json
    if output_mode is not None:
        workflow_inputs["output_mode"] = output_mode
    if read_timeout_minutes is not None:
        workflow_inputs["read_timeout_minutes"] = str(read_timeout_minutes)

    mode_description = "single-version" if skip_compare else "comparison"

    # A refusal from GitHub (a seed past the 65,535-character input limit
    # comes back as a 422) or a network error on the dispatch is an answer,
    # not a traceback, which would carry the seed in its frames. A run lookup
    # that fails after GitHub took the dispatch does not raise: the run is
    # queued, only its ID is unknown.
    try:
        dispatch_result = trigger_workflow_dispatch(
            owner=REGRESSION_TEST_REPO_OWNER,
            repo=REGRESSION_TEST_REPO_NAME,
            workflow_file=REGRESSION_TEST_WORKFLOW_FILE,
            ref=resolve_default_workflow_branch(REGRESSION_TEST_DEFAULT_BRANCH),
            inputs=workflow_inputs,
            token=token,
        )
    except requests.RequestException as exc:
        return RunRegressionTestsResponse(
            run_id=run_id,
            status=TestRunStatus.FAILED,
            message=f"Workflow dispatch failed: {_api_error_message(exc)}",
            workflow_url=None,
        )

    view_url = dispatch_result.run_url or dispatch_result.workflow_url
    connection_info = f" for connection {connection_id}" if connection_id else ""
    repo_info = f" from {repo}" if repo != ConnectorRepo.AIRBYTE else ""
    debug_logs_note = (
        " Debug logs will be off: the run is masked."
        if effective_output_mode == "masked" and enable_debug_logs
        else ""
    )
    skipped_check = (
        f"\nEU data-plane check skipped: {eu_check.skipped}."
        if eu_check and eu_check.skipped
        else ""
    )
    return RunRegressionTestsResponse(
        run_id=run_id,
        status=TestRunStatus.QUEUED,
        message=(
            f"{mode_description.capitalize()} regression test workflow triggered "
            f"for {connector_name} (PR #{pr}{repo_info}){connection_info}. "
            f"View progress at: {view_url}{skipped_check}{debug_logs_note}"
        ),
        workflow_url=dispatch_result.workflow_url,
        github_run_id=dispatch_result.run_id,
        github_run_url=dispatch_result.run_url,
    )


AIRBYTE_REPO_OWNER = "airbytehq"

AIRBYTE_REPO_NAME = "airbyte"

BLOCK_RELEASE_WORKFLOW_FILE = "block-release.yml"

DEFAULT_REF = "master"


class BlockConnectorReleaseResult(BaseModel):
    """Result of triggering a release block workflow."""

    success: bool = Field(description="Whether the workflow dispatch succeeded")
    message: str = Field(description="Human-readable result message")
    workflow_url: str = Field(description="URL to the workflow")
    run_id: int | None = Field(
        default=None, description="Workflow run ID, if discovered"
    )
    run_url: str | None = Field(default=None, description="URL to the workflow run")


class UnblockConnectorReleaseResult(BaseModel):
    """Result of triggering a release unblock workflow."""

    success: bool = Field(description="Whether the workflow dispatch succeeded")
    message: str = Field(description="Human-readable result message")
    workflow_url: str = Field(description="URL to the workflow")
    run_id: int | None = Field(
        default=None, description="Workflow run ID, if discovered"
    )
    run_url: str | None = Field(default=None, description="URL to the workflow run")


class ListBlockedConnectorsResult(BaseModel):
    """Result of listing blocked connectors via the GitHub API."""

    blocked_connectors: list[dict] = Field(
        default_factory=list,
        description="List of blocked connectors with optional block metadata",
    )
    count: int = Field(default=0, description="Number of blocked connectors")


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def block_connector_release(
    connector_name: Annotated[
        str,
        Field(
            description="Connector technical name (e.g., `source-faker`, `destination-postgres`)"
        ),
    ],
    reason: Annotated[
        str,
        Field(description="Human-readable reason for blocking the release"),
    ],
    yanked_version: Annotated[
        str | None,
        Field(description="Version that was yanked (for reference)"),
    ] = None,
    blocked_by: Annotated[
        str | None,
        Field(description="Email or identifier of the person requesting the block"),
    ] = None,
) -> BlockConnectorReleaseResult:
    """Block a connector from being released by creating a `block-release.yaml` marker.

    Triggers the `block-release.yml` workflow in the airbyte monorepo, which
    creates a marker file, opens a PR, and force-merges it to master. While the
    marker exists, the publish pipeline will skip the connector with a warning.

    Use this after yanking a connector version to prevent CI from accidentally
    re-publishing the broken code.
    """
    token = resolve_ci_trigger_github_token()

    inputs: dict[str, str] = {
        "connector-name": connector_name,
        "action": "block",
        "reason": reason,
    }
    if yanked_version:
        inputs["yanked-version"] = yanked_version
    if blocked_by:
        inputs["blocked-by"] = blocked_by

    result = trigger_workflow_dispatch(
        owner=AIRBYTE_REPO_OWNER,
        repo=AIRBYTE_REPO_NAME,
        workflow_file=BLOCK_RELEASE_WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(DEFAULT_REF),
        inputs=inputs,
        token=token,
        find_run=True,
    )

    if result.run_id:
        message = (
            f"Successfully triggered release block for {connector_name}. "
            f"Run ID: {result.run_id}"
        )
    else:
        message = (
            f"Successfully triggered release block for {connector_name}. "
            "Run ID not yet available."
        )

    return BlockConnectorReleaseResult(
        success=True,
        message=message,
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def unblock_connector_release(
    connector_name: Annotated[
        str,
        Field(
            description="Connector technical name (e.g., `source-faker`, `destination-postgres`)"
        ),
    ],
) -> UnblockConnectorReleaseResult:
    """Remove a release block for a connector by deleting its `block-release.yaml` marker.

    Triggers the `block-release.yml` workflow with action=unblock, which removes
    the marker file, opens a PR, and force-merges it to master. After this, the
    connector can be published normally again.
    """
    token = resolve_ci_trigger_github_token()

    result = trigger_workflow_dispatch(
        owner=AIRBYTE_REPO_OWNER,
        repo=AIRBYTE_REPO_NAME,
        workflow_file=BLOCK_RELEASE_WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(DEFAULT_REF),
        inputs={
            "connector-name": connector_name,
            "action": "unblock",
        },
        token=token,
        find_run=True,
    )

    if result.run_id:
        message = (
            f"Successfully triggered release unblock for {connector_name}. "
            f"Run ID: {result.run_id}"
        )
    else:
        message = (
            f"Successfully triggered release unblock for {connector_name}. "
            "Run ID not yet available."
        )

    return UnblockConnectorReleaseResult(
        success=True,
        message=message,
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def list_blocked_connector_releases(
    connector_name: Annotated[
        str | None,
        Field(
            description="Optional connector name to check. If not provided, scans all connectors."
        ),
    ] = None,
    include_details: Annotated[
        bool,
        Field(
            description="Whether to fetch and parse each marker file for reason and metadata."
        ),
    ] = True,
) -> ListBlockedConnectorsResult:
    """List connectors that are currently blocked from release.

    Searches the airbyte monorepo for `block-release.yaml` marker files using
    the GitHub API. Returns a list of blocked connectors, with marker metadata
    when `include_details` is `True`.
    """

    token = resolve_ci_trigger_github_token()
    ref = resolve_default_workflow_branch(DEFAULT_REF)
    blocked: list[dict] = []

    if connector_name:
        blocked = _check_single_connector_block(connector_name, token, ref)
    else:
        blocked = _search_all_blocked_connectors(token, ref, include_details)

    return ListBlockedConnectorsResult(
        blocked_connectors=blocked,
        count=len(blocked),
    )


def _check_single_connector_block(
    connector_name: str,
    token: str,
    ref: str,
) -> list[dict]:
    """Check if a single connector has a release block."""
    path = f"airbyte-integrations/connectors/{connector_name}/block-release.yaml"
    content = get_file_contents_at_ref(
        owner=AIRBYTE_REPO_OWNER,
        repo=AIRBYTE_REPO_NAME,
        path=path,
        ref=ref,
        token=token,
    )
    if content is None:
        return []

    return _parse_block_marker_content(connector_name, content)


def _parse_block_marker_content(connector_name: str, content: str) -> list[dict]:
    """Parse a `block-release.yaml` marker into the MCP response shape."""
    try:
        block_file_data = yaml.safe_load(content)
        if isinstance(block_file_data, dict):
            return [
                {
                    "connector_name": connector_name,
                    "reason": block_file_data.get("reason", "(no reason provided)"),
                    "yanked_version": block_file_data.get("yanked_version"),
                    "blocked_at": block_file_data.get("blocked_at"),
                    "blocked_by": block_file_data.get("blocked_by"),
                }
            ]
    except yaml.YAMLError:
        return [
            {"connector_name": connector_name, "reason": "(unable to parse marker)"}
        ]

    return [
        {
            "connector_name": connector_name,
            "reason": "(invalid block-release.yaml format)",
        }
    ]


def _search_all_blocked_connectors(
    token: str,
    ref: str,
    include_details: bool,
) -> list[dict]:
    """Search the repo for all `block-release.yaml` files at the requested ref."""
    tree_ref = quote(ref, safe="")
    url = (
        f"{GITHUB_API_BASE}/repos/{AIRBYTE_REPO_OWNER}/{AIRBYTE_REPO_NAME}"
        f"/git/trees/{tree_ref}"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(
        url,
        headers=headers,
        params={"recursive": "1"},
        timeout=30,
    )
    response.raise_for_status()

    tree = response.json().get("tree", [])
    blocked: list[dict] = []

    for item in tree:
        file_path = item.get("path", "")
        if not file_path.endswith("/block-release.yaml"):
            continue

        parts = file_path.split("/")
        if (
            len(parts) == 4
            and parts[0] == "airbyte-integrations"
            and parts[1] == "connectors"
        ):
            connector_name = parts[2]
            if not include_details:
                blocked.append({"connector_name": connector_name})
                continue

            content = get_file_contents_at_ref(
                owner=AIRBYTE_REPO_OWNER,
                repo=AIRBYTE_REPO_NAME,
                path=file_path,
                ref=ref,
                token=token,
            )
            if content is not None:
                blocked.extend(_parse_block_marker_content(connector_name, content))

    return blocked


def register_connector_qa_tools(app: FastMCP) -> None:
    """Register connector_qa tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
