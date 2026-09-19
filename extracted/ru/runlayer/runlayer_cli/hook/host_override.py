"""Hook host precedence on managed devices, plus the device-local deviation record.

On a device with an MDM ``Host`` the hook relay always targets that host:
``runlayer login <other-host>`` writes ``default_host`` to ``config.yaml`` and
must only steer interactive ``runlayer`` commands, never the hook traffic
(tool inputs/outputs, prompts, transcripts) the tenant admin provisioned the
device for. The org key travels with the managed host and nowhere else.

The ``aiwatch`` runtime already synthesizes ``default_host`` from MDM
(``config.load_config``), so it can never deviate. The full ``runlayer`` CLI
hook path (``runlayer hook``, ``python -m runlayer_cli.hook``) reads the YAML
and is the path this module exists for. When it observes a deviating
``default_host`` it records a marker under ``~/.runlayer/state`` that the
``aiwatch scan`` Detect check-in reports to the tenant; ``aiwatch`` itself
never reads the YAML, so it must never write or clear that marker.

Best-effort throughout: any read or write failure degrades to "no record",
never to a hook error.
"""

from __future__ import annotations

import contextlib
import json
import os
import stat
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict

from runlayer_cli.config import Config, hosts_equal, load_config, normalize_url
from runlayer_cli.mdm_config import ManagedConfig, read_managed_config
from runlayer_cli.paths import get_runlayer_dir
from runlayer_cli.runtime import is_aiwatch_runtime

# A marker older than this no longer reflects the hooks that currently fire
# on the device (the check-in reports it as absent). Matches the backend's
# 24h feature-freshness window so the badge and the device status age together.
MARKER_MAX_AGE_S = 24 * 3600.0
# Hooks fire dozens of times a minute under an agent; an unchanged marker is
# refreshed at most this often so the hot path pays one stat, not a write.
_REWRITE_INTERVAL_S = 3600.0

_STATE_FILENAME = "hook_host_override.json"
# Two hosts and a timestamp: anything bigger is not a record this module wrote.
_MARKER_MAX_BYTES = 4096
# Backend DTO bound for either host field.
_HOST_MAX_LEN = 255

_lock = threading.Lock()


class ResolvedHookHost(TypedDict):
    """Outcome of hook host resolution for one credential load."""

    # Host the hooks will POST to (managed host when present), or None.
    host: str | None
    managed_host: str | None
    user_host: str | None
    # Both hosts present and different: the user's ``default_host`` would have
    # redirected hooks off the managed host.
    overridden: bool


class HostOverride(TypedDict):
    """Wire shape of the deviation record carried by the Detect check-in."""

    user_host: str
    managed_host: str
    last_seen_at: str


def resolve_hook_host(config: Config, managed: ManagedConfig) -> ResolvedHookHost:
    """Managed host first, user ``default_host`` only on unmanaged devices.

    Both values are normalized (trailing slash stripped) so the MDM ``Host``,
    which skips ``set_host_credentials`` normalization, compares and builds
    URLs like a logged-in host does. The deviation check is case-insensitive
    on the host component (see :func:`runlayer_cli.config.hosts_equal`) so a
    pure case variant of the same backend is not a deviation.
    """
    raw_managed = managed.get("host")
    managed_host = normalize_url(raw_managed) if raw_managed else None
    user_host = normalize_url(config.default_host) if config.default_host else None
    return {
        "host": managed_host or user_host,
        "managed_host": managed_host,
        "user_host": user_host,
        "overridden": (
            managed_host is not None
            and user_host is not None
            and not hosts_equal(user_host, managed_host)
        ),
    }


def current() -> ResolvedHookHost | None:
    """The deviation the next credential load would observe, else ``None``.

    Fast ``None`` in the ``aiwatch`` runtime (it cannot deviate). On the
    full-CLI path this costs one small YAML read that ``relay._load_credentials``
    repeats moments later; that path has no daemon, so nothing to cache in.
    """
    if is_aiwatch_runtime():
        return None
    try:
        resolved = resolve_hook_host(load_config(), read_managed_config())
    except Exception:
        return None
    return resolved if resolved["overridden"] else None


