"""Tests for _run_generated_script."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.setup.autorun import _AUTORUN_MARKER, _run_generated_script
from agentic_devtools.cli.setup.phase_markers import EXECUTION_END, EXECUTION_START


class TestRunGeneratedScript:
    """Tests for _run_generated_script."""

    def test_invokes_script_in_foreground_with_child_env(self, tmp_path: Path) -> None:
        """The script is launched with shell=False, check=True and the recursion marker."""
        script = tmp_path / "setup-dev-tools.py"
        child_env = {_AUTORUN_MARKER: "1"}
        mock_result = MagicMock()

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result) as mock_run:
            result = _run_generated_script(script, child_env)

        assert result is mock_result
        mock_run.assert_called_once_with(
            [sys.executable, str(script), "--foreground"],
            shell=False,
            env=child_env,
            check=True,
        )

    def test_brackets_invocation_with_markers(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Markers are emitted before and after the invocation."""
        script = tmp_path / "setup-dev-tools.py"

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=MagicMock()):
            _run_generated_script(script, {})

        assert capsys.readouterr().out == f"{EXECUTION_START}\n{EXECUTION_END}\n"

    def test_emits_end_marker_when_invocation_raises(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """The end marker is emitted (and the error re-raised) when the child fails."""
        script = tmp_path / "setup-dev-tools.py"

        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=subprocess.CalledProcessError(2, "setup-dev-tools.py"),
        ):
            with pytest.raises(subprocess.CalledProcessError):
                _run_generated_script(script, {})

        assert capsys.readouterr().out == f"{EXECUTION_START}\n{EXECUTION_END}\n"
