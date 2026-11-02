"""Tests for GitHubActionsProvider._strip_trailing_sdk_footer_lines."""

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

_strip_footers = GitHubActionsProvider._strip_trailing_sdk_footer_lines


class TestStripTrailingSdkFooterLines:
    """Tests for stripping trailing SDK footers from message bodies."""

    def test_trims_trailing_blank_lines_without_footer(self) -> None:
        assert _strip_footers("- detail\n\n") == "- detail"

    def test_strips_footer_with_trailing_blanks(self) -> None:
        assert _strip_footers("- detail\n\n#2202\n\n") == "- detail"

    def test_strips_multiple_footer_lines_with_separating_blanks(self) -> None:
        body = "- detail\n\n#2202\n\nBREAKING CHANGE: migrated behavior\n\n"
        assert _strip_footers(body) == "- detail"
