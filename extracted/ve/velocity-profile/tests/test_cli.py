import subprocess
import sys

from velocity_profile import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "velocity_profile", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
