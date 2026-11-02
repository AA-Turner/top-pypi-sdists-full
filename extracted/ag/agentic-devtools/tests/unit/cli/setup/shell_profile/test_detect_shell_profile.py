"""Tests for detect_shell_profile."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.shell_profile import detect_shell_profile


class TestDetectShellProfile:
    """Tests for detect_shell_profile."""

    def test_returns_bashrc_when_shell_is_bash(self, monkeypatch):
        """Returns ~/.bashrc when $SHELL is /bin/bash."""
        monkeypatch.setenv("SHELL", "/bin/bash")
        with patch("agentic_devtools.cli.setup.shell_profile.sys") as mock_sys:
            mock_sys.platform = "linux"
            result = detect_shell_profile()
        assert result == Path.home() / ".bashrc"

    def test_returns_zshrc_when_shell_is_zsh(self, monkeypatch):
        """Returns ~/.zshrc when $SHELL is /usr/bin/zsh."""
        monkeypatch.setenv("SHELL", "/usr/bin/zsh")
        with patch("agentic_devtools.cli.setup.shell_profile.sys") as mock_sys:
            mock_sys.platform = "linux"
            result = detect_shell_profile()
        assert result == Path.home() / ".zshrc"

    def test_returns_none_when_shell_is_fish(self, monkeypatch):
        """Returns None for unsupported shells like fish."""
        monkeypatch.setenv("SHELL", "/usr/bin/fish")
        with patch("agentic_devtools.cli.setup.shell_profile.sys") as mock_sys:
            mock_sys.platform = "linux"
            result = detect_shell_profile()
        assert result is None

    def test_returns_none_when_shell_empty(self, monkeypatch):
        """Returns None when $SHELL is empty."""
        monkeypatch.setenv("SHELL", "")
        with patch("agentic_devtools.cli.setup.shell_profile.sys") as mock_sys:
            mock_sys.platform = "linux"
            result = detect_shell_profile()
        assert result is None

    def test_returns_none_when_shell_unset(self, monkeypatch):
        """Returns None when $SHELL is not set."""
        monkeypatch.delenv("SHELL", raising=False)
        with patch("agentic_devtools.cli.setup.shell_profile.sys") as mock_sys:
            mock_sys.platform = "linux"
            result = detect_shell_profile()
        assert result is None

    def test_delegates_to_powershell_detection_on_windows(self, monkeypatch):
        """Delegates to _detect_powershell_profile when the shell is PowerShell."""
        expected = Path(r"C:\Users\u\OneDrive - Org\Dokumente\PowerShell\Microsoft.PowerShell_profile.ps1")
        monkeypatch.delenv("SHELL", raising=False)
        monkeypatch.delenv("MSYSTEM", raising=False)
        with (
            patch("agentic_devtools.cli.setup.shell_profile.sys") as mock_sys,
            patch(
                "agentic_devtools.cli.setup.shell_profile._detect_powershell_profile",
                return_value=expected,
            ),
        ):
            mock_sys.platform = "win32"
            result = detect_shell_profile()
        assert result == expected

    def test_returns_none_on_windows_when_profile_undetectable(self, monkeypatch):
        """Returns None on Windows when the PowerShell profile cannot be detected."""
        monkeypatch.delenv("SHELL", raising=False)
        monkeypatch.delenv("MSYSTEM", raising=False)
        with (
            patch("agentic_devtools.cli.setup.shell_profile.sys") as mock_sys,
            patch(
                "agentic_devtools.cli.setup.shell_profile._detect_powershell_profile",
                return_value=None,
            ),
        ):
            mock_sys.platform = "win32"
            result = detect_shell_profile()
        assert result is None
