"""Tests for write_ledger."""

from __future__ import annotations

import json
from unittest.mock import patch

from agentic_devtools.cli.github.issue_dedup_integration import (
    LEDGER_MAX_ENTRIES,
    write_ledger,
)

_MOD = "agentic_devtools.cli.github.issue_dedup_integration"


class TestWriteLedger:
    """Tests for write_ledger."""

    @patch(f"{_MOD}._get_ledger_path")
    def test_creates_new_file(self, mock_path, tmp_path) -> None:
        """Creates the ledger file if it does not exist."""
        ledger_path = tmp_path / "ledger.json"
        mock_path.return_value = ledger_path
        data = {"session_id": "test", "entries": {"sig1": {"issue_number": 1, "created_utc": "2024-01-01T00:00:00Z"}}}
        write_ledger(data)
        assert ledger_path.exists()
        written = json.loads(ledger_path.read_text())
        assert written == data

    @patch(f"{_MOD}._get_ledger_path")
    def test_overwrites_existing_file(self, mock_path, tmp_path) -> None:
        """Overwrites existing ledger content."""
        ledger_path = tmp_path / "ledger.json"
        ledger_path.write_text('{"old": true}')
        mock_path.return_value = ledger_path
        data = {"session_id": "new", "entries": {}}
        write_ledger(data)
        written = json.loads(ledger_path.read_text())
        assert written == data

    @patch(f"{_MOD}._get_ledger_path")
    def test_eviction_enforced_on_write(self, mock_path, tmp_path) -> None:
        """Writing 101 entries results in only 100 after eviction."""
        ledger_path = tmp_path / "ledger.json"
        mock_path.return_value = ledger_path
        entries = {
            f"sig{i:04d}": {"issue_number": i, "created_utc": f"2024-01-{i + 1:02d}T00:00:00Z"}
            for i in range(LEDGER_MAX_ENTRIES + 1)
        }
        data = {"session_id": "test", "entries": entries}
        write_ledger(data)
        written = json.loads(ledger_path.read_text())
        assert len(written["entries"]) == LEDGER_MAX_ENTRIES

    @patch(f"{_MOD}._get_ledger_path")
    def test_no_entries_key_skips_eviction(self, mock_path, tmp_path) -> None:
        """Data without 'entries' key skips eviction but still writes."""
        ledger_path = tmp_path / "ledger.json"
        mock_path.return_value = ledger_path
        data = {"session_id": "test"}
        write_ledger(data)
        written = json.loads(ledger_path.read_text())
        assert written == {"session_id": "test"}
