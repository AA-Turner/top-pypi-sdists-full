"""the device's daily token counter every session's worker adds to, under a device-wide lock."""

from __future__ import annotations

import json
import os
import tempfile
import time
from pathlib import Path
from probe.daemon.store.store import state_dir


# -- the device's daily token counter (every session's worker adds to it) --


def device_path() -> Path:
    return state_dir() / "device.json"


def utc_day(now: float | None = None) -> str:
    """The counter's day: UTC, like the server's `daemon_spend_daily` meter."""
    return time.strftime("%Y-%m-%d", time.gmtime(time.time() if now is None else now))


#: The device counter keeps one total per lane: the writer's under its original
#: key (older CLIs read it), the reader's beside it, so a busy reader can never
#: trip the writer's daily fuse.
LANE_WRITE = "write"
LANE_READ = "read"
_LANE_KEYS = {LANE_WRITE: "tokens", LANE_READ: "read_tokens"}
#: `add_device_tokens` waits at most this long for the device-wide lock: it runs on
#: the event loop two lanes share, so a stalled holder must never freeze both.
DEVICE_LOCK_WAIT_S = 1.0


def _device_today(now: float | None = None) -> dict:
    try:
        data = json.loads(device_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict) or data.get("day") != utc_day(now):
        return {}
    return data


def device_tokens_today(now: float | None = None, lane: str = LANE_WRITE) -> int:
    return int(_device_today(now).get(_LANE_KEYS[lane], 0) or 0)


def add_device_tokens(n: int, lane: str = LANE_WRITE) -> None:
    """Add `n` to today's counter for `lane`, under a device-wide lock
    (`device.lock`) and through a temp file of its own: two sessions' workers
    never lose an update or rename each other's half-written file. The lock is
    waited for at most DEVICE_LOCK_WAIT_S; past that, TimeoutError (the caller
    counts it next time)."""
    from probe._shared import oscompat as fcntl  # fcntl.flock, or msvcrt on Windows

    if n <= 0:
        return
    path = device_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix(".lock").open("a") as lock:
        deadline = time.monotonic() + DEVICE_LOCK_WAIT_S
        while True:
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise TimeoutError("the device token counter is locked by another process")
                time.sleep(0.05)
        today = _device_today()
        counts = {key: int(today.get(key, 0) or 0) for key in _LANE_KEYS.values()}
        counts[_LANE_KEYS[lane]] += n
        fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump({"day": utc_day(), **counts}, handle)
            os.replace(tmp, path)
        except BaseException:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise
