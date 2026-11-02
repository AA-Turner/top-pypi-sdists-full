"""Retrieve node: fetch issue details from Jira or GitHub.

Handles both Jira (via ``fetch_jira_issue_data``) and GitHub
(via ``fetch_github_issue_data``) issue retrieval paths using direct
Python calls. Normalizes issue data into a common state format.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from agentic_devtools.orchestration.nodes._helpers import (
    detect_issue_provider,
    utc_now,
)
from agentic_devtools.orchestration.nodes._issue_retrieval import (
    fetch_github_issue_data,
    fetch_jira_issue_data,
)
from agentic_devtools.orchestration.state_schema import WorkOnIssueState

logger = logging.getLogger(__name__)


def retrieve_node(state: WorkOnIssueState) -> dict[str, Any]:
    """Fetch issue details and store normalized data in state.

    Dispatches to Jira or GitHub retrieval based on ``issue_provider``.
    """
    issue_key = state.get("issue_key", "")
    # Fail fast when issue_key is missing, blank, or not a string — provider
    # detection and Jira/GitHub retrieval both require a valid key.
    if not isinstance(issue_key, str):
        return _error_result("issue_key is required and must be a non-empty string")
    issue_key = issue_key.strip()
    if not issue_key:
        return _error_result("issue_key is required and must be a non-empty string")
    raw_issue_provider = state.get("issue_provider")
    issue_provider = (
        raw_issue_provider
        if isinstance(raw_issue_provider, str) and raw_issue_provider in {"jira", "github"}
        else detect_issue_provider(issue_key)
    )

    if issue_provider == "jira":
        result = _retrieve_jira(issue_key)
    else:
        result = _retrieve_github(issue_key)

    # Propagate the (potentially derived) issue_provider back to state so downstream
    # nodes (e.g. pull_request_node) don't default to Jira/Azure DevOps when
    # issue_provider was absent or corrupted in the checkpoint.
    result["issue_provider"] = issue_provider
    return result


def _retrieve_jira(issue_key: str) -> dict[str, Any]:
    """Retrieve issue details from Jira via direct Python call."""
    # Resolve state directory for response persistence
    state_dir: Path | None = None
    try:
        from agentic_devtools.state import get_state_dir

        state_dir = Path(get_state_dir())
    except Exception as exc:
        logger.debug("get_state_dir() failed; response persistence disabled: %s", exc)

    try:
        normalized = fetch_jira_issue_data(issue_key, state_dir=state_dir)
    except ValueError as exc:
        return _error_result(f"Jira credential/config error: {exc}")
    except RuntimeError as exc:
        return _error_result(f"Jira retrieval failed: {exc}")
    except Exception as exc:  # noqa: BLE001
        return _error_result(f"Unexpected error retrieving Jira issue {issue_key}: {exc}")

    return {
        "step": "retrieve",
        "error": None,
        "issue_data": normalized,
        "issue_retrieved": True,
        "events": [
            {
                "event": "retrieve_completed",
                "timestamp": utc_now(),
                "signals": {"provider": "jira", "issue_key": issue_key},
            }
        ],
    }


def _retrieve_github(issue_key: str) -> dict[str, Any]:
    """Retrieve issue details from GitHub via adapter."""
    # Resolve state directory for response persistence
    state_dir: Path | None = None
    try:
        from agentic_devtools.state import get_state_dir

        state_dir = Path(get_state_dir())
    except Exception as exc:
        logger.debug("get_state_dir() failed; response persistence disabled: %s", exc)

    try:
        normalized = fetch_github_issue_data(issue_key, state_dir=state_dir)
    except RuntimeError as exc:
        return _error_result(f"GitHub issue retrieval failed: {exc}")
    except Exception as exc:  # noqa: BLE001
        return _error_result(f"Unexpected error retrieving GitHub issue {issue_key}: {exc}")

    return {
        "step": "retrieve",
        "error": None,
        "issue_data": normalized,
        "issue_retrieved": True,
        "events": [
            {
                "event": "retrieve_completed",
                "timestamp": utc_now(),
                "signals": {"provider": "github", "issue_key": issue_key},
            }
        ],
    }


def _error_result(message: str) -> dict[str, Any]:
    """Build an error result dict."""
    return {
        "step": "retrieve",
        "error": message,
        "issue_data": {},
        "issue_retrieved": False,
        "events": [
            {
                "event": "retrieve_failed",
                "timestamp": utc_now(),
                "signals": {"error": message},
            }
        ],
    }
