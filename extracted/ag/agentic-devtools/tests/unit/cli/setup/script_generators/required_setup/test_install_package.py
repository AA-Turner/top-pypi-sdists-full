"""Tests for install_package."""

import io
from unittest.mock import patch

from agentic_devtools.cli.setup.script_generators.required_setup import install_package


class _FakePopen:
    def __init__(self, *, returncode: int, stdout: str, stderr: str) -> None:
        self._returncode = returncode
        self.stdout = io.StringIO(stdout)
        self.stderr = io.StringIO(stderr)

    def wait(self) -> int:
        return self._returncode


class TestInstallPackage:
    """Tests for install_package."""

    def test_success(self, capsys):
        """Successful pip install streams stdout and returns (True, output)."""
        with patch(
            "agentic_devtools.cli.setup.script_generators.required_setup.subprocess.Popen",
            return_value=_FakePopen(returncode=0, stdout="Successfully installed\n", stderr=""),
        ):
            ok, output = install_package()
            assert ok is True
            assert "Successfully installed" in output
            assert capsys.readouterr().out == "Successfully installed\n"

    def test_failure(self, capsys):
        """Failed pip install preserves stderr and returns (False, output)."""
        with patch(
            "agentic_devtools.cli.setup.script_generators.required_setup.subprocess.Popen",
            return_value=_FakePopen(returncode=1, stdout="", stderr="ERROR: Could not install\n"),
        ):
            ok, output = install_package()
            assert ok is False
            assert "ERROR" in output
            assert capsys.readouterr().err == "ERROR: Could not install\n"

    def test_windows_autorun_skips_pip(self, monkeypatch):
        """On Windows during autorun, pip install is proactively skipped."""
        monkeypatch.setattr("sys.platform", "win32")
        monkeypatch.setenv("AGDT_SETUP_AUTORUN", "1")

        ok, output = install_package()
        assert ok is False
        assert "[WinError 32]" in output
