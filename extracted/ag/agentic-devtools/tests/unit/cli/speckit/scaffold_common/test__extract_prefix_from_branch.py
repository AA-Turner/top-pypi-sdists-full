"""Tests for ``_extract_prefix_from_branch``."""

from agentic_devtools.cli.speckit.scaffold_common import _extract_prefix_from_branch


class TestExtractPrefixFromBranch:
    """_extract_prefix_from_branch extracts numeric spec-dir prefix from branch names."""

    # Legacy <number>-description format
    def test_legacy_format_returns_prefix(self) -> None:
        assert _extract_prefix_from_branch("042-existing-feature") == "042"

    def test_legacy_format_multidigit_prefix(self) -> None:
        assert _extract_prefix_from_branch("1234-some-feature") == "1234"

    # Repository-standard type/ISSUE-KEY/description with numeric key
    def test_github_numeric_key(self) -> None:
        assert _extract_prefix_from_branch("fix/2249/squash-fix") == "2249"

    def test_github_numeric_key_feat_type(self) -> None:
        assert _extract_prefix_from_branch("feat/42/add-webhook") == "42"

    def test_github_numeric_key_no_description_segment(self) -> None:
        # type/number with no trailing segment is also valid
        assert _extract_prefix_from_branch("fix/2249") == "2249"

    # Repository-standard type/ISSUE-KEY/description with Jira-style key
    def test_jira_key_returns_numeric_portion(self) -> None:
        assert _extract_prefix_from_branch("feature/PROJECT-1234/add-webhook") == "1234"

    def test_jira_key_single_letter_project(self) -> None:
        assert _extract_prefix_from_branch("fix/A-99/squash-fix") == "99"

    def test_jira_key_mixed_case(self) -> None:
        assert _extract_prefix_from_branch("feat/Proj-5678/desc") == "5678"

    # Non-matching cases
    def test_plain_branch_name_returns_none(self) -> None:
        assert _extract_prefix_from_branch("main") is None

    def test_type_slash_text_description_returns_none(self) -> None:
        # type/text/description where text is not numeric and not Jira-style
        assert _extract_prefix_from_branch("copilot/repair-branch") is None

    def test_type_slash_jira_style_no_digits_returns_none(self) -> None:
        # Ensure partial Jira-like patterns without a trailing number don't match
        assert _extract_prefix_from_branch("fix/PROJECT/no-number") is None
