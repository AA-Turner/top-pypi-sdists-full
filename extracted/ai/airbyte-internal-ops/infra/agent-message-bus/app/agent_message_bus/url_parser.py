# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""URL parsing utilities for GitHub and Devin URLs."""

from __future__ import annotations

import re

from agent_message_bus.models import SubscriptionType

# Matches: https://github.com/{owner}/{repo}/issues/{number}
# Matches: https://github.com/{owner}/{repo}/pull/{number}
_GITHUB_URL_PATTERN = re.compile(
    r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/"
    r"(?P<type>issues|pull)/(?P<number>\d+)"
)

# Matches: https://app.devin.ai/sessions/{session_id}
_DEVIN_SESSION_PATTERN = re.compile(
    r"https://app\.devin\.ai/sessions/(?P<session_id>[a-fA-F0-9-]+)"
)


class ParsedGitHubURL:
    """Parsed components of a GitHub issue or PR URL."""

    def __init__(self, owner: str, repo: str, number: int, type: SubscriptionType) -> None:
        self.owner = owner
        self.repo = repo
        self.number = number
        self.type = type


def parse_github_url(url: str) -> ParsedGitHubURL:
    """Parse a GitHub issue or PR URL into its components.

    Args:
        url: A GitHub URL like https://github.com/owner/repo/issues/123
             or https://github.com/owner/repo/pull/456

    Returns:
        ParsedGitHubURL with owner, repo, number, and type.

    Raises:
        ValueError: If the URL doesn't match the expected pattern.
    """
    match = _GITHUB_URL_PATTERN.match(url)
    if not match:
        raise ValueError(
            f"Invalid GitHub URL: {url}. "
            "Expected format: https://github.com/owner/repo/issues/123 "
            "or https://github.com/owner/repo/pull/123"
        )

    url_type = match.group("type")
    sub_type = SubscriptionType.PULL_REQUEST if url_type == "pull" else SubscriptionType.ISSUE

    return ParsedGitHubURL(
        owner=match.group("owner"),
        repo=match.group("repo"),
        number=int(match.group("number")),
        type=sub_type,
    )


def extract_session_id(session_url: str) -> str:
    """Extract the session ID from a Devin session URL.

    Args:
        session_url: A Devin session URL like https://app.devin.ai/sessions/abc123

    Returns:
        The session ID string.

    Raises:
        ValueError: If the URL doesn't match the expected pattern.
    """
    match = _DEVIN_SESSION_PATTERN.search(session_url)
    if not match:
        raise ValueError(
            f"Invalid Devin session URL: {session_url}. "
            "Expected format: https://app.devin.ai/sessions/<session_id>"
        )
    return match.group("session_id")
