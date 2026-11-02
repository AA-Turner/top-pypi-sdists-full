"""Tests for check_post_autorun_version."""

from __future__ import annotations

import subprocess
import sys
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.setup.post_autorun_version_check import (
    _VERSION_READ_TIMEOUT_SECONDS,
    check_post_autorun_version,
)


class TestCheckPostAutorunVersion:
    """Tests for the check_post_autorun_version function."""

    def test_successful_read_returns_stripped_version(self) -> None:
        """Returns the stripped version string on success."""
        mock_result = MagicMock(returncode=0, stdout="  1.2.3\n  ")
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            return_value=mock_result,
        ):
            result = check_post_autorun_version("0.0.1")
        assert result == "1.2.3"

    def test_nonzero_exit_returns_none_and_warns(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Returns None and warns on non-zero exit code."""
        mock_result = MagicMock(returncode=1, stdout="", stderr="PackageNotFoundError: agentic-devtools")
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            return_value=mock_result,
        ):
            result = check_post_autorun_version("0.0.1")
        assert result is None
        stderr = capsys.readouterr().err
        assert "exited with code 1" in stderr
        assert "PackageNotFoundError" in stderr

    def test_nonzero_exit_stderr_truncated_and_newlines_flattened(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Long, multi-line stderr is truncated to 120 chars and newlines flattened."""
        long_stderr = "line1\n" + "x" * 200
        mock_result = MagicMock(returncode=1, stdout="", stderr=long_stderr)
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            return_value=mock_result,
        ):
            result = check_post_autorun_version("0.0.1")
        assert result is None
        stderr = capsys.readouterr().err
        assert "exited with code 1" in stderr
        assert "\n" not in stderr.split("; stderr: ", 1)[-1].rstrip("\n")
        assert "…" in stderr

    def test_multiline_stdout_uses_first_nonempty_line(self) -> None:
        """Uses only the first non-empty line of stdout, ignoring trailing noise."""
        mock_result = MagicMock(returncode=0, stdout="1.2.3\nsome startup hook output\n")
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            return_value=mock_result,
        ):
            result = check_post_autorun_version("0.0.1")
        assert result == "1.2.3"

    def test_empty_output_returns_none_and_warns(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Returns None and warns when subprocess returns empty output."""
        mock_result = MagicMock(returncode=0, stdout="   \n  ")
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            return_value=mock_result,
        ):
            result = check_post_autorun_version("0.0.1")
        assert result is None
        assert "empty output" in capsys.readouterr().err

    def test_file_not_found_returns_none_and_warns(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Returns None and warns when Python interpreter is not found."""
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            side_effect=FileNotFoundError("No such file"),
        ):
            result = check_post_autorun_version("0.0.1")
        assert result is None
        assert "not found" in capsys.readouterr().err

    def test_timeout_returns_none_and_warns(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Returns None and warns when subprocess times out."""
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            side_effect=subprocess.TimeoutExpired(cmd="python", timeout=10),
        ):
            result = check_post_autorun_version("0.0.1")
        assert result is None
        assert "timed out" in capsys.readouterr().err

    def test_generic_oserror_returns_none_and_warns(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Returns None and warns on generic OSError."""
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            side_effect=OSError("Permission denied"),
        ):
            result = check_post_autorun_version("0.0.1")
        assert result is None
        assert "OS error" in capsys.readouterr().err

    def test_timeout_param_is_version_read_timeout_seconds(self) -> None:
        """Uses _VERSION_READ_TIMEOUT_SECONDS as the timeout parameter."""
        mock_result = MagicMock(returncode=0, stdout="1.0.0\n")
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            return_value=mock_result,
        ) as mock_run:
            check_post_autorun_version("0.0.1")
        _, kwargs = mock_run.call_args
        assert kwargs["timeout"] == _VERSION_READ_TIMEOUT_SECONDS

    def test_uses_run_safe_with_shell_false(self) -> None:
        """Calls run_safe with shell=False for security."""
        mock_result = MagicMock(returncode=0, stdout="1.0.0\n")
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            return_value=mock_result,
        ) as mock_run:
            check_post_autorun_version("0.0.1")
        _, kwargs = mock_run.call_args
        assert kwargs["shell"] is False

    def test_subprocess_command_uses_importlib_metadata(self) -> None:
        """Subprocess command uses importlib.metadata to read version."""
        mock_result = MagicMock(returncode=0, stdout="1.0.0\n")
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            return_value=mock_result,
        ) as mock_run:
            check_post_autorun_version("0.0.1")
        args, _ = mock_run.call_args
        cmd = args[0]
        assert cmd == [
            sys.executable,
            "-c",
            "from importlib.metadata import version; print(version('agentic-devtools'))",
        ]

    def test_uses_capture_output_and_text(self) -> None:
        """Calls run_safe with capture_output=True and text=True."""
        mock_result = MagicMock(returncode=0, stdout="1.0.0\n")
        with patch(
            "agentic_devtools.cli.setup.post_autorun_version_check.run_safe",
            return_value=mock_result,
        ) as mock_run:
            check_post_autorun_version("0.0.1")
        _, kwargs = mock_run.call_args
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True

    def test_version_read_timeout_is_ten_seconds(self) -> None:
        """The timeout constant is 10 seconds."""
        assert _VERSION_READ_TIMEOUT_SECONDS == 10