def record(resolved: ResolvedHookHost) -> None:
    """Persist (or clear) the deviation marker from the hook path.

    No-op in the ``aiwatch`` runtime: it cannot see the YAML ``default_host``,
    so a clear from it would erase what a full-CLI hook legitimately recorded.
    """
    if is_aiwatch_runtime():
        return
    user_host = resolved["user_host"]
    managed_host = resolved["managed_host"]
    if resolved["overridden"] and user_host and managed_host:
        _record_override(user_host, managed_host)
    else:
        clear()


def read_marker(*, max_age_s: float = MARKER_MAX_AGE_S) -> HostOverride | None:
    """The fresh deviation record, or ``None`` when absent, stale or unreadable.

    Reads the current user's marker only: privileged scan fan-outs already run
    as (or with the home of) the user they report on. The open refuses
    symlinks and caps the read, since that file sits in a user-controlled
    directory.
    """
    try:
        raw = json.loads(_read_small_nofollow(_marker_path()))
        at = float(raw["at"])
        user_host = str(raw["user_host"])[:_HOST_MAX_LEN]
        managed_host = str(raw["managed_host"])[:_HOST_MAX_LEN]
    except Exception:
        return None
    age = time.time() - at
    if not (0 <= age < max_age_s):
        return None
    return {
        "user_host": user_host,
        "managed_host": managed_host,
        "last_seen_at": datetime.fromtimestamp(at, tz=timezone.utc).isoformat(),
    }


def clear() -> None:
    with contextlib.suppress(Exception):
        _marker_path().unlink()


def _state_dir() -> Path:
    return get_runlayer_dir() / "state"


def _marker_path() -> Path:
    return _state_dir() / _STATE_FILENAME


def _record_override(user_host: str, managed_host: str) -> None:
    with _lock:
        now = time.time()
        existing = _read_raw()
        if (
            existing is not None
            and existing.get("user_host") == user_host
            and existing.get("managed_host") == managed_host
            and 0 <= now - _at(existing) < _REWRITE_INTERVAL_S
        ):
            return
        _write({"at": now, "user_host": user_host, "managed_host": managed_host})


def _at(record_data: dict[str, object]) -> float:
    at = record_data.get("at")
    return float(at) if isinstance(at, (int, float)) else 0.0


def _read_raw() -> dict[str, object] | None:
    try:
        raw = json.loads(_read_small_nofollow(_marker_path()))
    except Exception:
        return None
    return raw if isinstance(raw, dict) else None


_READ_FLAGS = (
    os.O_RDONLY
    | getattr(os, "O_NOFOLLOW", 0)
    | getattr(os, "O_CLOEXEC", 0)
    # A FIFO planted at the marker path would park ``open`` until a writer
    # shows up; non-blocking open returns at once so the fstat below can
    # refuse it. No effect on a regular file.
    | getattr(os, "O_NONBLOCK", 0)
)


def _read_small_nofollow(path: Path) -> str:
    """Bounded read of a regular file in a user-controlled directory: no
    symlink follow, no blocking on special files, no unbounded read."""
    fd = os.open(path, _READ_FLAGS)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise OSError("marker is not a regular file")
        data = os.read(fd, _MARKER_MAX_BYTES)
    finally:
        os.close(fd)
    return data.decode("utf-8")


def _write(record_data: dict[str, object]) -> None:
    """Unique temp file + atomic replace (same contract as ``credential_state``)."""
    state_dir = _state_dir()
    path = _marker_path()
    tmp_path: str | None = None
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=state_dir, prefix=f"{path.name}.")
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(record_data))
        os.replace(tmp_path, path)
    except Exception:
        if tmp_path is not None:
            with contextlib.suppress(Exception):
                os.unlink(tmp_path)
