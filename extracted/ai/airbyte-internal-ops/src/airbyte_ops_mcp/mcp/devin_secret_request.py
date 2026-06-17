# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for on-demand Devin secret request and discovery.

Tools:

- **list_devin_secrets**: Lists all available secret names in the
  1Password vault, so the agent can discover valid secret aliases.
- **request_devin_secret**: Two-phase approval workflow to request
  and deliver a secret.

## MCP reference

.. include:: ../../../docs/mcp-generated/devin_secret_request.md
    :start-line: 2
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred annotations
# are used. See: https://github.com/jlowin/fastmcp/issues/905

__all__: list[str] = []

import json
import logging
import re
from typing import Annotated

import requests
from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.github_actions import (
    download_job_logs,
    get_workflow_jobs,
    resolve_default_workflow_branch,
    trigger_workflow_dispatch,
    wait_for_workflow_completion,
)
from airbyte_ops_mcp.github_api import resolve_ci_trigger_github_token
from airbyte_ops_mcp.human_in_the_loop import HITL_SLACK_CHANNEL_URL

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WORKFLOW_REPO_OWNER = "airbytehq"
WORKFLOW_REPO_NAME = "airbyte-ops-mcp"
WORKFLOW_FILE = "devin-secret-request.yml"
WORKFLOW_DEFAULT_BRANCH = "main"


_SESSION_ID_PATTERN = re.compile(r"[0-9a-fA-F]{32}")


class SecretListResponse(BaseModel):
    """Response from the list_devin_secrets tool."""

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable status message")
    available_secrets: list[str] = Field(
        default_factory=list,
        description="Sorted list of available secret names in the vault",
    )


