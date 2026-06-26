# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Shared approval resolution logic for MCP admin tools.

This module provides a unified interface for resolving an admin's
`@airbyte.io` email address from an approval URL.  The preferred
approval method is a Slack approval record URL obtained via the
`escalate_to_human` tool.  GitHub comment URLs are still supported
as a legacy fallback but should not be advertised to agents.

Both URL types follow the same trust model: the agent supplies a URL
that cannot be forged, the server fetches the underlying resource,
extracts the identity, and validates the email domain.

When running inside the Ops Webapp (detected via the
`AIRBYTE_OPS_WEBAPP_PUBLIC_URL` environment variable), approval
resolution can be bypassed entirely — the human operator is already
authenticated via OAuth and their email is known from the session.
"""

import os
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlparse

from airbyte_ops_mcp.github_api import (
    GitHubAPIError,
    GitHubCommentParseError,
    GitHubUserEmailNotFoundError,
    get_admin_email_from_approval_comment,
)
from airbyte_ops_mcp.slack_api import (
    SlackAPIError,
    SlackApprovalRecordError,
    SlackURLParseError,
    SlackUserEmailNotFoundError,
    validate_slack_approval_record,
)

WEBAPP_PUBLIC_URL_ENV_VAR = "AIRBYTE_OPS_WEBAPP_PUBLIC_URL"
ADMIN_EMAIL_DOMAIN = "@airbyte.io"


class ApprovalResolutionError(Exception):
    """Raised when admin email cannot be resolved from any approval URL."""


class ApprovalStatus(Enum):
    """Ternary outcome of an approval check."""

    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_APPROVAL = "needs_approval"


@dataclass(frozen=True)
class ApprovalCheck:
    """Result of `check_approval_status`."""

    status: ApprovalStatus
    admin_email: str | None = None
    reason: str | None = None


def is_webapp_environment() -> bool:
    """Return `True` when running inside the Ops Webapp process.

    Detection is based on the presence of `AIRBYTE_OPS_WEBAPP_PUBLIC_URL`,
    which is set exclusively in the webapp's Cloud Run service definition
    (via Pulumi infra) and cannot be injected by tool callers.
    """
    return bool(os.environ.get(WEBAPP_PUBLIC_URL_ENV_VAR, "").strip())


def _is_slack_url(url: str) -> bool:
    """Return True if *url* looks like a Slack message permalink."""
    hostname = urlparse(url).hostname or ""
    return hostname.endswith(".slack.com")


def _is_github_url(url: str) -> bool:
    """Return True if *url* looks like a GitHub comment URL."""
    hostname = urlparse(url).hostname or ""
    return hostname == "github.com"


def check_approval_status(
    *,
    approval_comment_url: str | None = None,
    user_email: str | None = None,
) -> ApprovalCheck:
    """Unified entry point for authorization checks.

    Returns an `ApprovalCheck` with one of three statuses:

    - `APPROVED`: Authorization is satisfied. `admin_email` is populated.
    - `REJECTED`: Authorization was attempted but failed (e.g., invalid
      email domain, bad approval URL). `reason` explains why.
    - `NEEDS_APPROVAL`: No authorization artifacts provided and not in
      webapp mode. Caller should obtain an approval URL first.
    """
    # Normalize inputs: strip whitespace, lowercase email for domain check.
    if user_email:
        user_email = user_email.strip()
    if approval_comment_url:
        approval_comment_url = approval_comment_url.strip() or None

    # Webapp path: human is already authenticated via OAuth.
    if is_webapp_environment() and user_email:
        if not user_email.lower().endswith(ADMIN_EMAIL_DOMAIN):
            return ApprovalCheck(
                status=ApprovalStatus.REJECTED,
                reason=(
                    f"Email must be an {ADMIN_EMAIL_DOMAIN} address, got: {user_email}"
                ),
            )
        return ApprovalCheck(
            status=ApprovalStatus.APPROVED,
            admin_email=user_email,
        )

    # Agent/cron path: need an external approval URL.
    if not approval_comment_url:
        return ApprovalCheck(
            status=ApprovalStatus.NEEDS_APPROVAL,
            reason=(
                "'approval_comment_url' is required. Use `escalate_to_human` with "
                "`approval_requested=True` to obtain a Slack approval record URL."
            ),
        )

    # Resolve email from the external approval URL.
    try:
        admin_email = resolve_admin_email_from_approval(
            approval_comment_url=approval_comment_url,
        )
        return ApprovalCheck(
            status=ApprovalStatus.APPROVED,
            admin_email=admin_email,
        )
    except ApprovalResolutionError as e:
        return ApprovalCheck(
            status=ApprovalStatus.REJECTED,
            reason=str(e),
        )


def resolve_admin_email_from_approval(
    *,
    approval_comment_url: str | None = None,
) -> str:
    """Resolve admin email from an approval URL (GitHub or Slack).

    The parameter `approval_comment_url` accepts URLs from either
    domain.  The backend is selected automatically based on the URL:

    * URLs containing `.slack.com/` are dispatched to the Slack
      approval-record resolver.
    * URLs starting with `https://github.com/` are dispatched to the
      GitHub comment resolver (with additional fragment validation).

    Returns:
        The admin's `@airbyte.io` email address.

    Raises:
        ApprovalResolutionError: If validation fails, the URL cannot be
            parsed, the API call fails, or the email cannot be resolved.
    """
    if not approval_comment_url:
        raise ApprovalResolutionError(
            "'approval_comment_url' is required. Use `escalate_to_human` with "
            "`approval_requested=True` to obtain a Slack approval record URL."
        )

    # Domain-based dispatch
    if _is_slack_url(approval_comment_url):
        return _resolve_from_slack(approval_comment_url)

    if _is_github_url(approval_comment_url):
        return _resolve_from_github(approval_comment_url)

    raise ApprovalResolutionError(
        f"Unrecognized approval URL domain: {approval_comment_url}. "
        "Expected a Slack approval record URL (https://<workspace>.slack.com/...). "
        "Use `escalate_to_human` with `approval_requested=True` to obtain one."
    )


def _resolve_from_github(approval_comment_url: str) -> str:
    """Resolve admin email from a GitHub comment URL.

    Raises:
        ApprovalResolutionError: On any failure.
    """
    if (
        "#issuecomment-" not in approval_comment_url
        and "#discussion_r" not in approval_comment_url
    ):
        raise ApprovalResolutionError(
            "approval_comment_url must be a GitHub comment URL "
            "(containing #issuecomment- or #discussion_r)"
        )

    try:
        return get_admin_email_from_approval_comment(approval_comment_url)
    except GitHubCommentParseError as e:
        raise ApprovalResolutionError(
            f"Failed to parse approval comment URL: {e}"
        ) from e
    except GitHubAPIError as e:
        raise ApprovalResolutionError(
            f"Failed to fetch approval comment from GitHub: {e}"
        ) from e
    except GitHubUserEmailNotFoundError as e:
        raise ApprovalResolutionError(str(e)) from e


def _resolve_from_slack(approval_slack_url: str) -> str:
    """Resolve admin email from a Slack approval record URL.

    Raises:
        ApprovalResolutionError: On any failure.
    """
    try:
        record = validate_slack_approval_record(
            approval_slack_url,
            require_approved=True,
            resolve_admin_email=True,
        )
        assert record.admin_email is not None  # guaranteed by resolve_admin_email=True
        return record.admin_email
    except SlackURLParseError as e:
        raise ApprovalResolutionError(f"Failed to parse Slack approval URL: {e}") from e
    except SlackAPIError as e:
        raise ApprovalResolutionError(
            f"Failed to fetch approval record from Slack: {e}"
        ) from e
    except SlackApprovalRecordError as e:
        raise ApprovalResolutionError(f"Invalid Slack approval record: {e}") from e
    except SlackUserEmailNotFoundError as e:
        raise ApprovalResolutionError(str(e)) from e
