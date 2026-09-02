"""Tests for resolve_owner_repo partial resolution and edge cases."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli.hierarchy.helpers import resolve_owner_repo


class TestResolveOwnerRepoPartial:
    """Cover partial owner/repo from git remote and error paths."""

    def test_explicit_owner_and_repo(self):
        owner, repo = resolve_owner_repo(owner="myowner", repo="myrepo")
        assert owner == "myowner"
        assert repo == "myrepo"

    def test_detect_from_https_remote(self):
        mock_result = type(
            "R", (), {"returncode": 0, "stdout": "https://github.com/detected-owner/detected-repo.git\n", "stderr": ""}
        )()
        with patch("subprocess.run", return_value=mock_result):
            owner, repo = resolve_owner_repo()
            assert owner == "detected-owner"
            assert repo == "detected-repo"

    def test_detect_from_ssh_remote(self):
        mock_result = type(
            "R", (), {"returncode": 0, "stdout": "git@github.com:ssh-owner/ssh-repo.git\n", "stderr": ""}
        )()
        with patch("subprocess.run", return_value=mock_result):
            owner, repo = resolve_owner_repo()
            assert owner == "ssh-owner"
            assert repo == "ssh-repo"

    def test_partial_owner_uses_remote_repo(self):
        """When owner is provided but repo is None, fills from remote."""
        mock_result = type(
            "R", (), {"returncode": 0, "stdout": "https://github.com/remote-owner/remote-repo.git\n", "stderr": ""}
        )()
        with patch("subprocess.run", return_value=mock_result):
            owner, repo = resolve_owner_repo(owner="explicit-owner", repo=None)
            assert owner == "explicit-owner"
            assert repo == "remote-repo"

    def test_partial_repo_uses_remote_owner(self):
        """When repo is provided but owner is None, fills from remote."""
        mock_result = type(
            "R", (), {"returncode": 0, "stdout": "https://github.com/remote-owner/remote-repo.git\n", "stderr": ""}
        )()
        with patch("subprocess.run", return_value=mock_result):
            owner, repo = resolve_owner_repo(owner=None, repo="explicit-repo")
            assert owner == "remote-owner"
            assert repo == "explicit-repo"

    def test_detect_from_ssh_url_remote(self):
        """Handle ssh://git@github.com/owner/repo.git variant."""
        mock_result = type(
            "R",
            (),
            {"returncode": 0, "stdout": "ssh://git@github.com/ssh-url-owner/ssh-url-repo.git\n", "stderr": ""},
        )()
        with patch("subprocess.run", return_value=mock_result):
            owner, repo = resolve_owner_repo()
            assert owner == "ssh-url-owner"
            assert repo == "ssh-url-repo"

    def test_unrecognized_remote_url_raises(self):
        """URL that doesn't match known patterns raises ValueError."""
        mock_result = type("R", (), {"returncode": 0, "stdout": "https://gitlab.com/owner/repo.git\n", "stderr": ""})()
        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(ValueError, match="Cannot resolve"):
                resolve_owner_repo()

    def test_git_command_fails_raises(self):
        """Non-zero returncode from git raises ValueError."""
        mock_result = type("R", (), {"returncode": 128, "stdout": "", "stderr": "not a git repo"})()
        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(ValueError, match="Cannot resolve"):
                resolve_owner_repo()

    def test_git_not_found_raises(self):
        """FileNotFoundError from subprocess raises ValueError."""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(ValueError, match="Cannot resolve"):
                resolve_owner_repo()

    def test_remote_with_insufficient_parts_raises(self):
        """URL with only one part after prefix raises ValueError."""
        mock_result = type("R", (), {"returncode": 0, "stdout": "https://github.com/onlyowner\n", "stderr": ""})()
        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(ValueError, match="Cannot resolve"):
                resolve_owner_repo()