class SecretRequestResponse(BaseModel):
    """Response from the request_devin_secret tool."""

    success: bool = Field(description="Whether the operation succeeded")
    phase: str = Field(
        description=(
            "Current phase: 'approval_requested' (Phase 1) or "
            "'delivery_dispatched' (Phase 2)"
        ),
    )
    message: str = Field(description="Human-readable status message")
    slack_channel_url: str = Field(
        default=HITL_SLACK_CHANNEL_URL,
        description="Direct URL to the #human-in-the-loop Slack channel",
    )
    secret_alias: str = Field(description="The requested secret alias")
    session_id: str = Field(description="The Devin session ID")
    workflow_url: str | None = Field(
        default=None,
        description="URL to the GitHub Actions workflow",
    )
    run_id: int | None = Field(
        default=None,
        description="GitHub Actions workflow run ID",
    )
    run_url: str | None = Field(
        default=None,
        description="Direct URL to the GitHub Actions workflow run",
    )
    request_id: str | None = Field(
        default=None,
        description=(
            "Unique request identifier (UUID). Returned in Phase 1; "
            "pass it back in Phase 2 for replay-protection validation."
        ),
    )


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def list_devin_secrets() -> SecretListResponse:
    """List all available secret names in the 1Password vault.

    Returns the sorted list of item titles from the
    'devin-on-demand-secrets' vault. Use this to discover valid
    secret aliases before calling request_devin_secret.

    This dispatches a GitHub Actions workflow (which has the
    1Password credentials), waits for it to complete, then reads
    the list from the job logs.
    """
    return _list_secrets_via_workflow()


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def request_devin_secret(
    secret_alias: Annotated[
        str,
        "The name of the secret to request. This must exactly match an item "
        "title in the 'devin-on-demand-secrets' 1Password vault.",
    ],
    session_url: Annotated[
        str,
        "Your Devin session URL (e.g. 'https://app.devin.ai/sessions/abc123...'). "
        "Use the session URL from your system prompt.",
    ],
    approval_evidence_url: Annotated[
        str | None,
        "Slack approval record URL "
        "(https://<workspace>.slack.com/archives/...). "
        "Leave empty for Phase 1 (requesting approval). Provide the "
        "Slack URL for Phase 2 (delivering the secret after approval).",
    ] = None,
    target_approver: Annotated[
        str | None,
        "Person to notify for approval (GitHub handle, email, or Slack user ID). "
        "Required for Phase 1 (approval request).",
    ] = None,
    request_id: Annotated[
        str | None,
        "Request ID returned by Phase 1. Pass it back in Phase 2 "
        "so the approval record can be validated against the original request. "
        "Leave empty for Phase 1.",
    ] = None,
) -> SecretRequestResponse:
    """Request a secret on demand via an approval workflow.

    This tool operates in two phases:

    **Phase 1** (no approval_evidence_url): Dispatches a GitHub Actions
    workflow that validates the secret name against the 1Password vault
    and, if valid, sends a Slack approval request. If the secret name is
    not found, returns immediately with the list of available secret
    names so you can correct any typos.

    **Phase 2** (with approval_evidence_url): After a human approves the
    request, call this tool again with the approval evidence URL. This
    triggers a GitHub Actions workflow that reads the secret from
    1Password and sends you a time-limited share link.
    Open the link in your browser to view and copy the secret.

    Typical workflow:
    0. (Optional) Call list_devin_secrets first to see available names.
    1. Call this tool without approval_evidence_url to request approval.
    2. Note the `request_id` in the response.
    3. Wait for a human to approve the request in Slack.
    4. Obtain the approval evidence URL (Slack approval record URL).
    5. Call this tool again with the approval_evidence_url **and** the
       request_id from step 2.
    6. You will receive a 1Password share link -- open it in your
       browser to view and copy the secret values.
    """
    # Extract session ID from URL
    match = _SESSION_ID_PATTERN.search(session_url)
    if not match:
        return SecretRequestResponse(
            success=False,
            phase="error",
            message=(
                f"No valid session ID found in URL: {session_url}. "
                "Expected a 32-character hex string."
            ),
            secret_alias=secret_alias,
            session_id="",
        )
    session_id = match.group(0)

    if not approval_evidence_url:
        # Phase 1: Dispatch the request workflow (validates secret name
        # inline using op CLI, then sends Slack approval if valid).
        if not target_approver:
            return SecretRequestResponse(
                success=False,
                phase="error",
                message=(
                    "target_approver is required when requesting approval "
                    "(no approval_evidence_url provided)."
                ),
                secret_alias=secret_alias,
                session_id=session_id,
            )

        return _request_secret_via_workflow(
            secret_alias=secret_alias,
            session_id=session_id,
            session_url=session_url,
            target_approver=target_approver,
        )

    # Phase 2: Deliver secret via GitHub Actions workflow
    token = resolve_ci_trigger_github_token()

    workflow_inputs: dict[str, str] = {
        "action": "deliver",
        "secret_alias": secret_alias,
        "session_id": session_id,
        "approval_evidence_url": approval_evidence_url,
    }
    if request_id:
        workflow_inputs["expected_request_id"] = request_id

    result = trigger_workflow_dispatch(
        owner=WORKFLOW_REPO_OWNER,
        repo=WORKFLOW_REPO_NAME,
        workflow_file=WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(WORKFLOW_DEFAULT_BRANCH),
        inputs=workflow_inputs,
        token=token,
    )

    view_url = result.run_url or result.workflow_url
    return SecretRequestResponse(
        success=True,
        phase="delivery_dispatched",
        message=(
            f"Secret delivery workflow dispatched for '{secret_alias}'. "
            f"The workflow will read the secret from 1Password and send "
            f"you a time-limited share link. Once you receive the link, "
            f"open it in your browser to view and copy the secret. "
            f"View progress: {view_url}"
        ),
        secret_alias=secret_alias,
        session_id=session_id,
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
        request_id=request_id,
    )


