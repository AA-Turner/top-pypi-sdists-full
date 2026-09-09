# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for Devin agent-session operations: reminders, on-demand secret requests, session feedback, and session naming.

## MCP reference

.. include:: ../../../docs/mcp-generated/devin_ops.md
    :start-line: 2
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred annotations
# are used. See: https://github.com/jlowin/fastmcp/issues/905
# Python 3.12+ supports modern type hint syntax natively, so this is not needed.

__all__: list[str] = []

import json
import logging
import re
import zipfile
from enum import StrEnum
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.devin_reminders import dispatch_cancel_reminder, dispatch_reminder
from airbyte_ops_mcp.github_actions import (
    WorkflowDispatchResult,
    download_job_logs,
    get_workflow_jobs,
    resolve_default_workflow_branch,
    trigger_workflow_dispatch,
    wait_for_workflow_completion,
)
from airbyte_ops_mcp.github_api import resolve_ci_trigger_github_token
from airbyte_ops_mcp.human_in_the_loop import (
    HITL_SLACK_CHANNEL_URL,
    dispatch_escalation,
)
from airbyte_ops_mcp.session_namer import (
    extract_session_id,
    generate_friendly_name,
)
from airbyte_ops_mcp.slack_api import SlackAPIError, SlackURLParseError
from airbyte_ops_mcp.slack_posting import (
    SlackPostResult,
    parse_slack_thread_url,
    post_channel_message,
    post_thread_reply,
    send_hitl_notification,
)


