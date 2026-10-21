"""Take down what Capy capture left on a machine: Capy support was removed.

A machine that connected Capy capture with an older CLI still has a timer
(launchd `ai.prbe.probe-capy-sync`, or the systemd user timer
`probe-capy-sync`) that runs `probe capy sync --quiet` every 10 minutes; a
Capy API key, a paired capture credential and the thread mirror under
`~/.local/state/probe/capy`; and an upload journal in the transcript state
folder. The timer runs whichever `probe` is installed, so after an update its
next tick lands HERE, and `probe wizard --action update` and sign-out call
`retire` too.

`retire` revokes the capture credential with the server it was paired to,
deletes the journal and the folder (the key goes with it), then removes the
timer, LAST: removing a launchd job stops the run that is doing it. Only those
fixed places: the removed row's override variables are never followed, so no
path from someone's environment is ever deleted. A crontab line is the
researcher's own, so it is named, never edited. Nothing here raises: an update
must never fail on this.

Hidden from `--help`. Delete once no supported CLI predates the removal.
"""

from __future__ import annotations

import contextlib
import json
import os
import platform
import shutil
import sqlite3
import subprocess
from collections.abc import Callable
from pathlib import Path

import typer

#: What the removed `probe capy connect` installed.
LAUNCHD_LABEL = "ai.prbe.probe-capy-sync"
TIMER_NAME = "probe-capy-sync"
#: The removed registry row's folder, relative to the home directory.
STATE_ROOT = ".local/state/probe/capy"

REMOVED = (
    "Capy support was removed from Probe: this machine's Capy capture, saved Capy key and sync timer are gone.",
    "In Capy, remove Probe's plugin (Settings > MCP & plugins) and any PROBE_TOKEN you set there, then revoke "
    "that Probe token (dashboard Settings) and the Capy API key you gave Probe (Capy Settings > API).",
)
NOT_REMOVED = "! Some of Capy's leftovers could not be removed ({}); `probe capy sync` tries again."
CRONTAB_HINT = "If your crontab runs `probe capy sync`, delete that line (`crontab -e`)."

capy_app = typer.Typer(hidden=True, help="Capy support was removed; this takes down what it left.")


def _root() -> Path:
    return Path.home() / STATE_ROOT


def _plugin_dir() -> Path:
    return _root() / "probe-research-tap"


def _launchd_plist() -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{LAUNCHD_LABEL}.plist"


def _systemd_units() -> list[Path]:
    base = os.environ.get("XDG_CONFIG_HOME")
    unit_dir = (Path(base) if base else Path.home() / ".config") / "systemd" / "user"
    return [unit_dir / f"{TIMER_NAME}{suffix}" for suffix in (".timer", ".service")]


def _present(path: Path) -> bool:
    try:
        return path.exists() or path.is_symlink()
    except OSError:
        return False


def leftovers() -> list[Path]:
    """What of Capy capture is still on this machine."""
    return [path for path in (_root(), _launchd_plist(), *_systemd_units()) if _present(path)]


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def _run(argv: list[str]) -> bool:
    try:
        return subprocess.run(argv, capture_output=True, timeout=30).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _revoke_capture_credential() -> None:
    """Tell the server the Capy capture device is gone, while its token is
    still on disk to authenticate with. The server is the one it was paired
    to (`capy.json`, then the capture config), never whatever this shell
    points Probe at. Offline leaves the device row in the dashboard's device
    list, never a credential anyone holds."""
    from .capabilities import probe_config_credentials, revoke_capture_token

    try:
        token = (_plugin_dir() / ".token").read_text(encoding="utf-8").strip()
    except (OSError, ValueError):
        return
    for candidate in (
        _read_json(_plugin_dir() / "capy.json").get("base_url"),
        _read_json(_plugin_dir() / ".config").get("api_base_url"),
        probe_config_credentials().get("base_url"),
    ):
        base_url = str(candidate or "").strip().rstrip("/")
        if token and base_url:
            revoke_capture_token(token, base_url)
            return


def _remove_journals(session_ids: set[str]) -> None:
    """The upload journal is one folder per (server, team, source) named by a
    hash, so Capy's is the one holding Capy's sessions (the mirror's file
    stems)."""
    from probe.tap_core.session_journal import state_root

    if not session_ids:
        return
    for folder in state_root().iterdir():
        database = folder / "state.sqlite3"
        if not database.is_file():
            continue
        try:
            with contextlib.closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as db:
                held = {row[0] for row in db.execute("SELECT session_id FROM sessions UNION SELECT session_id FROM pending")}
        except sqlite3.Error:
            continue
        if held & session_ids:
            shutil.rmtree(folder)


def _remove_state() -> None:
    root = _root()
    if root.is_symlink():
        root.unlink()
        return
    if not root.exists():
        return
    with contextlib.suppress(OSError):
        _remove_journals({path.stem for path in (root / "threads").glob("*.jsonl")})
    shutil.rmtree(root)


def _remove_timer() -> None:
    units = _systemd_units()
    if any(_present(unit) for unit in units):
        systemctl = platform.system() == "Linux" and shutil.which("systemctl")
        if systemctl:
            # Not `stop` on the service: it may be the run doing this.
            _run(["systemctl", "--user", "disable", "--now", f"{TIMER_NAME}.timer"])
        for unit in units:
            unit.unlink(missing_ok=True)
        if systemctl:
            _run(["systemctl", "--user", "daemon-reload"])
    plist = _launchd_plist()
    if _present(plist):
        plist.unlink(missing_ok=True)
        if platform.system() == "Darwin":
            _run(["launchctl", "remove", LAUNCHD_LABEL])


def retire() -> list[str]:
    """Remove every trace of Capy capture here. Never raises; returns what to
    tell the researcher (nothing when there was nothing to remove)."""
    try:
        if not leftovers():
            return []
        steps: tuple[Callable[[], None], ...] = (_revoke_capture_credential, _remove_state, _remove_timer)
        for step in steps:
            with contextlib.suppress(Exception):  # each step is best-effort; the next still runs
                step()
        left = leftovers()
    except Exception:  # noqa: BLE001 -- no home directory, say: nothing to report
        return []
    if left:
        return [NOT_REMOVED.format(", ".join(str(path) for path in left))]
    return list(REMOVED)


@capy_app.command("sync", hidden=True)
@capy_app.command("disconnect", hidden=True)
def sync_cmd(
    quiet: bool = typer.Option(False, "--quiet", hidden=True),  # noqa: ARG001 -- the old timer passes it
) -> None:
    """What the old Capy timer runs (and what the old docs said to run): take it down instead."""
    lines = retire()
    for line in lines:
        typer.echo(line)
    if lines:
        typer.echo(CRONTAB_HINT, err=True)
