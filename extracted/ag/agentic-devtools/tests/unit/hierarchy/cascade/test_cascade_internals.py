"""Tests for CascadeProcessor internal methods."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from agentic_devtools.hierarchy.cascade import CascadeProcessor, IssueStateError


class TestGetIssueState:
    """Cover _get_issue_state method."""

    def test_success(self):
        proc = CascadeProcessor("owner", "repo")
        mock_result = type("R", (), {"returncode": 0, "stdout": json.dumps({"state": "open"}), "stderr": ""})()
        with patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result):
            result = proc._get_issue_state(42)
            assert result == {"state": "open"}

    def test_404_returns_none(self):
        proc = CascadeProcessor("owner", "repo")
        mock_result = type("R", (), {"returncode": 1, "stdout": "", "stderr": "404 Not Found"})()
        with patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result):
            result = proc._get_issue_state(42)
            assert result is None

    def test_non_404_error_raises(self):
        proc = CascadeProcessor("owner", "repo")
        mock_result = type("R", (), {"returncode": 1, "stdout": "", "stderr": "502 Bad Gateway"})()
        with patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result):
            with pytest.raises(IssueStateError, match="gh API error for issue #42"):
                proc._get_issue_state(42)

    def test_file_not_found_raises(self):
        proc = CascadeProcessor("owner", "repo")
        with patch("agentic_devtools.hierarchy.cascade.run_safe", side_effect=FileNotFoundError):
            with pytest.raises(IssueStateError, match="gh CLI not found"):
                proc._get_issue_state(42)

    def test_json_decode_error_raises(self):
        proc = CascadeProcessor("owner", "repo")
        mock_result = type("R", (), {"returncode": 0, "stdout": "not json", "stderr": ""})()
        with patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result):
            with pytest.raises(IssueStateError, match="Failed to parse"):
                proc._get_issue_state(42)


class TestApplyLabel:
    """Cover _apply_label method."""

    def test_success(self):
        proc = CascadeProcessor("owner", "repo")
        mock_result = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        with patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result):
            assert proc._apply_label(42) is True

    def test_failure(self):
        proc = CascadeProcessor("owner", "repo")
        mock_result = type("R", (), {"returncode": 1, "stdout": "", "stderr": ""})()
        with patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result):
            assert proc._apply_label(42) is False

    def test_file_not_found(self):
        proc = CascadeProcessor("owner", "repo")
        with patch("agentic_devtools.hierarchy.cascade.run_safe", side_effect=FileNotFoundError):
            assert proc._apply_label(42) is False


class TestPostComment:
    """Cover _post_comment method."""

    def test_success(self):
        proc = CascadeProcessor("owner", "repo")
        mock_result = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        with patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result):
            assert proc._post_comment(42, "hello") is True

    def test_failure(self):
        proc = CascadeProcessor("owner", "repo")
        mock_result = type("R", (), {"returncode": 1, "stdout": "", "stderr": ""})()
        with patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result):
            assert proc._post_comment(42, "hello") is False

    def test_file_not_found(self):
        proc = CascadeProcessor("owner", "repo")
        with patch("agentic_devtools.hierarchy.cascade.run_safe", side_effect=FileNotFoundError):
            assert proc._post_comment(42, "hello") is False