class SetDevinReminderResponse(BaseModel):
    """Response from the set_devin_reminder tool."""

    success: bool = Field(description="Whether the workflow was triggered successfully")
    message: str = Field(description="Human-readable status message")
    workflow_url: str | None = Field(
        default=None,
        description="URL to view the GitHub Actions workflow file",
    )
    run_id: int | None = Field(
        default=None,
        description="GitHub Actions workflow run ID",
    )
    run_url: str | None = Field(
        default=None,
        description="Direct URL to the GitHub Actions workflow run",
    )


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def set_devin_reminder(
    reminder_message: Annotated[
        str,
        "The reminder message to deliver. Should clearly describe what "
        "you need to be reminded about.",
    ],
    agent_session_url: Annotated[
        str,
        "Your Devin session URL so the reminder can be injected back into "
        "your session. Use the session URL from your system prompt.",
    ],
    delay_minutes: Annotated[
        int | None,
        "Number of minutes until the reminder fires. Must be a positive "
        "multiple of 30, up to 10080 (7 days). Examples: 30, 60, 120, 1440. "
        "Mutually exclusive with remind_at_local_time.",
    ] = None,
    remind_at_local_time: Annotated[
        str | None,
        "Date-time in local time when the reminder should fire. "
        "At Airbyte, local time is always Pacific (America/Los_Angeles). "
        "Accepts '2026-04-02 09:00' (24-hour), "
        "'2026-04-02 9:00 AM' (12-hour), or ISO-like 'YYYY-MM-DDTHH:MM'. "
        "Must be in the future and within 7 days. "
        "Mutually exclusive with delay_minutes. "
        "PREFERRED — use this instead of delay_minutes to avoid "
        "timezone-conversion errors.",
    ] = None,
    slack_users_cc: Annotated[
        str | None,
        "Optional comma-delimited list of Slack user tags to CC on the "
        "reminder notification. Example: '<@U12345>, <@U67890>'.",
    ] = None,
) -> SetDevinReminderResponse:
    """Schedule a reminder that fires at a specified time or after a delay.

    Creates a reminder that will be delivered back to your Devin session
    and posted to the #devin-reminders Slack channel when the time arrives.
    Reminders are checked every 30 minutes via a cron schedule.

    Exactly one of `delay_minutes` or `remind_at_local_time` must be provided.
    Prefer `remind_at_local_time` (Pacific local time) over `delay_minutes`
    to avoid timezone-conversion mistakes — unless the user explicitly
    asks for a reminder in N minutes.

    The reminder is stored as a GitHub Actions artifact and processed by
    the devin-reminders-action. When the reminder is due, it injects a
    message into the originating Devin session and sends a Slack notification.

    Use this tool when you need to schedule a follow-up action, check on
    a long-running process, or remind yourself about a task.
    """
    try:
        result = dispatch_reminder(
            delay_minutes=delay_minutes,
            remind_at_local_time=remind_at_local_time,
            reminder_message=reminder_message,
            agent_session_url=agent_session_url,
            slack_users_cc=slack_users_cc,
        )
    except ValueError as e:
        return SetDevinReminderResponse(
            success=False,
            message=f"Invalid input: {e}",
        )

    if remind_at_local_time:
        time_desc = f"at {remind_at_local_time} Pacific"
    else:
        time_desc = f"in {delay_minutes} minutes"

    view_url = result.run_url or result.workflow_url
    return SetDevinReminderResponse(
        success=True,
        message=(
            f"Reminder scheduled to fire {time_desc}. "
            f"View progress at: {view_url}\n\n"
            f"To cancel pending reminders for this session, use the "
            f"`cancel_devin_reminder` tool."
        ),
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


class CancelDevinReminderResponse(BaseModel):
    """Response from the cancel_devin_reminder tool."""

    success: bool = Field(
        description="Whether the cancel workflow was triggered successfully"
    )
    message: str = Field(description="Human-readable status message")
    workflow_url: str | None = Field(
        default=None,
        description="URL to view the GitHub Actions workflow file",
    )
    run_id: int | None = Field(
        default=None,
        description="GitHub Actions workflow run ID",
    )
    run_url: str | None = Field(
        default=None,
        description="Direct URL to the GitHub Actions workflow run",
    )


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def cancel_devin_reminder(
    agent_session_url: Annotated[
        str,
        "Your Devin session URL. Use the session URL from your system prompt. "
        "Required together with cancel_guids.",
    ],
    cancel_guids: Annotated[
        list[str],
        "List of reminder GUIDs to cancel. You can get GUIDs from "
        "the reminder creation response or from the reminders list.",
    ],
) -> CancelDevinReminderResponse:
    """Cancel pending Devin reminders by session URL and specific GUIDs.

    Removes matching reminders so they will not fire. Use this when instructed
    to stop reminders, or when a reminder is no longer needed.

    Both agent_session_url and cancel_guids are required. Only reminders
    matching the session URL AND present in the GUID list are cancelled.
    """
    try:
        result = dispatch_cancel_reminder(
            agent_session_url=agent_session_url,
            cancel_guids=cancel_guids,
        )
    except ValueError as e:
        return CancelDevinReminderResponse(
            success=False,
            message=f"Invalid input: {e}",
        )

    view_url = result.run_url or result.workflow_url
    guid_list = ", ".join(cancel_guids)
    return CancelDevinReminderResponse(
        success=True,
        message=(
            f"Cancel workflow triggered for GUIDs [{guid_list}] "
            f"in session {agent_session_url}. View progress at: {view_url}"
        ),
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


logger = logging.getLogger(__name__)

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


_FEEDBACK_CHANNEL = "C0ACUHRP6B1"

_FEEDBACK_CC_USERGROUPS = [
    "S0BJ4K3LC4X",  # @oc-hydra
    "S0BKR63VAN5",  # @oc-internal-ai
]

_TRIAGE_REPO_OWNER = "airbytehq"

_TRIAGE_REPO_NAME = "airbyte-ops-mcp"

_TRIAGE_WORKFLOW_FILE = "devin-session-triage.yml"

_TRIAGE_DEFAULT_BRANCH = "main"

_AI_SKILLS_REPO_URL = "https://github.com/airbytehq/ai-skills"

_INTERNAL_SKILLS_URL = (
    "https://internal.airbyte.ai/docs/internal-docs/ai-engineering/skills"
)

_PLAYBOOK_ID_PATTERN = re.compile(r"^[a-z0-9_-]+$")

_SKILL_ID_PATTERN = re.compile(r"^[a-z0-9-]+$")

_CATEGORY_DISPLAY: dict[str, str] = {
    "tool_failure": "Tool Failure",
    "missing_guidance": "Missing Guidance",
    "suspected_hallucination": "Suspected Hallucination",
    "bad_approach": "Bad Approach",
    "excessive_iteration": "Excessive Iteration",
    "poor_quality": "Poor Quality",
    "other_concern": "Other Concern",
    "great_results": "Great Results",
    "exceeded_expectations": "Exceeded Expectations",
    "fast_completion": "Fast Completion",
    "good_communication": "Good Communication",
    "other_positive_feedback": "Other Positive Feedback",
}


class FeedbackCategory(StrEnum):
    """Feedback categories for Devin session reports."""

    # Negative categories
    TOOL_FAILURE = "tool_failure"
    MISSING_GUIDANCE = "missing_guidance"
    SUSPECTED_HALLUCINATION = "suspected_hallucination"
    BAD_APPROACH = "bad_approach"
    EXCESSIVE_ITERATION = "excessive_iteration"
    POOR_QUALITY = "poor_quality"
    OTHER_CONCERN = "other_concern"

    # Positive categories
    GREAT_RESULTS = "great_results"
    EXCEEDED_EXPECTATIONS = "exceeded_expectations"
    FAST_COMPLETION = "fast_completion"
    GOOD_COMMUNICATION = "good_communication"
    OTHER_POSITIVE_FEEDBACK = "other_positive_feedback"

    def is_negative(self) -> bool:
        """Return True if this is a negative feedback category."""
        return self in _NEGATIVE_MEMBERS

    def display_name(self) -> str:
        """Return the human-readable display name for this category."""
        return _CATEGORY_DISPLAY.get(self.value, self.value)


_NEGATIVE_MEMBERS = frozenset(
    {
        FeedbackCategory.TOOL_FAILURE,
        FeedbackCategory.MISSING_GUIDANCE,
        FeedbackCategory.SUSPECTED_HALLUCINATION,
        FeedbackCategory.BAD_APPROACH,
        FeedbackCategory.EXCESSIVE_ITERATION,
        FeedbackCategory.POOR_QUALITY,
        FeedbackCategory.OTHER_CONCERN,
    }
)

_SEVERITY_DISPLAY: dict[str, str] = {
    "low": "Low",
    "medium": "Medium",
    "high": "High",
    "critical": "Critical",
}


def _feedback_emoji(feedback_type: str) -> str:
    """Return the header emoji for the given feedback type."""
    return ":tada:" if feedback_type == "positive" else ":warning:"


def _feedback_label(feedback_type: str) -> str:
    """Return the header label for the given feedback type."""
    type_display = "Positive" if feedback_type == "positive" else "Negative"
    return f"Devin Session Feedback ({type_display})"


def _format_playbook_link(playbook_id: str) -> str:
    """Return Slack mrkdwn for a playbook identifier."""
    if playbook_id == "none":
        return "none"
    return f"<{_AI_SKILLS_REPO_URL}/blob/main/devin/playbooks/{playbook_id}.md|{playbook_id}>"


def _format_skill_link(skill_id: str) -> str:
    """Return Slack mrkdwn for a skill identifier."""
    return f"<{_INTERNAL_SKILLS_URL}/#{skill_id}|{skill_id}>"


def _validate_playbook_id(playbook_id: str) -> str | None:
    """Return an error message if `playbook_id` is not a valid playbook identifier."""
    if playbook_id == "none" or _PLAYBOOK_ID_PATTERN.fullmatch(playbook_id):
        return None
    return "session_playbook must be 'none' or a lowercase playbook ID using only letters, numbers, '-' and '_'."


def _validate_skill_id(skill_id: str | None) -> str | None:
    """Return an error message if `skill_id` is not a valid skill identifier."""
    if skill_id is None or _SKILL_ID_PATTERN.fullmatch(skill_id):
        return None
    return "related_skill_name must be a lowercase skill ID using only letters, numbers, and '-'."


def _build_feedback_body(
    *,
    feedback_type: str,
    category: str,
    task_description: str,
    session_playbook: str,
    related_skill_name: str | None,
    expected_behavior: str | None,
    observed_behavior: str | None,
    what_went_well: str | None,
    severity: str | None,
    steps_to_reproduce: str | None,
    session_to_evaluate: str | None = None,
) -> str:
    """Build a Slack mrkdwn message body from structured feedback fields."""
    lines: list[str] = []

    cat = FeedbackCategory(category)
    lines.append(f"*Category:* {cat.display_name()}")

    if severity:
        sev_display = _SEVERITY_DISPLAY.get(severity, severity)
        lines.append(f"*Severity:* {sev_display}")

    lines.append("")
    lines.append(f"*Task:* {task_description}")
    lines.append(f"*Session Playbook:* {_format_playbook_link(session_playbook)}")
    if related_skill_name:
        lines.append(f"*Related Skill:* {_format_skill_link(related_skill_name)}")
    if not session_to_evaluate:
        lines.extend(
            [
                "",
                "*Session link missing:* Please provide the Devin session URL so "
                "the team can inspect it.",
            ]
        )

    if feedback_type == "negative":
        if expected_behavior:
            lines.append("")
            lines.append(f"*Expected Behavior:* {expected_behavior}")
        if observed_behavior:
            lines.append("")
            lines.append(f"*Observed Behavior:* {observed_behavior}")
        if steps_to_reproduce:
            lines.append("")
            lines.append(f"*Steps to Reproduce:* {steps_to_reproduce}")
    else:
        if what_went_well:
            lines.append("")
            lines.append(f"*What Went Well:* {what_went_well}")

    if feedback_type == "negative":
        lines.append("")
        lines.append(
            "_Auto-triage: a Devin session with v3 analyze mode will inspect the "
            "linked session when one is provided._"
        )

    return "\n".join(lines)


def _validate_negative_fields(
    expected_behavior: str | None,
    observed_behavior: str | None,
) -> str | None:
    """Return an error message if required negative feedback fields are missing."""
    missing: list[str] = []
    if not expected_behavior:
        missing.append("expected_behavior")
    if not observed_behavior:
        missing.append("observed_behavior")
    if missing:
        return f"Negative feedback requires: {', '.join(missing)}."
    return None


def _validate_positive_fields(
    what_went_well: str | None,
) -> str | None:
    """Return an error message if required positive feedback fields are missing."""
    if not what_went_well:
        return "Positive feedback requires: what_went_well."
    return None


def _dispatch_triage_workflow(
    session_url: str,
    feedback_context: str,
    reporting_user: str,
    session_playbook: str,
    related_skill_name: str | None = None,
    cc_persons: str = "",
    header_emoji: str = "",
    header_label: str = "",
    linear_issue_url: str = "",
    linear_issue_id: str = "",
    thread_url: str = "",
) -> WorkflowDispatchResult | None:
    """Dispatch the v3 session triage workflow.

    The triage workflow launches a Devin session with v3 analyze mode and
    posts a single Slack notification via the HITL reusable workflow.
    Formatting params (emoji, header, cc) are passed through to the HITL
    notification so the caller doesn't need to post separately.

    Returns the dispatch result, or None if dispatch fails.
    """
    token = resolve_ci_trigger_github_token()
    inputs: dict[str, str] = {
        "session_url": session_url,
        "feedback_context": feedback_context,
        "reporting_user": reporting_user,
        "session_playbook": session_playbook,
    }
    if related_skill_name:
        inputs["related_skill_name"] = related_skill_name
    if cc_persons:
        inputs["cc_persons"] = cc_persons
    if header_emoji:
        inputs["header_emoji"] = header_emoji
    if header_label:
        inputs["header_label"] = header_label
    if linear_issue_url:
        inputs["linear_issue_url"] = linear_issue_url
    if linear_issue_id:
        inputs["linear_issue_id"] = linear_issue_id
    if thread_url:
        inputs["thread_url"] = thread_url
    try:
        return trigger_workflow_dispatch(
            owner=_TRIAGE_REPO_OWNER,
            repo=_TRIAGE_REPO_NAME,
            workflow_file=_TRIAGE_WORKFLOW_FILE,
            ref=resolve_default_workflow_branch(_TRIAGE_DEFAULT_BRANCH),
            inputs=inputs,
            token=token,
        )
    except requests.HTTPError:
        logger.exception("Failed to dispatch triage workflow")
        return None


_LINEAR_ISSUE_KEY_PATTERN = re.compile(r"/issue/([A-Z][A-Z0-9]*-\d+)")


def _linear_issue_key(issue_url: str | None, issue_id: str | None) -> str | None:
    """Human-readable issue key such as `HYD-137`, taken from the issue URL.

    The issue identifier is recovered from the URL when possible and otherwise
    uses the supplied identifier.
    """
    if issue_url:
        match = _LINEAR_ISSUE_KEY_PATTERN.search(issue_url)
        if match:
            return match.group(1)
    return issue_id or None


def _post_feedback_report(
    message: str,
    thread_url: str | None = None,
    *,
    target_person: str | None = None,
    agent_session_url: str | None = None,
    cc_persons: list[str] | None = None,
    issue_url: str | None = None,
    header_emoji: str = "\U0001f64b",
    header_label: str = "Human-in-the-loop request",
) -> str:
    """Post feedback to the channel or an existing Slack thread."""
    thread_ts: str | None = None
    if thread_url:
        channel_id, thread_ts = parse_slack_thread_url(thread_url)
    else:
        channel_id = _FEEDBACK_CHANNEL

    def post_plain() -> SlackPostResult:
        if thread_ts:
            return post_thread_reply(
                channel_id=channel_id,
                thread_ts=thread_ts,
                message=message,
            )
        return post_channel_message(channel_id, message)

    if target_person is None:
        return post_plain().permalink

    try:
        result = send_hitl_notification(
            target_person=target_person,
            message=message,
            agent_session_url=agent_session_url or "",
            cc_persons=cc_persons,
            issue_url=issue_url,
            channel_override=channel_id,
            header_emoji=header_emoji,
            header_label=header_label,
            thread_ts=thread_ts,
        )
    except (
        SlackAPIError,
        RuntimeError,
        requests.RequestException,
        zipfile.BadZipFile,
    ) as exc:
        logger.warning(
            "Rich feedback notification failed; falling back to plain-text posting: %s",
            exc,
        )
        result = post_plain()
    return result.permalink


class SessionFeedbackResponse(BaseModel):
    """Response from the session feedback tool."""

    success: bool = Field(description="Whether the workflow was triggered successfully")
    message: str = Field(description="Human-readable status message")
    workflow_url: str | None = Field(
        default=None,
        description="URL to view the GitHub Actions workflow file",
    )
    run_id: int | None = Field(
        default=None,
        description="GitHub Actions workflow run ID",
    )
    run_url: str | None = Field(
        default=None,
        description="Direct URL to the GitHub Actions workflow run",
    )
    triage_run_url: str | None = Field(
        default=None,
        description="URL to the auto-triage workflow run",
    )
    linear_issue_url: str | None = Field(
        default=None,
        description="URL of the Linear issue tracking this feedback",
    )
    linear_issue_identifier: str | None = Field(
        default=None,
        description=(
            "Human-readable Linear issue key, e.g. `HYD-123`, recovered from "
            "`linear_issue_url`. Falls back to `linear_issue_id` when the URL "
            "carries no key."
        ),
    )


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def devin_session_feedback(
    feedback_type: Annotated[
        Literal["positive", "negative"],
        Field(
            description=(
                "Type of feedback: 'positive' for a good experience or 'negative' for a "
                "bad experience. Use 'positive' when the user expresses satisfaction, "
                "praise, or a success story. Use 'negative' when the user reports a problem, "
                "frustration, or failure."
            ),
        ),
    ],
    category: Annotated[
        FeedbackCategory,
        Field(
            description=(
                "Feedback category. "
                "For NEGATIVE feedback, use one of: "
                "'tool_failure' (a specific tool/integration broke), "
                "'missing_guidance' (Devin lacked instructions or context), "
                "'suspected_hallucination' (Devin fabricated information or made incorrect claims), "
                "'bad_approach' (Devin took a fundamentally wrong strategy), "
                "'excessive_iteration' (too many loops/retries before success), "
                "'poor_quality' (output quality below expectations), "
                "'other_concern'. "
                "For POSITIVE feedback, use one of: "
                "'great_results' (task completed with high quality), "
                "'exceeded_expectations' (went above and beyond), "
                "'fast_completion' (completed quickly and efficiently), "
                "'good_communication' (kept user well-informed), "
                "'other_positive_feedback'."
            ),
        ),
    ],
    task_description: Annotated[
        str,
        Field(
            description=(
                "Brief description of what the user asked Devin to do. "
                "This sets the context for the feedback."
            ),
        ),
    ],
    reporting_user: Annotated[
        str,
        Field(
            description=(
                "The person providing the feedback. Accepts an email address "
                "(e.g. 'aj@airbyte.io'), a GitHub handle prefixed with @ "
                "(e.g. '@aaronsteers'), or a Slack user ID (e.g. 'U05AKF1BCC9')."
            ),
        ),
    ],
    session_playbook: Annotated[
        str,
        Field(
            description=(
                "ID of the Devin playbook associated with the session (e.g. "
                "'devin_feedback_triage'), or 'none' when no playbook is associated. "
                "Required so feedback can identify whether playbook instructions may need updates."
            ),
        ),
    ],
    agent_session_url: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional URL of the reporting Devin session. Use the session URL "
                "from your system prompt when reporting your own session."
            ),
        ),
    ] = None,
    related_skill_name: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional skill ID associated with the feedback (e.g. "
                "'delete-declarative-source-def') when a related skill may need updates "
                "or is suspected of having issues."
            ),
        ),
    ] = None,
    expected_behavior: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "What should have happened. REQUIRED for negative feedback. "
                "Describe the expected outcome clearly."
            ),
        ),
    ] = None,
    observed_behavior: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "What actually happened. REQUIRED for negative feedback. "
                "Describe the actual outcome, including any error messages or unexpected results."
            ),
        ),
    ] = None,
    what_went_well: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "What specifically was good about the experience. REQUIRED for positive feedback. "
                "Be specific about what Devin did well."
            ),
        ),
    ] = None,
    severity: Annotated[
        Literal["low", "medium", "high", "critical"] | None,
        Field(
            default=None,
            description=(
                "Severity of the issue. Recommended for negative feedback. "
                "'low' = minor inconvenience, 'medium' = notable impact, "
                "'high' = significant blocker, 'critical' = complete failure."
            ),
        ),
    ] = None,
    steps_to_reproduce: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional steps to reproduce the issue. Helpful for negative feedback "
                "to enable the team to investigate."
            ),
        ),
    ] = None,
    session_to_evaluate: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional Devin session URL to evaluate/triage. Use this when reporting "
                "feedback about a *different* session (not your own). If omitted, "
                "agent_session_url is used as the session to triage (i.e., the reporter "
                "is reporting on itself)."
            ),
        ),
    ] = None,
    linear_issue_id: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional Linear issue identifier for the issue already tracking "
                "this feedback, used by the triage session for mutations. Pass "
                "the identifier, such as `HYD-123`; a UUID is also accepted if "
                "available."
            ),
        ),
    ] = None,
    linear_issue_url: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional URL of the Linear issue already tracking this feedback. "
                "When provided, Slack links to this exact URL."
            ),
        ),
    ] = None,
    post_only: Annotated[
        bool,
        Field(
            description=(
                "Post the report without dispatching triage. Set this explicitly "
                "for a repeat report; do not infer it from a ticket ID."
            ),
        ),
    ] = False,
    thread_url: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional Slack thread URL for a report filed on someone else's "
                "behalf. The report and triage findings are posted in this thread."
            ),
        ),
    ] = None,
) -> SessionFeedbackResponse:
    """Report structured feedback about a Devin session experience via Slack.

    Posts a formatted feedback message to the #hydra-feedback Slack channel,
    tagging the reporting user and the @oc-hydra and @oc-internal-ai groups.
    The message includes a clickable
    button for the Devin session link. For negative feedback, a triage workflow
    is automatically dispatched to launch a Devin session with v3 analyze mode
    that can inspect the original session's full conversation history.

    For negative feedback, the caller supplies any existing Linear tracking
    issue ID and URL. This tool transports those values to Slack and the
    triage workflow; it does not read or write Linear.

    IMPORTANT: This feedback will be logged publicly in Slack. Inform the user
    that their feedback is visible to the team and they may be contacted for
    additional details.

    Use this tool when a user explicitly asks to report a positive or negative
    experience with their Devin session. Before calling this tool, let the user
    know:
    - Their feedback will be posted publicly in the #hydra-feedback Slack channel
    - They may be contacted by the team for more details
    - The reporting user and the @oc-hydra and @oc-internal-ai groups will be tagged in the message
    - For negative feedback, a triage session will be automatically launched to inspect the reported session

    Depending on the path, the Slack message is posted by this tool or a GitHub
    Actions workflow; Slack credentials are never exposed to the calling agent.
    """
    # Validate category matches feedback type.
    cat = FeedbackCategory(category)
    is_negative_feedback = feedback_type == "negative"
    id_validation_error = _validate_playbook_id(session_playbook) or _validate_skill_id(
        related_skill_name
    )
    if id_validation_error:
        return SessionFeedbackResponse(
            success=False,
            message=id_validation_error,
        )

    if cat.is_negative() != is_negative_feedback:
        expected_kind = "negative" if is_negative_feedback else "positive"
        valid = [
            c.value for c in FeedbackCategory if c.is_negative() == is_negative_feedback
        ]
        return SessionFeedbackResponse(
            success=False,
            message=(
                f"Invalid category '{category}' for {feedback_type} feedback. "
                f"Valid {expected_kind} categories: {', '.join(valid)}."
            ),
        )

    # Validate required fields based on feedback type.
    if feedback_type == "negative":
        validation_error = _validate_negative_fields(
            expected_behavior=expected_behavior,
            observed_behavior=observed_behavior,
        )
    else:
        validation_error = _validate_positive_fields(
            what_went_well=what_went_well,
        )

    if validation_error:
        return SessionFeedbackResponse(
            success=False,
            message=validation_error,
        )

    on_behalf = bool(thread_url) or not agent_session_url
    session_under_investigation = session_to_evaluate or (
        "" if on_behalf else (agent_session_url or "")
    )
    message_body = _build_feedback_body(
        feedback_type=feedback_type,
        category=category,
        task_description=task_description,
        session_playbook=session_playbook,
        related_skill_name=related_skill_name,
        expected_behavior=expected_behavior,
        observed_behavior=observed_behavior,
        what_went_well=what_went_well,
        severity=severity,
        steps_to_reproduce=steps_to_reproduce,
        session_to_evaluate=session_under_investigation or None,
    )

    issue_key = _linear_issue_key(linear_issue_url, linear_issue_id)
    tracking_response_note = ""

    if is_negative_feedback:
        issue_note = (
            (
                f"\n\nTracking issue: <{linear_issue_url}|{issue_key}>"
                if linear_issue_url
                else f"\n\nTracking issue: {issue_key}"
            )
            if issue_key
            else (
                "\n\n⚠️ No Linear ticket recorded for this report. "
                "This report is not on the Linear list."
            )
        )
        tracking_response_note = (
            f"Tracking issue: {issue_key}. "
            if issue_key
            else (
                "⚠️ No Linear ticket recorded for this report; "
                "it is not on the Linear list. "
            )
        )
        report_message = message_body + issue_note

        if post_only:
            try:
                permalink = _post_feedback_report(
                    report_message,
                    thread_url,
                    target_person=reporting_user,
                    agent_session_url=session_under_investigation or "",
                    cc_persons=list(_FEEDBACK_CC_USERGROUPS),
                    issue_url=linear_issue_url or None,
                    header_emoji=_feedback_emoji(feedback_type),
                    header_label=_feedback_label(feedback_type),
                )
            except (SlackAPIError, SlackURLParseError) as exc:
                return SessionFeedbackResponse(
                    success=False,
                    message=f"{tracking_response_note}Feedback posting failed: {exc}",
                    linear_issue_url=linear_issue_url,
                    linear_issue_identifier=issue_key,
                )
            return SessionFeedbackResponse(
                success=True,
                message=(
                    f"{tracking_response_note}"
                    "Feedback posted to Slack without dispatching triage: "
                    f"{permalink}"
                ),
                linear_issue_url=linear_issue_url,
                linear_issue_identifier=issue_key,
            )

        posted_permalink: str | None = None
        slack_post_error: SlackAPIError | SlackURLParseError | None = None
        if thread_url:
            try:
                posted_permalink = _post_feedback_report(
                    report_message,
                    thread_url,
                    target_person=reporting_user,
                    agent_session_url=session_under_investigation or "",
                    cc_persons=list(_FEEDBACK_CC_USERGROUPS),
                    issue_url=linear_issue_url or None,
                    header_emoji=_feedback_emoji(feedback_type),
                    header_label=_feedback_label(feedback_type),
                )
            except (SlackAPIError, SlackURLParseError) as exc:
                slack_post_error = exc

        triage_result = _dispatch_triage_workflow(
            session_url=session_under_investigation,
            feedback_context=message_body,
            reporting_user=reporting_user,
            session_playbook=session_playbook,
            related_skill_name=related_skill_name,
            cc_persons=",".join(_FEEDBACK_CC_USERGROUPS),
            header_emoji=_feedback_emoji(feedback_type),
            header_label=_feedback_label(feedback_type),
            linear_issue_url=linear_issue_url or "",
            linear_issue_id=linear_issue_id or "",
            thread_url=thread_url or "",
        )
        if triage_result is not None:
            view_url = triage_result.run_url or triage_result.workflow_url
            notification_note = (
                f"Slack report posted at {posted_permalink}. "
                if posted_permalink
                else (
                    f"Slack posting failed: {slack_post_error}. "
                    if slack_post_error
                    else "A Slack notification will be posted to #hydra-feedback "
                    "once the triage session starts. "
                )
            )
            return SessionFeedbackResponse(
                success=True,
                message=(
                    "Feedback submitted. Auto-triage workflow launched. "
                    f"{tracking_response_note}"
                    f"{notification_note}"
                    f"View workflow progress at: {view_url}"
                ),
                workflow_url=triage_result.workflow_url,
                run_id=triage_result.run_id,
                run_url=triage_result.run_url,
                triage_run_url=view_url,
                linear_issue_url=linear_issue_url,
                linear_issue_identifier=issue_key,
            )
        if posted_permalink:
            return SessionFeedbackResponse(
                success=True,
                message=(
                    tracking_response_note
                    + "Feedback was posted to the originating Slack thread, but "
                    "auto-triage dispatch failed. "
                    f"View the report at: {posted_permalink}"
                ),
                linear_issue_url=linear_issue_url,
                linear_issue_identifier=issue_key,
            )

        # Triage dispatch failed — fall back to direct HITL notification
        # so negative feedback is still recorded in Slack.
        if slack_post_error:
            logger.warning(
                "Thread posting failed (%s) and triage dispatch failed; "
                "falling back to direct HITL dispatch.",
                slack_post_error,
            )
        else:
            logger.warning(
                "Triage workflow dispatch failed; falling back to direct HITL dispatch."
            )

    if not is_negative_feedback and thread_url:
        try:
            permalink = _post_feedback_report(
                message_body,
                thread_url,
                target_person=reporting_user,
                agent_session_url=session_under_investigation or "",
                cc_persons=list(_FEEDBACK_CC_USERGROUPS),
                issue_url=linear_issue_url or None,
                header_emoji=_feedback_emoji(feedback_type),
                header_label=_feedback_label(feedback_type),
            )
        except (SlackAPIError, SlackURLParseError) as exc:
            return SessionFeedbackResponse(
                success=False,
                message=f"Feedback posting failed: {exc}",
            )
        return SessionFeedbackResponse(
            success=True,
            message=f"Feedback posted to the originating Slack thread: {permalink}",
        )

    # Positive feedback (or negative feedback fallback): dispatch HITL directly
    result = dispatch_escalation(
        target_person=reporting_user,
        message=report_message if is_negative_feedback else message_body,
        agent_session_url=agent_session_url or "",
        cc=list(_FEEDBACK_CC_USERGROUPS),
        channel_override=_FEEDBACK_CHANNEL,
        header_emoji=_feedback_emoji(feedback_type),
        header_label=_feedback_label(feedback_type),
    )

    view_url = result.run_url or result.workflow_url
    return SessionFeedbackResponse(
        success=True,
        message=(
            f"{tracking_response_note}"
            f"Feedback submitted and posted to #hydra-feedback. "
            f"The reporting user and the @oc-hydra and @oc-internal-ai groups "
            f"have been tagged. "
            f"View progress at: {view_url}"
        ),
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
        linear_issue_url=linear_issue_url if is_negative_feedback else None,
        linear_issue_identifier=issue_key if is_negative_feedback else None,
    )


