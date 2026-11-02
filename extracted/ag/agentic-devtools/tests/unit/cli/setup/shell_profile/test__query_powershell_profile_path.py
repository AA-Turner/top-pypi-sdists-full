"""Tests for _query_powershell_profile_path."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.shell_profile import _query_powershell_profile_path

_MODULE = "agentic_devtools.cli.setup.shell_profile"


class TestQueryPowershellProfilePath:
    """Tests for _query_powershell_profile_path."""

    def test_returns_none_when_no_interpreter_available(self):
        """Returns None when neither pwsh nor powershell is on PATH."""
        with (
            patch(f"{_MODULE}.shutil.which", return_value=None),
            patch(f"{_MODULE}._run_powershell_expression") as mock_run,
        ):
            assert _query_powershell_profile_path() is None
        mock_run.assert_not_called()

    def test_returns_current_host_profile_from_pwsh(self):
        """Prefers pwsh and the CurrentUserCurrentHost profile."""
        expected = Path(r"C:\Users\u\OneDrive - Org\Dokumente\PowerShell\Microsoft.PowerShell_profile.ps1")
        with (
            patch(f"{_MODULE}.shutil.which", return_value=r"C:\pwsh.exe"),
            patch(f"{_MODULE}._run_powershell_expression", return_value=expected) as mock_run,
        ):
            assert _query_powershell_profile_path() == expected
        assert mock_run.call_args[0] == ("pwsh", "$PROFILE.CurrentUserCurrentHost")

    def test_falls_back_to_all_hosts_expression(self):
        """Falls back to $PROFILE.CurrentUserAllHosts when the first query yields nothing."""
        expected = Path(r"C:\Users\u\Dokumente\PowerShell\profile.ps1")
        with (
            patch(f"{_MODULE}.shutil.which", return_value=r"C:\pwsh.exe"),
            patch(f"{_MODULE}._run_powershell_expression", side_effect=[None, expected]) as mock_run,
        ):
            assert _query_powershell_profile_path() == expected
        assert mock_run.call_count == 2

    def test_falls_back_to_windows_powershell_interpreter(self):
        """Falls back to powershell.exe when pwsh is not installed."""
        expected = Path(r"C:\Users\u\Dokumente\WindowsPowerShell\Microsoft.PowerShell_profile.ps1")

        def which(executable):
            return None if executable == "pwsh" else r"C:\powershell.exe"

        with (
            patch(f"{_MODULE}.shutil.which", side_effect=which),
            patch(f"{_MODULE}._run_powershell_expression", return_value=expected) as mock_run,
        ):
            assert _query_powershell_profile_path() == expected
        assert mock_run.call_args[0][0] == "powershell"

    def test_returns_none_when_all_queries_fail(self):
        """Returns None when every interpreter/expression combination fails."""
        with (
            patch(f"{_MODULE}.shutil.which", return_value=r"C:\pwsh.exe"),
            patch(f"{_MODULE}._run_powershell_expression", return_value=None) as mock_run,
        ):
            assert _query_powershell_profile_path() is None
        assert mock_run.call_count == 4
