"""Tests for agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter."""

from __future__ import annotations

import json
import subprocess
from typing import Any
from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.github_adapter import GitHubIssuesAdapter
from agentic_devtools.adapters.types import IssueDetailWithRaw


def _mock_run(stdout: str = "", stderr: str = "", returncode: int = 0) -> MagicMock:
    """Build a mock run_command callable returning a CompletedProcess."""
    mock = MagicMock()
    mock.return_value = subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)
    return mock


class TestGitHubIssuesAdapter:
    """Tests for the GitHubIssuesAdapter concrete implementation."""

    def test_create_issue_parses_url(self) -> None:
        """create_issue extracts issue ID from the URL returned by gh."""
        run = _mock_run(stdout="https://github.com/owner/repo/issues/42\n")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        result = adapter.create_issue("My title", "My body")

        assert result["issue_id"] == "42"
        assert result["url"] == "https://github.com/owner/repo/issues/42"
        args = run.call_args[0][0]
        assert args[:4] == ["gh", "issue", "create", "--repo"]

    def test_create_issue_with_labels(self) -> None:
        """create_issue adds --label flags for each label."""
        run = _mock_run(stdout="https://github.com/owner/repo/issues/1\n")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        adapter.create_issue("Title", "Body", labels=["bug", "urgent"])

        args = run.call_args[0][0]
        assert "--label" in args
        label_indices = [i for i, a in enumerate(args) if a == "--label"]
        label_values = [args[i + 1] for i in label_indices]
        assert label_values == ["bug", "urgent"]

    def test_create_issue_without_labels(self) -> None:
        """create_issue omits --label when labels is None."""
        run = _mock_run(stdout="https://github.com/owner/repo/issues/1\n")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        adapter.create_issue("Title", "Body")

        args = run.call_args[0][0]
        assert "--label" not in args

    def test_get_issue_parses_json(self) -> None:
        """get_issue parses gh JSON output into IssueDetail."""
        data = {
            "number": 42,
            "title": "Test issue",
            "body": "Description",
            "state": "OPEN",
            "labels": [{"name": "bug"}],
            "url": "https://github.com/owner/repo/issues/42",
            "comments": [
                {"id": "c1", "body": "A comment", "createdAt": "2026-01-01T00:00:00Z"},
            ],
        }
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        detail = adapter.get_issue("42")

        assert detail["issue_id"] == "42"
        assert detail["title"] == "Test issue"
        assert detail["description"] == "Description"
        assert detail["status"] == "OPEN"
        assert detail["labels"] == ["bug"]
        assert len(detail["comments"]) == 1
        assert detail["comments"][0]["body"] == "A comment"

    def test_get_issue_handles_string_labels(self) -> None:
        """get_issue handles labels as plain strings (not dicts)."""
        data = {
            "number": 1,
            "title": "T",
            "body": "",
            "state": "OPEN",
            "labels": ["bug"],
            "url": "",
            "comments": [],
        }
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        detail = adapter.get_issue("1")
        assert detail["labels"] == ["bug"]

    def test_add_comment_returns_empty_id(self) -> None:
        """add_comment returns empty comment_id since gh doesn't provide one."""
        run = _mock_run(stdout="")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        result = adapter.add_comment("42", "Hello")

        assert result["comment_id"] == ""
        args = run.call_args[0][0]
        assert "comment" in args
        assert "--body" in args

    def test_list_issues_no_filters(self) -> None:
        """list_issues returns summaries without filters."""
        data = [
            {"number": 1, "title": "A", "state": "OPEN", "labels": [{"name": "bug"}], "url": "u1"},
            {"number": 2, "title": "B", "state": "CLOSED", "labels": [], "url": "u2"},
        ]
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        summaries = adapter.list_issues()

        assert len(summaries) == 2
        assert summaries[0]["issue_id"] == "1"
        assert summaries[1]["title"] == "B"

    def test_list_issues_with_labels_filter(self) -> None:
        """list_issues passes --label flags from filters."""
        run = _mock_run(stdout="[]")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        adapter.list_issues(filters={"labels": ["bug", "feature"]})

        args = run.call_args[0][0]
        label_indices = [i for i, a in enumerate(args) if a == "--label"]
        label_values = [args[i + 1] for i in label_indices]
        assert label_values == ["bug", "feature"]

    def test_list_issues_with_state_filter(self) -> None:
        """list_issues passes --state flag from filters."""
        run = _mock_run(stdout="[]")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        adapter.list_issues(filters={"state": "open"})

        args = run.call_args[0][0]
        state_idx = args.index("--state")
        assert args[state_idx + 1] == "open"

    def test_list_issues_with_assignee_filter(self) -> None:
        """list_issues passes --assignee flag from filters."""
        run = _mock_run(stdout="[]")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        adapter.list_issues(filters={"assignee": "octocat"})

        args = run.call_args[0][0]
        idx = args.index("--assignee")
        assert args[idx + 1] == "octocat"

    def test_subprocess_failure_raises_runtime_error(self) -> None:
        """Non-zero returncode raises RuntimeError."""
        run = _mock_run(returncode=1, stderr="not authenticated")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        with pytest.raises(RuntimeError, match="gh command failed"):
            adapter.create_issue("T", "D")

    def test_json_parse_failure_raises_runtime_error(self) -> None:
        """Invalid JSON from gh raises RuntimeError."""
        run = _mock_run(stdout="not json")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        with pytest.raises(RuntimeError, match="Failed to parse gh output"):
            adapter.get_issue("1")

    def test_get_issue_non_dict_json_raises_runtime_error(self) -> None:
        """get_issue raises when gh returns a JSON list instead of dict."""
        run = _mock_run(stdout="[1,2,3]")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        with pytest.raises(RuntimeError, match="expected dict"):
            adapter.get_issue("1")

    def test_list_issues_non_list_json_raises_runtime_error(self) -> None:
        """list_issues raises when gh returns a JSON dict instead of list."""
        run = _mock_run(stdout='{"not": "list"}')
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        with pytest.raises(RuntimeError, match="expected list"):
            adapter.list_issues()

    def test_list_issues_non_dict_item_raises_runtime_error(self) -> None:
        """list_issues raises when an item in the list is not a dict."""
        run = _mock_run(stdout='[{"number": 1, "title": "A", "state": "OPEN", "labels": [], "url": "u"}, "bad"]')
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        with pytest.raises(RuntimeError, match="expected each issue to be a dict.*index 1"):
            adapter.list_issues()

    def test_create_issue_empty_url(self) -> None:
        """create_issue handles empty stdout gracefully."""
        run = _mock_run(stdout="")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)

        result = adapter.create_issue("T", "D")
        assert result["issue_id"] == ""
        assert result["url"] == ""

    def test_shell_false_always_passed(self) -> None:
        """Verify shell=False is always passed to run_command."""
        run = _mock_run(stdout="https://github.com/o/r/issues/1\n")
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=run)

        adapter.create_issue("T", "D")
        assert run.call_args[1]["shell"] is False

    def test_get_issue_null_labels_and_comments(self) -> None:
        """get_issue handles null labels and comments gracefully."""
        data = {
            "number": 1,
            "title": "T",
            "body": "D",
            "state": "OPEN",
            "labels": None,
            "url": "u",
            "comments": None,
        }
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=run)

        detail = adapter.get_issue("1")
        assert detail["labels"] == []
        assert detail["comments"] == []

    def test_get_issue_non_list_comments_raises(self) -> None:
        """get_issue raises RuntimeError when comments is not a list."""
        data = {
            "number": 1,
            "title": "T",
            "body": "D",
            "state": "OPEN",
            "labels": [],
            "url": "u",
            "comments": "not-a-list",
        }
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=run)

        with pytest.raises(RuntimeError, match="expected comments to be a list"):
            adapter.get_issue("1")

    def test_get_issue_non_dict_comment_entry_raises(self) -> None:
        """get_issue raises RuntimeError when a comment entry is not a dict."""
        data = {
            "number": 1,
            "title": "T",
            "body": "D",
            "state": "OPEN",
            "labels": [],
            "url": "u",
            "comments": [{"id": "c1", "body": "ok", "createdAt": ""}, "bad"],
        }
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=run)

        with pytest.raises(RuntimeError, match="expected each comment to be a dict.*index 1"):
            adapter.get_issue("1")

    def test_get_issue_null_comment_fields_coerced_to_empty(self) -> None:
        """get_issue coerces null id/body/createdAt in a comment to empty string."""
        data = {
            "number": 1,
            "title": "T",
            "body": "D",
            "state": "OPEN",
            "labels": [],
            "url": "u",
            "comments": [{"id": None, "body": None, "createdAt": None}],
        }
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=run)

        detail = adapter.get_issue("1")
        assert len(detail["comments"]) == 1
        comment = detail["comments"][0]
        assert comment["comment_id"] == ""
        assert comment["body"] == ""
        assert comment["created_at"] == ""

    def test_get_issue_non_list_labels_normalised_to_empty(self) -> None:
        """get_issue normalises non-list labels to empty list."""
        data = {
            "number": 1,
            "title": "T",
            "body": "D",
            "state": "OPEN",
            "labels": "not-a-list",
            "url": "u",
            "comments": [],
        }
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=run)

        detail = adapter.get_issue("1")
        assert detail["labels"] == []

    def test_list_issues_non_list_labels_normalised_to_empty(self) -> None:
        """list_issues normalises non-list labels within items to empty list."""
        data = [
            {"number": 1, "title": "A", "state": "OPEN", "labels": {"unexpected": True}, "url": "u"},
        ]
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=run)

        summaries = adapter.list_issues()
        assert summaries[0]["labels"] == []

    def test_repo_args_non_empty(self) -> None:
        """_repo_args returns ['--repo', slug] when repo is set."""
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=_mock_run())
        assert adapter._repo_args() == ["--repo", "owner/repo"]

    def test_repo_args_empty(self) -> None:
        """_repo_args returns [] when repo is empty."""
        adapter = GitHubIssuesAdapter(repo="", run_command=_mock_run())
        assert adapter._repo_args() == []

    def test_create_issue_omits_repo_flag_when_empty(self) -> None:
        """create_issue omits --repo when repo slug is empty."""
        run = _mock_run(stdout="https://github.com/owner/repo/issues/1\n")
        adapter = GitHubIssuesAdapter(repo="", run_command=run)

        adapter.create_issue("T", "D")

        args = run.call_args[0][0]
        assert "--repo" not in args
        assert args[:3] == ["gh", "issue", "create"]

    def test_get_issue_omits_repo_flag_when_empty(self) -> None:
        """get_issue omits --repo when repo slug is empty."""
        data = {"number": 1, "title": "T", "body": "", "state": "OPEN", "labels": [], "url": "", "comments": []}
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="", run_command=run)

        adapter.get_issue("1")

        args = run.call_args[0][0]
        assert "--repo" not in args

    def test_add_comment_omits_repo_flag_when_empty(self) -> None:
        """add_comment omits --repo when repo slug is empty."""
        run = _mock_run(stdout="")
        adapter = GitHubIssuesAdapter(repo="", run_command=run)

        adapter.add_comment("1", "Hello")

        args = run.call_args[0][0]
        assert "--repo" not in args

    def test_list_issues_omits_repo_flag_when_empty(self) -> None:
        """list_issues omits --repo when repo slug is empty."""
        run = _mock_run(stdout="[]")
        adapter = GitHubIssuesAdapter(repo="", run_command=run)

        adapter.list_issues()

        args = run.call_args[0][0]
        assert "--repo" not in args

    def test_normalize_standard_issue_all_fields_populated(self) -> None:
        """normalize() maps all fields correctly for a standard issue."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "42",
            "title": "Fix bug",
            "description": "Description",
            "status": "OPEN",
            "labels": ["type:bug", "priority:high"],
            "url": "https://github.com/o/r/issues/42",
            "comments": [{"comment_id": "c1", "body": "A comment", "created_at": "2026-01-01"}],
            "raw": {
                "createdAt": "2026-01-01T00:00:00Z",
                "updatedAt": "2026-02-01T00:00:00Z",
                "assignees": [{"login": "alice"}],
            },
        }
        result = adapter.normalize(detail)

        assert result.issue_id == "42"
        assert result.title == "Fix bug"
        assert result.description == "Description"
        assert result.status == "open"
        assert result.labels == ["type:bug", "priority:high"]
        assert result.url == "https://github.com/o/r/issues/42"
        assert result.provider == "github"
        assert result.created_at == "2026-01-01T00:00:00Z"
        assert result.updated_at == "2026-02-01T00:00:00Z"
        assert len(result.comments) == 1
        assert result.raw == detail["raw"]

    def test_normalize_provider_is_github(self) -> None:
        """normalize() always returns provider='github'."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        assert adapter.normalize(detail).provider == "github"

    def test_normalize_required_fields_pass_through(self) -> None:
        """normalize() maps identity fields verbatim."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "99",
            "title": "My Title",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/99",
            "comments": [],
            "raw": {},
        }
        result = adapter.normalize(detail)
        assert result.issue_id == "99"
        assert result.title == "My Title"
        assert result.url == "https://github.com/o/r/issues/99"

    def test_normalize_status_lowercased(self) -> None:
        """normalize() lowercases the status field."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "OPEN",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        assert adapter.normalize(detail).status == "open"

    def test_normalize_created_at_from_raw(self) -> None:
        """normalize() extracts created_at from raw dict."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {"createdAt": "2026-05-01T00:00:00Z"},
        }
        assert adapter.normalize(detail).created_at == "2026-05-01T00:00:00Z"

    def test_normalize_updated_at_from_raw(self) -> None:
        """normalize() extracts updated_at from raw dict."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {"updatedAt": "2026-06-01T00:00:00Z"},
        }
        assert adapter.normalize(detail).updated_at == "2026-06-01T00:00:00Z"

    def test_normalize_raw_passthrough_verbatim(self) -> None:
        """normalize() passes raw dict through unchanged."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        raw_data = {"createdAt": "2026-05-01T00:00:00Z", "extra": "data"}
        detail: IssueDetailWithRaw = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": raw_data,
        }
        result = adapter.normalize(detail)
        assert result.raw == raw_data

    def test_normalize_description_none_becomes_empty(self) -> None:
        """normalize() coerces None description to empty string."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": None,
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        assert adapter.normalize(detail).description == ""

    def test_normalize_description_non_string_coerced_to_string(self) -> None:
        """normalize() coerces non-string descriptions to string."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": {"nested": "value"},
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        assert adapter.normalize(detail).description == "{'nested': 'value'}"

    def test_normalize_status_none_becomes_unknown(self) -> None:
        """normalize() coerces None status to 'unknown'."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": None,
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        assert adapter.normalize(detail).status == "unknown"

    def test_normalize_status_empty_string_becomes_unknown(self) -> None:
        """normalize() coerces empty status to 'unknown'."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        assert adapter.normalize(detail).status == "unknown"

    def test_normalize_status_whitespace_becomes_unknown(self) -> None:
        """normalize() coerces whitespace-only status to 'unknown'."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "   ",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        assert adapter.normalize(detail).status == "unknown"

    def test_normalize_labels_none_becomes_empty_list(self) -> None:
        """normalize() coerces None labels to empty list."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": None,
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        assert adapter.normalize(detail).labels == []

    def test_normalize_labels_non_list_becomes_empty_list(self) -> None:
        """normalize() coerces non-list labels to empty list."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": "not-a-list",
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        assert adapter.normalize(detail).labels == []

    def test_normalize_labels_coerces_items_and_skips_none(self) -> None:
        """normalize() coerces label items to string and skips None values."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": ["bug", None, 7, {"name": "docs"}],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        assert adapter.normalize(detail).labels == ["bug", "7", "{'name': 'docs'}"]

    def test_normalize_comments_none_becomes_empty_list(self) -> None:
        """normalize() coerces None comments to empty list."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": None,
            "raw": {},
        }
        assert adapter.normalize(detail).comments == []

    def test_normalize_comments_non_list_becomes_empty_list(self) -> None:
        """normalize() coerces non-list comments to empty list."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": "not-a-list",
            "raw": {},
        }
        assert adapter.normalize(detail).comments == []

    def test_normalize_comments_non_dict_entries_silently_skipped(self) -> None:
        """normalize() skips non-dict comment entries without raising."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [
                {"comment_id": "c1", "body": "valid", "created_at": "2026-01-01"},
                "string-entry",
                42,
                None,
            ],
            "raw": {},
        }
        result = adapter.normalize(detail)
        assert len(result.comments) == 1
        assert result.comments[0]["comment_id"] == "c1"
        assert result.comments[0]["body"] == "valid"

    def test_normalize_comments_null_fields_coerced_to_empty(self) -> None:
        """normalize() coerces None comment_id/body/created_at to empty string."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [{"comment_id": None, "body": None, "created_at": None}],
            "raw": {},
        }
        result = adapter.normalize(detail)
        assert len(result.comments) == 1
        assert result.comments[0]["comment_id"] == ""
        assert result.comments[0]["body"] == ""
        assert result.comments[0]["created_at"] == ""

    def test_normalize_raw_none_becomes_empty_dict(self) -> None:
        """normalize() coerces None raw to empty dict."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": None,
        }
        assert adapter.normalize(detail).raw == {}

    def test_normalize_raw_absent_becomes_empty_dict(self) -> None:
        """normalize() coerces absent raw to empty dict."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
        }
        assert adapter.normalize(detail).raw == {}

    def test_normalize_created_at_missing_raw(self) -> None:
        """normalize() returns empty string when raw lacks createdAt."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        assert adapter.normalize(detail).created_at == ""

    def test_normalize_missing_issue_id_raises_keyerror(self) -> None:
        """normalize() raises KeyError when issue_id is missing."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        with pytest.raises(KeyError):
            adapter.normalize(detail)  # type: ignore[arg-type]

    def test_normalize_missing_title_raises_keyerror(self) -> None:
        """normalize() raises KeyError when title is missing."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        with pytest.raises(KeyError):
            adapter.normalize(detail)  # type: ignore[arg-type]

    def test_normalize_missing_url_raises_keyerror(self) -> None:
        """normalize() raises KeyError when url is missing."""
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: Any = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "comments": [],
            "raw": {},
        }
        with pytest.raises(KeyError):
            adapter.normalize(detail)  # type: ignore[arg-type]

    def test_normalize_empty_issue_id_raises_adaptervalidationerror(self) -> None:
        """normalize() raises AdapterValidationError for empty issue_id."""
        from agentic_devtools.adapters.exceptions import AdapterValidationError

        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        with pytest.raises(AdapterValidationError):
            adapter.normalize(detail)

    def test_normalize_empty_title_raises_adaptervalidationerror(self) -> None:
        """normalize() raises AdapterValidationError for empty title."""
        from agentic_devtools.adapters.exceptions import AdapterValidationError

        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "1",
            "title": "",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "https://github.com/o/r/issues/1",
            "comments": [],
            "raw": {},
        }
        with pytest.raises(AdapterValidationError):
            adapter.normalize(detail)

    def test_normalize_empty_url_raises_adaptervalidationerror(self) -> None:
        """normalize() raises AdapterValidationError for empty url."""
        from agentic_devtools.adapters.exceptions import AdapterValidationError

        adapter = GitHubIssuesAdapter(repo="o/r", run_command=_mock_run())
        detail: IssueDetailWithRaw = {
            "issue_id": "1",
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "url": "",
            "comments": [],
            "raw": {},
        }
        with pytest.raises(AdapterValidationError):
            adapter.normalize(detail)


