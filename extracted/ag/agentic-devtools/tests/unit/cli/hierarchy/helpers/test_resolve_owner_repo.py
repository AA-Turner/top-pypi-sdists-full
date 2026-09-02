"""Tests for resolve_owner_repo helper."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.hierarchy.helpers import resolve_owner_repo


class TestResolveOwnerRepo:
    """Tests for GitHub owner/repo resolution."""

    def test_explicit_values(self) -> None:
        owner, repo = resolve_owner_repo(owner="org", repo="my-repo")
        assert owner == "org"
        assert repo == "my-repo"

    def test_detects_from_https_remote(self) -> None:
        mock_result = type(
            "Result",
            (),
            {
                "returncode": 0,
                "stdout": "https://github.com/swai-factory/agentic-devtools.git\n",
            },
        )()

        with patch("subprocess.run", return_value=mock_result):
            owner, repo = resolve_owner_repo()
        assert owner == "swai-factory"
        assert repo == "agentic-devtools"

    def test_detects_from_ssh_remote(self) -> None:
        mock_result = type(
            "Result",
            (),
            {
                "returncode": 0,
                "stdout": "git@github.com:swai-factory/agentic-devtools.git\n",
            },
        )()

        with patch("subprocess.run", return_value=mock_result):
            owner, repo = resolve_owner_repo()
        assert owner == "swai-factory"
        assert repo == "agentic-devtools"

    def test_raises_on_failure(self) -> None:
        mock_result = type(
            "Result",
            (),
            {
                "returncode": 1,
                "stdout": "",
            },
        )()

        with (
            patch("subprocess.run", return_value=mock_result),
            pytest.raises(ValueError, match="Cannot resolve"),
        ):
            resolve_owner_repo()
