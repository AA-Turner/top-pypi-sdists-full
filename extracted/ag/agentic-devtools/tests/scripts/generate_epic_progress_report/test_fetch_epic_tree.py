"""Tests for fetch_epic_tree in generate_epic_progress_report."""

from __future__ import annotations

import json
import re
from unittest.mock import patch

import pytest

from tests.scripts.generate_epic_progress_report import report


def _run_gh_returning(payload: dict):
    """Patch _run_gh to return the JSON-serialised payload."""
    return patch.object(report, "_run_gh", return_value=json.dumps(payload))


def test_raises_on_graphql_errors_array():
    """Raises RuntimeError with error messages when the response has an errors array."""
    payload = {"errors": [{"message": "Could not resolve to a Repository"}]}
    with _run_gh_returning(payload):
        with pytest.raises(RuntimeError, match="Could not resolve to a Repository"):
            report.fetch_epic_tree("owner", "repo", 1)


def test_raises_on_graphql_errors_array_includes_context():
    """RuntimeError from errors array includes the owner/repo#number context."""
    payload = {"errors": [{"message": "some error"}]}
    with _run_gh_returning(payload):
        with pytest.raises(RuntimeError, match=re.escape("owner/repo#1")):
            report.fetch_epic_tree("owner", "repo", 1)


def test_raises_when_issue_is_null():
    """Raises RuntimeError with context when data.repository.issue is null."""
    payload = {"data": {"repository": {"issue": None}}}
    with _run_gh_returning(payload):
        with pytest.raises(RuntimeError, match=re.escape("owner/repo#99")):
            report.fetch_epic_tree("owner", "repo", 99)


def test_raises_when_issue_is_null_includes_missing_issue_text():
    """RuntimeError for null issue contains 'missing issue' for debuggability."""
    payload = {"data": {"repository": {"issue": None}}}
    with _run_gh_returning(payload):
        with pytest.raises(RuntimeError, match="missing issue"):
            report.fetch_epic_tree("owner", "repo", 99)


def test_raises_when_data_key_missing():
    """Raises RuntimeError when the response has no 'data' key at all."""
    payload = {}
    with _run_gh_returning(payload):
        with pytest.raises(RuntimeError, match=re.escape("owner/repo#5")):
            report.fetch_epic_tree("owner", "repo", 5)


def test_returns_node_for_valid_response():
    """Returns a Node when the GraphQL response is well-formed."""
    issue = {
        "number": 42,
        "title": "My Epic",
        "state": "OPEN",
        "updatedAt": "2026-07-10T00:00:00Z",
        "labels": {"nodes": []},
        "assignees": {"nodes": []},
        "subIssues": {"nodes": [], "totalCount": 0},
    }
    payload = {"data": {"repository": {"issue": issue}}}
    with _run_gh_returning(payload):
        node = report.fetch_epic_tree("owner", "repo", 42)
    assert node.number == 42
    assert node.title == "My Epic"


def _run_gh_returning_raw(raw: str):
    """Patch _run_gh to return a raw (non-JSON) string."""
    return patch.object(report, "_run_gh", return_value=raw)


def test_raises_runtime_error_on_invalid_json():
    """Raises RuntimeError when gh returns non-JSON text."""
    with _run_gh_returning_raw("error: authentication required"):
        with pytest.raises(RuntimeError, match="non-JSON"):
            report.fetch_epic_tree("owner", "repo", 7)


def test_runtime_error_on_invalid_json_includes_context():
    """RuntimeError from invalid JSON includes the owner/repo#number context."""
    with _run_gh_returning_raw("bad gateway"):
        with pytest.raises(RuntimeError, match=re.escape("owner/repo#7")):
            report.fetch_epic_tree("owner", "repo", 7)


def test_runtime_error_on_invalid_json_includes_output_snippet():
    """RuntimeError from invalid JSON includes a snippet of the bad output."""
    with _run_gh_returning_raw("error: bad credentials"):
        with pytest.raises(RuntimeError, match="bad credentials"):
            report.fetch_epic_tree("owner", "repo", 7)