class TestExtractFirstLabelValue:
    """Tests for GitHubIssuesAdapter._extract_first_label_value."""

    def test_label_type_extraction(self) -> None:
        """Extracts value after 'type:' prefix from labels."""
        result = GitHubIssuesAdapter._extract_first_label_value(["type:bug", "priority:high"], "type:")
        assert result == "bug"

    def test_label_priority_extraction(self) -> None:
        """Extracts value after 'priority:' prefix from labels."""
        result = GitHubIssuesAdapter._extract_first_label_value(["type:bug", "priority:high"], "priority:")
        assert result == "high"

    def test_no_matching_labels_returns_empty_string(self) -> None:
        """Returns empty string when no label matches the prefix."""
        result = GitHubIssuesAdapter._extract_first_label_value(["enhancement", "docs"], "type:")
        assert result == ""

    def test_multiple_type_labels_first_wins(self) -> None:
        """First matching label wins when multiple match."""
        result = GitHubIssuesAdapter._extract_first_label_value(["type:bug", "type:task"], "type:")
        assert result == "bug"

    def test_label_case_sensitive(self) -> None:
        """Prefix matching is case-sensitive: 'Type:bug' does NOT match 'type:'."""
        result = GitHubIssuesAdapter._extract_first_label_value(["Type:bug"], "type:")
        assert result == ""

    def test_empty_labels_list(self) -> None:
        """Returns empty string for empty labels list."""
        result = GitHubIssuesAdapter._extract_first_label_value([], "type:")
        assert result == ""


