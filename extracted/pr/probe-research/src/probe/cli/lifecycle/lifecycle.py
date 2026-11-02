"""what runs around every command: classify the invoked command, gate each ask to one process per window, and run the before-command notices in order."""

from __future__ import annotations
import json
import os
import sys
import time
from pathlib import Path
from ...sdk.settings.settings import load_context


# Commands that must never trigger an upgrade, whatever the terminal looks like.
#
# These are the run-scoped writes a training loop makes. The TTY test alone does
# not cover them: `python train.py` started from a terminal passes its TTY down to
# every child, so `probe log` inside an interactive training run IS a TTY -- the
# check says "a human is present" in precisely the case where the hazard is worst.
#
# `exec` is here for the opposite reason: it does not run INSIDE a training loop,
# it OWNS one. It holds a run-lock flock for the wrapped process's whole life
# (see the exec command), so it is both barred from triggering and protected from
# being triggered on.
#
# Group name, not full path: Typer dispatches `probe run start` through the `run`
# group, and every subcommand under these groups is run-scoped.
_UPDATE_HOT_PATH_COMMANDS = frozenset({"log", "span", "artifact", "run", "exec", "outbox"})
#: Where the Probe service is the updater, these hot-path commands still ask it
#: for an update (`_hand_update_to_service`) when they do not run inside a run
#: (plan fool-proof-updates B3): no run in their environment (`_RUN_ENV`) and
#: no run lock held by their own process tree. A machine whose only Probe use
#: is `probe run ...`/`probe artifact ...` from a script is otherwise never
#: asked. `log`, `span` and `exec` never ask: they are a training loop's own
#: writes, or own the loop.
_ASK_OUTSIDE_A_RUN = frozenset({"artifact", "run", "outbox"})
#: What a run's own processes carry (`Run.subprocess`, `probe exec`, the
#: launchers): any of them set and this command is inside a run.
_RUN_ENV = ("PROBE_RUN_ID", "PROBE_RUN_EPOCH", "PROBE_EXEC_FINALIZES")
#: How far up the process tree a run lock's holder is looked for.
_RUN_ANCESTORS_MAX = 64

#: The commands that open the setup wizard (`npx probe-research` runs `wizard`).
#: The wizard's own server call (`POST /v1/device-state`) carries the manifest
#: and refreshes the cache, so a detached refresher would be a second request
#: for the same document in the same second.
_WIZARD_COMMANDS = frozenset({"wizard", "install"})

#: Machine interfaces own their side effects. Generic every-command notices
#: must not start updates or emit output around their bounded JSON replies.
_READ_ONLY_COMMANDS = frozenset({"status", "desktop"})


def _uninstall_invoked(command: str | None) -> bool:
    """`probe uninstall`, or `probe wizard --action uninstall`."""
    if command == "uninstall":
        return True
    if command != "wizard":
        return False
    args = sys.argv[1:]
    return "--action=uninstall" in args or any(
        token == "--action" and args[index + 1: index + 2] == ["uninstall"] for index, token in enumerate(args)
    )
#: `probe service ...` talks to the service itself: `probe service check-now` IS
#: the SessionStart hook's ask, and `probe service stop` must not start it again.
_SERVICE_COMMAND = "service"
#: Never act on that request from these. `daemon` and `mcp` run for a whole
#: session: an ask from one would wait out `WAIT_FOR_PID_S` for its own exit, and
#: the Probe service hands daemon workers over at an update anyway. The wizard and
#: the hidden `update` (an older plugin's SessionStart hook) ARE an update.
_REMOTE_UPDATE_SKIP_COMMANDS = frozenset(
    {_SERVICE_COMMAND, "daemon", "mcp", "update", *_WIZARD_COMMANDS}
)


#: Root options that consume the NEXT argv token as their value. Skipping the
#: flag but not its value is how `probe --base-url URL log` resolves to "URL" --
#: which is not in the denylist, so `log` would sail through the gate it exists
#: to stop. Flags (--async, --version) take no value and must NOT be listed.
_ROOT_OPTIONS_WITH_VALUES = frozenset({"--base-url", "--spool-dir"})


