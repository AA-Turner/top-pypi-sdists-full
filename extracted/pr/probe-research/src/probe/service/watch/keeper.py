"""the keeper's view with no service to ask: live sessions from the files, a report sent blocking."""

from __future__ import annotations
import json
import os
import subprocess
import time

from ...foundation.service_api import paths
from probe.service.watch.consent import Live, consent_env
from probe.service.watch.files import read_json
from probe.service.watch.settings import REPORT_READ, REPORT_TIMEOUT_S
#: Windows: no SIGTERM handler, and a logoff ends the service with no stop
#: record while the uptime-based boot id survives it, so a missing stop record
#: says nothing there; only a recorded crash (`last-crash.json`) is one.
WINDOWS = os.name == "nt"


# -- the keeper's view (no service to ask) ------------------------------------


def sessions_on_disk(now: float | None = None) -> list[Live]:
    """Every session whose agent runs, as the files say: `recorders.json`'s
    hosted sessions (with their environment) and `sessions.json`'s
    registrations, mode off included (with their `report_env`). For a process
    with no service to ask (the keeper). Never raises."""
    from ...foundation.service_api import procid
    from ..sessions.sessions import HEARTBEAT_TTL_S

    now = time.time() if now is None else now
    found: dict = {}
    recorded = read_json(paths.service_dir() / "recorders.json")
    for raw in (recorded.get("sessions") or []) if isinstance(recorded, dict) else []:
        if not isinstance(raw, dict) or not isinstance(raw.get("sid"), str):
            continue
        owner = raw.get("owner")
        try:
            if not isinstance(owner, dict) or procid.alive(int(owner["pid"]), str(owner["start_time"])) is False:
                continue
        except (KeyError, TypeError, ValueError):
            continue
        found[raw["sid"]] = Live(raw["sid"], hosted_env=consent_env(raw.get("env")) if isinstance(raw.get("env"), dict)
                                 else {})
    registered = read_json(paths.registry_path())
    for raw in (registered.get("sessions") or []) if isinstance(registered, dict) else []:
        if not isinstance(raw, dict) or not isinstance(raw.get("sid"), str) or raw["sid"] in found:
            continue
        owner = raw.get("owner")
        try:
            if owner is None:
                alive = now - float(raw.get("heartbeat_at") or 0) < HEARTBEAT_TTL_S
            else:
                alive = procid.alive(int(owner["pid"]), str(owner["start_time"])) is not False
        except (KeyError, TypeError, ValueError):
            continue
        if alive:
            value = raw.get("report_env")
            found[raw["sid"]] = Live(raw["sid"], report_env=value if isinstance(value, bool) else None)
    return list(found.values())


def _windowless() -> dict:
    """Windows: the keeper runs as pythonw, with no console at all, so a
    python.exe child would open a console window of its own for up to 60 s:
    it gets one with no window (`subprocess.CREATE_NO_WINDOW`, a Windows-only
    name). The service's children need no flag: the service itself runs in a
    console with no window (`client._DETACHED`), which they share."""
    return {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}


def report_blocking(params: dict, *, timeout: float = REPORT_TIMEOUT_S) -> tuple[int | None, object]:
    """`probe.core.run report` from a process with no event loop (the keeper):
    `(exit status, its one JSON value)`, `(None, None)` when killed at
    `timeout`. Raises OSError when it could not start."""
    from ..actions import children

    try:
        done = subprocess.run(  # noqa: S603 -- the CLI's own interpreter, our own module
            children.core_argv(REPORT_READ), input=json.dumps(params).encode("utf-8"), capture_output=True,
            timeout=timeout, cwd=str(paths.home()), check=False, **_windowless(),
        )
    except subprocess.TimeoutExpired:
        return None, None
    try:
        value = json.loads(done.stdout.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        value = None
    return done.returncode, value


def outcome(code: int | None, value: object) -> str:
    """One line for service.log: what the report child answered."""
    if code is None:
        return f"killed after {REPORT_TIMEOUT_S:.0f} s"
    if isinstance(value, dict):
        if value.get("sent"):
            return f"sent {value.get('id')}"
        if value.get("skipped"):
            return f"not sent: {value.get('skipped')}" + (f" (local copy {value['path']})" if value.get("path") else "")
    return f"failed (exit {code})"


#: `skipped` words the report child answers keeping its claim of the window.
KEPT_CLAIM = frozenset({"unauthorized", "too_large"})


def taken(value: object) -> bool:
    """Did the report child settle it: `sent`, or skipped as `deduped` or
    `disabled:*` (asking again would answer the same)?"""
    if not isinstance(value, dict):
        return False
    skipped = value.get("skipped")
    return bool(value.get("sent")) or skipped == "deduped" or (isinstance(skipped, str) and skipped.startswith("disabled:"))