class TestExtractAssignees:
    """Tests for GitHubIssuesAdapter._extract_assignees."""

    def test_assignees_extraction(self) -> None:
        """Extracts login strings from valid assignee dicts."""
        raw = {"assignees": [{"login": "alice"}, {"login": "bob"}]}
        assert GitHubIssuesAdapter._extract_assignees(raw) == ["alice", "bob"]

    def test_assignees_missing_raw(self) -> None:
        """Returns empty list when raw has no assignees key."""
        assert GitHubIssuesAdapter._extract_assignees({}) == []

    def test_assignees_none_value(self) -> None:
        """Returns empty list when assignees is None."""
        assert GitHubIssuesAdapter._extract_assignees({"assignees": None}) == []

    def test_assignees_malformed_entries_skipped(self) -> None:
        """Skips non-dict, missing login, None login, and non-string login."""
        raw = {
            "assignees": [
                {"login": "alice"},
                "not-a-dict",
                {"no_login_key": True},
                {"login": None},
                {"login": 42},
            ]
        }
        assert GitHubIssuesAdapter._extract_assignees(raw) == ["alice"]

    def test_assignees_empty_login_skipped(self) -> None:
        """Skips assignees with empty string login."""
        raw = {"assignees": [{"login": ""}, {"login": "bob"}]}
        assert GitHubIssuesAdapter._extract_assignees(raw) == ["bob"]


