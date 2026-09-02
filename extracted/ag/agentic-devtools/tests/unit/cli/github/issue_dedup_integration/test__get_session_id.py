"""Tests for _get_session_id."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.github.issue_dedup_integration import _get_session_id

_MOD = "agentic_devtools.cli.github.issue_dedup_integration"


class TestGetSessionId:
    """Tests for _get_session_id."""

    @patch(f"{_MOD}.get_state_dir")
    def test_returns_string_representation_of_state_dir(self, mock_state_dir, tmp_path) -> None:
        """Returns the state directory path as a string."""
        mock_state_dir.return_value = tmp_path
        result = _get_session_id()
        assert result == str(tmp_path)
        assert isinstance(result, str)
