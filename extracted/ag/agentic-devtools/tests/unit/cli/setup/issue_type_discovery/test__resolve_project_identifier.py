"""Tests for _resolve_project_identifier in issue_type_discovery."""

from __future__ import annotations

from agentic_devtools.cli.setup.issue_type_discovery import _resolve_project_identifier


class TestResolveProjectIdentifier:
    """Tests for _resolve_project_identifier."""

    def test_jira_project_key(self) -> None:
        """Returns (project_key, 'jira') for Jira adapter."""
        config = {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}}
        result = _resolve_project_identifier(config)
        assert result == ("PROJ", "jira")

    def test_jira_project_key_stripped(self) -> None:
        """Strips whitespace from Jira project key."""
        config = {"issue_adapter": "jira", "jira": {"project_key": "  PROJ  "}}
        result = _resolve_project_identifier(config)
        assert result == ("PROJ", "jira")

    def test_jira_missing_project_key(self) -> None:
        """Returns None when Jira config lacks project_key."""
        config = {"issue_adapter": "jira", "jira": {}}
        assert _resolve_project_identifier(config) is None

    def test_jira_blank_project_key(self) -> None:
        """Returns None when Jira project_key is blank."""
        config = {"issue_adapter": "jira", "jira": {"project_key": "  "}}
        assert _resolve_project_identifier(config) is None

    def test_jira_section_not_dict(self) -> None:
        """Returns None when jira section is not a dict."""
        config = {"issue_adapter": "jira", "jira": "not-a-dict"}
        assert _resolve_project_identifier(config) is None

    def test_jira_section_missing(self) -> None:
        """Returns None when jira section is missing."""
        config = {"issue_adapter": "jira"}
        assert _resolve_project_identifier(config) is None

    def test_github_repo_key(self) -> None:
        """Returns (repo, 'github') when github.repo is set."""
        config = {"issue_adapter": "github", "github": {"repo": "owner/repo"}}
        result = _resolve_project_identifier(config)
        assert result == ("owner/repo", "github")

    def test_github_repo_key_stripped(self) -> None:
        """Strips whitespace from GitHub repo key."""
        config = {"issue_adapter": "github", "github": {"repo": " owner/repo "}}
        result = _resolve_project_identifier(config)
        assert result == ("owner/repo", "github")

    def test_github_fallback_owner_name(self) -> None:
        """Falls back to owner/name when repo key absent."""
        config = {"issue_adapter": "github", "github": {"repo_owner": "org", "repo_name": "project"}}
        result = _resolve_project_identifier(config)
        assert result == ("org/project", "github")

    def test_github_fallback_owner_name_stripped(self) -> None:
        """Strips whitespace from owner and name."""
        config = {"issue_adapter": "github", "github": {"repo_owner": " org ", "repo_name": " project "}}
        result = _resolve_project_identifier(config)
        assert result == ("org/project", "github")

    def test_github_missing_owner(self) -> None:
        """Returns None when repo_owner is missing."""
        config = {"issue_adapter": "github", "github": {"repo_name": "project"}}
        assert _resolve_project_identifier(config) is None

    def test_github_missing_name(self) -> None:
        """Returns None when repo_name is missing."""
        config = {"issue_adapter": "github", "github": {"repo_owner": "org"}}
        assert _resolve_project_identifier(config) is None

    def test_github_blank_owner(self) -> None:
        """Returns None when repo_owner is blank."""
        config = {"issue_adapter": "github", "github": {"repo_owner": "", "repo_name": "project"}}
        assert _resolve_project_identifier(config) is None

    def test_github_section_not_dict(self) -> None:
        """Returns None when github section is not a dict."""
        config = {"issue_adapter": "github", "github": "not-a-dict"}
        assert _resolve_project_identifier(config) is None

    def test_markdown_default(self) -> None:
        """Returns ('_default', 'markdown') for markdown adapter."""
        config = {"issue_adapter": "markdown"}
        result = _resolve_project_identifier(config)
        assert result == ("_default", "markdown")

    def test_unknown_adapter(self) -> None:
        """Returns None for unknown adapter."""
        config = {"issue_adapter": "unknown"}
        assert _resolve_project_identifier(config) is None

    def test_empty_config(self) -> None:
        """Returns None for empty config."""
        assert _resolve_project_identifier({}) is None
