"""Tests for GitHubActionsProvider._resolve_issue_type_from_branch."""

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

_resolve = GitHubActionsProvider._resolve_issue_type_from_branch


class TestResolveIssueTypeFromBranch:
    """Tests for mapping a branch type prefix to a Conventional Commit type."""

    @pytest.mark.parametrize(
        ("branch", "expected"),
        [
            ("fix/2249/x", "fix"),
            ("bugfix/2249/x", "fix"),
            ("hotfix/2249/x", "fix"),
            ("feat/42/x", "feat"),
            ("feature/42/x", "feat"),
            ("docs/42/x", "docs"),
            ("doc/42/x", "docs"),
            ("refactor/42/x", "refactor"),
            ("perf/42/x", "perf"),
            ("test/42/x", "test"),
            ("tests/42/x", "test"),
            ("build/42/x", "build"),
            ("ci/42/x", "ci"),
            ("chore/42/x", "chore"),
            ("revert/42/x", "revert"),
            ("style/42/x", "style"),
        ],
    )
    def test_known_prefixes(self, branch: str, expected: str) -> None:
        assert _resolve(branch) == expected

    def test_case_insensitive(self) -> None:
        assert _resolve("FIX/42/x") == "fix"

    def test_unknown_prefix_defaults_to_chore(self) -> None:
        assert _resolve("wip/42/x") == "chore"

    def test_empty_branch_defaults_to_chore(self) -> None:
        assert _resolve("") == "chore"

    def test_no_slash_unknown_defaults_to_chore(self) -> None:
        assert _resolve("main") == "chore"

    def test_no_slash_known_type(self) -> None:
        assert _resolve("fix") == "fix"
