"""Tests for resolve_github_repo."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.github.repo_resolution import resolve_github_repo

_MOD = "agentic_devtools.cli.github.repo_resolution"


@pytest.fixture(autouse=True)
def _clear_repository_environment(monkeypatch):
    """Keep environment fallback tests independent from the runner repository."""
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    monkeypatch.setattr("agentic_devtools.cli.github.repo_resolution.get_repo_root", lambda: None)
    monkeypatch.setattr("agentic_devtools.cli.github.repo_resolution.load_platform_config", lambda _root: {})


class TestResolveGithubRepo:
    """Tests for resolve_github_repo."""

    def test_cli_arg_preferred(self):
        """CLI arg is used when provided."""
        result = resolve_github_repo("myorg/myrepo")
        assert result == "myorg/myrepo"

    def test_cli_arg_strips_whitespace(self):
        """CLI arg is stripped before validation."""
        result = resolve_github_repo("  myorg/myrepo  ")
        assert result == "myorg/myrepo"

    def test_cli_arg_invalid_format_exits(self, capsys):
        """Exits with code 1 for invalid --repo format."""
        with pytest.raises(SystemExit) as exc_info:
            resolve_github_repo("justrepo")
        assert exc_info.value.code == 1
        assert "Invalid --repo format" in capsys.readouterr().err

    @patch(f"{_MOD}.get_value", return_value="state-org/state-repo")
    def test_fallback_to_state(self, mock_get):
        """Falls back to github.repo state key."""
        result = resolve_github_repo(None)
        assert result == "state-org/state-repo"
        mock_get.assert_called_once_with("github.repo")

    @patch(f"{_MOD}.get_value", side_effect=[None, "platform-org/platform-repo"])
    def test_fallback_to_platform_state(self, mock_get):
        """Falls back to the provider-neutral platform GitHub repository."""
        assert resolve_github_repo(None) == "platform-org/platform-repo"

    @patch(f"{_MOD}.load_platform_config", return_value={"github": {"repo": "config-org/config-repo"}})
    @patch(f"{_MOD}.get_repo_root", return_value="/repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_fallback_to_platform_config(self, mock_get, mock_root, mock_config):
        """Falls back to the repository config when state does not define a repo."""
        assert resolve_github_repo(None) == "config-org/config-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.load_platform_config", return_value={"github": None})
    @patch(f"{_MOD}.get_repo_root", return_value="/repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_non_mapping_platform_config_falls_through(self, mock_get, mock_root, mock_config, mock_remote):
        """A non-mapping config GitHub section falls through to later sources."""
        assert resolve_github_repo(None) == "remote-org/remote-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.load_platform_config", return_value={"github": {"repo": ["bad"]}})
    @patch(f"{_MOD}.get_repo_root", return_value="/repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_non_string_platform_config_repo_falls_through(self, mock_get, mock_root, mock_config, mock_remote):
        """A non-string config repo falls through to later sources."""
        assert resolve_github_repo(None) == "remote-org/remote-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.load_platform_config", return_value={"github": {"repo": "invalid"}})
    @patch(f"{_MOD}.get_repo_root", return_value="/repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_invalid_platform_config_repo_falls_through(self, mock_get, mock_root, mock_config, mock_remote):
        """A malformed config repo falls through to later sources."""
        assert resolve_github_repo(None) == "remote-org/remote-repo"

    @patch(f"{_MOD}.get_value", return_value=None)
    @patch.dict("os.environ", {"GITHUB_REPOSITORY": "env-org/env-repo"})
    def test_fallback_to_github_repository_environment(self, mock_get):
        """Falls back to GITHUB_REPOSITORY before consulting the remote."""
        assert resolve_github_repo(None) == "env-org/env-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    @patch.dict("os.environ", {"GITHUB_REPOSITORY": "invalid"})
    def test_invalid_github_repository_environment_falls_through(self, mock_get, mock_remote):
        """Ignores malformed GITHUB_REPOSITORY values."""
        assert resolve_github_repo(None) == "remote-org/remote-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_fallback_to_git_remote(self, mock_get, mock_remote):
        """Falls back to git remote URL."""
        result = resolve_github_repo(None)
        assert result == "remote-org/remote-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.get_value", return_value="justrepo")
    def test_malformed_state_falls_through_to_remote(self, mock_get, mock_remote):
        """Malformed state value (no slash) falls through to git remote."""
        result = resolve_github_repo(None)
        assert result == "remote-org/remote-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.get_value", return_value="a/b/c")
    def test_state_with_extra_slashes_falls_through(self, mock_get, mock_remote):
        """State value with extra slashes is rejected, falls through."""
        result = resolve_github_repo(None)
        assert result == "remote-org/remote-repo"

    @patch(f"{_MOD}.get_value", return_value="  state-org/state-repo  ")
    def test_state_value_stripped(self, mock_get):
        """State value is stripped before use."""
        result = resolve_github_repo(None)
        assert result == "state-org/state-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value=None)
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_exits_when_all_fail(self, mock_get, mock_remote, capsys):
        """Calls sys.exit(1) when no resolution succeeds."""
        with pytest.raises(SystemExit) as exc_info:
            resolve_github_repo(None)
        assert exc_info.value.code == 1
        assert "GITHUB_REPOSITORY" in capsys.readouterr().err
