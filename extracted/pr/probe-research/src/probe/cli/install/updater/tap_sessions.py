"""which open sessions run an old tap (live daemons, the service's hosted taps), and whether they follow an update without a restart."""

from __future__ import annotations
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from probe.shared.harness.harnesses.kimi_code import live as kimi_live
from probe.cli.lifecycle import service_calls
from probe.cli.wizard.state.state import TAP_PLUGIN_ID
from probe.foundation.harness_registry import get_registry


# -- live capture daemons ---------------------------------------------------
#
# An update moves the tap a coding agent INSTALLS; it cannot move the daemon a
# running session already started. Each session runs its own capture daemon for
# as long as the session lives, the server shows a machine's OLDEST live tap,
# and researchers keep sessions alive for days. So a machine whose update
# worked can still report the old tap: anthrogen's dev pod and new-workspace's
# laptop both read tap 0.9.3 on 2026-10-07, each with a session born on 10-04
# (before its tap moved) still uploading, while the dev pod's own update report
# said its tap was current at 0.9.14. These find those daemons, so the report
# says why beside "current": the tap's detail, the printed line, `probe doctor`.

#: A capture daemon as `hooks/session-start.sh` spawns it:
#: `<python> -m tap watch --session-id <id> --cwd <dir> --plugin-root <root>
#: --transcript <path>` (`--transcript-dir <dir>` for Codex). Its wrapper's own
#: command line carries the same words with `"$SID"` quoted, which the id's
#: character class refuses. `tap start` spawns without `--plugin-root`, from the
#: tap installed now, so it is never the stale one this looks for.
_TAP_DAEMON = re.compile(
    r"-m tap watch --session-id (?P<sid>[A-Za-z0-9_.:-]+) (?:.*? )?"
    r"--plugin-root (?P<root>.+?) --transcript"
)
_VERSION_DIR = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class TapDaemon:
    session_id: str
    #: The plugin root it was started from (it may no longer exist: Codex
    #: replaces a plugin's folder when it updates it).
    root: str
    version: str | None


def _process_commands() -> list[str]:
    """This user's processes' full command lines: `ps`, else Linux's `/proc`.
    Empty when neither can be read (Windows, a sandbox)."""
    if not hasattr(os, "getuid"):
        return []
    uid = os.getuid()
    try:
        listing = subprocess.run(  # noqa: S603 - fixed binary, no shell
            ["ps", "-ww", "-U", str(uid), "-o", "command="],
            capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=5, check=False,
        )
        if listing.returncode == 0:
            return [line.strip() for line in listing.stdout.splitlines() if line.strip()]
    except (OSError, subprocess.SubprocessError):
        pass
    commands: list[str] = []
    try:
        entries = [entry for entry in os.scandir("/proc") if entry.name.isdigit()]
    except OSError:
        return []
    for entry in entries:
        try:
            if entry.stat().st_uid != uid:
                continue
            with open(os.path.join(entry.path, "cmdline"), "rb") as handle:
                raw = handle.read()
        except OSError:
            continue  # exited between the listing and the read
        text = raw.replace(b"\0", b" ").decode(errors="replace").strip()
        if text:
            commands.append(text)
    return commands


def _daemon_version(session_id: str, root: str) -> str | None:
    """The tap a daemon runs: its marketplace folder's name (Claude Code and
    Codex keep one folder per version), else the record its spawner left beside
    its pid file (taps 0.9.16+), else the manifest in its root."""
    name = Path(root).name
    if _VERSION_DIR.match(name):
        return name
    from probe.cli.capture import state as capture_state

    harnesses = [h for h in get_registry().all() if h.capture is not None]
    for harness in harnesses:
        record = capture_state._watcher_dir(harness.id) / f"{harness.capture.watcher_prefix}-watcher-{session_id}.version"  # noqa: SLF001
        try:
            text = record.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if text:
            return text
    for harness in harnesses:
        manifest_dir = (harness.plugin or {}).get("manifest_dir")
        if not manifest_dir:
            continue
        try:
            version = json.loads((Path(root) / manifest_dir / "plugin.json").read_text())["version"]
        except (OSError, ValueError, KeyError, TypeError):
            continue
        if isinstance(version, str):
            return version
    return None


