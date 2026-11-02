"""what every OS scheduler shares: the unit's names and timings, running the manager, writing a unit file (the OsScheduler interface joins it in a later PR)."""

from __future__ import annotations
import os
import subprocess
from pathlib import Path
NAME = "probe-service-keeper"
LABEL = "ai.prbe.probe-service-keeper"
INTERVAL_S = 60
#: systemd's bound on one keeper run (`TimeoutStartSec`), past every bound the
#: wrapper keeps itself (its slowest path, every child at its limit, is ~25 min).
START_TIMEOUT_S = 30 * 60
TIMEOUT_S = 10


def _manager_env() -> dict:
    """The environment `systemctl --user` needs to find this user's manager:
    the service runs with a clean one (`client._clean_env`), without
    XDG_RUNTIME_DIR or the session bus, so they are filled in from
    `/run/user/<uid>` when that is this user's."""
    env = dict(os.environ)
    if hasattr(os, "getuid"):
        runtime = Path(env.get("XDG_RUNTIME_DIR") or f"/run/user/{os.getuid()}")
        try:
            if runtime.is_dir() and runtime.stat().st_uid == os.getuid():
                env["XDG_RUNTIME_DIR"] = str(runtime)
                bus = runtime / "bus"
                if "DBUS_SESSION_BUS_ADDRESS" not in env and bus.exists():
                    env["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path={bus}"
        except OSError:
            pass
    return env


def _run(argv: list[str]) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=TIMEOUT_S, check=False,
                              stdin=subprocess.DEVNULL, env=_manager_env())
    except (OSError, subprocess.SubprocessError):
        return None


def _write(path: Path, text: str) -> bool:
    """Write `text` when it differs. True when it changed."""
    try:
        if path.read_text(encoding="utf-8") == text:
            return False
    except OSError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)
    return True
