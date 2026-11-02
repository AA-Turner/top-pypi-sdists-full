"""Tests for _detect_owner_repo in nest/commands.py."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.nest.commands import _detect_owner_repo


class TestDetectOwnerRepo:
    """Tests for the _detect_owner_repo function."""

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("https://github.com/octo/repo.git\n", ("octo", "repo")),
            ("git@github.com:octo/repo.git\n", ("octo", "repo")),
        ],
    )
    def test_parses_https_and_ssh_remotes(self, url: str, expected: tuple[str, str]) -> None:
        """Test that supported GitHub remote formats are parsed correctly."""
        with patch(
            "agentic_devtools.cli.speckit.nest.commands.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, url, ""),
        ):
            assert _detect_owner_repo() == expected

    def test_returns_none_pair_when_git_remote_lookup_fails(self) -> None:
        """Test that command failures return no repository coordinates."""
        with patch(
            "agentic_devtools.cli.speckit.nest.commands.subprocess.run",
            return_value=subprocess.CompletedProcess([], 1, "", "boom"),
        ):
            assert _detect_owner_repo() == (None, None)

    def test_returns_none_pair_when_url_does_not_match_pattern(self) -> None:
        """Test that unparseable remote URLs return no coordinates."""
        with patch(
            "agentic_devtools.cli.speckit.nest.commands.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, "not-a-github-url\n", ""),
        ):
            assert _detect_owner_repo() == (None, None)

    @pytest.mark.parametrize(
        "url",
        [
            "https://gitlab.com/octo/repo.git\n",
            "git@gitlab.com:octo/repo.git\n",
            "https://dev.azure.com/org/project/_git/repo\n",
            "git@ssh.dev.azure.com:v3/org/project/repo\n",
        ],
    )
    def test_returns_none_pair_for_non_github_remote(self, url: str) -> None:
        """Test that non-GitHub remotes do not produce false matches."""
        with patch(
            "agentic_devtools.cli.speckit.nest.commands.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, url, ""),
        ):
            assert _detect_owner_repo() == (None, None)
