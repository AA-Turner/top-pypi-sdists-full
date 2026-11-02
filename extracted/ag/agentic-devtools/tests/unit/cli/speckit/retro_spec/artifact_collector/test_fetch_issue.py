"""Tests for fetch_issue in retro_spec/artifact_collector.py."""

from __future__ import annotations

import json
import subprocess
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import fetch_issue


class TestFetchIssue:
    """Tests for the fetch_issue function."""

    def test_returns_issue_with_labels_and_comments(self) -> None:
        """Test that closed issues are returned with normalized body and comments."""
        payload = {
            "title": "Retro issue",
            "body": None,
            "state": "closed",
            "labels": [{"name": "retro"}, {"name": "done"}],
        }
        run_results = [
            subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            subprocess.CompletedProcess([], 0, '"first comment"\n"second comment"\n', ""),
        ]

        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            side_effect=run_results,
        ):
            artifact = fetch_issue("owner", "repo", 42)

        assert artifact.number == 42
        assert artifact.title == "Retro issue"
        assert artifact.body == ""
        assert artifact.labels == ["retro", "done"]
        assert artifact.comments == ["first comment", "second comment"]

    def test_preserves_multiline_comment_body(self) -> None:
        """Test that a single multiline comment remains a single entry."""
        payload = {
            "title": "Retro issue",
            "body": "",
            "state": "closed",
            "labels": [],
        }
        run_results = [
            subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            subprocess.CompletedProcess([], 0, '"Line one\\nLine two"\n', ""),
        ]

        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            side_effect=run_results,
        ):
            artifact = fetch_issue("owner", "repo", 42)

        assert artifact.comments == ["Line one\nLine two"]

    def test_ignores_blank_invalid_and_empty_comment_lines(self) -> None:
        """Test that only valid non-empty JSON string comment lines are kept."""
        payload = {
            "title": "Retro issue",
            "body": "",
            "state": "closed",
            "labels": [],
        }
        run_results = [
            subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            subprocess.CompletedProcess([], 0, '\nnot-json\n""\n123\n"kept"\n', ""),
        ]

        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            side_effect=run_results,
        ):
            artifact = fetch_issue("owner", "repo", 42)

        assert artifact.comments == ["kept"]

    def test_returns_empty_comments_when_comment_fetch_fails(self) -> None:
        """Test that comment collection gracefully degrades on failure."""
        payload = {
            "title": "Retro issue",
            "body": "body",
            "state": "closed",
            "labels": [],
        }
        run_results = [
            subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            subprocess.CompletedProcess([], 1, "", "boom"),
        ]

        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            side_effect=run_results,
        ):
            artifact = fetch_issue("owner", "repo", 42)

        assert artifact.comments == []

    def test_returns_empty_comments_when_comment_fetch_raises_os_error(self) -> None:
        """Test that an OSError during comment fetch degrades to empty comments."""
        payload = {
            "title": "Retro issue",
            "body": "body",
            "state": "closed",
            "labels": [],
        }

        call_count = 0

        def run_side_effect(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return subprocess.CompletedProcess([], 0, json.dumps(payload), "")
            raise OSError("Permission denied")

        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            side_effect=run_side_effect,
        ):
            artifact = fetch_issue("owner", "repo", 42)

        assert artifact.comments == []

    def test_exits_when_initial_fetch_fails(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that a failed issue fetch exits with details."""
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            return_value=subprocess.CompletedProcess([], 1, "", "forbidden"),
        ):
            with pytest.raises(SystemExit, match="1"):
                fetch_issue("owner", "repo", 42)

        captured = capsys.readouterr()
        assert "Could not fetch issue #42" in captured.err
        assert "forbidden" in captured.err

    def test_exits_with_guidance_when_gh_is_unavailable(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that a missing gh CLI exits with actionable guidance."""
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            side_effect=FileNotFoundError("No such file or directory: 'gh'"),
        ):
            with pytest.raises(SystemExit, match="1"):
                fetch_issue("owner", "repo", 42)

        captured = capsys.readouterr()
        assert "Could not execute GitHub CLI" in captured.err
        assert "Install GitHub CLI" in captured.err
        assert "gh auth login" in captured.err

    def test_exits_with_generic_guidance_for_other_os_errors(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that non-file-not-found OS errors provide generic execution guidance."""
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            side_effect=OSError("Permission denied"),
        ):
            with pytest.raises(SystemExit, match="1"):
                fetch_issue("owner", "repo", 42)

        captured = capsys.readouterr()
        assert "Verify that `gh` is executable" in captured.err
        assert "Permission denied" in captured.err
        assert "Install GitHub CLI" not in captured.err

    def test_exits_when_json_response_is_invalid(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that a non-JSON response from the GitHub API exits with actionable guidance."""
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, "not valid json {{{", ""),
        ):
            with pytest.raises(SystemExit, match="1"):
                fetch_issue("owner", "repo", 42)

        assert "Unexpected response" in capsys.readouterr().err

    def test_exits_when_json_response_has_wrong_shape(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Malformed issue JSON is reported instead of raising an attribute error."""
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, "[]", ""),
        ):
            with pytest.raises(SystemExit, match="1"):
                fetch_issue("owner", "repo", 42)

        assert "Unexpected response" in capsys.readouterr().err

    def test_normalizes_non_string_issue_fields(self) -> None:
        """Malformed optional fields are ignored while retaining a usable issue."""
        payload = {
            "title": 42,
            "body": 42,
            "state": "closed",
            "labels": "invalid",
            "milestone": {"title": 42},
        }
        run_results = [
            subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            subprocess.CompletedProcess([], 0, "", ""),
        ]
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            side_effect=run_results,
        ):
            artifact = fetch_issue("owner", "repo", 42)

        assert artifact.title == "Issue #42"
        assert artifact.body == ""
        assert artifact.labels == []
        assert artifact.milestone == ""

    def test_falls_back_to_neutral_title_when_issue_title_is_blank(self) -> None:
        """Blank issue titles are replaced with a deterministic fallback."""
        payload = {
            "title": "   ",
            "body": "body",
            "state": "closed",
            "labels": [],
        }
        run_results = [
            subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
            subprocess.CompletedProcess([], 0, "", ""),
        ]

        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            side_effect=run_results,
        ):
            artifact = fetch_issue("owner", "repo", 42)

        assert artifact.title == "Issue #42"

    def test_exits_when_issue_is_not_closed(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that open issues are rejected."""
        payload = {
            "title": "Retro issue",
            "body": "body",
            "state": "open",
            "labels": [],
        }
        run_results = [
            subprocess.CompletedProcess([], 0, json.dumps(payload), ""),
        ]

        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            side_effect=run_results,
        ):
            with pytest.raises(SystemExit, match="1"):
                fetch_issue("owner", "repo", 42)

        assert "is not closed" in capsys.readouterr().err