def tap_daemons(commands: list[str] | None = None) -> list[TapDaemon]:
    """Every live capture daemon this user runs, one per session and root
    (from `commands`, a process listing already read, else `_process_commands`)."""
    found: dict[tuple[str, str], TapDaemon] = {}
    for command in _process_commands() if commands is None else commands:
        match = _TAP_DAEMON.search(command)
        if match is None:
            continue
        key = (match["sid"], match["root"])
        if key not in found:
            found[key] = TapDaemon(key[0], key[1], _daemon_version(*key))
    return list(found.values())


def hosted_taps(source: str) -> dict[str, str]:
    """`{session id: tap version}` for each session of `source` the Probe
    service records now: the tap the service LOADED, which every one of its
    recorders runs, whatever tap the session named when it asked. It loads one
    tap and keeps it until a session names a newer one, so after an update its
    sessions keep the old tap, and no `tap watch` command line shows it.

    From `service.status` alone (`recorders[].tap_version`, `harness`): a
    service too old to say which tap it loaded, or a recorder that names no
    agent, is left out rather than guessed at. Empty when no service answers:
    then nothing is recorded there."""
    rows = service_calls.recorders()
    found: dict[str, str] = {}
    for row in rows or []:
        sid, agent, version = row.get("sid"), row.get("harness"), row.get("tap_version")
        if row.get("alive") is False or agent != source:
            continue
        if isinstance(sid, str) and isinstance(version, str) and version:
            found[sid] = version
    return found


def stale_tap_daemons(source: str, installed: str | None) -> tuple[str, ...]:
    """The version each live capture daemon of `source` runs, for every one
    older than the tap `installed` now, oldest first: each session's own `tap
    watch` (a daemon is `source`'s when it was started from a folder under
    that agent's home), and each session the Probe service records on the tap
    it loaded (`hosted_taps`), one per session. NEVER RAISES: an observation
    for the report, never a reason an update fails (what could not be looked
    at counts as none here)."""
    return _stale(source, installed, strict=False) or ()


def stale_tap_sessions(source: str, installed: str | None) -> tuple[str, ...] | None:
    """`stale_tap_daemons`, or None when this process could not look: no
    process listing could be read (this process is always in one, so an empty
    listing is an unreadable one: Windows, a sandbox without `ps` or `/proc`),
    the agent's home is unknown, or the look failed. For a claim made to a
    person (`settle_stale_notes`, doctor's warning), where "could not look"
    must never read as "none left". Never raises."""
    return _stale(source, installed, strict=True)


def _stale(source: str, installed: str | None, *, strict: bool) -> tuple[str, ...] | None:
    if not installed:
        return ()
    try:
        harness = get_registry().get(source)
        home = harness.home_dir() if harness is not None else None
        if home is None:
            return None if strict else ()
        home = home.resolve()
        commands = _process_commands()
        if strict and not commands:
            return None
        running: dict[str, str] = {}
        stale = []
        for daemon in tap_daemons(commands):
            if daemon.version and Path(daemon.root).resolve().is_relative_to(home):
                running.setdefault(daemon.session_id, daemon.version)
                if is_newer(installed, daemon.version):
                    stale.append(daemon.version)
        try:
            hosted = hosted_taps(source)
        except Exception:  # noqa: BLE001 - the daemons above are still worth reporting
            if strict:
                return None
            hosted = {}
        for sid, version in hosted.items():
            # A session whose own `tap watch` still holds it is counted above
            # (the service's recorder waits for that one to let go).
            if sid not in running and is_newer(installed, version):
                stale.append(version)
        return tuple(sorted(stale, key=lambda v: _triplet(v) or (0, 0, 0)))
    except Exception:  # noqa: BLE001 - see the docstrings
        return None if strict else ()


#: The first tap whose `tap watch` hands its session to the Probe service
#: (`hooks/tap_handover.py` HANDBACK_TAP), and the first on protocol 2, which
#: the prompt hook can move at all (PROTOCOL2_TAP).
HANDBACK_TAP = "0.10.13"
PROTOCOL2_TAP = "0.4.5"
def _harness_can(source: str, capability: str) -> bool:
    """Does the registry row `source` names have `capability`? False for a
    name the registry does not know."""
    harness = get_registry().find(source)
    return harness is not None and harness.can(capability)


