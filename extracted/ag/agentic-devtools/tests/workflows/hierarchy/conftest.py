"""Shared fixtures for hierarchy integration tests."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.hierarchy.cascade import CascadeProcessor


def make_issue_state(
    number: int,
    title: str = "",
    labels: list[str] | None = None,
    state: str = "open",
) -> dict[str, Any]:
    """Build a dict mimicking the GitHub REST API issue response."""
    return {
        "number": number,
        "title": title or f"Issue #{number}",
        "state": state,
        "labels": [{"name": lbl} for lbl in (labels or [])],
    }


@pytest.fixture()
def specs_root(tmp_path: Path) -> Path:
    """Return a temporary specs/ directory."""
    root = tmp_path / "specs"
    root.mkdir()
    return root


@pytest.fixture()
def mock_cascade_api() -> Generator[tuple[CascadeProcessor, MagicMock, MagicMock, MagicMock], None, None]:
    """Create a CascadeProcessor with mocked API methods.

    Returns:
        Tuple of (processor, mock_get_issue_state, mock_apply_label, mock_post_comment).
    """
    processor = CascadeProcessor(owner="test-owner", repo="test-repo")
    with (
        patch.object(processor, "_get_issue_state") as mock_state,
        patch.object(processor, "_apply_label", return_value=True) as mock_label,
        patch.object(processor, "_post_comment", return_value=True) as mock_comment,
    ):
        yield processor, mock_state, mock_label, mock_comment


def assert_label_applied(mock_label: MagicMock, issue_number: int) -> None:
    """Assert _apply_label was called with the given issue number."""
    calls = [c.args[0] for c in mock_label.call_args_list]
    assert issue_number in calls, f"Expected label applied to #{issue_number}, but calls were: {calls}"


def assert_label_not_applied(mock_label: MagicMock, issue_number: int) -> None:
    """Assert _apply_label was NOT called with the given issue number."""
    calls = [c.args[0] for c in mock_label.call_args_list]
    assert issue_number not in calls, f"Expected label NOT applied to #{issue_number}, but it was in calls: {calls}"


def assert_comment_posted(
    mock_comment: MagicMock,
    issue_number: int,
    substring: str,
) -> None:
    """Assert _post_comment was called with issue_number and body containing substring."""
    matching = [c for c in mock_comment.call_args_list if c.args[0] == issue_number and substring in c.args[1]]
    assert matching, (
        f"Expected comment on #{issue_number} containing {substring!r}. "
        f"Actual calls: {[(c.args[0], c.args[1][:80]) for c in mock_comment.call_args_list]}"
    )
