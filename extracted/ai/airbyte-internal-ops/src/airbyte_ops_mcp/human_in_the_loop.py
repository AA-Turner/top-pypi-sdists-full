# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Slack notification dispatch: workflow dispatch and person resolution.

This module provides the core logic for dispatching Slack notifications via
GitHub Actions. It is used by both the `escalate_to_human` and
`devin_session_feedback` MCP tools.

The Slack API call happens inside CI (not at MCP runtime) so that Slack tokens
are never exposed to the calling agent. The workflow resolves person identifiers
to Slack user IDs using the internal team roster artifact.

Person identifier conventions:
- `@username` → GitHub handle (the leading `@` is stripped)
- `U` followed by uppercase alphanumeric (e.g. `U05AKF1BCC9`) → Slack user ID
- Contains `@` with a domain part (e.g. `aj@airbyte.io`) → email address
"""

from __future__ import annotations

import json
import logging
import re

from airbyte_ops_mcp.github_actions import (
    WorkflowDispatchResult,
    resolve_default_workflow_branch,
    trigger_workflow_dispatch,
)
from airbyte_ops_mcp.github_api import resolve_ci_trigger_github_token

logger = logging.getLogger(__name__)

HITL_REPO_OWNER = "airbytehq"
HITL_REPO_NAME = "airbyte-ops-mcp"
HITL_WORKFLOW_FILE = "human-in-the-loop.yml"
HITL_DEFAULT_BRANCH = "main"

HITL_SLACK_CHANNEL_URL = "https://airbytehq-team.slack.com/archives/C0AEXV81Q7N"

# Slack Block Kit `confirm.text.text` caps at 300 chars; the CI renderer
# prepends `"> "` (2 chars) as a blockquote prefix.
APPROVAL_REQUEST_SUMMARY_MAX_LENGTH = 280


_SLACK_ID_PATTERN = re.compile(r"^U[A-Z0-9]{8,}$")
_SLACK_USERGROUP_ID_PATTERN = re.compile(r"^S[A-Z0-9]{8,}$")


def classify_person_id(identifier: str) -> str:
    """Classify a person or Slack usergroup identifier string.

    Args:
        identifier: A person or Slack usergroup identifier (email, GitHub
            handle, Slack user ID, or Slack usergroup ID).

    Returns:
        One of `"github_handle"`, `"slack_id"`, `"slack_usergroup_id"`, or
        `"email"`.
    """
    identifier = identifier.strip()
    if identifier.startswith("@"):
        return "github_handle"
    if _SLACK_USERGROUP_ID_PATTERN.match(identifier):
        return "slack_usergroup_id"
    if _SLACK_ID_PATTERN.match(identifier):
        return "slack_id"
    if "@" in identifier and "." in identifier.split("@", 1)[-1]:
        return "email"
    return "github_handle"


_AIRBYTE_EMAIL_DOMAIN = "@airbyte.io"


def validate_person_id(identifier: str) -> None:
    """Validate that a person or Slack usergroup identifier is well-formed.

    Accepted formats:
    - GitHub handle prefixed with `@` (e.g. `@aaronsteers`)
    - Slack user ID matching `U` + uppercase alphanumeric (e.g. `U05AKF1BCC9`)
    - Slack usergroup ID matching `S` + uppercase alphanumeric
      (e.g. `S0BKR63VAN5`)
    - Email address ending in `@airbyte.io` (e.g. `aj@airbyte.io`)

    A bare string without `@` prefix that does not match the Slack ID or
    email patterns is ambiguous and rejected.  The caller must use an
    explicit `@` prefix for GitHub handles.

    Args:
        identifier: Raw person or Slack usergroup identifier string.

    Raises:
        ValueError: If the identifier does not match any recognized format.
    """
    stripped = identifier.strip()
    if not stripped:
        raise ValueError("Identifier is empty.")

    # @-prefixed → GitHub handle
    if stripped.startswith("@"):
        handle = stripped[1:]
        if not handle:
            raise ValueError("Identifier '@' is missing the GitHub handle after '@'.")
        return

    # Slack user or usergroup ID
    if _SLACK_ID_PATTERN.match(stripped) or _SLACK_USERGROUP_ID_PATTERN.match(stripped):
        return

    # Email
    if "@" in stripped and "." in stripped.split("@", 1)[-1]:
        if not stripped.endswith(_AIRBYTE_EMAIL_DOMAIN):
            raise ValueError(
                f"Identifier '{stripped}' looks like an email but does not "
                f"end in '{_AIRBYTE_EMAIL_DOMAIN}'. Only Airbyte emails are accepted."
            )
        return

    raise ValueError(
        f"Identifier '{stripped}' is not a recognized format. "
        "Use '@username' for a GitHub handle, an Airbyte email address "
        "(e.g. 'aj@airbyte.io'), a Slack user ID (e.g. 'U05AKF1BCC9'), "
        "or a Slack usergroup ID (e.g. 'S0BKR63VAN5')."
    )


def validate_approval_request_summary(summary: str | None) -> None:
    """Validate an `approval_request_summary` fits the Slack confirm dialog.

    Enforces a max length of `APPROVAL_REQUEST_SUMMARY_MAX_LENGTH` and a balanced
    backtick count. `None` and empty strings are accepted.

    Raises:
        ValueError: If `summary` violates either constraint.
    """
    if summary is None or summary == "":
        return

    if len(summary) > APPROVAL_REQUEST_SUMMARY_MAX_LENGTH:
        raise ValueError(
            f"approval_request_summary is {len(summary)} characters but must be "
            f"at most {APPROVAL_REQUEST_SUMMARY_MAX_LENGTH} characters to fit "
            "inside Slack's confirm-dialog limit. Shorten the summary to only "
            "the context the approver needs to identify what they are approving."
        )

    if summary.count("`") % 2 != 0:
        raise ValueError(
            "approval_request_summary has an odd number of backticks, which leaves "
            "an unterminated inline-code span in the Slack confirm dialog and "
            "causes the Approve/Reject buttons to fail silently. Balance the "
            "backticks or drop them entirely."
        )


def normalize_person_id(identifier: str) -> str:
    """Normalize a person identifier for workflow input.

    Strips leading `@` from GitHub handles and trims whitespace.

    Args:
        identifier: Raw person identifier string.

    Returns:
        Normalized identifier string.
    """
    identifier = identifier.strip()
    if identifier.startswith("@"):
        return identifier[1:]
    return identifier


def dispatch_escalation(
    target_person: str,
    message: str,
    agent_session_url: str,
    cc: list[str] | None = None,
    pr_url: str | None = None,
    issue_url: str | None = None,
    additional_actions: dict[str, str] | None = None,
    approval_requested: bool = False,
    approval_request_summary: str | None = None,
    approval_request_detail_url: str | None = None,
    approval_metadata: dict[str, str] | None = None,
    channel_override: str | None = None,
    header_emoji: str | None = None,
    header_label: str | None = None,
    context_footer: str | None = None,
    connector_name: str | None = None,
) -> WorkflowDispatchResult:
    """Dispatch a Slack notification via the GitHub Actions workflow.

    Triggers the `human-in-the-loop.yml` workflow which resolves person
    identifiers to Slack user IDs (using the roster artifact), preserves
    Slack usergroup IDs, and posts a formatted message to Slack.

    The `channel_override`, `header_emoji`, `header_label`, and
    `context_footer` parameters are set by the calling MCP tool and
    are NOT exposed to agents directly.

    Raises:
        ValueError: If `target_person` or any `cc` entry is not a
            recognized person or Slack usergroup identifier format, or if
            `approval_request_summary` violates Slack confirm-dialog
            constraints.
    """
    validate_person_id(target_person)
    if cc:
        for person in cc:
            validate_person_id(person)
    if approval_requested:
        validate_approval_request_summary(approval_request_summary)

    token = resolve_ci_trigger_github_token()

    workflow_inputs: dict[str, str] = {
        "target_person": normalize_person_id(target_person),
        "message": message,
        "agent_session_url": agent_session_url,
    }

    if cc:
        normalized_cc = [normalize_person_id(person) for person in cc]
        workflow_inputs["cc_persons"] = ",".join(normalized_cc)

    if pr_url:
        workflow_inputs["pr_url"] = pr_url

    if issue_url:
        workflow_inputs["issue_url"] = issue_url

    if additional_actions:
        workflow_inputs["additional_actions"] = json.dumps(additional_actions)

    if approval_requested:
        workflow_inputs["approval_requested"] = "true"

    if approval_request_summary:
        workflow_inputs["approval_request_summary"] = approval_request_summary

    if approval_request_detail_url:
        workflow_inputs["approval_request_detail_url"] = approval_request_detail_url

    if approval_metadata:
        workflow_inputs["approval_metadata"] = json.dumps(approval_metadata)

    if channel_override:
        workflow_inputs["channel_override"] = channel_override

    if header_emoji:
        workflow_inputs["header_emoji"] = header_emoji

    if header_label:
        workflow_inputs["header_label"] = header_label

    if context_footer:
        workflow_inputs["context_footer"] = context_footer

    if connector_name:
        workflow_inputs["connector_name"] = connector_name

    return trigger_workflow_dispatch(
        owner=HITL_REPO_OWNER,
        repo=HITL_REPO_NAME,
        workflow_file=HITL_WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(HITL_DEFAULT_BRANCH),
        inputs=workflow_inputs,
        token=token,
    )
