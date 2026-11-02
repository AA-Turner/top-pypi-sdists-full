"""Tests for _get_ledger_path."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.github.issue_dedup_integration import (
    LEDGER_FILENAME,
    _get_ledger_path,
)

_MOD = "agentic_devtools.cli.github.issue_dedup_integration"


class TestGetLedgerPath:
    """Tests for _get_ledger_path."""

    @patch(f"{_MOD}.get_state_dir")
    def test_returns_ledger_file_in_state_dir(self, mock_state_dir, tmp_path) -> None:
        """Returns the ledger filename appended to the state directory."""
        mock_state_dir.return_value = tmp_path
        result = _get_ledger_path()
        assert result == tmp_path / LEDGER_FILENAME
        assert isinstance(result, Path)
