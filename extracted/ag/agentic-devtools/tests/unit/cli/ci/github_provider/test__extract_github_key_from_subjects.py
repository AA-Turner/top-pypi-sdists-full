"""Tests for GitHubActionsProvider._extract_github_key_from_subjects."""

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

_extract = GitHubActionsProvider._extract_github_key_from_subjects


class TestExtractGithubKeyFromSubjects:
    """Tests for extracting a GitHub issue number from commit subject lines."""

    def test_conventional_scope_returns_key(self) -> None:
        assert _extract(["fix(#2249): squash commit bug"]) == "2249"

    def test_first_matching_subject_wins(self) -> None:
        assert _extract(["fix(#42): first", "feat(#99): second"]) == "42"

    def test_bare_hash_reference_in_body(self) -> None:
        assert _extract(["chore: update deps\n\n#123"]) == "123"

    def test_no_hash_reference_returns_none(self) -> None:
        assert _extract(["feat: add feature", "chore: clean up"]) is None

    def test_empty_list_returns_none(self) -> None:
        assert _extract([]) is None

    def test_blank_subjects_returns_none(self) -> None:
        assert _extract(["", "  "]) is None

    def test_jira_key_without_hash_is_not_matched(self) -> None:
        # Jira-style subjects like ``feat(PROJECT-1234): …`` have no ``#``.
        assert _extract(["feat(PROJECT-1234): add thing"]) is None

    @pytest.mark.parametrize(
        ("subjects", "expected"),
        [
            (["chore(#1): x", "fix(#2): y"], "1"),
            (["no issue here", "fix(#777): found"], "777"),
            (["fix(#0): zero-issue"], "0"),
        ],
    )
    def test_parametrized(self, subjects: list[str], expected: str) -> None:
        assert _extract(subjects) == expected
