"""Tests for resolve_github_repo_safe."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe

_MOD = "agentic_devtools.cli.github.repo_resolution"


@pytest.fixture(autouse=True)
def _clear_repository_environment(monkeypatch):
    """Keep environment fallback tests independent from the runner repository."""
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    monkeypatch.setattr("agentic_devtools.cli.github.repo_resolution.get_repo_root", lambda: None)
    monkeypatch.setattr("agentic_devtools.cli.github.repo_resolution.load_platform_config", lambda _root: {})


class TestResolveGithubRepoSafe:
    """Tests for resolve_github_repo_safe."""

    @patch(f"{_MOD}.get_value", side_effect=AssertionError("live state must not be read"))
    def test_uses_supplied_snapshot(self, mock_get):
        """Uses the captured state mapping instead of rereading global state."""
        result = resolve_github_repo_safe({"github": {"repo": "snapshot-org/snapshot-repo"}})

        assert result == "snapshot-org/snapshot-repo"
        mock_get.assert_not_called()

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    def test_snapshot_without_github_section_falls_back_to_remote(self, mock_remote):
        """A snapshot without GitHub state falls back to the remote."""
        result = resolve_github_repo_safe({})

        assert result == "remote-org/remote-repo"
        mock_remote.assert_called_once()

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    def test_snapshot_with_empty_platform_github_falls_back_to_remote(self, mock_remote):
        """An empty platform GitHub section falls back to the remote."""
        assert resolve_github_repo_safe({"platform": {"github": {}}}) == "remote-org/remote-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    def test_snapshot_with_non_mapping_platform_github_falls_back_to_remote(self, mock_remote):
        """A malformed platform GitHub section falls back to the remote."""
        assert resolve_github_repo_safe({"platform": {"github": "invalid"}}) == "remote-org/remote-repo"

    @patch(f"{_MOD}.get_value", side_effect=AssertionError("live state must not be read"))
    def test_uses_platform_github_repo_from_snapshot(self, mock_get):
        """Uses the provider-neutral platform repository in a supplied snapshot."""
        result = resolve_github_repo_safe({"platform": {"github": {"repo": "platform-org/platform-repo"}}})

        assert result == "platform-org/platform-repo"
        mock_get.assert_not_called()

    @patch(f"{_MOD}.load_platform_config", return_value={"github": {"repo": "config-org/config-repo"}})
    @patch(f"{_MOD}.get_repo_root", return_value="/repo")
    @patch(f"{_MOD}.get_value", side_effect=AssertionError("live state must not be read"))
    def test_snapshot_without_repo_can_fall_back_to_platform_config(self, mock_get, mock_root, mock_config):
        """A supplied snapshot still uses repository config before env/remote fallbacks."""
        assert resolve_github_repo_safe({}) == "config-org/config-repo"
        mock_get.assert_not_called()

    @patch(f"{_MOD}.get_value", return_value="myorg/myrepo")
    def test_returns_state_repo(self, mock_get):
        """Returns github.repo state key when valid."""
        result = resolve_github_repo_safe()
        assert result == "myorg/myrepo"
        mock_get.assert_called_once_with("github.repo")

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_falls_back_to_git_remote(self, mock_get, mock_remote):
        """Falls back to git remote when state is empty."""
        result = resolve_github_repo_safe()
        assert result == "remote-org/remote-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value=None)
    @patch(f"{_MOD}.get_value", return_value=None)
    @patch.dict("os.environ", {"GITHUB_REPOSITORY": "env-org/env-repo"})
    def test_falls_back_to_github_repository_environment(self, mock_get, mock_remote):
        """Uses GITHUB_REPOSITORY when state and the git remote are unavailable."""
        assert resolve_github_repo_safe() == "env-org/env-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    @patch.dict("os.environ", {"GITHUB_REPOSITORY": "invalid"})
    def test_invalid_github_repository_environment_falls_back_to_remote(self, mock_get, mock_remote):
        """Ignores malformed GITHUB_REPOSITORY values."""
        assert resolve_github_repo_safe() == "remote-org/remote-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value=None)
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_returns_none_when_all_fail(self, mock_get, mock_remote):
        """Returns None when no resolution succeeds (no sys.exit)."""
        result = resolve_github_repo_safe()
        assert result is None

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.load_platform_config", return_value={"github": None})
    @patch(f"{_MOD}.get_repo_root", return_value="/repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_non_mapping_platform_config_falls_through(self, mock_get, mock_root, mock_config, mock_remote):
        """A non-mapping config GitHub section falls through to later resolution sources."""
        assert resolve_github_repo_safe() == "remote-org/remote-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.load_platform_config", return_value={"github": {"repo": ["bad"]}})
    @patch(f"{_MOD}.get_repo_root", return_value="/repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_non_string_platform_config_repo_falls_through(self, mock_get, mock_root, mock_config, mock_remote):
        """A non-string config repo falls through to later resolution sources."""
        assert resolve_github_repo_safe() == "remote-org/remote-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.load_platform_config", return_value={"github": {"repo": "invalid"}})
    @patch(f"{_MOD}.get_repo_root", return_value="/repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_invalid_platform_config_repo_falls_through(self, mock_get, mock_root, mock_config, mock_remote):
        """A malformed config repo falls through to later resolution sources."""
        assert resolve_github_repo_safe() == "remote-org/remote-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value=None)
    @patch(f"{_MOD}.load_platform_config", return_value={"github": {"repo": "config-org/config-repo"}})
    @patch(f"{_MOD}.get_repo_root", return_value="/repo")
    @patch(f"{_MOD}.get_value", return_value=None)
    def test_falls_back_to_platform_config_repo(self, mock_get, mock_root, mock_config, mock_remote):
        """Uses .github/agdt-config.json when state does not define a repository."""
        assert resolve_github_repo_safe() == "config-org/config-repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value="remote-org/remote-repo")
    @patch(f"{_MOD}.get_value", return_value="invalid-format")
    def test_malformed_state_falls_through(self, mock_get, mock_remote):
        """Malformed state value falls through to git remote."""
        result = resolve_github_repo_safe()
        assert result == "remote-org/remote-repo"

    @patch(f"{_MOD}.get_value", return_value="  owner/repo  ")
    def test_state_value_stripped(self, mock_get):
        """State value is stripped before validation."""
        result = resolve_github_repo_safe()
        assert result == "owner/repo"

    @patch(f"{_MOD}.get_value", return_value="owner/repo.git")
    def test_strips_dot_git_suffix(self, mock_get):
        """Strips .git suffix from state value."""
        result = resolve_github_repo_safe()
        assert result == "owner/repo"

    @patch(f"{_MOD}._resolve_repo_from_git_remote", return_value=None)
    @patch(f"{_MOD}.get_value", return_value="")
    def test_empty_state_returns_none(self, mock_get, mock_remote):
        """Empty string state value returns None."""
        result = resolve_github_repo_safe()
        assert result is None
