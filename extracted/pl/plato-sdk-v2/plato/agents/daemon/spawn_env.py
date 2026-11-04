"""Login-equivalent environment for daemon-spawned processes.

Every SSH session re-read ``/etc/environment`` via PAM at login, and the
command lines prepended ``VM_PATH_EXPORT`` — so SSH-spawned work always saw
the CURRENT file and the full VM tool path. The daemon, by contrast, inherits
its bootstrap-time environ forever: anything written to ``/etc/environment``
after bootstrap (e.g. ``setup_agent_env`` racing the daemon start) would be
invisible to jobs, and the ordering of setup steps would suddenly matter where
it never did over SSH.

``login_env`` restores the SSH semantics: layer the current file over the
inherited environ (file wins — it is the newer truth), then prepend
``VM_PATH_PREFIX`` exactly like the export did. Callers still overlay the
per-request ``env`` on top, which wins over both.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path

from plato.utils.subprocess import VM_PATH_PREFIX

_ETC_ENVIRONMENT = Path("/etc/environment")


def parse_env_file(text: str) -> dict[str, str]:
    """Parse ``/etc/environment`` the way PAM does: ``KEY=VALUE`` lines,
    optional surrounding quotes, ``#`` comments; tolerates ``export`` prefixes."""
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if not sep:
            continue
        key = key.strip()
        if key.startswith("export "):
            key = key.removeprefix("export ").strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key:
            out[key] = value
    return out


def login_env(base: Mapping[str, str] | None = None, *, etc_environment: Path | None = None) -> dict[str, str]:
    """The env a fresh SSH login would see: ``base`` (default ``os.environ``)
    + current ``/etc/environment`` on top + ``VM_PATH_PREFIX`` prepended."""
    env = dict(os.environ if base is None else base)
    path_file = etc_environment if etc_environment is not None else _ETC_ENVIRONMENT
    try:
        env.update(parse_env_file(path_file.read_text()))
    except OSError:
        pass  # no file → no PAM contribution, same as a bare image
    current_path = env.get("PATH", "")
    env["PATH"] = f"{VM_PATH_PREFIX}:{current_path}" if current_path else VM_PATH_PREFIX
    return env
