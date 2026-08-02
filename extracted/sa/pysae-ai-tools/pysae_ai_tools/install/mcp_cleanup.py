"""Clean up orphan MCP server processes left behind by dead Claude Code sessions.

When a Claude Code session dies (crash, ``kill -9``, terminal closed without a
clean exit), the MCP server subprocesses it spawned get reparented to the
platform's init/launcher process:

- **Linux** — ``systemd --user`` if a user session is running, otherwise PID 1.
- **macOS** — ``launchd`` at PID 1.

The orphans stay alive forever, eating RAM (a single ``mongodb-mcp-server``
can hold ~1 GiB). After a few weeks of usage the host saturates and swaps
heavily.

This module detects/kills those orphans and runs the scheduled cleanup. The
``SessionEnd`` hook that triggers it now ships with the Pysae plugin
(``hooks/hooks.json``); this module only migrates away any legacy hook a prior
version wrote directly into ``~/.claude/settings.json``. The delay (default
30 s) is intentional: at ``SessionEnd`` time, the current session's MCP
processes are still children of the dying ``claude`` — we wait for the parent
to fully exit so the remaining MCPs get reparented (and thus classified as
orphans) or are already gone.

Scheduling uses a detached Python subprocess (``subprocess.Popen`` +
``start_new_session=True``) so the hook returns immediately and the cleanup
survives the parent ``claude`` process. Works on Linux and macOS with no
external scheduler dependency (no ``systemd-run``, no ``at``, no ``launchctl``).
"""

import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from ..common.fs import atomic_write_text

app = typer.Typer(help="Detect and kill orphan MCP server processes; manage the cleanup hook.")


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SETTINGS_PATH = Path.home() / ".claude" / "settings.json"

HOOK_EVENT = "SessionEnd"
# Substring matched against any existing hook command to detect ours. Kept
# loose so hooks installed under either command path (``env mcp-cleanup`` or
# ``tools mcp-cleanup``) are recognized.
HOOK_MARKER = "mcp-cleanup"
DEFAULT_DELAY_SECONDS = 30

SUPPORTED_PLATFORMS = ("Linux", "Darwin")

# Substrings used to identify MCP server processes. Matched against the full
# command line (basename + args). Any match is enough.
DEFAULT_MCP_PATTERNS: tuple[str, ...] = (
    "mcp-server",
    "chrome-devtools-mcp",
)


# ---------------------------------------------------------------------------
# Settings.json helpers (Claude Code hook configuration)
# ---------------------------------------------------------------------------


