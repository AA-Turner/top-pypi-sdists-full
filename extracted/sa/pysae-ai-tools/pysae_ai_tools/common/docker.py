"""Docker daemon and registry-login probes shared across groups.

Runtime checks needed by more than one group: a reachable Docker daemon
(``install`` reports Docker's state, ``ci run-local`` decides whether it can run
a job in a container) and the registries the local Docker holds credentials for
(``install`` reports them, ``registry_auth`` checks whether the GitLab registry
login is posed). They live in ``common/`` so no group has to reach into another.
"""

import json
import shutil
import subprocess
from pathlib import Path

from . import winpath


def docker_config_path() -> Path:
    return Path.home() / ".docker" / "config.json"


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


def registry_logins() -> dict[str, str]:
    """Read ``~/.docker/config.json`` and report registries with stored auth or credHelper."""
    config = docker_config_path()
    if not config.exists():
        return {}
    try:
        data = json.loads(config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    out: dict[str, str] = {}
    for reg in data.get("auths") or {}:
        out[reg] = "auth"
    for reg, helper in (data.get("credHelpers") or {}).items():
        out[reg] = f"credHelper:{helper}"
    return out
