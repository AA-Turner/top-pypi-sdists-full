"""Safe, non-retryable GitHub API failures."""

from __future__ import annotations

import re
from typing import NoReturn

from .agent_task_diagnostics import AgentTaskDiagnostics


def parse_bare_http_status(stderr: str) -> int | None:
    """Accept a leading CLI HTTP error code, never incidental URL/identifier digits."""
    match = re.match(r"([45]\d{2})\b", stderr)
    return int(match.group(1)) if match else None


class GitHubApiError(RuntimeError):
    """An API rejection with parsed status, never raw response or credential data."""

    def __init__(self, http_status: int | None = None, *, safe_message: str | None = None) -> None:
        self.http_status = http_status
        status = f"HTTP {http_status}" if http_status is not None else "status unavailable"
        message = safe_message if safe_message is not None else f"GitHub API error: {status}"
        super().__init__(message)


def resolve_http_status(
    diagnostics: AgentTaskDiagnostics,
    status: int | None,
    stderr: str,
) -> int | None:
    """Resolve a missing response status from a leading bare stderr status."""
    if status is None:
        status = parse_bare_http_status(stderr)
        if status is not None:
            diagnostics.status, diagnostics.status_source = status, "stderr"
    return status


def is_rate_limit_failure(
    stderr: str,
    status: int | None,
    retry_after: float | None,
    remaining: int | None,
) -> bool:
    """Return whether GitHub response evidence identifies a rate-limit failure."""
    stderr_lower = stderr.lower()
    rate_indicator = "rate limit" in stderr_lower or "secondary rate limit" in stderr_lower
    has_rate_headers = retry_after is not None or remaining == 0
    return (
        rate_indicator or status == 429 or (status == 403 and has_rate_headers) or (status is None and has_rate_headers)
    )


def raise_github_api_error(
    diagnostics: AgentTaskDiagnostics,
    status: int | None,
    stderr: str,
    returncode: int,
) -> NoReturn:
    """Raise a permanent API error, exposing only sanitized Agent Tasks diagnostics."""
    safe_message = (
        diagnostics.format_error(
            stderr if stderr else f"exit code {returncode}",
            prefix="GitHub API error: ",
        )
        if diagnostics.is_agent_tasks
        else None
    )
    raise GitHubApiError(status, safe_message=safe_message)
