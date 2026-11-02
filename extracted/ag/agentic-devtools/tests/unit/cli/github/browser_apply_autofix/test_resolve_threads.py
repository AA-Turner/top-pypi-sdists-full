"""Tests for _resolve_threads."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.github.browser_apply_autofix import _resolve_threads

_TARGET = "agentic_devtools.cli.github.apply_thread_autofix._resolve_thread_for_comment"


class TestResolveThreads:
    """Tests for _resolve_threads."""

    def test_resolves_and_records_failures(self) -> None:
        with patch(_TARGET, side_effect=[True, False]) as mock_resolve:
            result = _resolve_threads(10, "owner/repo", [101, 202])
        assert result == {"resolved": [101], "failed": [202]}
        assert mock_resolve.call_count == 2

    def test_empty_comment_ids(self) -> None:
        with patch(_TARGET) as mock_resolve:
            result = _resolve_threads(10, "owner/repo", [])
        assert result == {"resolved": [], "failed": []}
        mock_resolve.assert_not_called()