def _read_settings() -> dict[str, object]:
    if not SETTINGS_PATH.exists():
        return {}
    try:
        data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_settings(cfg: dict[str, object]) -> None:
    atomic_write_text(SETTINGS_PATH, json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")


def _find_hook(cfg: dict[str, object]) -> bool:
    hooks = cfg.get("hooks", {})
    if not isinstance(hooks, dict):
        return False
    session_end = hooks.get(HOOK_EVENT, [])
    if not isinstance(session_end, list):
        return False
    for group in session_end:
        if not isinstance(group, dict):
            continue
        for h in group.get("hooks", []):
            if isinstance(h, dict) and HOOK_MARKER in str(h.get("command", "")):
                return True
    return False


# ---------------------------------------------------------------------------
# Process discovery
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProcessInfo:
    pid: int
    ppid: int
    rss_kb: int
    command: str


def _find_user_systemd_pid() -> int | None:
    """Return the PID of ``systemd --user`` for the current user (Linux only).

    Returns ``None`` outside of a systemd-user session.
    """
    try:
        result = subprocess.run(
            ["pgrep", "-u", str(os.getuid()), "-nf", r"^/usr/lib/systemd/systemd --user"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        return None
    stdout = (result.stdout or "").strip()
    if not stdout:
        return None
    try:
        return int(stdout.splitlines()[0])
    except ValueError:
        return None


def _find_orphan_parent_pids() -> set[int]:
    """Return PIDs of the init/launcher processes that adopt orphans on this OS.

    - **macOS** — ``launchd`` at PID 1.
    - **Linux** — PID 1 (always), plus ``systemd --user`` if a user session
      is running (the common case on desktops; absent on bare servers).
    """
    system = platform.system()
    if system == "Darwin":
        return {1}
    if system == "Linux":
        pids: set[int] = {1}
        user_systemd = _find_user_systemd_pid()
        if user_systemd:
            pids.add(user_systemd)
        return pids
    return set()


def _list_processes() -> list[ProcessInfo]:
    """Snapshot of all running processes (pid, ppid, rss, full command).

    Uses POSIX-compatible ``ps`` flags so it works on both Linux and macOS
    (BSD ``ps``). The header row is skipped manually since ``--no-headers``
    is GNU-specific.
    """
    result = subprocess.run(
        ["ps", "-eo", "pid,ppid,rss,command"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    procs: list[ProcessInfo] = []
    for line in result.stdout.splitlines():
        parts = line.split(None, 3)
        if len(parts) < 4:
            continue
        try:
            pid = int(parts[0])
            ppid = int(parts[1])
            rss = int(parts[2])
        except ValueError:
            # Header row ("PID PPID RSS COMMAND") or malformed line — skip.
            continue
        procs.append(ProcessInfo(pid=pid, ppid=ppid, rss_kb=rss, command=parts[3]))
    return procs


def _find_orphan_mcp(
    parent_pids: set[int],
    patterns: tuple[str, ...] = DEFAULT_MCP_PATTERNS,
    extra_regex: str | None = None,
) -> list[ProcessInfo]:
    """Return MCP server processes whose parent is one of ``parent_pids``."""
    regex = re.compile(extra_regex) if extra_regex else None
    orphans: list[ProcessInfo] = []
    for proc in _list_processes():
        if proc.ppid not in parent_pids:
            continue
        matched = any(p in proc.command for p in patterns)
        if not matched and regex is not None:
            matched = bool(regex.search(proc.command))
        if matched:
            orphans.append(proc)
    return orphans


def _kill_processes(pids: list[int], grace_seconds: float = 3.0) -> tuple[list[int], list[int]]:
    """SIGTERM all pids, wait, SIGKILL the survivors. Return (terminated, killed)."""
    if not pids:
        return [], []
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    time.sleep(grace_seconds)
    terminated: list[int] = []
    killed: list[int] = []
    for pid in pids:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            terminated.append(pid)
            continue
        try:
            os.kill(pid, signal.SIGKILL)
            killed.append(pid)
        except ProcessLookupError:
            terminated.append(pid)
    return terminated, killed


# ---------------------------------------------------------------------------
# Public API (used by install/mcp_cleanup_hook.py)
# ---------------------------------------------------------------------------


def is_hook_installed() -> bool:
    """Return True if a legacy SessionEnd cleanup hook still lingers in ``~/.claude/settings.json``.

    The hook now ships with the plugin; a True here means a stale settings.json entry remains and
    should be migrated away."""
    return _find_hook(_read_settings())


def install_hook() -> str:
    """Strip the legacy SessionEnd cleanup hook from ``~/.claude/settings.json``.

    The plugin now ships this hook (``hooks/hooks.json``, auto-discovered while the plugin is
    enabled); a leftover settings.json entry would schedule the cleanup twice per session. Returns:
    - ``"migrated"`` — a legacy hook was removed
    - ``"already-migrated"`` — none present (no-op)
    """
    return "migrated" if uninstall_hook() == "removed" else "already-migrated"


def uninstall_hook() -> str:
    """Remove the SessionEnd cleanup hook.

    Returns ``"removed"`` or ``"not-configured"``.
    """
    cfg = _read_settings()
    if not _find_hook(cfg):
        return "not-configured"

    hooks = cfg.get("hooks", {})
    if isinstance(hooks, dict):
        session_end = hooks.get(HOOK_EVENT, [])
        if isinstance(session_end, list):
            filtered: list[object] = []
            for group in session_end:
                if not isinstance(group, dict):
                    filtered.append(group)
                    continue
                inner = group.get("hooks", [])
                if not isinstance(inner, list):
                    filtered.append(group)
                    continue
                kept = [h for h in inner if not (isinstance(h, dict) and HOOK_MARKER in str(h.get("command", "")))]
                if kept:
                    new_group = {**group, "hooks": kept}
                    filtered.append(new_group)
            if filtered:
                hooks[HOOK_EVENT] = filtered
            else:
                hooks.pop(HOOK_EVENT, None)

        if hooks:
            cfg["hooks"] = hooks
        else:
            cfg.pop("hooks", None)

    _write_settings(cfg)
    return "removed"


def cleanup_orphans(
    dry_run: bool = False,
    extra_regex: str | None = None,
) -> dict[str, object]:
    """Detect orphan MCP processes and (unless ``dry_run``) terminate them.

    Returns a dict with keys ``platform``, ``parent_pids``, ``orphans``
    (list of dicts), ``terminated`` (list of pids), ``killed`` (list of pids).
    """
    system = platform.system()
    result: dict[str, object] = {
        "platform": system,
        "parent_pids": [],
        "orphans": [],
        "terminated": [],
        "killed": [],
    }
    if system not in SUPPORTED_PLATFORMS:
        return result

    parent_pids = _find_orphan_parent_pids()
    result["parent_pids"] = sorted(parent_pids)
    if not parent_pids:
        return result

    orphans = _find_orphan_mcp(parent_pids, extra_regex=extra_regex)
    result["orphans"] = [{"pid": p.pid, "ppid": p.ppid, "rss_kb": p.rss_kb, "command": p.command} for p in orphans]

    if dry_run or not orphans:
        return result

    terminated, killed = _kill_processes([p.pid for p in orphans])
    result["terminated"] = terminated
    result["killed"] = killed
    return result


# ---------------------------------------------------------------------------
# Typer commands
# ---------------------------------------------------------------------------


@app.command()
def status() -> None:
    """Report whether a legacy SessionEnd cleanup hook is still in settings.json."""
    if is_hook_installed():
        print("HOOK: LEGACY (migrated on install)")
    else:
        print("HOOK: MIGRATED TO PLUGIN")


@app.command()
def install() -> None:
    """Migrate the SessionEnd hook out of ``~/.claude/settings.json`` (now shipped by the plugin)."""
    outcome = install_hook()
    if outcome == "already-migrated":
        print("HOOK: ALREADY MIGRATED")
        return
    print("HOOK: MIGRATED TO PLUGIN")


@app.command()
def uninstall() -> None:
    """Remove the SessionEnd cleanup hook from ``~/.claude/settings.json``."""
    outcome = uninstall_hook()
    if outcome == "not-configured":
        print("HOOK: NOT CONFIGURED")
        return
    print("HOOK: REMOVED")


@app.command()
def run(
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Report what would be killed without sending any signal."),
    ] = False,
    pattern: Annotated[
        str | None,
        typer.Option(
            "--pattern",
            help="Extra regex matched against the command line (added to the built-in patterns).",
        ),
    ] = None,
) -> None:
    """Detect and SIGTERM orphan MCP server processes.

    An orphan is a process whose parent is the platform's init/launcher
    process (= reparented after its original Claude Code session died) and
    whose command matches one of the known MCP patterns.
    """
    system = platform.system()
    if system not in SUPPORTED_PLATFORMS:
        print(f"SKIP: platform {system} not supported.", file=sys.stderr)
        raise typer.Exit(code=0)

    parent_pids = _find_orphan_parent_pids()
    if not parent_pids:
        print("SKIP: could not locate init/launcher PID.", file=sys.stderr)
        raise typer.Exit(code=0)

    orphans = _find_orphan_mcp(parent_pids, extra_regex=pattern)
    if not orphans:
        print("OK: no orphan MCP server.")
        return

    total_rss_mb = sum(p.rss_kb for p in orphans) / 1024
    print(f"FOUND: {len(orphans)} orphan(s), {total_rss_mb:.0f} MiB total")
    for proc in orphans:
        rss_mb = proc.rss_kb / 1024
        cmd = proc.command if len(proc.command) <= 100 else proc.command[:97] + "..."
        print(f"  pid={proc.pid} rss={rss_mb:6.1f}MiB {cmd}")

    if dry_run:
        print("DRY-RUN: no signal sent.")
        return

    terminated, killed = _kill_processes([p.pid for p in orphans])
    print(f"DONE: terminated={len(terminated)} sigkilled={len(killed)}")


@app.command()
def schedule(
    delay: Annotated[
        int,
        typer.Option(
            "--delay",
            help="Seconds to wait before running the cleanup.",
            min=5,
            max=600,
        ),
    ] = DEFAULT_DELAY_SECONDS,
) -> None:
    """Spawn a detached child that runs the cleanup after ``--delay`` seconds.

    Returns immediately. This is the command invoked by the ``SessionEnd`` hook
    — it lets the hook complete fast while a background process waits for the
    parent ``claude`` to fully exit before sweeping its orphans.
    """
    system = platform.system()
    if system not in SUPPORTED_PLATFORMS:
        print(f"SKIP: platform {system} not supported.", file=sys.stderr)
        raise typer.Exit(code=0)

    binary = shutil.which("pysae-ai-tools") or "pysae-ai-tools"
    subprocess.Popen(
        [binary, "env", "mcp-cleanup", "_run-after", "--delay", str(delay)],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
    )
    print(f"SCHEDULED: cleanup in {delay}s.")


@app.command(name="_run-after", hidden=True)
def _run_after(
    delay: Annotated[int, typer.Option("--delay", min=0, max=600)] = DEFAULT_DELAY_SECONDS,
) -> None:
    """Internal: sleep ``--delay`` seconds, then run the cleanup silently.

    Invoked exclusively by :func:`schedule` as the detached background worker.
    """
    time.sleep(delay)
    cleanup_orphans(dry_run=False)
