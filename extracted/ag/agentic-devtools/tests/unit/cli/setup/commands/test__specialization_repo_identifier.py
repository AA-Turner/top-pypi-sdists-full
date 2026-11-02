"""Tests for _specialization_repo_identifier."""

from agentic_devtools.cli.setup import commands


class TestSpecializationRepoIdentifier:
    """Direct tests for _specialization_repo_identifier — one test per branch."""

    def test_returns_empty_string_for_none(self) -> None:
        """None remote URL returns an empty string."""
        assert commands._specialization_repo_identifier(None) == ""

    def test_returns_empty_string_for_empty_url(self) -> None:
        """Empty string remote URL returns an empty string."""
        assert commands._specialization_repo_identifier("") == ""

    def test_returns_identifier_for_ado_https_url(self) -> None:
        """Azure DevOps HTTPS URL is parsed into org/project."""
        url = "https://dev.azure.com/myorg/myproject/_git/myrepo"
        assert commands._specialization_repo_identifier(url) == "myorg/myproject"

    def test_returns_identifier_for_ado_ssh_url(self) -> None:
        """Azure DevOps SSH URL is parsed into org/project."""
        url = "git@ssh.dev.azure.com:v3/myorg/myproject/myrepo"
        assert commands._specialization_repo_identifier(url) == "myorg/myproject"

    def test_returns_identifier_for_ado_legacy_url(self) -> None:
        """Azure DevOps legacy visualstudio.com URL is parsed into org/project."""
        url = "https://myorg.visualstudio.com/myproject/_git/myrepo"
        assert commands._specialization_repo_identifier(url) == "myorg/myproject"

    def test_returns_identifier_for_generic_https_url(self) -> None:
        """Generic HTTPS remote URL (e.g. GitHub) is parsed into owner/repo."""
        url = "https://github.com/example/project.git"
        assert commands._specialization_repo_identifier(url) == "example/project"

    def test_returns_identifier_for_generic_scp_url(self) -> None:
        """Generic SCP-style remote URL (e.g. GitHub SSH) is parsed into owner/repo."""
        url = "git@github.com:example/project.git"
        assert commands._specialization_repo_identifier(url) == "example/project"

    def test_returns_empty_string_for_unrecognised_url(self) -> None:
        """A URL that matches none of the known patterns returns an empty string."""
        assert commands._specialization_repo_identifier("not-a-real-url") == ""
