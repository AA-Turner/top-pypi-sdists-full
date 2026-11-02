"""Tests for GitHubActionsProvider._build_squash_commit_message."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _provider() -> GitHubActionsProvider:
    return GitHubActionsProvider(repo="owner/repo")


class TestBuildSquashCommitMessage:
    """Tests for the deterministic last-resort squash message builder."""

    def test_no_subjects_no_key(self) -> None:
        result = _provider()._build_squash_commit_message("abc123def456", [])
        assert result == "chore: post-repair squash for abc123de"

    def test_no_subjects_with_key(self) -> None:
        result = _provider()._build_squash_commit_message("abc123def456", [], issue_key="2249")
        assert result == "chore(#2249): post-repair squash for abc123de\n\n#2249"

    @patch("agentic_devtools.cli.ci.github_provider.load_platform_config", return_value={"issue_adapter": "markdown"})
    def test_no_subjects_with_numeric_key_uses_markdown_adapter_convention(self, _mock_config) -> None:
        result = _provider()._build_squash_commit_message(
            "abc123def456",
            [],
            issue_key="2249",
            git_root=Path("/repo"),
        )
        assert result == "chore(2249): post-repair squash for abc123de\n\n2249"

    @patch("agentic_devtools.cli.ci.github_provider.load_platform_config", return_value={})
    def test_no_subjects_with_numeric_key_defaults_missing_adapter_to_github(self, _mock_config) -> None:
        result = _provider()._build_squash_commit_message(
            "abc123def456",
            [],
            issue_key="2249",
            git_root=Path("/repo"),
        )
        assert result == "chore(#2249): post-repair squash for abc123de\n\n#2249"

    @patch(
        "agentic_devtools.cli.ci.github_provider._derive_issue_link_from_key",
        return_value="https://jira.example.com/browse/PROJECT-1234",
    )
    def test_no_subjects_with_jira_key_uses_browse_link_when_available(self, _mock_derive) -> None:
        result = _provider()._build_squash_commit_message(
            "abc123def456",
            [],
            issue_key="PROJECT-1234",
            git_root=Path("/repo"),
        )
        assert (
            result
            == "chore(PROJECT-1234): post-repair squash for abc123de\n\n[PROJECT-1234](https://jira.example.com/browse/PROJECT-1234)"
        )

    @patch("agentic_devtools.cli.ci.github_provider.load_platform_config", return_value={"issue_adapter": "github"})
    def test_no_subjects_with_jira_key_uses_plain_footer_for_github_adapter(self, _mock_config) -> None:
        result = _provider()._build_squash_commit_message(
            "abc123def456",
            [],
            issue_key="PROJECT-1234",
            git_root=Path("/repo"),
        )
        assert result == "chore(PROJECT-1234): post-repair squash for abc123de\n\nPROJECT-1234"

    @patch("agentic_devtools.cli.ci.github_provider.load_platform_config", return_value={"issue_adapter": "markdown"})
    @patch(
        "agentic_devtools.cli.ci.github_provider._derive_issue_link_from_key",
        return_value="https://jira.example.com/browse/PROJECT-1234",
    )
    def test_no_subjects_with_jira_key_uses_plain_footer_for_markdown_adapter(
        self,
        _mock_derive,
        _mock_config,
    ) -> None:
        result = _provider()._build_squash_commit_message(
            "abc123def456",
            [],
            issue_key="PROJECT-1234",
            git_root=Path("/repo"),
        )
        assert result == "chore(PROJECT-1234): post-repair squash for abc123de\n\nPROJECT-1234"

    def test_single_subject_returned_verbatim_no_key(self) -> None:
        # A single original subject with no issue key is reused as-is.
        result = _provider()._build_squash_commit_message("abc123def456", ["feat: update flow"])
        assert result == "feat: update flow"

    def test_single_subject_with_key_appends_footer(self) -> None:
        # A single original subject gets the issue footer appended for convention compliance.
        result = _provider()._build_squash_commit_message("abc123def456", ["feat: update flow"], issue_key="2249")
        assert result == "feat: update flow\n\n#2249"

    @patch("agentic_devtools.cli.ci.github_provider.load_platform_config", return_value={"issue_adapter": "markdown"})
    def test_single_subject_with_numeric_key_uses_markdown_adapter_footer(self, _mock_config) -> None:
        result = _provider()._build_squash_commit_message(
            "abc123def456",
            ["feat: update flow"],
            issue_key="2249",
            git_root=Path("/repo"),
        )
        assert result == "feat: update flow\n\n2249"

    def test_multi_subjects_no_key(self) -> None:
        result = _provider()._build_squash_commit_message("abc123def456", ["a", "b"])
        assert result.startswith("chore: squash post-repair updates")
        assert "- a" in result
        assert "- b" in result
        # No footer when the issue key is unknown.
        assert not result.strip().endswith("#")

    def test_multi_subjects_with_key_has_scope_and_footer(self) -> None:
        result = _provider()._build_squash_commit_message("abc123def456", ["a", "b"], issue_key="2249")
        assert result.startswith("chore(#2249): squash post-repair updates")
        assert "- a" in result
        assert "- b" in result
        assert result.strip().endswith("#2249")

    @patch("agentic_devtools.cli.ci.github_provider.load_platform_config", return_value={"issue_adapter": "markdown"})
    def test_multi_subjects_with_numeric_key_uses_markdown_adapter_convention(self, _mock_config) -> None:
        result = _provider()._build_squash_commit_message(
            "abc123def456",
            ["a", "b"],
            issue_key="2249",
            git_root=Path("/repo"),
        )
        assert result.startswith("chore(2249): squash post-repair updates")
        assert result.strip().endswith("2249")

    @patch(
        "agentic_devtools.cli.ci.github_provider._derive_issue_link_from_key",
        return_value="https://jira.example.com/browse/PROJECT-1234",
    )
    def test_multi_subjects_with_jira_key_uses_browse_link_when_available(self, _mock_derive) -> None:
        result = _provider()._build_squash_commit_message(
            "abc123def456",
            ["a", "b"],
            issue_key="PROJECT-1234",
            git_root=Path("/repo"),
        )
        assert result.startswith("chore(PROJECT-1234): squash post-repair updates")
        assert result.strip().endswith("[PROJECT-1234](https://jira.example.com/browse/PROJECT-1234)")

    @patch("agentic_devtools.cli.ci.github_provider._derive_issue_link_from_key", return_value=None)
    def test_multi_subjects_with_jira_key_falls_back_to_bare_footer_when_unconfigured(self, _mock_derive) -> None:
        result = _provider()._build_squash_commit_message(
            "abc123def456",
            ["a", "b"],
            issue_key="PROJECT-1234",
            git_root=Path("/repo"),
        )
        assert result.startswith("chore(PROJECT-1234): squash post-repair updates")
        assert result.strip().endswith("PROJECT-1234")

    def test_blank_subjects_filtered(self) -> None:
        result = _provider()._build_squash_commit_message("abc123def456", ["  ", "real"], issue_key="7")
        # Only one non-blank subject remains → returned with footer.
        assert result == "real\n\n#7"

    def test_caps_bullets_at_ten(self) -> None:
        subjects = [f"s{i}" for i in range(15)]
        result = _provider()._build_squash_commit_message("abc123def456", subjects, issue_key="7")
        assert result.count("\n- ") == 10
