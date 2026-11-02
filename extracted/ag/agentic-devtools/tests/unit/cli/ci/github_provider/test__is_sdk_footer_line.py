"""Tests for GitHubActionsProvider._is_sdk_footer_line."""

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

_is_footer = GitHubActionsProvider._is_sdk_footer_line


class TestIsSdkFooterLine:
    """Tests for SDK footer-line classification."""

    def test_blank_line_is_not_footer(self) -> None:
        assert _is_footer("   ") is False