def _request_secret_via_workflow(
    secret_alias: str,
    session_id: str,
    session_url: str,
    target_approver: str,
) -> SecretRequestResponse:
    """Dispatch the request workflow, wait, and parse the result from job logs.

    The workflow validates the secret alias against the vault inline,
    then sends the Slack approval if valid.  On a bad alias the workflow
    fails and the job logs contain a JSON object with `available_secrets`.
    """
    token = resolve_ci_trigger_github_token()

    dispatch_result = trigger_workflow_dispatch(
        owner=WORKFLOW_REPO_OWNER,
        repo=WORKFLOW_REPO_NAME,
        workflow_file=WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(WORKFLOW_DEFAULT_BRANCH),
        inputs={
            "action": "request",
            "secret_alias": secret_alias,
            "session_id": session_id,
            "target_approver": target_approver,
        },
        token=token,
    )
    if not dispatch_result.run_id:
        return SecretRequestResponse(
            success=False,
            phase="error",
            message=(
                "Workflow dispatched but no run ID returned. "
                f"Check: {dispatch_result.workflow_url}"
            ),
            secret_alias=secret_alias,
            session_id=session_id,
            workflow_url=dispatch_result.workflow_url,
        )

    run_status = wait_for_workflow_completion(
        owner=WORKFLOW_REPO_OWNER,
        repo=WORKFLOW_REPO_NAME,
        run_id=dispatch_result.run_id,
        token=token,
    )

    # Download logs from the validation job (multi-job workflow)
    raw_logs = _download_run_logs(
        dispatch_result.run_id, token, job_name="Validate Secret Name"
    )

    if run_status.succeeded:
        # Parse the approval-requested JSON from the logs
        result_data = _find_json_in_logs(raw_logs, "phase") if raw_logs else None
        request_id = result_data.get("request_id") if result_data else None
        view_url = run_status.run_url or dispatch_result.workflow_url
        return SecretRequestResponse(
            success=True,
            phase="approval_requested",
            message=(
                f"Approval request for secret '{secret_alias}' sent to "
                f"#human-in-the-loop ({HITL_SLACK_CHANNEL_URL}). "
                f"Waiting for human approval. "
                f"Once approved, call this tool again with the "
                f"approval_evidence_url to deliver the secret. "
                f"View progress: {view_url}"
            ),
            secret_alias=secret_alias,
            session_id=session_id,
            workflow_url=dispatch_result.workflow_url,
            run_id=dispatch_result.run_id,
            run_url=run_status.run_url,
            request_id=request_id,
        )

    # Workflow failed — check if it was a validation failure
    error_data = _find_json_in_logs(raw_logs, "available_secrets") if raw_logs else None
    if error_data:
        available = error_data.get("available_secrets", [])
        formatted = ", ".join(f"`{s}`" for s in available)
        return SecretRequestResponse(
            success=False,
            phase="validation_failed",
            message=(
                f"Secret '{secret_alias}' not found in the vault. "
                f"Available secrets: {formatted}"
            ),
            secret_alias=secret_alias,
            session_id=session_id,
            workflow_url=dispatch_result.workflow_url,
            run_id=dispatch_result.run_id,
            run_url=run_status.run_url,
        )

    # Generic workflow failure
    return SecretRequestResponse(
        success=False,
        phase="error",
        message=(
            f"Request workflow failed (conclusion={run_status.conclusion}). "
            f"See: {run_status.run_url}"
        ),
        secret_alias=secret_alias,
        session_id=session_id,
        workflow_url=dispatch_result.workflow_url,
        run_id=dispatch_result.run_id,
        run_url=run_status.run_url,
    )


def _download_run_logs(
    run_id: int,
    token: str,
    *,
    job_name: str | None = None,
) -> str | None:
    """Best-effort download of a job's logs for a workflow run.

    Args:
        run_id: GitHub Actions workflow run ID.
        token: GitHub API token used for log download. Note: job listing
            uses `get_workflow_jobs` which resolves its own token via
            `resolve_ci_trigger_github_token()`.
        job_name: If provided, find the job whose name contains this
            substring (case-insensitive). Skipped jobs are always
            excluded. Falls back to the first non-skipped job.
    """
    try:
        jobs = get_workflow_jobs(
            owner=WORKFLOW_REPO_OWNER,
            repo=WORKFLOW_REPO_NAME,
            run_id=run_id,
        )
        # Filter out skipped jobs (common in multi-job conditional workflows)
        active_jobs = [j for j in jobs if j.conclusion != "skipped"]
        if not active_jobs:
            return None

        target = active_jobs[0]  # default: first non-skipped job
        if job_name:
            needle = job_name.lower()
            for j in active_jobs:
                if needle in j.name.lower():
                    target = j
                    break

        return download_job_logs(
            owner=WORKFLOW_REPO_OWNER,
            repo=WORKFLOW_REPO_NAME,
            job_id=target.job_id,
            token=token,
        )
    except (requests.HTTPError, ValueError) as exc:
        logger.warning("Failed to download job logs for run %s: %s", run_id, exc)
        return None


