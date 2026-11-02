"""Tests for list_epics in generate_epic_progress_report."""

from __future__ import annotations

import re
from unittest.mock import patch

import pytest

from tests.scripts.generate_epic_progress_report import report


def _run_gh_returning(raw: str):
    """Patch _run_gh to return a raw string."""
    return patch.object(report, "_run_gh", return_value=raw)


def test_raises_runtime_error_on_invalid_json():
    """Raises RuntimeError when gh returns non-JSON text."""
    with _run_gh_returning("not json at all"):
        with pytest.raises(RuntimeError, match="non-JSON"):
            report.list_epics("owner", "repo")


def test_runtime_error_includes_repo_context():
    """RuntimeError from invalid JSON includes the owner/repo context."""
    with _run_gh_returning("error: authentication required"):
        with pytest.raises(RuntimeError, match=re.escape("owner/repo")):
            report.list_epics("owner", "repo")


def test_runtime_error_includes_output_snippet():
    """RuntimeError from invalid JSON includes a snippet of the bad output."""
    with _run_gh_returning("error: bad credentials"):
        with pytest.raises(RuntimeError, match="bad credentials"):
            report.list_epics("owner", "repo")


def test_returns_issue_numbers_for_valid_response():
    """Returns list of issue numbers from a valid JSON response."""
    import json

    payload = json.dumps([{"number": 10}, {"number": 20}])
    with _run_gh_returning(payload):
        result = report.list_epics("owner", "repo")
    assert result == [10, 20]
