"""Tests for is_self_upgrade_lock."""

from agentic_devtools.cli.setup.script_generators.required_setup import is_self_upgrade_lock

_WINERROR_OUTPUT = (
    "ERROR: Could not install packages due to an OSError: [WinError 32] The process "
    "cannot access the file because it is being used by another process: "
    r"'c:\users\dev\appdata\roaming\python\python313\scripts\agdt-setup.exe'"
)


class TestIsSelfUpgradeLock:
    """Tests for is_self_upgrade_lock."""

    def test_detects_winerror_32_on_console_script(self):
        """The real Windows console-script lock is recognised."""
        assert is_self_upgrade_lock(_WINERROR_OUTPUT) is True

    def test_detects_message_without_winerror_code(self):
        """The prose form alone is enough when an .exe path is present."""
        assert is_self_upgrade_lock("used by another process: 'agdt-setup.exe'") is True

    def test_ignores_lock_without_executable_path(self):
        """A lock on a non-executable file is not a self-upgrade lock."""
        assert is_self_upgrade_lock("[WinError 32] ... used by another process: 'record'") is False

    def test_ignores_lock_on_other_executable(self):
        """A locked executable other than agdt-setup.exe stays fatal."""
        assert is_self_upgrade_lock("used by another process: 'python.exe'") is False

    def test_ignores_unrelated_failure(self):
        """Unrelated pip failures are not treated as a self-upgrade lock."""
        assert is_self_upgrade_lock("ERROR: No matching distribution found") is False

    def test_ignores_executable_path_without_lock(self):
        """An .exe path alone is not a self-upgrade lock."""
        assert is_self_upgrade_lock("Removing agdt-setup.exe") is False
