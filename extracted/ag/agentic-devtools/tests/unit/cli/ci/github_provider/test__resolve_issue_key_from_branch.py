"""Tests for GitHubActionsProvider._resolve_issue_key_from_branch."""

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

_resolve = GitHubActionsProvider._resolve_issue_key_from_branch


class TestResolveIssueKeyFromBranch:
    """Tests for extracting an issue key from a branch name."""

    def test_github_numeric_key_after_type_prefix(self) -> None:
        assert _resolve("fix/2249/squash-commit-message-convention") == "2249"

    def test_jira_key_after_type_prefix(self) -> None:
        assert _resolve("feature/PROJECT-1234/add-webhook") == "PROJECT-1234"

    def test_numeric_key_with_trailing_description(self) -> None:
        assert _resolve("fix/123-null-guard") == "123"

    def test_no_type_prefix_numeric(self) -> None:
        assert _resolve("2249-add-webhook") == "2249"

    def test_jira_key_with_trailing_description_in_segment(self) -> None:
        assert _resolve("feature/PROJECT-1234-add-webhook") == "PROJECT-1234"

    def test_empty_branch_returns_none(self) -> None:
        assert _resolve("") is None

    def test_only_slashes_returns_none(self) -> None:
        assert _resolve("///") is None

    def test_branch_without_issue_returns_none(self) -> None:
        assert _resolve("main") is None

    def test_branch_with_non_issue_segments_returns_none(self) -> None:
        assert _resolve("release/v2-migration") is None

    @pytest.mark.parametrize(
        ("branch", "expected"),
        [
            ("feat/42/x", "42"),
            ("chore/ABC-9/y", "ABC-9"),
            ("docs/100/update", "100"),
        ],
    )
    def test_parametrized(self, branch: str, expected: str) -> None:
        assert _resolve(branch) == expected
