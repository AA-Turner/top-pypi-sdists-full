"""Shared JiraProvider test factories."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from agentic_devtools.adapters.issue_provider import IssueProvider


def _make_mock_session():
    """Create a mock requests session."""
    return MagicMock()


def _make_response(status_code=200, json_data=None, text=None):
    """Create a mock response."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    resp.text = text if text is not None else json.dumps(json_data or {})
    resp.raise_for_status = MagicMock()
    if status_code >= 400:
        resp.raise_for_status.side_effect = Exception(f"HTTP {status_code}")
    return resp


def _assert_jira_provider_conforms(provider: IssueProvider) -> None:
    """Typed helper for mypy static verification of protocol conformance."""