class TestGetIssueRaw:
    """Tests for get_issue() raw field extension."""

    def test_get_issue_raw_populated_when_keys_present(self) -> None:
        """get_issue includes createdAt, updatedAt, assignees in raw when present."""
        data = {
            "number": 1,
            "title": "T",
            "body": "D",
            "state": "OPEN",
            "labels": [],
            "url": "u",
            "comments": [],
            "createdAt": "2026-01-01T00:00:00Z",
            "updatedAt": "2026-02-01T00:00:00Z",
            "assignees": [{"login": "alice"}],
        }
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=run)

        detail = adapter.get_issue("1")
        assert detail["raw"]["createdAt"] == "2026-01-01T00:00:00Z"
        assert detail["raw"]["updatedAt"] == "2026-02-01T00:00:00Z"
        assert detail["raw"]["assignees"] == [{"login": "alice"}]

    def test_get_issue_raw_omits_missing_keys(self) -> None:
        """get_issue raw dict omits keys not present in GitHub response."""
        data = {
            "number": 1,
            "title": "T",
            "body": "D",
            "state": "OPEN",
            "labels": [],
            "url": "u",
            "comments": [],
        }
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=run)

        detail = adapter.get_issue("1")
        assert "createdAt" not in detail["raw"]
        assert "updatedAt" not in detail["raw"]
        assert "assignees" not in detail["raw"]

    def test_get_issue_raw_always_returned(self) -> None:
        """get_issue always includes raw dict in the result."""
        data = {
            "number": 1,
            "title": "T",
            "body": "D",
            "state": "OPEN",
            "labels": [],
            "url": "u",
            "comments": [],
        }
        run = _mock_run(stdout=json.dumps(data))
        adapter = GitHubIssuesAdapter(repo="o/r", run_command=run)

        detail = adapter.get_issue("1")
        assert "raw" in detail
        assert isinstance(detail["raw"], dict)