def _invoked_command() -> str | None:
    """The top-level command name from argv, or None.

    Read from argv rather than a Typer context because the root callback runs
    before dispatch -- there is no command context yet.

    Conservative by construction: an unrecognized `--opt value` form returns the
    value, which is not a known command, so the denylist does not match and the
    gate falls through to the RUN LOCK. Getting this wrong costs a redundant
    lock scan, never an upgrade into a live run.
    """
    import sys as _sys

    skip_next = False
    for token in _sys.argv[1:]:
        if skip_next:
            skip_next = False
            continue
        if token.startswith("--") and "=" in token:
            continue  # --base-url=URL carries its own value
        if token in _ROOT_OPTIONS_WITH_VALUES:
            skip_next = True
            continue
        if token.startswith("-"):
            continue
        return token
    return None


def _inside_a_run() -> bool:
    """Is this command part of a run: a run's variables in its environment
    (`_RUN_ENV`), or a run lock (`run_lock`'s flock tier, the SDK's and `probe
    exec`'s) held by this process or one of its ancestors? A run in another
    terminal is not this command's: the service decides about that one.
    Unknown reads as inside (nothing is asked). Cheap when no run holds a lock:
    one listing."""
    if any((os.environ.get(name) or "").strip() for name in _RUN_ENV):
        return True
    try:
        from probe.foundation.durable import run_lock

        directory = run_lock.runs_dir()
        if not directory.is_dir():
            return False
        holders: dict[int, Path] = {}
        for entry in directory.iterdir():
            if not entry.name.endswith(run_lock.FLOCK_SUFFIX):
                continue
            try:
                pid = int(json.loads(entry.read_text(encoding="utf-8"))["pid"])
            except (OSError, ValueError, TypeError, KeyError):
                continue  # mid-write, or left by a process long gone: no holder to find
            holders[pid] = entry
        if not holders:
            return False
        from probe.foundation.service_api import procid

        pid = os.getpid()
        for _ in range(_RUN_ANCESTORS_MAX):
            if pid in holders and run_lock._flock_is_held(holders[pid]):  # noqa: SLF001 -- its own probe
                return True
            proc = procid.proc(pid)
            if proc is None or proc.ppid <= 1 or proc.ppid == pid:
                return False
            pid = proc.ppid
        return False
    except Exception:  # noqa: BLE001 -- unknown: ask nothing from what may be a run
        return True


def _claim_window(stamp_name: str, every_s: float) -> bool:
    """Claim this window's one ask: True for the one process that may ask now.

    The window is claimed under an exclusive, non-blocking lock on the stamp
    (`stamp_name`, beside `autoupdate.json`: one byte once an ask is claimed, empty
    only before the first, and its mtime is the last ask), so a burst of commands
    starting together asks once; a command that finds
    the lock taken leaves the ask to its holder. Raises OSError when the stamp
    cannot be opened: the callers ask nothing then, since one asking process per
    command is worse than none."""
    from probe._shared import oscompat

    from probe.shared.updates import autoupdate

    stamp = autoupdate.state_dir() / stamp_name
    stamp.parent.mkdir(parents=True, exist_ok=True)
    with open(stamp, "a+b") as handle:
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        except OSError:
            return False  # another command is claiming this window
        # A stamp just created by this open has no ask behind it yet: its
        # size is the mark (one byte is written once an ask is claimed).
        age = time.time() - os.fstat(handle.fileno()).st_mtime
        if os.fstat(handle.fileno()).st_size and 0 <= age < every_s:
            return False
        handle.truncate(0)
        handle.write(b"1")
        handle.flush()
        os.utime(stamp)
    return True


def _repair_identity_is_the_files(settings) -> bool:
    """The token the CLI would use is the config file's current context's. A
    repair's credentials are written into that context (Claude Code's) and pinned
    to that context's API (every other agent's), so fetching under another token
    (`PROBE_TOKEN`) would hand one account's capture to another's context. The
    token alone decides: a URL override for the same token reaches the same
    account."""
    stored = load_context()
    # The token decides: the same token is the same account on the server that
    # sent the header, whatever URL reaches it (an in-cluster alias, a port).
    return bool(stored.get("token")) and settings.token == stored.get("token")
