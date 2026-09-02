"""Tests for _is_ledger_stale."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from agentic_devtools.cli.github.issue_dedup_integration import _is_ledger_stale

_MOD = "agentic_devtools.cli.github.issue_dedup_integration"


class TestIsLedgerStale:
    """Tests for _is_ledger_stale."""

    @patch(f"{_MOD}._get_session_id", return_value="/path/to/state")
    def test_matching_session_fresh_timestamp(self, mock_sid) -> None:
        """Matching session with fresh timestamp is not stale."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {"session_id": "/path/to/state", "created_utc": now}
        assert _is_ledger_stale(data) is False

    @patch(f"{_MOD}._get_session_id", return_value="/path/to/state")
    def test_mismatched_session_is_stale(self, mock_sid) -> None:
        """Mismatched session_id means stale."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {"session_id": "/different/path", "created_utc": now}
        assert _is_ledger_stale(data) is True

    @patch(f"{_MOD}._get_session_id", return_value="/path/to/state")
    def test_expired_timestamp_is_stale(self, mock_sid) -> None:
        """Timestamp older than 24 hours is stale."""
        old = (datetime.now(timezone.utc) - timedelta(hours=25)).strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {"session_id": "/path/to/state", "created_utc": old}
        assert _is_ledger_stale(data) is True

    @patch(f"{_MOD}._get_session_id", return_value="/path/to/state")
    def test_missing_created_utc_is_stale(self, mock_sid) -> None:
        """Matching session with missing created_utc is treated as stale."""
        data = {"session_id": "/path/to/state"}
        assert _is_ledger_stale(data) is True

    @patch(f"{_MOD}._get_session_id", return_value="/path/to/state")
    def test_missing_session_id_is_stale(self, mock_sid) -> None:
        """Missing session_id is treated as stale regardless of timestamp."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {"created_utc": now}
        assert _is_ledger_stale(data) is True

    @patch(f"{_MOD}._get_session_id", return_value="/path/to/state")
    def test_missing_both_fields_is_stale(self, mock_sid) -> None:
        """Empty dict is treated as stale (cannot verify session or freshness)."""
        assert _is_ledger_stale({}) is True

    @patch(f"{_MOD}._get_session_id", return_value="/path/to/state")
    def test_invalid_timestamp_is_stale(self, mock_sid) -> None:
        """Unparseable timestamp is treated as stale to prevent reuse of malformed ledger."""
        data = {"session_id": "/path/to/state", "created_utc": "not-a-date"}
        assert _is_ledger_stale(data) is True

    @patch(f"{_MOD}._get_session_id", return_value="/path/to/state")
    def test_offset_naive_timestamp_is_stale(self, mock_sid) -> None:
        """Offset-naive timestamps cannot be compared to UTC time and are treated as stale."""
        data = {"session_id": "/path/to/state", "created_utc": "2024-01-01T00:00:00"}
        assert _is_ledger_stale(data) is True
