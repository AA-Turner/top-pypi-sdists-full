"""Tests for _sanitize_diagnostic."""

import pytest

from agentic_devtools.cli.pull_request_thread import (
    _sanitize_diagnostic,
)


class TestHelper:
    def test_sanitizes_credentials(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GH_TOKEN", "secret")
        assert _sanitize_diagnostic("failed secret") == "failed [redacted]"

    def test_sanitizes_default_repo_workflow_pat(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "direct-pat")
        assert _sanitize_diagnostic("failed direct-pat") == "failed [redacted]"