_FOLLOWUP_HEADER = "🤖 *Automated Triage Update*"

_FOLLOWUP_FOOTER_TEMPLATE = (
    "_ℹ️ This thread is not monitored by Devin. "
    "Replies here will not be seen by any agent. "
    "For follow-up, use the <{agent_session_url}|linked session> or create a new task._"
)


def _wrap_followup_message(message: str, *, agent_session_url: str) -> str:
    """Wrap a follow-up message with session link and non-interactive disclaimer."""
    footer = _FOLLOWUP_FOOTER_TEMPLATE.format(agent_session_url=agent_session_url)
    return f"{_FOLLOWUP_HEADER}\n\n{message}\n\n{footer}"


class SessionFeedbackFollowupResponse(BaseModel):
    """Response from the session feedback follow-up tool."""

    success: bool = Field(description="Whether the follow-up was posted successfully")
    message: str = Field(description="Human-readable status message")
    reply_ts: str | None = Field(
        default=None,
        description="Timestamp of the posted reply (Slack ts format)",
    )


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def devin_session_feedback_followup(
    thread_url: Annotated[
        str,
        Field(
            description=(
                "Slack thread URL from the original feedback post in #hydra-feedback. "
                "This is the thread where follow-up context will be appended. "
                "Example: https://airbytehq-team.slack.com/archives/C0ACUHRP6B1/p1773062711122019"
            ),
        ),
    ],
    message: Annotated[
        str,
        Field(
            description=(
                "Follow-up message text in Slack mrkdwn format. "
                "Typically a triage report or additional context about the "
                "feedback being investigated. "
                "Supports *bold*, _italic_, `code`, ```code blocks```, "
                "> blockquotes, and <url|label> links."
            ),
        ),
    ],
    agent_session_url: Annotated[
        str,
        Field(
            description=(
                "Your agent session URL for audit trail. "
                "Use the session URL from your system prompt."
            ),
        ),
    ],
) -> SessionFeedbackFollowupResponse:
    """Post a follow-up to an existing feedback thread in #hydra-feedback.

    This is the "second call" in the feedback workflow: after
    `devin_session_feedback` creates the initial report, this tool appends
    triage findings or additional context as a threaded reply.

    Each reply is wrapped with a disclaimer clarifying that the thread is
    non-interactive and not monitored by any agent.

    Workspace validation ensures only URLs from the expected Slack
    workspace are accepted.
    """
    try:
        channel_id, thread_ts = parse_slack_thread_url(thread_url)
    except SlackURLParseError as exc:
        return SessionFeedbackFollowupResponse(
            success=False,
            message=str(exc),
        )

    wrapped_message = _wrap_followup_message(
        message, agent_session_url=agent_session_url
    )

    try:
        result = post_thread_reply(
            channel_id=channel_id,
            thread_ts=thread_ts,
            message=wrapped_message,
        )
        reply_ts = result.ts
    except SlackAPIError as exc:
        return SessionFeedbackFollowupResponse(
            success=False,
            message=f"Slack API error: {exc}",
        )

    logger.info(
        "Feedback follow-up posted: channel=%s thread_ts=%s agent=%s",
        channel_id,
        thread_ts,
        agent_session_url,
    )
    return SessionFeedbackFollowupResponse(
        success=True,
        message=f"Follow-up posted to feedback thread in channel {channel_id}.",
        reply_ts=reply_ts,
    )


class DevinSessionNameResponse(BaseModel):
    """Response from the Devin session naming tool."""

    session_id: str = Field(description="Resolved session ID")
    name: str = Field(description="Two-word session name")
    full_name: str = Field(description="Session name with the Devin suffix")


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def get_devin_session_name(
    session_id: Annotated[
        str,
        "Bare session ID or session URL.",
    ],
) -> DevinSessionNameResponse:
    """Deterministically look up a Devin session name from its ID or URL."""
    resolved_id = extract_session_id(session_id)
    name = generate_friendly_name(resolved_id)
    full_name = f"{name} Devin"
    return DevinSessionNameResponse(
        session_id=resolved_id,
        name=name,
        full_name=full_name,
    )


def register_devin_ops_tools(app: FastMCP) -> None:
    """Register devin_ops tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
