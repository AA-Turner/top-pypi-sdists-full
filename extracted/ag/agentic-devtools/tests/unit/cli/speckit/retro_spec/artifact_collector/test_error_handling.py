"""Tests for error handling in artifact_collector.py."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import (
    _search_prs_by_keywords,
    _search_prs_by_title_scope,
    fetch_issue,
)

_MOD = "agentic_devtools.cli.speckit.retro_spec.artifact_collector"


class TestFetchIssueErrors:
    """Tests for fetch_issue error handling paths."""

    def test_exits_with_404_message(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that 404 errors produce dual-cause guidance."""
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 1, "", "404 Not Found"),
        ):
            with pytest.raises(SystemExit):
                fetch_issue("owner", "repo", 99)
        err = capsys.readouterr().err
        assert "not found" in err.lower()
        assert "permissions" in err.lower()

    def test_exits_with_rate_limit_message(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that rate limit errors report the situation clearly."""
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 1, "", "403 rate limit exceeded"),
        ):
            with pytest.raises(SystemExit):
                fetch_issue("owner", "repo", 99)
        err = capsys.readouterr().err
        assert "rate limit" in err.lower()

    def test_exits_with_generic_message_for_non_rate_limit_403(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that non-rate-limit 403 errors do not produce rate-limit guidance."""
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 1, "", "403 Forbidden"),
        ):
            with pytest.raises(SystemExit):
                fetch_issue("owner", "repo", 99)
        err = capsys.readouterr().err
        assert "could not fetch issue" in err.lower()
        assert "rate limit" not in err.lower()


class TestSearchPrsErrors:
    """Tests for PR search error handling."""

    def test_keyword_search_returns_empty_on_os_error(self) -> None:
        """Test that OSError in keyword search returns empty list."""
        with patch(f"{_MOD}.subprocess.run", side_effect=OSError("fail")):
            assert _search_prs_by_keywords("o", "r", 1) == []

    def test_keyword_search_returns_empty_on_failure(self) -> None:
        """Test that non-zero exit code returns empty list."""
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 1, "", ""),
        ):
            assert _search_prs_by_keywords("o", "r", 1) == []

    def test_keyword_search_returns_empty_on_invalid_json(self) -> None:
        """Test that invalid JSON returns empty list."""
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, "not json", ""),
        ):
            assert _search_prs_by_keywords("o", "r", 1) == []

    def test_title_search_returns_empty_on_os_error(self) -> None:
        """Test that OSError in title scope search returns empty list."""
        with patch(f"{_MOD}.subprocess.run", side_effect=OSError("fail")):
            assert _search_prs_by_title_scope("o", "r", 1) == []

    def test_title_search_returns_empty_on_failure(self) -> None:
        """Test that non-zero exit code returns empty list."""
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 1, "", ""),
        ):
            assert _search_prs_by_title_scope("o", "r", 1) == []

    def test_title_search_returns_empty_on_invalid_json(self) -> None:
        """Test that invalid JSON returns empty list."""
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, "{{bad", ""),
        ):
            assert _search_prs_by_title_scope("o", "r", 1) == []
