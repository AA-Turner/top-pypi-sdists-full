"""Tests for GitHubProvider."""

from __future__ import annotations

import json
import subprocess

import pytest

from agentic_devtools.adapters.exceptions import (
    AdapterValidationError,
)
from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.github_provider._fixtures import _link_run_mock, _make_run_mock


class TestGitHubProviderLinkSubissue:
    """Tests for GitHubProvider.link_subissue."""

    def test_link_subissue_returns_already_linked(self):
        calls: list[list[str]] = []

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            calls.append(argv)
            if any(argument.endswith("/sub_issues") for argument in argv):
                stdout = json.dumps([{"id": 420}])
            else:
                stdout = json.dumps({"id": 420, "node_id": "I_x", "html_url": "u"})
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=stdout, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.link_subissue("1", "42", dry_run=False)

        assert result.status == "already-linked"
        assert result.source_id == "1"
        assert result.target_id == "42"
        assert len(calls) == 2

    def test_link_subissue_success(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_link_run_mock(resolve_id=123456))
        result = provider.link_subissue("1", "42", dry_run=False)
        assert result.status == "linked"
        assert result.source_id == "1"
        assert result.target_id == "42"

    def test_link_subissue_sends_resolved_database_id_in_payload(self):
        captured: dict[str, object] = {}

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                captured["input"] = kwargs.get("input")
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="{}", stderr="")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(
                args=argv,
                returncode=0,
                stdout=json.dumps({"id": 987654, "node_id": "I_x", "html_url": "u"}),
                stderr="",
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        provider.link_subissue("1", "42", dry_run=False)
        assert json.loads(captured["input"]) == {"sub_issue_id": 987654}

    def test_link_subissue_child_without_database_id_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_link_run_mock(resolve_id=0))
        with pytest.raises(RuntimeError, match="valid positive integer database ID"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_child_non_integer_database_id_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_link_run_mock(resolve_id="not-an-int"))
        with pytest.raises(RuntimeError, match="valid positive integer database ID"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_empty_parent_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="parent_id must be a non-empty string"):
            provider.link_subissue("  ", "42", dry_run=False)

    def test_link_subissue_empty_child_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="child_id must be a non-empty string"):
            provider.link_subissue("1", "  ", dry_run=False)

    def test_link_subissue_non_numeric_parent_raises(self):
        """link_subissue raises ValueError for a non-numeric parent_id."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="parent_id must be a numeric GitHub issue number"):
            provider.link_subissue("not-a-number", "42", dry_run=False)

    def test_link_subissue_non_numeric_child_raises(self):
        """link_subissue raises ValueError for a non-numeric child_id."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="child_id must be a numeric GitHub issue number"):
            provider.link_subissue("1", "not-a-number", dry_run=False)

    def test_link_subissue_dry_run_rejects_path_fragment_parent(self):
        """link_subissue dry-run rejects path-traversal-style parent_id."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="parent_id must be a numeric GitHub issue number"):
            provider.link_subissue("1/comments", "42", dry_run=True)

    def test_link_subissue_dry_run_rejects_path_fragment_child(self):
        """link_subissue dry-run rejects path-traversal-style child_id."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="child_id must be a numeric GitHub issue number"):
            provider.link_subissue("1", "42/labels", dry_run=True)

    def test_link_subissue_api_not_enabled(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_link_run_mock(post_returncode=1, post_stdout="", post_stderr="404 Not Found"),
        )
        with pytest.raises(RuntimeError, match="Sub-issues API not available"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.link_subissue("1", "123456", dry_run=True)
        assert result.status == "dry-run"
        assert result.source_id == "1"
        assert result.target_id == "123456"

    def test_link_subissue_transient_error(self, monkeypatch):
        """link_subissue raises TransientError on 502."""
        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *a, **k: None)
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_link_run_mock(post_returncode=1, post_stdout="", post_stderr="HTTP 502 bad gateway"),
        )
        with pytest.raises(TransientError):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_generic_error(self):
        """link_subissue raises RuntimeError on non-transient, non-404/422 failure."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_link_run_mock(post_returncode=1, post_stdout="", post_stderr="internal error"),
        )
        with pytest.raises(RuntimeError, match="Failed to link sub-issue"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_child_not_found_raises_value_error(self):
        """link_subissue raises ValueError when the child issue is not found (404)."""

        def mock_run(*args, **kwargs):
            argv = args[0]
            # Simulate 404 for child resolution (GET /issues/{n})
            return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="gh: Not Found (HTTP 404)")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(ValueError, match="not found"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_parent_not_found_raises_value_error(self):
        """link_subissue raises ValueError when the parent issue is not found (404)."""
        resolve_response = json.dumps({"id": 420, "node_id": "I_kwDO42", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            # Child resolve succeeds; parent sub_issues GET returns 404
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(
                    args=argv, returncode=1, stdout="", stderr="gh: Not Found (HTTP 404)"
                )
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(ValueError, match="Parent issue.*not found"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_parent_non_404_error_propagates_as_runtime_error(self):
        """link_subissue re-raises non-404 RuntimeError from _find_existing_sub_issue."""
        resolve_response = json.dumps({"id": 420, "node_id": "I_kwDO42", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            # Child resolve succeeds; parent sub_issues GET returns a non-404 error
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="internal server error")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider.link_subissue("1", "42", dry_run=False)


class TestGitHubProviderHierarchyValidation:
    """Provider-contract hierarchy validation (FR-001, FR-016)."""

    def _provider(self):
        def mock_run(*args, **kwargs):
            return subprocess.CompletedProcess(args=list(args[0]), returncode=0, stdout="{}", stderr="")

        return GitHubProvider(owner_repo="org/repo", run_command=mock_run)

    def test_validate_issue_type_accepts_supported_types(self):
        provider = self._provider()
        for issue_type in ("epic", "feature", "task", "bug", "subtask"):
            assert provider.validate_issue_type(issue_type) is None

    def test_validate_issue_type_is_case_insensitive(self):
        provider = self._provider()
        assert provider.validate_issue_type("Epic") is None

    def test_validate_issue_type_rejects_unsupported_type(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_issue_type("saga")

    def test_validate_issue_type_rejects_empty_string(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_issue_type("   ")

    def test_validate_issue_type_rejects_non_string(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_issue_type(None)  # type: ignore[arg-type]

    def test_validate_hierarchy_pair_accepts_valid_pairs(self):
        provider = self._provider()
        assert provider.validate_hierarchy_pair("feature", "epic") is None
        assert provider.validate_hierarchy_pair("subtask", "feature") is None

    def test_validate_hierarchy_pair_rejects_same_level(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_hierarchy_pair("feature", "feature")

    def test_validate_hierarchy_pair_rejects_inverted_pair(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_hierarchy_pair("epic", "feature")

    def test_validate_hierarchy_pair_rejects_unsupported_type(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_hierarchy_pair("saga", "epic")

    def test_provider_is_hierarchy_validation_capable(self):
        from agentic_devtools.adapters.issue_provider import HierarchyValidationProvider

        assert isinstance(self._provider(), HierarchyValidationProvider)


class TestGitHubProviderContractGaps:
    """GitHub-specific gap tests complementing the shared contract suite."""

    def test_link_subissue_passes_integer_sub_issue_id_in_payload(self):
        """link_subissue sends the resolved integer database ID as sub_issue_id (T014)."""
        captured: dict[str, object] = {}

        def capturing_run(args, **kwargs):
            argv = list(args)
            if "--method" in argv and "POST" in argv:
                captured["input"] = kwargs.get("input")
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=json.dumps({}), stderr="")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(
                args=argv, returncode=0, stdout=json.dumps({"id": 456, "node_id": "I_x", "html_url": "u"}), stderr=""
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=capturing_run)
        provider.link_subissue("1", "42", dry_run=False)
        payload = json.loads(captured["input"])
        assert payload == {"sub_issue_id": 456}
        assert isinstance(payload["sub_issue_id"], int)

    def test_link_subissue_uses_parent_number_in_path(self):
        """link_subissue targets the parent number in the sub_issues path (T014)."""
        captured: dict[str, object] = {}

        def capturing_run(args, **kwargs):
            argv = list(args)
            if "--method" in argv and "POST" in argv:
                captured["args"] = argv
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=json.dumps({}), stderr="")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(
                args=argv, returncode=0, stdout=json.dumps({"id": 22, "node_id": "I_x", "html_url": "u"}), stderr=""
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=capturing_run)
        provider.link_subissue("11", "22", dry_run=False)
        assert "/repos/org/repo/issues/11/sub_issues" in captured["args"]


class TestGitHubProviderHelpers:
    """Tests for internal helper methods."""

    def test_find_existing_sub_issue_non_matching_id_returns_false(self):
        """_find_existing_sub_issue returns False when listed items have a different id."""
        # Sub-issues list has one item with id=9999, not matching child_db_id=1234
        sub_issues_response = json.dumps([{"id": 9999, "number": 99, "node_id": "I_other"}])
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=sub_issues_response))
        assert provider._find_existing_sub_issue("1", 1234) is False

    def test_find_existing_sub_issue_non_list_response_raises(self):
        """A malformed (non-list) sub_issues response is propagated instead of failing open."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps({"unexpected": "object"})),
        )
        with pytest.raises(RuntimeError, match="Expected sub-issues list response"):
            provider._find_existing_sub_issue("1", 1234)

    def test_find_existing_sub_issue_requests_max_page_size(self):
        captured: list[list[str]] = []

        def capturing_run(args, **kwargs):
            captured.append(args)
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=capturing_run)
        provider._find_existing_sub_issue("1", 1234)
        assert captured
        assert "--method" in captured[0]
        assert "GET" in captured[0]
        assert "-f" in captured[0]
        assert "per_page=100" in captured[0]
