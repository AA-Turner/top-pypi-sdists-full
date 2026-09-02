"""Tests for _github_token."""

import pytest

from agentic_devtools.cli.pull_request_thread import (
    _github_token,
)


class TestHelper:
    @pytest.mark.parametrize("env_name", ["GH_TOKEN", "GITHUB_TOKEN", "COPILOT_GITHUB_TOKEN"])
    def test_github_token_precedence_sources(self, monkeypatch: pytest.MonkeyPatch, env_name: str) -> None:
        monkeypatch.setenv(env_name, "token")
        assert _github_token() == "token"
