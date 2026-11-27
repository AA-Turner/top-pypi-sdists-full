import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path


def run_python(script: str, *args: str, cwd: Path, env: Mapping[str, str]) -> subprocess.CompletedProcess[str]:
    """Run ``script`` in a fresh interpreter, so import-time configuration starts from a clean process."""
    return subprocess.run(
        [sys.executable, "-c", script, *args],
        capture_output=True,
        check=False,
        cwd=cwd,
        env=dict(env),
        text=True,
        timeout=120,
    )
