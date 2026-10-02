"""`python -m probe.cli` runs the CLI (the daemon's fallback in `tools.probe_executable`)."""

import subprocess
import sys


def test_python_dash_m_probe_cli_runs_the_cli() -> None:
    done = subprocess.run(
        [sys.executable, "-m", "probe.cli", "--version"], capture_output=True, text=True, timeout=60
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith("probe ")
