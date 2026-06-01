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
"""

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


class ApprovalResolutionError(Exception):
    """Raised when admin email cannot be resolved from any approval URL."""


def _is_slack_url(url: str) -> bool:
    """Return True if *url* looks like a Slack message permalink."""
    hostname = urlparse(url).hostname or ""
    return hostname.endswith(".slack.com")


def _is_github_url(url: str) -> bool:
    """Return True if *url* looks like a GitHub comment URL."""
    hostname = urlparse(url).hostname or ""
    return hostname == "github.com"


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

    Args:
        approval_comment_url: URL to the approval comment or Slack
            approval record message.

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