def _ledger_user_scope(plugin_ids: tuple[str, ...]) -> bool:
    """Is every install Claude Code's ledger records for these plugins user
    scope, with the first of them installed at all? A project-scoped install
    serves its project only, and an open session's hooks never hand over to
    it (`dispatch.installed_root`)."""
    path = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    try:
        plugins = json.loads(path.read_text()).get("plugins") or {}
        if not plugins.get(plugin_ids[0]):
            return False
        return all(
            isinstance(entry, dict) and entry.get("scope") == "user"
            for plugin_id in plugin_ids
            for entry in plugins.get(plugin_id) or []
        )
    except Exception:  # noqa: BLE001 - unreadable: unproven, so the restart line
        return False


def _windows() -> bool:
    return os.name == "nt"


def _recording_now() -> set:
    """The sessions the running Probe service records now: its recorders whose
    loop holds the session's claim (`service.status`). Empty when none answers."""
    rows = service_calls.recorders()
    return {r["sid"] for r in rows or [] if r.get("alive") is True and r.get("recording") is True and r.get("sid")}


def follows_without_restart(
    source: str, result: PluginResult, tap_after: str | None = None, *, predicting: bool = False
) -> bool:
    """Do this agent's open sessions follow the update with no restart, so
    "no restart needed" is true? Only for an agent whose open sessions follow
    updates (the registry's `follows_updates`: Claude Code, Codex, Kimi Code;
    one that keeps its manifest from its start, `loaded_records`, only when every
    live process's record proves it loaded what is installed now:
    `kimi_live.sessions_follow`), not on
    Windows (the prompt hook leaves its sessions alone: no Git Bash pid can be
    proven there, `tap_handover.watchers_movable`), every install at user scope
    where the agent's ledger has scopes (`scoped_installs`: Claude Code's), a
    tap that hands its sessions
    to the Probe service (`tap_after`, default the one installed now:
    HANDBACK_TAP or later, or none at all) and every session still on an
    older tap on protocol 2 (PROTOCOL2_TAP), which the prompt hook can move:
    that hook ships in the Probe plugin (`result.after`), so a watcher from
    before the hand-back follows only where it is installed (a session the
    service records moves with the service). Anything else keeps the restart
    line. `predicting`: asked before the release is installed (the manual
    update line); an agent whose proof reads what is installed now
    (`loaded_records`, and pi's pins) then never follows. Never raises."""
    try:
        from probe.foundation.harness_registry.harness_registry import (
            CAPABILITY_FOLLOWS_UPDATES,
            CAPABILITY_LOADED_RECORDS,
            CAPABILITY_SCOPED_INSTALLS,
            FAMILY_EXTENSION,
        )

        if not _harness_can(source, CAPABILITY_FOLLOWS_UPDATES) or _windows():
            return False
        harness_row = get_registry().find(source)
        if harness_row is not None and harness_row.family == FAMILY_EXTENSION:
            # pi: its shim switches to the pinned version at a session's next
            # turn; proven per live pi process from its shim's record.
            from probe.shared.harness.harnesses.pi import pins as pi_pins

            if predicting or not pi_pins.sessions_follow((harness_row.binary,)):
                return False
        if _harness_can(source, CAPABILITY_LOADED_RECORDS):
            if predicting:
                return False
            harness = get_registry().find(source)
            titles = (getattr(harness, "process_title", None), getattr(harness, "binary", None))
            if harness is None or not kimi_live.sessions_follow(harness.id, titles, recorded=_recording_now()):
                return False
        if _harness_can(source, CAPABILITY_SCOPED_INSTALLS) and not _ledger_user_scope(
            (tracking_plugin_id(source), TAP_PLUGIN_ID)
        ):
            return False
        tap = result.tap_after if tap_after is None else tap_after
        if tap and is_newer(HANDBACK_TAP, tap):
            return False
        stale = result.tap_running_stale
        if not result.after and any(is_newer(HANDBACK_TAP, version) for version in stale):
            return False
        return not any(is_newer(PROTOCOL2_TAP, version) for version in stale)
    except Exception:  # noqa: BLE001 - see docstring
        return False
from probe.shared.harness.plugin_update import PluginResult, _triplet, is_newer, tracking_plugin_id  # noqa: E402 -- pieces need each other; the front door loads this one first
