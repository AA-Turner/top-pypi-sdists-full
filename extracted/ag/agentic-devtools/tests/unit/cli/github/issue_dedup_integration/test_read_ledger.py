"""Tests for read_ledger."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.github.issue_dedup_integration import read_ledger
from agentic_devtools.file_locking import FileLockError

_MOD = "agentic_devtools.cli.github.issue_dedup_integration"


class TestReadLedger:
    """Tests for read_ledger."""

    @patch(f"{_MOD}._get_ledger_path")
    def test_missing_file_returns_empty(self, mock_path, tmp_path) -> None:
        """Missing ledger file returns empty dict without creating file."""
        ledger_path = tmp_path / "nonexistent.json"
        mock_path.return_value = ledger_path
        result = read_ledger()
        assert result == {}
        assert not ledger_path.exists()

    @patch(f"{_MOD}._is_ledger_stale", return_value=False)
    @patch(f"{_MOD}._get_ledger_path")
    def test_valid_ledger_returns_data(self, mock_path, mock_stale, tmp_path) -> None:
        """Valid JSON ledger file returns parsed dict."""
        ledger_path = tmp_path / "ledger.json"
        data = {"session_id": "test", "entries": {"sig1": {"issue_number": 42}}}
        ledger_path.write_text(json.dumps(data))
        mock_path.return_value = ledger_path
        result = read_ledger()
        assert result == data

    @patch(f"{_MOD}._get_ledger_path")
    def test_corrupted_json_warns_returns_empty(self, mock_path, tmp_path) -> None:
        """Corrupted JSON warns and returns empty dict."""
        ledger_path = tmp_path / "ledger.json"
        ledger_path.write_text("{invalid json!!!}")
        mock_path.return_value = ledger_path
        with pytest.warns(UserWarning, match="invalid JSON"):
            result = read_ledger()
        assert result == {}

    @patch(f"{_MOD}._is_ledger_stale", return_value=True)
    @patch(f"{_MOD}._get_ledger_path")
    def test_stale_ledger_returns_empty(self, mock_path, mock_stale, tmp_path) -> None:
        """Stale ledger returns empty dict."""
        ledger_path = tmp_path / "ledger.json"
        data = {"session_id": "old", "entries": {"sig1": {"issue_number": 1}}}
        ledger_path.write_text(json.dumps(data))
        mock_path.return_value = ledger_path
        result = read_ledger()
        assert result == {}

    @patch(f"{_MOD}._get_ledger_path")
    def test_empty_file_returns_empty(self, mock_path, tmp_path) -> None:
        """Empty file returns empty dict."""
        ledger_path = tmp_path / "ledger.json"
        ledger_path.write_text("")
        mock_path.return_value = ledger_path
        result = read_ledger()
        assert result == {}

    @patch(f"{_MOD}._get_ledger_path")
    def test_non_dict_json_warns_returns_empty(self, mock_path, tmp_path) -> None:
        """Non-dict JSON (e.g., a list) warns and returns empty."""
        ledger_path = tmp_path / "ledger.json"
        ledger_path.write_text("[1, 2, 3]")
        mock_path.return_value = ledger_path
        with pytest.warns(UserWarning, match="unexpected format"):
            result = read_ledger()
        assert result == {}

    @patch(f"{_MOD}._get_ledger_path")
    def test_file_lock_error_propagates(self, mock_path, tmp_path) -> None:
        """FileLockError is re-raised when lock cannot be acquired."""
        ledger_path = tmp_path / "ledger.json"
        ledger_path.write_text('{"entries": {}}')
        mock_path.return_value = ledger_path

        with patch(f"{_MOD}.locked_file", side_effect=FileLockError("timeout")):
            with pytest.raises(FileLockError):
                read_ledger()

    @patch(f"{_MOD}._get_ledger_path")
    def test_file_deleted_between_exists_check_and_open_returns_empty(self, mock_path, tmp_path) -> None:
        """FileNotFoundError during locked_file open (TOCTOU race) returns empty dict."""
        ledger_path = tmp_path / "ledger.json"
        ledger_path.write_text('{"entries": {}}')
        mock_path.return_value = ledger_path

        with patch(f"{_MOD}.locked_file", side_effect=FileNotFoundError("file removed")):
            result = read_ledger()
        assert result == {}

    @patch(f"{_MOD}._get_ledger_path")
    def test_uses_shared_lock(self, mock_path, tmp_path) -> None:
        """read_ledger acquires a shared (non-exclusive) lock for cross-platform compatibility."""
        ledger_path = tmp_path / "ledger.json"
        ledger_path.write_text('{"entries": {}}')
        mock_path.return_value = ledger_path

        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=MagicMock(read=MagicMock(return_value="{}")))
        mock_ctx.__exit__ = MagicMock(return_value=False)

        with patch(f"{_MOD}.locked_file", return_value=mock_ctx) as mock_lf:
            read_ledger()

        assert mock_lf.call_count == 1
        _, kwargs = mock_lf.call_args
        assert kwargs.get("exclusive") is False, "read_ledger must use exclusive=False (shared lock)"
