"""Tests for :func:`agentic_devtools.cli.setup.provider_connectivity._resolve_github_repo_slug`."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.provider_connectivity import _resolve_github_repo_slug


class TestResolveGitHubRepoSlug:
    """Verify GitHub repo-slug resolution precedence and validation."""

    def test_missing_repo_config_returns_false(self, tmp_path: Path) -> None:
        """Missing GitHub repo configuration fails before any CLI call."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.load_platform_config",
            return_value={"github": {}},
        ):
            repo_slug, error = _resolve_github_repo_slug(tmp_path)

        assert repo_slug is None
        assert error == "GitHub repository is not configured"

    def test_invalid_repo_config_returns_false(self, tmp_path: Path) -> None:
        """Invalid GitHub repo slugs are rejected."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.load_platform_config",
            return_value={"github": {"repo": "owner/repo/extra"}},
        ):
            repo_slug, error = _resolve_github_repo_slug(tmp_path)

        assert repo_slug is None
        assert "Invalid GitHub repository configuration" in (error or "")

    def test_falls_back_to_owner_and_name_fields(self, tmp_path: Path) -> None:
        """Separate owner/name config is combined into the final repo slug."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.load_platform_config",
            return_value={"github": {"repo_owner": "owner", "repo_name": "repo"}},
        ):
            repo_slug, error = _resolve_github_repo_slug(tmp_path)

        assert repo_slug == "owner/repo"
        assert error is None

    def test_non_mapping_config_returns_false(self, tmp_path: Path) -> None:
        """Non-dict GitHub config sections are treated as missing repo configuration."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.load_platform_config",
            return_value={"github": "owner/repo"},
        ):
            repo_slug, error = _resolve_github_repo_slug(tmp_path)

        assert repo_slug is None
        assert error == "GitHub repository is not configured"
