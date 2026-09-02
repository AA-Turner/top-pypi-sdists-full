"""Tests for _derive_issue_link_from_key."""

import json
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from agentic_devtools.cli.git.commit_template import _derive_issue_link_from_key

_MOD = "agentic_devtools.cli.git.commit_template"


class TestDeriveIssueLinkFromKey:
    """Tests for _derive_issue_link_from_key."""

    @patch(f"{_MOD}.run_git")
    def test_numeric_key_returns_github_url(self, mock_run_git):
        """A numeric key produces a GitHub issues URL."""
        mock_run_git.return_value = CompletedProcess(
            args=["git", "-C", "/repo", "remote", "get-url", "origin"],
            returncode=0,
            stdout="git@github.com:owner/repo.git\n",
            stderr="",
        )
        result = _derive_issue_link_from_key("42", Path("/repo"))
        assert result == "https://github.com/owner/repo/issues/42"
        mock_run_git.assert_called_once_with("-C", "/repo", "remote", "get-url", "origin", check=False)

    @patch(f"{_MOD}.run_git")
    def test_numeric_key_returns_none_when_repo_unresolvable(self, mock_run_git):
        """Returns None when the GitHub repo cannot be resolved."""
        mock_run_git.return_value = CompletedProcess(
            args=["git", "-C", "/repo", "remote", "get-url", "origin"],
            returncode=1,
            stdout="",
            stderr="fatal: no such remote",
        )
        result = _derive_issue_link_from_key("42", Path("/repo"))
        assert result is None

    @patch(f"{_MOD}.run_git")
    def test_numeric_key_returns_none_for_non_github_remote(self, mock_run_git):
        """Returns None when the origin URL is not a GitHub remote."""
        mock_run_git.return_value = CompletedProcess(
            args=["git", "-C", "/repo", "remote", "get-url", "origin"],
            returncode=0,
            stdout="https://example.com/owner/repo.git\n",
            stderr="",
        )
        result = _derive_issue_link_from_key("42", Path("/repo"))
        assert result is None

    def test_jira_key_returns_browse_url_from_project_config(self, tmp_path):
        """A Jira-style key produces a browse URL from project config."""
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "project.json").write_text(
            json.dumps({"jira_base_url": "https://jira.example.com"}) + "\n",
            encoding="utf-8",
        )
        result = _derive_issue_link_from_key("PROJECT-1234", tmp_path)
        assert result == "https://jira.example.com/browse/PROJECT-1234"

    def test_jira_url_strips_trailing_slash_from_env(self, monkeypatch, tmp_path):
        """A trailing slash on the Jira base URL is normalized away."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://jira.example.com/")
        result = _derive_issue_link_from_key("PROJECT-1234", tmp_path)
        assert result == "https://jira.example.com/browse/PROJECT-1234"

    def test_jira_key_returns_none_when_no_base_url(self, monkeypatch, tmp_path):
        """Returns None when no Jira base URL is configured."""
        monkeypatch.delenv("JIRA_BASE_URL", raising=False)
        result = _derive_issue_link_from_key("PROJECT-1234", tmp_path)
        assert result is None

    def test_jira_key_returns_none_for_whitespace_base_url(self, monkeypatch, tmp_path):
        """Whitespace-only Jira base URLs are treated as unconfigured."""
        monkeypatch.setenv("JIRA_BASE_URL", "   ")
        result = _derive_issue_link_from_key("PROJECT-1234", tmp_path)
        assert result is None

    def test_jira_key_ignores_whitespace_project_config_and_falls_back_to_env(self, monkeypatch, tmp_path):
        """Whitespace-only config values fall through to the environment."""
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "project.json").write_text(
            json.dumps({"jira_base_url": "   "}) + "\n",
            encoding="utf-8",
        )
        monkeypatch.setenv("JIRA_BASE_URL", "https://jira.example.com")
        result = _derive_issue_link_from_key("PROJECT-1234", tmp_path)
        assert result == "https://jira.example.com/browse/PROJECT-1234"

    @patch(f"{_MOD}.run_git")
    def test_does_not_read_state(self, mock_run_git):
        """Does not call get_value (no state reads)."""
        mock_run_git.return_value = CompletedProcess(
            args=["git", "-C", "/repo", "remote", "get-url", "origin"],
            returncode=0,
            stdout="https://github.com/owner/repo.git\n",
            stderr="",
        )
        with patch(f"{_MOD}.get_value", side_effect=AssertionError("must not read state")):
            result = _derive_issue_link_from_key("99", Path("/repo"))
        assert result == "https://github.com/owner/repo/issues/99"

    def test_jira_key_does_not_read_state(self, tmp_path, monkeypatch):
        """The Jira branch derives links without reading workflow state."""
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "project.json").write_text(
            json.dumps({"jira_base_url": "https://jira.example.com"}) + "\n",
            encoding="utf-8",
        )
        monkeypatch.delenv("JIRA_BASE_URL", raising=False)
        with patch(f"{_MOD}.get_value", side_effect=AssertionError("must not read state")):
            result = _derive_issue_link_from_key("PROJECT-99", tmp_path)
        assert result == "https://jira.example.com/browse/PROJECT-99"
