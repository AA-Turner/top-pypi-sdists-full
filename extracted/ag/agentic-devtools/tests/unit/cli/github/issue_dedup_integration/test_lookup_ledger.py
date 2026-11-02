"""Tests for lookup_ledger."""

from __future__ import annotations

import json
from unittest.mock import patch

from agentic_devtools.cli.github.issue_dedup_integration import lookup_ledger

_MOD = "agentic_devtools.cli.github.issue_dedup_integration"


class TestLookupLedger:
    """Tests for lookup_ledger."""

    @patch(f"{_MOD}._is_ledger_stale", return_value=False)
    @patch(f"{_MOD}._get_ledger_path")
    def test_hit_returns_issue_number(self, mock_path, mock_stale, tmp_path) -> None:
        """Matching signature returns issue number."""
        ledger_path = tmp_path / "ledger.json"
        data = {"session_id": "s", "entries": {"abc123": {"issue_number": 42, "created_utc": "2024-01-01T00:00:00Z"}}}
        ledger_path.write_text(json.dumps(data))
        mock_path.return_value = ledger_path
        assert lookup_ledger("abc123") == 42

    @patch(f"{_MOD}._is_ledger_stale", return_value=False)
    @patch(f"{_MOD}._get_ledger_path")
    def test_miss_returns_none(self, mock_path, mock_stale, tmp_path) -> None:
        """Non-matching signature returns None."""
        ledger_path = tmp_path / "ledger.json"
        data = {"session_id": "s", "entries": {"abc123": {"issue_number": 42, "created_utc": "2024-01-01T00:00:00Z"}}}
        ledger_path.write_text(json.dumps(data))
        mock_path.return_value = ledger_path
        assert lookup_ledger("xyz789") is None

    @patch(f"{_MOD}._get_ledger_path")
    def test_empty_ledger_returns_none(self, mock_path, tmp_path) -> None:
        """Missing ledger returns None."""
        mock_path.return_value = tmp_path / "nonexistent.json"
        assert lookup_ledger("abc123") is None

    @patch(f"{_MOD}._is_ledger_stale", return_value=False)
    @patch(f"{_MOD}._get_ledger_path")
    def test_non_dict_entry_returns_none(self, mock_path, mock_stale, tmp_path) -> None:
        """Entry that is not a dict returns None."""
        ledger_path = tmp_path / "ledger.json"
        data = {"session_id": "s", "entries": {"abc123": "not_a_dict"}}
        ledger_path.write_text(json.dumps(data))
        mock_path.return_value = ledger_path
        assert lookup_ledger("abc123") is None

    @patch(f"{_MOD}._is_ledger_stale", return_value=False)
    @patch(f"{_MOD}._get_ledger_path")
    def test_non_int_issue_number_returns_none(self, mock_path, mock_stale, tmp_path) -> None:
        """Entry with non-int issue_number returns None."""
        ledger_path = tmp_path / "ledger.json"
        data = {
            "session_id": "s",
            "entries": {"abc123": {"issue_number": "not_int", "created_utc": "2024-01-01T00:00:00Z"}},
        }
        ledger_path.write_text(json.dumps(data))
        mock_path.return_value = ledger_path
        assert lookup_ledger("abc123") is None

    @patch(f"{_MOD}._is_ledger_stale", return_value=False)
    @patch(f"{_MOD}._get_ledger_path")
    def test_non_dict_entries_field_returns_none(self, mock_path, mock_stale, tmp_path) -> None:
        """Entries field that is not a dict returns None."""
        ledger_path = tmp_path / "ledger.json"
        data = {"session_id": "s", "entries": "not_a_dict"}
        ledger_path.write_text(json.dumps(data))
        mock_path.return_value = ledger_path
        assert lookup_ledger("abc123") is None