def _list_secrets_via_workflow() -> SecretListResponse:
    """Dispatch the list workflow, wait for completion, and parse titles from job logs."""
    token = resolve_ci_trigger_github_token()

    # 1. Dispatch the workflow with action="list"
    dispatch_result = trigger_workflow_dispatch(
        owner=WORKFLOW_REPO_OWNER,
        repo=WORKFLOW_REPO_NAME,
        workflow_file=WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(WORKFLOW_DEFAULT_BRANCH),
        inputs={"action": "list", "session_id": "0" * 32},
        token=token,
    )
    if not dispatch_result.run_id:
        return SecretListResponse(
            success=False,
            message=(
                "Workflow dispatched but no run ID returned. "
                f"Check: {dispatch_result.workflow_url}"
            ),
        )

    # 2. Wait for the workflow to complete
    run_status = wait_for_workflow_completion(
        owner=WORKFLOW_REPO_OWNER,
        repo=WORKFLOW_REPO_NAME,
        run_id=dispatch_result.run_id,
        token=token,
    )
    if not run_status.succeeded:
        return SecretListResponse(
            success=False,
            message=(
                f"Workflow run failed (conclusion={run_status.conclusion}). "
                f"See: {run_status.run_url}"
            ),
        )

    # 3. Find the job and download its logs
    jobs = get_workflow_jobs(
        owner=WORKFLOW_REPO_OWNER,
        repo=WORKFLOW_REPO_NAME,
        run_id=dispatch_result.run_id,
    )
    if not jobs:
        return SecretListResponse(
            success=False,
            message="Workflow completed but no jobs found.",
        )

    # Find the list job (multi-job workflow; skip skipped jobs)
    active_jobs = [j for j in jobs if j.conclusion != "skipped"]
    if not active_jobs:
        return SecretListResponse(
            success=False,
            message="Workflow completed but all jobs were skipped.",
        )

    target_job = active_jobs[0]
    for j in active_jobs:
        if "list" in j.name.lower():
            target_job = j
            break

    raw_logs = download_job_logs(
        owner=WORKFLOW_REPO_OWNER,
        repo=WORKFLOW_REPO_NAME,
        job_id=target_job.job_id,
        token=token,
    )

    # 4. Parse JSON output from the logs
    data = _find_json_in_logs(raw_logs, "available_secrets")
    if data is None:
        return SecretListResponse(
            success=False,
            message=(
                "Could not parse secret list from workflow logs. "
                f"See: {run_status.run_url}"
            ),
        )

    secrets = data.get("available_secrets", [])
    titles = [str(t) for t in secrets] if isinstance(secrets, list) else []
    return SecretListResponse(
        success=True,
        message=f"Found {len(titles)} available secrets in the vault.",
        available_secrets=sorted(titles),
    )


def _find_json_in_logs(raw_logs: str, required_key: str) -> dict | None:
    """Find the first JSON object in job logs that contains *required_key*.

    GitHub Actions job logs prefix each line with a timestamp.  We scan
    every line looking for a JSON object that contains the given key.
    Returns the parsed dict, or `None` if not found.
    """
    for line in raw_logs.splitlines():
        stripped = line.strip()
        if not stripped.startswith("{"):
            idx = stripped.find("{")
            if idx < 0:
                continue
            stripped = stripped[idx:]
        try:
            data = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and required_key in data:
            return data
    return None


def register_devin_secret_request_tools(app: FastMCP) -> None:
    """Register Devin secret request tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
