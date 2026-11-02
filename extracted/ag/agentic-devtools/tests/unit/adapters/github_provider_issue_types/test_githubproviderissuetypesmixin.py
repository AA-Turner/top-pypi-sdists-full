"""Tests for GitHubProvider."""

from __future__ import annotations

import json
import subprocess

import pytest

from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.issue_provider import (
    IssueTypeMappingError,
)
from tests.unit.adapters.github_provider._fixtures import _make_run_mock


class TestGitHubProviderSetIssueType:
    """Tests for GitHubProvider.set_issue_type."""

    def test_set_issue_type_epic(self):
        # set_issue_type will make 2 calls: GET labels, PATCH issue.
        responses = [
            json.dumps([]),  # GET existing labels
            json.dumps({}),  # PATCH issue response
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.set_issue_type("42", "epic", dry_run=False)
        assert result.status == "updated"
        assert result.identifier == "42"
        assert result.metadata["issue_type"] == "epic"

    def test_set_issue_type_returns_no_op_when_label_already_present(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps([{"name": "bug"}])),
        )
        result = provider.set_issue_type("42", "bug", dry_run=False)
        assert result.status == "no-op"
        assert result.identifier == "42"
        assert result.metadata["issue_type"] == "bug"

    def test_set_issue_type_replaces_existing_type_label(self):
        captured: dict[str, object] = {}
        responses = [
            json.dumps([{"name": "bug"}, {"name": "priority-high"}]),  # GET existing labels
            json.dumps({}),  # PATCH issue response
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            captured["args"] = args[0]
            captured["input"] = kwargs.get("input")
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.set_issue_type("42", "task", dry_run=False)

        assert result.status == "updated"
        assert result.identifier == "42"
        assert result.metadata["issue_type"] == "task"
        assert isinstance(captured["args"], list)
        assert "--method" in captured["args"]
        assert captured["args"][captured["args"].index("--method") + 1] == "PATCH"
        assert captured["args"][2] == "/repos/org/repo/issues/42"
        payload = json.loads(str(captured["input"]))
        assert payload["labels"] == ["priority-high", "task"]

    def test_set_issue_type_fetches_all_label_pages_before_patch(self):
        captured_calls: list[list[str]] = []
        captured_payload: dict[str, object] = {}
        first_page = [{"name": f"label-{i}"} for i in range(100)]
        first_page[0] = {"name": "bug"}
        responses = [
            json.dumps(first_page),
            json.dumps([{"name": "carry-over"}]),
            json.dumps({}),
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            captured_calls.append(list(args[0]))
            if kwargs.get("input") is not None:
                captured_payload["input"] = kwargs["input"]
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.set_issue_type("42", "task", dry_run=False)

        assert result.status == "updated"
        assert any("page=1" in arg for arg in captured_calls[0])
        assert any("page=2" in arg for arg in captured_calls[1])
        payload = json.loads(str(captured_payload["input"]))
        assert "carry-over" in payload["labels"]
        assert "bug" not in payload["labels"]
        assert "task" in payload["labels"]

    def test_set_issue_type_patch_error_raises_runtimeerror(self):
        responses = [
            json.dumps([{"name": "bug"}]),  # GET existing labels
            "",  # PATCH issue response body (ignored on failure)
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            if call_idx["i"] == 2:  # PATCH call
                return subprocess.CompletedProcess(args=args[0], returncode=1, stdout=resp, stderr="permission denied")
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(RuntimeError, match="Failed to set issue type label"):
            provider.set_issue_type("42", "task", dry_run=False)

    def test_set_issue_type_subtask_maps_to_label(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.set_issue_type("42", "subtask", dry_run=True)
        assert result.status == "dry-run"
        assert result.metadata["label"] == "subtask"
        assert result.metadata["issue_type"] == "subtask"

    def test_set_issue_type_sub_task_hyphenated_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(IssueTypeMappingError, match="sub-task"):
            provider.set_issue_type("42", "sub-task", dry_run=False)

    def test_set_issue_type_unknown_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(IssueTypeMappingError, match="no GitHub label mapping"):
            provider.set_issue_type("42", "story", dry_run=False)

    def test_set_issue_type_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.set_issue_type("42", "bug", dry_run=True)
        assert result.status == "dry-run"
        assert result.metadata["issue_type"] == "bug"

    def test_set_issue_type_empty_identifier_raises_before_dry_run(self):
        """An empty identifier is rejected before any dry-run handling or provider call."""
        calls: list[list[str]] = []

        def recording_run(args, **kwargs):
            calls.append(list(args))
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=recording_run)
        with pytest.raises(ValueError, match="identifier must be a non-empty string"):
            provider.set_issue_type("", "bug", dry_run=True)
        with pytest.raises(ValueError, match="identifier must be a non-empty string"):
            provider.set_issue_type("   ", "bug", dry_run=False)
        assert calls == []

    def test_set_issue_type_rejects_non_numeric_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="numeric GitHub issue number"):
            provider.set_issue_type("1/comments", "bug", dry_run=False)

    def test_set_issue_type_404_raises_value_error(self):
        """set_issue_type raises ValueError when the issue is not found (HTTP 404)."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="gh: Not Found (HTTP 404)", returncode=1),
        )
        with pytest.raises(ValueError, match="not found"):
            provider.set_issue_type("999", "bug", dry_run=False)
