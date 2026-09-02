"""Tests for _resolve_pull_request_id."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_accept import _resolve_pull_request_id

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_accept"


class TestResolvePullRequestId:
    def test_uses_explicit_arg(self):
        assert _resolve_pull_request_id(42) == 42

    def test_falls_back_to_state(self):
        with patch(f"{_MODULE}.get_value", return_value="9"):
            assert _resolve_pull_request_id(None) == 9

    def test_missing_returns_none(self, capsys):
        with patch(f"{_MODULE}.get_value", return_value=None):
            assert _resolve_pull_request_id(None) is None
        assert "PR ID required" in capsys.readouterr().err

    def test_bool_rejected(self, capsys):
        with patch(f"{_MODULE}.get_value", return_value=True):
            assert _resolve_pull_request_id(None) is None
        assert "not a boolean" in capsys.readouterr().err

    def test_non_int_rejected(self, capsys):
        with patch(f"{_MODULE}.get_value", return_value="abc"):
            assert _resolve_pull_request_id(None) is None
        assert "must be an integer" in capsys.readouterr().err
