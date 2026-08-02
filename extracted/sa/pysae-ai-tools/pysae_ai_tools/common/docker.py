"""Docker daemon probe shared across groups.

A runtime check for a reachable Docker daemon — needed both by ``install`` (to
report Docker's state) and by ``ci run-local`` (to decide whether it can run a
job in a container). It lives in ``common/`` so neither group has to reach into
the other.
"""

import shutil
import subprocess

from . import winpath


def daemon_running() -> bool:
    """True when a Docker daemon is reachable (``docker version`` succeeds)."""
    winpath.refresh_process_path_from_registry()
    if not shutil.which("docker"):
        return False
    r = subprocess.run(
        ["docker", "version", "--format", "{{.Server.Version}}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=5,
    )
    return r.returncode == 0 and bool(r.stdout.strip())
