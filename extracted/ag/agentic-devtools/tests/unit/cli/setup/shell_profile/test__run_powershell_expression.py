"""Tests for _run_powershell_expression."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.shell_profile import _run_powershell_expression

_UTF8_PREFIX = (
    "$utf8NoBom = New-Object System.Text.UTF8Encoding $false; "
    "[Console]::OutputEncoding = $utf8NoBom; "
    "$OutputEncoding = $utf8NoBom; "
)


def _completed(returncode: int = 0, stdout: str | None = "") -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(args=["pwsh"], returncode=returncode, stdout=stdout, stderr="")


class TestRunPowershellExpression:
    """Tests for _run_powershell_expression."""

    def test_returns_path_from_stdout(self):
        """Returns the trimmed stdout as a Path when the interpreter succeeds."""
        profile = r"C:\Users\u\OneDrive\Dokumente\PowerShell\Microsoft.PowerShell_profile.ps1"
        with patch(
            "agentic_devtools.cli.setup.shell_profile.run_safe",
            return_value=_completed(stdout=f"  {profile}  \r\n"),
        ) as mock_run:
            result = _run_powershell_expression("pwsh", "$PROFILE.CurrentUserCurrentHost")

        assert result == Path(profile)
        args, kwargs = mock_run.call_args
        assert args[0] == [
            "pwsh",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            f"{_UTF8_PREFIX}$PROFILE.CurrentUserCurrentHost",
        ]
        assert kwargs["shell"] is False

    def test_preserves_non_ascii_profile_path(self):
        """Preserves non-ASCII path characters from PowerShell stdout."""
        profile = r"C:\Users\u\OneDrive - Org\Dokumente\Jörg\PowerShell\Microsoft.PowerShell_profile.ps1"
        with patch(
            "agentic_devtools.cli.setup.shell_profile.run_safe",
            return_value=_completed(stdout=f"{profile}\r\n"),
        ):
            result = _run_powershell_expression("powershell", "$PROFILE")

        assert result == Path(profile)

    def test_returns_none_when_run_safe_raises(self):
        """Returns None when the interpreter cannot be launched."""
        with patch(
            "agentic_devtools.cli.setup.shell_profile.run_safe",
            side_effect=OSError("boom"),
        ):
            assert _run_powershell_expression("pwsh", "$PROFILE") is None

    def test_returns_none_on_non_zero_exit(self):
        """Returns None when the interpreter exits non-zero."""
        with patch(
            "agentic_devtools.cli.setup.shell_profile.run_safe",
            return_value=_completed(returncode=1, stdout="ignored"),
        ):
            assert _run_powershell_expression("pwsh", "$PROFILE") is None

    def test_returns_none_on_blank_stdout(self):
        """Returns None when the interpreter produces no usable output."""
        with patch(
            "agentic_devtools.cli.setup.shell_profile.run_safe",
            return_value=_completed(stdout="   \n"),
        ):
            assert _run_powershell_expression("pwsh", "$PROFILE") is None

    def test_returns_none_when_stdout_is_none(self):
        """Returns None when stdout was not captured."""
        with patch(
            "agentic_devtools.cli.setup.shell_profile.run_safe",
            return_value=_completed(stdout=None),
        ):
            assert _run_powershell_expression("pwsh", "$PROFILE") is None
