"""Tests for _get_log_path in agentic_devtools.cli.setup.decision_log."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.decision_log import _get_log_path


class TestGetLogPath:
    """Tests for _get_log_path resolution."""

    def test_resolves_to_setup_subdir(self, tmp_path: Path) -> None:
        """Returns {state_dir}/setup/run-setup-decision-log.md."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            result = _get_log_path()
            expected = tmp_path / "setup" / "run-setup-decision-log.md"
            assert result == expected

    def test_does_not_create_directories(self, tmp_path: Path) -> None:
        """_get_log_path does not create any directories on its own."""
        state_dir = tmp_path / "nonexistent"
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=state_dir,
        ):
            result = _get_log_path()
            assert not result.parent.exists()
