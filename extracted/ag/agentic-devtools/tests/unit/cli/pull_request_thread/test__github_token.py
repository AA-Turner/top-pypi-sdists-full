"""Tests for _github_token."""

import pytest

from agentic_devtools.cli.ci.credential_roles import DEFAULT_CLASSIC_REPO_WORKFLOW_PAT
from agentic_devtools.cli.pull_request_thread import (
    _github_token,
)


class TestHelper:
    def test_github_token_reads_default_pat(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(DEFAULT_CLASSIC_REPO_WORKFLOW_PAT, "token")
        assert _github_token() == "token"

    def test_github_token_accepts_identity_matched_gh_token(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GH_TOKEN", "token")
        monkeypatch.setenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", DEFAULT_CLASSIC_REPO_WORKFLOW_PAT)
        assert _github_token() == "token"

    @pytest.mark.parametrize("env_name", ["GITHUB_TOKEN", "COPILOT_GITHUB_TOKEN"])
    def test_github_token_rejects_other_roles(self, monkeypatch: pytest.MonkeyPatch, env_name: str) -> None:
        monkeypatch.setenv(env_name, "token")
        with pytest.raises(RuntimeError, match=DEFAULT_CLASSIC_REPO_WORKFLOW_PAT):
            _github_token()
