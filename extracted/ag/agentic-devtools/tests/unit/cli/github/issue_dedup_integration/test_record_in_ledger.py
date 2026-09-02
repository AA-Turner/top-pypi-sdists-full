"""Tests for record_in_ledger."""

from __future__ import annotations

import json
from collections.abc import Iterator
from contextlib import contextmanager
from unittest.mock import patch

import pytest

from agentic_devtools.cli.github import issue_dedup_integration
from agentic_devtools.cli.github.issue_dedup_integration import record_in_ledger

_MOD = "agentic_devtools.cli.github.issue_dedup_integration"


class TestRecordInLedger:
    """Tests for record_in_ledger."""

    @patch(f"{_MOD}._get_session_id", return_value="/test/session")
    @patch(f"{_MOD}._get_ledger_path")
    def test_first_write_creates_ledger(self, mock_path, mock_sid, tmp_path) -> None:
        """First record creates ledger with session_id and entry."""
        ledger_path = tmp_path / "ledger.json"
        mock_path.return_value = ledger_path
        record_in_ledger("sig123", 42, action="create")
        data = json.loads(ledger_path.read_text())
        assert data["session_id"] == "/test/session"
        assert data["entries"]["sig123"]["issue_number"] == 42
        assert data["entries"]["sig123"]["last_action"] == "create"
        assert "created_utc" in data["entries"]["sig123"]

    @patch(f"{_MOD}._get_session_id", return_value="/test/session")
    @patch(f"{_MOD}.locked_file")
    def test_empty_file_content_creates_new_ledger(self, mock_locked_file, mock_sid, tmp_path) -> None:
        """Empty file content is treated as an empty ledger."""
        ledger_path = tmp_path / "ledger.json"
        file_handle = (tmp_path / "ledger.json").open("w+", encoding="utf-8")
        file_handle.write("")
        file_handle.seek(0)

        @contextmanager
        def locked_empty_file(*args, **kwargs) -> Iterator[object]:
            try:
                yield file_handle
            finally:
                file_handle.close()

        mock_locked_file.side_effect = locked_empty_file

        record_in_ledger("sig123", 42, action="create")

        data = json.loads(ledger_path.read_text())
        assert data["entries"]["sig123"]["issue_number"] == 42

    @patch(f"{_MOD}._get_session_id", return_value="/test/session")
    @patch(f"{_MOD}._is_ledger_stale", return_value=False)
    @patch(f"{_MOD}._get_ledger_path")
    def test_subsequent_augment_preserves_created_utc(self, mock_path, mock_stale, mock_sid, tmp_path) -> None:
        """Second write preserves the immutable created_utc from first write."""
        ledger_path = tmp_path / "ledger.json"
        mock_path.return_value = ledger_path

        # First write
        record_in_ledger("sig123", 42, action="create")
        data1 = json.loads(ledger_path.read_text())
        original_ts = data1["entries"]["sig123"]["created_utc"]

        # Second write (augment)
        record_in_ledger("sig123", 42, action="augment")
        data2 = json.loads(ledger_path.read_text())
        assert data2["entries"]["sig123"]["created_utc"] == original_ts
        assert data2["entries"]["sig123"]["last_action"] == "augment"

    @patch(f"{_MOD}._get_session_id", return_value="/test/session")
    @patch(f"{_MOD}._is_ledger_stale", return_value=False)
    @patch(f"{_MOD}._get_ledger_path")
    def test_eviction_at_cap(self, mock_path, mock_stale, mock_sid, tmp_path) -> None:
        """Recording when at cap triggers eviction."""
        ledger_path = tmp_path / "ledger.json"
        mock_path.return_value = ledger_path

        # Pre-populate with 100 entries
        entries = {
            f"sig{i:04d}": {
                "issue_number": i,
                "created_utc": f"2024-01-{(i % 28) + 1:02d}T00:00:00Z",
                "last_action": "create",
            }
            for i in range(100)
        }
        data = {"session_id": "/test/session", "created_utc": "2024-06-01T00:00:00Z", "entries": entries}
        ledger_path.write_text(json.dumps(data))

        # Add one more
        record_in_ledger("new_sig", 999, action="create")
        result = json.loads(ledger_path.read_text())
        assert len(result["entries"]) == 100
        assert "new_sig" in result["entries"]

    @patch(f"{_MOD}._get_session_id", return_value="/test/session")
    @patch(f"{_MOD}._is_ledger_stale", return_value=False)
    @patch(f"{_MOD}._get_ledger_path")
    def test_non_dict_entries_field_gets_reset(self, mock_path, mock_stale, mock_sid, tmp_path) -> None:
        """Non-dict entries field is replaced with empty dict."""
        ledger_path = tmp_path / "ledger.json"
        mock_path.return_value = ledger_path

        data = {"session_id": "/test/session", "created_utc": "2024-06-01T00:00:00Z", "entries": "not_a_dict"}
        ledger_path.write_text(json.dumps(data))

        record_in_ledger("sig_new", 55, action="create")
        result = json.loads(ledger_path.read_text())
        assert result["entries"]["sig_new"]["issue_number"] == 55

    @patch(f"{_MOD}._get_session_id", return_value="/test/session")
    @patch(f"{_MOD}._get_ledger_path")
    def test_invalid_json_warns_and_resets_ledger(self, mock_path, mock_sid, tmp_path) -> None:
        """Invalid JSON is treated as empty with a warning."""
        ledger_path = tmp_path / "ledger.json"
        mock_path.return_value = ledger_path
        ledger_path.write_text("{not-json", encoding="utf-8")

        with pytest.warns(UserWarning, match="contains invalid JSON"):
            record_in_ledger("sig123", 42, action="create")

        data = json.loads(ledger_path.read_text())
        assert data["entries"]["sig123"]["issue_number"] == 42

    @patch(f"{_MOD}._get_session_id", return_value="/test/session")
    @patch(f"{_MOD}._get_ledger_path")
    def test_non_dict_json_warns_and_resets_ledger(self, mock_path, mock_sid, tmp_path) -> None:
        """Non-dict JSON is treated as empty with a warning."""
        ledger_path = tmp_path / "ledger.json"
        mock_path.return_value = ledger_path
        ledger_path.write_text('["not", "a", "dict"]', encoding="utf-8")

        with pytest.warns(UserWarning, match="unexpected format"):
            record_in_ledger("sig123", 42, action="create")

        data = json.loads(ledger_path.read_text())
        assert data["entries"]["sig123"]["issue_number"] == 42

    @patch(f"{_MOD}._get_session_id", return_value="/test/session")
    @patch(f"{_MOD}._is_ledger_stale", return_value=True)
    @patch(f"{_MOD}._get_ledger_path")
    def test_stale_ledger_gets_reinitialized(self, mock_path, mock_stale, mock_sid, tmp_path) -> None:
        """Stale ledgers are discarded before recording the new entry."""
        ledger_path = tmp_path / "ledger.json"
        mock_path.return_value = ledger_path
        ledger_path.write_text(
            json.dumps(
                {
                    "session_id": "/old/session",
                    "created_utc": "2024-01-01T00:00:00Z",
                    "entries": {"old_sig": {"issue_number": 1, "created_utc": "2024-01-01T00:00:00Z"}},
                }
            ),
            encoding="utf-8",
        )

        record_in_ledger("sig123", 42, action="create")

        data = json.loads(ledger_path.read_text())
        assert "old_sig" not in data["entries"]
        assert data["entries"]["sig123"]["issue_number"] == 42

    @patch(f"{_MOD}._get_session_id", return_value="/test/session")
    @patch(f"{_MOD}._get_ledger_path")
    def test_uses_single_lock_for_atomic_update(self, mock_path, mock_sid, tmp_path) -> None:
        """Record operation holds one lock across read-modify-write."""
        ledger_path = tmp_path / "ledger.json"
        mock_path.return_value = ledger_path
        original_locked_file = issue_dedup_integration.locked_file
        call_count = 0

        @contextmanager
        def counting_locked_file(*args, **kwargs) -> Iterator[object]:
            nonlocal call_count
            call_count += 1
            with original_locked_file(*args, **kwargs) as handle:
                yield handle

        with patch.object(issue_dedup_integration, "locked_file", side_effect=counting_locked_file):
            record_in_ledger("sig123", 42, action="create")

        assert call_count == 1
