"""Tests for _detect_powershell_profile."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.shell_profile import _detect_powershell_profile

_MODULE = "agentic_devtools.cli.setup.shell_profile"


class TestDetectPowershellProfile:
    """Tests for _detect_powershell_profile."""

    def test_returns_path_reported_by_powershell(self, monkeypatch):
        """Prefers the profile path reported by PowerShell itself (OneDrive KFM aware)."""
        expected = Path(r"C:\Users\u\OneDrive - Org\Dokumente\PowerShell\Microsoft.PowerShell_profile.ps1")
        monkeypatch.delenv("USERPROFILE", raising=False)
        with (
            patch(f"{_MODULE}._query_powershell_profile_path", return_value=expected),
            patch(f"{_MODULE}._documents_dir_from_known_folder") as mock_known,
        ):
            assert _detect_powershell_profile() == expected
        mock_known.assert_not_called()

    def test_falls_back_to_known_folder_documents(self, monkeypatch, tmp_path):
        """Uses the known-folder Documents directory when PowerShell cannot be queried."""
        documents = tmp_path / "OneDrive - Org" / "Dokumente"
        (documents / "PowerShell").mkdir(parents=True)
        monkeypatch.delenv("USERPROFILE", raising=False)
        with (
            patch(f"{_MODULE}._query_powershell_profile_path", return_value=None),
            patch(f"{_MODULE}._documents_dir_from_known_folder", return_value=documents),
        ):
            result = _detect_powershell_profile()
        assert result == documents / "PowerShell" / "Microsoft.PowerShell_profile.ps1"

    def test_falls_back_to_userprofile_documents(self, monkeypatch, tmp_path):
        """Falls back to %USERPROFILE%\\Documents when the known folder is unavailable."""
        legacy_dir = tmp_path / "Documents" / "WindowsPowerShell"
        legacy_dir.mkdir(parents=True)
        monkeypatch.setenv("USERPROFILE", str(tmp_path))
        with (
            patch(f"{_MODULE}._query_powershell_profile_path", return_value=None),
            patch(f"{_MODULE}._documents_dir_from_known_folder", return_value=None),
        ):
            result = _detect_powershell_profile()
        assert result == legacy_dir / "Microsoft.PowerShell_profile.ps1"

    def test_returns_none_when_no_profile_dir_exists(self, monkeypatch, tmp_path):
        """Returns None when no candidate Documents sub-directory exists."""
        monkeypatch.setenv("USERPROFILE", str(tmp_path))
        with (
            patch(f"{_MODULE}._query_powershell_profile_path", return_value=None),
            patch(f"{_MODULE}._documents_dir_from_known_folder", return_value=None),
        ):
            assert _detect_powershell_profile() is None

    def test_returns_none_when_no_candidates_at_all(self, monkeypatch):
        """Returns None when USERPROFILE is empty and the known folder is unavailable."""
        monkeypatch.setenv("USERPROFILE", "")
        with (
            patch(f"{_MODULE}._query_powershell_profile_path", return_value=None),
            patch(f"{_MODULE}._documents_dir_from_known_folder", return_value=None),
        ):
            assert _detect_powershell_profile() is None
