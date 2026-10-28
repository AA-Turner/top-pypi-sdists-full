"""`probe uninstall`: Probe off this computer, leaving a clean slate (plan clean-uninstall-reinstall, PR U).

ONE implementation: `probe uninstall`, `probe wizard --action uninstall` (its
menu's Uninstall too) and the desktop app's Uninstall (`probe uninstall --yes
--json`, never a service action) all run `run()`. It goes through phases, each
recorded in the uninstall barrier (`S/uninstall/barrier.json`, S =
`~/.local/state/probe`) BEFORE it starts, so a run that is killed anywhere is
finished by running it again (C8):

    (scope)       who still uses this install, and are we inside a recorded
                  agent session: refuse (exit 2) unless --force (D2 = A)
    (plan)        the exact paths and server ids this uninstall owns
                  (`uninstall_plan`); a server it cannot reach refuses (exit 2)
                  before anything is touched, unless --offline
    planned       install lock taken (held to the very end, through the
                  finisher), plan and barrier written: from here nothing of
                  Probe's starts (`probe._shared.uninstall_barrier`)
    stopping      the keeper's units and the lifeboat FIRST (a deployed v2
                  lifeboat must not fire), then every Probe process
                  (`uninstall_procs`), verified gone
    draining      every outbox sent and every unsent note edit pushed
                  (`uninstall_notes`), bounded (DRAIN_BUDGET_S); what is still
                  unsent (queued writes, unsynced offline runs, transcript
                  queues, note edits) follows D1 = A: asked (delete / save a
                  backup file / cancel), never deleted silently; `--yes` stops
                  (exit 2) unless --discard-unsent
    server        this device's installation rows retired (a DELETE-scope
                  token: the daemon key, else the API token; 404 = done), THEN
                  every attributable credential revoked: each context's API and
                  MCP tokens, the daemon key, every capture key. A key the
                  server only DETACHED (another computer holds it) is reported.
                  The point of no return: from here the barrier stays LIVE
                  until the job is finished
    integrations  every coding agent with a trace of Probe (`uninstall_agents`)
    state         Probe's files for this user on this machine (C1, C4)
    finishing     this process BECOMES the stdlib finisher (`os.execv`, same
                  pid and terminal, run by the base interpreter, the install
                  lock's fd inherited), which deletes the CLI's env
                  generations and shims, then the barrier

Exit codes: 0 done, 2 refused (live users / inside a session / offline /
unsent research; nothing destroyed), 1 partial (the resume command printed).
A cancel or refusal before "server" puts everything back as it was: the
barrier goes, so the service and the keeper come back with the next session.
Only what THIS run wrote is called off (`Run.wrote_barrier`, and the barrier's
pid and start are this process's): a second run that is refused, or stopped
while it waits for the lock, leaves the first one's barrier and plan alone.
A run that RESUMED an earlier one never calls off: how far that one got is
unknown, so its barrier stays LIVE (phase "resuming" until "server") and the
run says the uninstall is half-done and how to finish it.
"""

from __future__ import annotations

import contextlib
import errno
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from probe._compat import StrEnum

EXIT_DONE = 0
EXIT_PARTIAL = 1
EXIT_REFUSED = 2
#: The drain's whole budget (plan: bounded, 60 s).
DRAIN_BUDGET_S = 60.0
#: How long a fresh uninstall waits for an update that holds the install lock.
LOCK_WAIT_S = 30.0
#: Transient server failures are tried this many times, this far apart.
SERVER_TRIES = 3
SERVER_RETRY_S = 1.0
BARRIER_VERSION = 1
TAIL_NAME = "tail.json"
FINISHER_NAME = "finisher.py"


class Phase(StrEnum):
    PLANNED = "planned"
    STOPPING = "stopping"
    DRAINING = "draining"
    SERVER = "server"
    INTEGRATIONS = "integrations"
    STATE = "state"
    FINISHING = "finishing"


PHASES = tuple(Phase)
#: The barrier's phase while a run that RESUMED an earlier one is before
#: "server": not a reversible phase, so LIVE to every reader whoever wrote it
#: (the earlier run may have got past the point of no return), and not one of
#: PHASES, so a rerun starts again from "stopping".
RESUMING = "resuming"


class UnsentChoice(StrEnum):
    DELETE = "delete"
    BACKUP = "backup"
    CANCEL = "cancel"


@dataclass
class Options:
    yes: bool = False
    force: bool = False
    offline: bool = False
    discard_unsent: bool = False
    #: D1 without a question: save the backup file, then go on (`--backup-unsent`).
    backup_unsent: bool = False
    json: bool = False
    #: A person can answer questions here (a TTY, no --yes).
    interactive: bool = False
    #: Finishing an interrupted uninstall for an installer that goes on after it
    #: (`finish_interrupted`): no result rows of its own in the installer's
    #: events, and the finisher runs in this process (no exec), keeping the env
    #: this process runs from.
    embedded: bool = False


class Reason(StrEnum):
    """Why a run ended with exit 2 or 1: the `--json` result's `reason.code`
    (`reason_record`), which the desktop app maps to its buttons."""

    UNSENT_RESEARCH = "unsent_research"  # D1: delete anyway / save a backup / cancel
    LIVE_USERS = "live_users"  # D2: stop them (--force) / cancel
    IN_SESSION = "in_session"  # run from inside a recorded agent session
    OFFLINE = "offline"  # remove from this computer only (--offline) / cancel
    BUSY = "busy"  # another Probe update or uninstall holds the install lock
    PARTIAL = "partial"  # past the point of no return: `resume` finishes it
    INTERRUPTED = "interrupted"  # a signal before "server": called off
    CANCELLED = "cancelled"  # a person said no (interactive runs only)
    CONFIRM = "confirm"  # no terminal to confirm in, and no --yes


class Stop(Exception):
    """End the run with `code` after `message` (a refusal or a partial run),
    for `reason` (its `detail` rides along in the `--json` result)."""

    def __init__(self, code: int, message: str, reason: Reason | None = None, detail: dict | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.reason = reason or (Reason.PARTIAL if code == EXIT_PARTIAL else None)
        self.detail = dict(detail or {})


@dataclass
class Run:
    options: Options
    plan: dict = field(default_factory=dict)
    lock_fd: int | None = None
    telemetry: object | None = None
    resumed: bool = False
    #: What the current phase has to say, printed as the phase ends (or stops).
    out: list = field(default_factory=list)
    #: `! ` lines so far: a removal that left something behind is not a clean one.
    warnings: int = 0
    started_at: float = field(default_factory=time.monotonic)
    #: The coding agents with a trace of Probe, as found before anything changed.
    agents: list = field(default_factory=list)
    #: What the stop phase stopped, said if the run is called off before "server".
    stopped: list = field(default_factory=list)
    #: THIS run wrote the barrier / the plan: a call-off undoes only what it wrote.
    wrote_barrier: bool = False
    wrote_plan: bool = False
    #: The phase this run is in (for a resumed run, from where it resumed).
    at: Phase | None = None
    #: What the drain step found still unsent (the refusal's advice reads it).
    unsent: Unsent | None = None


class Terminated(BaseException):
    """SIGTERM (or SIGHUP) arrived: end the run through its handlers."""

    def __init__(self, signum: int) -> None:
        super().__init__(signum)
        self.signum = signum


# -- output ------------------------------------------------------------------------------


def _say(text: str) -> None:
    print(text, flush=True)


def _step(name, status, message: str = "") -> None:
    from probe.core import events

    events.step(name, status, message)


def _lines(lines: list[str]) -> None:
    for line in lines:
        _say(f"  {line}" if not line.startswith("  ") else line)


# -- the barrier (the WRITER; `probe._shared.uninstall_barrier` is the one reader) ----------


def _write_barrier(run: Run, phase: str) -> None:
    """The barrier at `phase`, owned by this process: written ATOMICALLY every
    time (a temp file in the same folder, fsynced, renamed over it, the folder
    fsynced), 0600 in a 0700 folder. A reader never sees half a record (the
    frozen lifeboat v3 reads an unreadable one as LIVE). A resumed run writes
    RESUMING before "server": LIVE whoever wrote it."""
    from probe.service import paths, procid

    target = paths.uninstall_barrier_path()
    paths.private_dir(target.parent)
    record = {
        "v": BARRIER_VERSION,
        "pid": os.getpid(),
        "start": procid.start_time(os.getpid()) or "",
        "at": time.time(),
        "plan": str(paths.uninstall_plan_path()),
        "phase": str(phase),
        # A shared home: another machine's reader sees an owner it cannot
        # check, and counts it as running (`uninstall_barrier._other_machine`).
        "host": _hostname(),
        "machine_key": str(run.plan.get("machine_key") or paths.machine_key()),
    }
    tmp = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with open(fd, "w", encoding="utf-8") as handle:
            json.dump(record, handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, target)
        run.wrote_barrier = True
        if os.name == "posix":
            with contextlib.suppress(OSError):
                folder = os.open(target.parent, os.O_RDONLY)
                try:
                    os.fsync(folder)
                finally:
                    os.close(folder)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def _hostname() -> str:
    import socket

    try:
        return socket.gethostname()
    except OSError:
        return ""


def _is_self(record: dict) -> bool:
    """Did THIS process write `record` (this machine, this pid)?"""
    from probe._shared import uninstall_barrier as reader

    return record.get("pid") == os.getpid() and not reader._other_machine(record)  # noqa: SLF001


def _owner_runs(record: dict) -> bool:
    """Does the process that wrote this barrier still run (pid and start)? One
    on another machine sharing this home does, as far as this one can tell."""
    from probe._shared import uninstall_barrier as reader
    from probe.service import procid

    if reader._other_machine(record):  # noqa: SLF001 -- the reader's one rule for a shared home
        return True
    pid, start = record.get("pid"), record.get("start")
    if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 1 or not isinstance(start, str) or not start:
        return False
    return procid.alive(pid, start) is not False


def _owns_barrier(run: Run, record: object) -> bool:
    """Is `record` (the barrier on disk) the one THIS run wrote: its flag set,
    and the record's pid and start this process's? Anything else (another
    run's barrier, an unreadable one) is never called off from here."""
    from probe.service import procid

    if not run.wrote_barrier or not isinstance(record, dict):
        return False
    pid = os.getpid()
    return record.get("pid") == pid and record.get("start") == (procid.start_time(pid) or "")


def _drop_barrier() -> None:
    """Cancel before the point of no return: the uninstall's folder goes, so
    Probe starts again as it was (the keeper and lifeboat come back with the
    service's next start). Only for what this run wrote (`_owns_barrier`)."""
    from probe.service import paths

    shutil.rmtree(paths.uninstall_dir(), ignore_errors=True)


# -- scope (U-T2) -------------------------------------------------------------------------


def _scope(run: Run) -> None:
    from probe.cli import uninstall_procs
    from probe.core import events

    force = run.options.force
    here = uninstall_procs.recorded_session_here()
    if here is not None:
        # Never with --force either: an agent must not uninstall Probe from
        # under the session it runs in. A person does it, outside any session.
        _step(events.Step.UNINSTALL_SCOPE, events.Status.FAILED, "inside a recorded agent session")
        raise Stop(EXIT_REFUSED, (
            f"probe uninstall: this runs inside an agent session Probe records ({here}), which uninstalling would "
            "tear down under it. Nothing was changed. Run `probe uninstall` yourself, in a terminal outside "
            "any agent session."), Reason.IN_SESSION, {"session": here})
    users = uninstall_procs.live_users()
    if users and not force:
        listed = "\n".join(f"  - {u.label}" for u in users)
        _step(events.Step.UNINSTALL_SCOPE, events.Status.FAILED, f"{len(users)} live user(s) of this install")
        raise Stop(EXIT_REFUSED, (
            f"probe uninstall: Probe is still in use on this computer:\n{listed}\n"
            "Nothing was changed. End them, or run `probe uninstall --force` to stop them all and go on."),
            Reason.LIVE_USERS, {"users": [u.as_json() for u in users]})
    _step(events.Step.UNINSTALL_SCOPE, events.Status.DONE,
          f"{len(users)} live user(s), stopped by --force" if users else "nothing else uses this install")


def _confirm(run: Run) -> None:
    """Interactive only: what is about to happen, Keep first."""
    if not run.options.interactive:
        return
    from probe.cli import setup as wizard
    from probe.cli import tui

    with tui.window(enabled=True):
        tui.clear()
        answer = wizard.confirm_removal(tuple(run.agents), offline=run.options.offline)
    tui.leave_window()
    if answer is not True:
        _telemetry_declined(run)
        raise Stop(EXIT_REFUSED, "probe uninstall: nothing was changed.", Reason.CANCELLED)


# -- planning ------------------------------------------------------------------------------


def _server_ids(run: Run) -> dict | None:
    from probe.cli import uninstall_plan

    if run.options.offline:
        return None
    try:
        return uninstall_plan.server_ids()
    except uninstall_plan.Offline as exc:
        if run.resumed:
            raise Stop(EXIT_REFUSED, _offline_resumed(exc), Reason.OFFLINE, {"error": str(exc)}) from None
        raise Stop(EXIT_REFUSED, (
            f"probe uninstall: cannot reach Probe's server ({exc}), so this computer's sign-in could not be "
            "revoked. Nothing was changed. Try again when online, or run `probe uninstall --offline` to remove "
            "Probe from this computer only and revoke its keys yourself in the dashboard."),
            Reason.OFFLINE, {"error": str(exc)}) from None


def _take_lock(run: Run) -> None:
    from probe._shared import handoff
    from probe.cli import uninstall_plan

    root = uninstall_plan.primary_versions_root()
    if handoff.holds(root):
        return  # this process holds it already (an installer finishing an uninstall)
    if handoff.fcntl is None:
        return  # Windows: no install lock exists there, for any installer
    try:
        fd = handoff.take_lock(root, wait_s=LOCK_WAIT_S)
    except OSError as exc:
        # Never on without it: an install could switch the CLI under this run.
        raise Stop(EXIT_REFUSED, f"probe uninstall: the install lock ({handoff.lock_path(root)}) cannot be taken "
                                 f"({exc}); nothing was changed. Fix that, then run it again.",
                   Reason.BUSY, {"error": str(exc)}) from None
    if fd is None:
        if run.resumed:
            raise Stop(EXIT_REFUSED, "probe uninstall: another Probe update or uninstall is running; try again "
                                     "when it ends.", Reason.BUSY)
        raise Stop(EXIT_REFUSED, "probe uninstall: another Probe update or uninstall is running; nothing was "
                                 "changed. Try again when it ends.", Reason.BUSY)
    run.lock_fd = fd


def _plan(run: Run, server: dict | None) -> None:
    from probe.cli import uninstall_plan
    from probe.core import events

    run.plan = uninstall_plan.compute(server=server)
    run.wrote_plan = True  # from here the folder holds this run's plan (a call-off takes it)
    uninstall_plan.write(run.plan)
    gens = len(run.plan.get("env_generations", []))
    agents = len(run.plan.get("agent_edits", []))
    _step(events.Step.UNINSTALL_PLAN, events.Status.DONE,
          f"{len(run.plan['paths'])} path(s), {gens} CLI env(s), {agents} coding agent(s)")


# -- stopping (U-T3 first step, U-T4) --------------------------------------------------------


def _phase_stopping(run: Run) -> list[str]:
    from probe.cli import uninstall_procs
    from probe.core import events
    from probe.service import keeper, lifeboat

    lines = run.out
    # FIRST: a deployed (v2) lifeboat or the keeper's timer must not fire in
    # the middle of this (they do not know the barrier). No `keeper-off` left.
    keeper.remove(mark_off=False)
    lifeboat.remove()
    lines.append("Removed the keeper and the lifeboat.")
    # Nothing that lasts before the point of no return: the barrier alone keeps
    # taps and starters quiet until then (the killswitches are the
    # integrations phase's, the import jobs the state phase's).
    _finish_recorders(lines)
    survivors = uninstall_procs.stop_everything(run.plan, force=run.options.force, lines=lines,
                                                stopped=run.stopped)
    _step(events.Step.UNINSTALL_STOP, events.Status.FAILED if survivors else events.Status.DONE,
          f"{len(survivors)} Probe process(es) still running" if survivors else "every Probe process stopped")
    return lines


def _set_killswitches(lines: list[str]) -> None:
    """`.disabled` in every tap state folder that EXISTS (never made here): a
    session starting meanwhile does not start an uploader of its own."""
    from probe.cli import uninstall_agents

    for folder in uninstall_agents.tap_dirs():
        if folder.is_dir() and not folder.is_symlink():
            with contextlib.suppress(OSError):
                (folder / ".disabled").write_text("disabled by probe uninstall\n", encoding="utf-8")


def _finish_recorders(lines: list[str]) -> None:
    """Ask the service to finish what it records (its last pass ships the
    transcripts it holds) before it is stopped."""
    from probe.harness import get_registry
    from probe.service import client

    if client.connect(0.5) is None:
        return
    from probe.cli import service_calls

    for harness in get_registry().captured():
        with contextlib.suppress(Exception):
            service_calls.finish_recorders(harness.id)


# -- draining (U-T5, D1 = A) ----------------------------------------------------------------


@dataclass
class Unsent:
    ops: int = 0
    offline_runs: int = 0
    transcripts: int = 0
    #: Team-note and note edits never sent (`uninstall_notes`).
    notes: int = 0
    #: Session summary drafts never sent. Never sent from here (a draft is its
    #: session's to send), so a rerun online does not clear them: only
    #: --discard-unsent or the backup file does.
    drafts: int = 0
    sources: list = field(default_factory=list)
    #: Queued writes and offline runs in an outbox PROBE_OUTBOX_DIR names outside
    #: Probe's folders: kept (never deleted), so never part of the D1 question.
    kept: int = 0
    kept_dirs: list = field(default_factory=list)

    @property
    def sendable(self) -> int:
        """What a run online could still send (everything but the drafts)."""
        return self.ops + self.offline_runs + self.transcripts + self.notes

    @property
    def total(self) -> int:
        return self.sendable + self.drafts

    def describe_sendable(self) -> str:
        parts = []
        if self.ops:
            parts.append(f"{self.ops} queued write(s)")
        if self.offline_runs:
            parts.append(f"{self.offline_runs} offline run(s) never synced")
        if self.transcripts:
            parts.append(f"{self.transcripts} session transcript piece(s)")
        if self.notes:
            parts.append(f"{self.notes} unsynced note edit(s)")
        return ", ".join(parts)

    def describe(self) -> str:
        drafts = f"{self.drafts} unsent summary draft(s)" if self.drafts else ""
        return ", ".join(part for part in (self.describe_sendable(), drafts) if part)

    def as_json(self) -> dict:
        """The `unsent_research` reason's detail: counts per kind, and whether a
        rerun online could still send some of it (never the drafts)."""
        return {
            "counts": {"queued_writes": self.ops, "offline_runs": self.offline_runs,
                       "transcript_pieces": self.transcripts, "note_edits": self.notes,
                       "summary_drafts": self.drafts},
            "total": self.total,
            "sending_can_help": self.sendable > 0,
        }

    def held(self) -> str:
        """`this computer still holds ...`: the sendable part, then the drafts."""
        said = []
        if self.sendable:
            said.append(f"{self.describe_sendable()} that never reached Probe's server")
        if self.drafts:
            said.append(f"{self.drafts} summary draft(s), never sent (only the session that wrote a draft sends it)")
        return " and ".join(said)


def _journal_dirs() -> list[Path]:
    from probe.sdk.journal import Journal

    try:
        return list(Journal.discover())
    except Exception:  # noqa: BLE001
        return []


def drain(deadline: float, lines: list[str]) -> None:
    """Send every outbox (the default root, its `rank-*` queues, the $TMPDIR
    fallback; each per-credential queue), within `deadline`."""
    from probe.sdk.journal import Journal
    from probe.sdk.journal import drain as drain_journal
    from probe.sdk.transport import deadline_scope

    delivered = 0
    for directory in _journal_dirs():
        left = deadline - time.monotonic()
        if left <= 0:
            lines.append("! ran out of time sending the outbox")
            break
        try:
            with deadline_scope(deadline):
                report = drain_journal(Journal(directory), lock_timeout=min(5.0, left), promote_timeout=left)
            delivered += report.delivered
        except Exception as exc:  # noqa: BLE001 - what is left is counted below
            lines.append(f"! could not send {directory}: {type(exc).__name__}")
    if delivered:
        lines.append(f"Sent {delivered} queued write(s).")


def _sqlite_count(db: Path, table: str) -> int:
    if not db.is_file():
        return 0
    try:
        with contextlib.closing(sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=2)) as conn:
            row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()  # noqa: S608 - a fixed table name
    except sqlite3.Error:
        return 0
    return int(row[0]) if row else 0


def _deleted_here(path: Path) -> bool:
    """Is `path` in what the uninstall deletes: Probe's state folders, or a
    `$TMPDIR` fallback outbox? (An outbox PROBE_OUTBOX_DIR names elsewhere is kept.)"""
    from probe.cli import uninstall_plan
    from probe.sdk.journal import _fallback_roots

    path = Path(path)
    roots = [*uninstall_plan.state_roots(), *_fallback_roots()]
    return any(path == root or root in path.parents for root in roots)


def count_unsent() -> Unsent:
    """What is still on this computer, never reached the server, and would be
    deleted (`kept`: what an outbox outside Probe's folders keeps)."""
    from probe.cli import uninstall_agents
    from probe.sdk import offline
    from probe.sdk.journal import Journal, _fallback_roots, default_root

    found = Unsent()
    for directory in _journal_dirs():
        try:
            journal = Journal(directory)
            count = sum(len(q.pending()) + len(q.failed()) + len(q.waiting()) for q in journal.namespaces())
        except Exception:  # noqa: BLE001 - unreadable: counted as nothing, kept by the backup
            continue
        if not _deleted_here(directory):
            found.kept += count
            if count:
                found.kept_dirs.append(directory)
            continue
        found.ops += count
        found.sources.append(directory)
    roots = [default_root(), *_fallback_roots()]
    for root in roots:
        with contextlib.suppress(Exception):
            for run_dir in offline.find_offline_dirs(root):
                if offline.describe(run_dir).get("state") == "synced":
                    continue
                if not _deleted_here(run_dir):
                    found.kept += 1
                    found.kept_dirs.append(run_dir)
                    continue
                found.offline_runs += 1
                found.sources.append(run_dir)
    for folder in uninstall_agents.tap_dirs():
        rows = _sqlite_count(folder / "state.db", "outbox")
        if rows:
            found.transcripts += rows
            found.sources.append(folder / "state.db")
    with contextlib.suppress(Exception):
        from probe.tap_core import session_journal

        for db in sorted(session_journal.state_root().glob("*/state.sqlite3")):
            rows = _sqlite_count(db, "pending")
            if rows:
                found.transcripts += rows
                found.sources.append(db)
    with contextlib.suppress(Exception):
        from probe.cli import uninstall_notes

        for edit in uninstall_notes.unsynced():
            if edit.kind == uninstall_notes.SUMMARY:
                found.drafts += 1
            else:
                found.notes += 1
            found.sources.append(edit.path)
    found.sources = list(dict.fromkeys(found.sources))
    return found


def backup(unsent: Unsent) -> Path:
    """`~/probe-unsent-<date>.tar.gz` (0600) holding everything still unsent.
    Written to a hidden temp name in the same folder, fsynced, then put in
    place under its real name (never over an existing file): a Ctrl-C or a
    full disk never leaves a truncated archive that looks complete."""
    import tarfile

    stamp = time.strftime("%Y%m%d-%H%M%S")
    target = Path.home() / f"probe-unsent-{stamp}.tar.gz"
    tmp = target.with_name(f".{target.name}.{os.getpid()}.part")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as raw:
            with tarfile.open(fileobj=raw, mode="w:gz") as archive:
                for source in unsent.sources:
                    source = Path(source)
                    if source.exists():
                        name = os.path.relpath(source, Path.home()) if Path.home() in source.parents else source.name
                        archive.add(str(source), arcname=name)
            raw.flush()
            os.fsync(raw.fileno())
        _publish(tmp, target)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
    return target


def _publish(tmp: Path, target: Path) -> None:
    """`tmp` becomes `target`, never over an existing file (a hard link fails
    on one; a filesystem without links checks, then renames)."""
    try:
        os.link(tmp, target)
    except FileExistsError:
        raise
    except OSError:
        if os.path.lexists(target):
            raise FileExistsError(errno.EEXIST, "a backup of that name exists", str(target)) from None
        os.replace(tmp, target)


#: The D1 question's way out: a fresh run is called off; a resumed one stays half-done.
CANCEL_LABEL = "Cancel the uninstall"
STOP_HERE_LABEL = "Stop here (the uninstall stays half-done; run `probe uninstall` to finish)"


def _ask_unsent(unsent: Unsent, *, resumed: bool = False) -> UnsentChoice:
    from probe.cli import tui

    with tui.window(enabled=True):
        tui.clear()
        answer = tui.review(
            "Some of your research was never sent",
            tui.wrap(
                f"This computer still holds {unsent.held()}"
                + (", and sending them did not finish" if unsent.sendable else "")
                + ". Uninstalling deletes them from this computer; a backup file keeps them."),
            [(STOP_HERE_LABEL if resumed else CANCEL_LABEL, UnsentChoice.CANCEL),
             ("Save a backup file in your home folder, then uninstall", UnsentChoice.BACKUP),
             ("Delete them and uninstall", UnsentChoice.DELETE)],
        )
    tui.leave_window()
    return answer if isinstance(answer, UnsentChoice) else UnsentChoice.CANCEL


def _phase_draining(run: Run) -> list[str]:
    from probe.core import events

    lines = run.out
    deadline = time.monotonic() + DRAIN_BUDGET_S
    drain(deadline, lines)
    from probe.cli import uninstall_notes

    uninstall_notes.send(deadline, lines)  # the same budget: note edits are unsent work too
    unsent = count_unsent()
    run.unsent = unsent
    if unsent.kept:
        where = ", ".join(str(d) for d in dict.fromkeys(unsent.kept_dirs))
        lines.append(f"Kept {unsent.kept} unsent item(s) in the outbox PROBE_OUTBOX_DIR names ({where}): "
                     "nothing there is deleted; they send when Probe is installed again.")
    if not unsent.total:
        _step(events.Step.UNINSTALL_DRAIN, events.Status.DONE, "everything was sent")
        return lines
    _decide_unsent(run, unsent, lines)
    _step(events.Step.UNINSTALL_DRAIN, events.Status.DONE, f"unsent: {unsent.describe()}")
    return lines


def _decide_unsent(run: Run, unsent: Unsent, lines: list[str]) -> None:
    """The D1 rule for what is still unsent: --discard-unsent deletes it,
    --backup-unsent saves the backup file, an installer finishing an uninstall
    (embedded: nobody to ask) saves the backup file and says so, a person is
    asked, and anything else stops the run (exit 2)."""
    from probe.core import events

    if run.options.discard_unsent:
        lines.append(f"Deleting {unsent.held()} (--discard-unsent).")
    elif run.options.backup_unsent:
        _save_backup(unsent, lines, flag=True)
    elif run.options.embedded:
        _save_backup(unsent, lines, why="finishing an uninstall that had stopped, with nobody to ask")
    elif not run.options.interactive:
        _step(events.Step.UNINSTALL_DRAIN, events.Status.FAILED, f"unsent: {unsent.describe()}")
        raise Stop(EXIT_REFUSED,
                   f"probe uninstall: this computer still holds {unsent.held()}. {_unsent_advice(unsent)}",
                   Reason.UNSENT_RESEARCH, unsent.as_json())
    else:
        choice = _ask_unsent(unsent, resumed=run.resumed)
        if choice is UnsentChoice.CANCEL:
            raise Stop(EXIT_REFUSED, "probe uninstall: stopped here." if run.resumed else "probe uninstall: cancelled.",
                       Reason.CANCELLED)
        if choice is UnsentChoice.BACKUP:
            _save_backup(unsent, lines)
        else:
            lines.append(f"Deleting {unsent.held()}.")


def _recount_unsent(run: Run) -> None:
    """Right before "state" deletes Probe's files, in a run that did not decide
    D1 itself (it resumed past "draining"): what was queued since the earlier
    run stopped (a training run's writes) is counted, and the D1 rule applies
    to it. Nothing is sent from here: the server phase revoked the keys."""
    if run.unsent is not None:
        return
    unsent = count_unsent()
    run.unsent = unsent
    if unsent.total:
        _decide_unsent(run, unsent, run.out)


def _save_backup(unsent: Unsent, lines: list[str], *, flag: bool = False, why: str = "") -> None:
    """D1's "save a backup file, then uninstall" (asked, `--backup-unsent`, or
    an installer finishing an uninstall). A backup that cannot be written
    stops the run: nothing is deleted."""
    try:
        saved = backup(unsent)
    except OSError as exc:
        raise Stop(EXIT_REFUSED, f"probe uninstall: could not save the backup ({exc}).", Reason.UNSENT_RESEARCH,
                   {**unsent.as_json(), "backup_error": str(exc)}) from None
    said = " (--backup-unsent)" if flag else f" ({why})" if why else ""
    lines.append(f"Saved {unsent.describe()} to {saved}{said}.")


def _unsent_advice(unsent: Unsent) -> str:
    """What gets a `--yes` run past what is unsent. A rerun online sends the
    sendable part only: summary drafts are never sent from here."""
    flags = "Pass --backup-unsent to save them to a backup file first, or --discard-unsent to delete them"
    if not unsent.drafts:
        return f"Run it again once online so they are sent. {flags}."
    rest = (" Running it again online sends the rest, but never the drafts." if unsent.sendable
            else " Running it again online does not send them.")
    return f"{flags}.{rest}"


# -- server (U-T6) ---------------------------------------------------------------------------


class Released(StrEnum):
    REVOKED = "revoked"
    DETACHED = "detached"
    GONE = "gone"
    REFUSED = "refused"
    TRANSIENT = "transient"
    #: Every key was refused (401): this computer cannot say whether it was retired.
    UNAUTHORIZED = "unauthorized"


def _client(base_url: str, token: str):
    from probe.sdk.client import Client
    from probe.sdk.config import Settings
    from probe.sdk.surface import Surface

    return Client(settings=Settings(base_url=base_url, token=token), async_writes=False, surface=Surface.CLI.value)


def _with_retries(call):
    """`call()` with transient failures tried SERVER_TRIES times. Returns
    (Released or None, answer, error)."""
    from probe.cli import uninstall_plan
    from probe.sdk import errors

    last = None
    for attempt in range(SERVER_TRIES):
        try:
            return None, call(), None
        except (errors.AuthError, errors.NotFoundError) as exc:
            return Released.GONE, None, exc
        except errors.ScopeError as exc:
            return Released.REFUSED, None, exc
        except Exception as exc:  # noqa: BLE001
            last = exc
            if not uninstall_plan.transient(exc):
                return Released.REFUSED, None, exc
            if attempt + 1 < SERVER_TRIES:
                time.sleep(SERVER_RETRY_S * (attempt + 1))
    return Released.TRANSIENT, None, last


def release(token: str, base_url: str) -> tuple[Released, list[str]]:
    """Revoke one API/MCP/daemon credential of this device (`DELETE
    /v1/tokens/current`, device-aware: a key another computer also holds is
    only detached from this one)."""

    def call():
        with _client(base_url, token) as client:
            return client.logout()

    outcome, result, _error = _with_retries(call)
    if outcome is not None:
        return outcome, []
    if isinstance(result, dict) and result.get("detached") and not result.get("revoked"):
        return Released.DETACHED, [str(n) for n in (result.get("still_used_by") or [])]
    return Released.REVOKED, []


def retire(ids: list[str], tokens: list[str], base_url: str) -> tuple[Released, str]:
    """Retire this device's rows with the first key that may (DELETE scope).
    REVOKED: retired now. GONE: the server has nothing live left to retire
    (404), done. TRANSIENT: no answer; the rerun retires first. UNAUTHORIZED:
    every key was refused (401), so nothing here can tell whether the rows were
    retired (an earlier run's lost answer did, and revoked the keys with them):
    the person removes it in the dashboard. REFUSED: a key without the scope."""
    if not ids:
        return Released.GONE, ""
    unauthorized = False
    error = ""
    for token in tokens:

        def call(token=token):
            with _client(base_url, token) as client:
                return client.retire_client_installations(ids)

        result, _answer, exc = _with_retries(call)
        if result is None:
            return Released.REVOKED, ""
        if result is Released.TRANSIENT:
            return result, str(exc)
        if result is Released.GONE and getattr(exc, "status", None) == 404:
            return Released.GONE, ""
        if result is Released.GONE:
            unauthorized = True  # a refused key: try the next one
        error = str(exc)
    return (Released.UNAUTHORIZED if unauthorized else Released.REFUSED), error


def _capture_tokens(run: Run) -> list[tuple[str, str, str]]:
    """(what, token, base_url) for every capture key this device holds: each
    agent's paired `.token` and every context's `ingest_token`."""
    from probe.cli import uninstall_agents, uninstall_plan

    out = []
    for folder in uninstall_agents.tap_dirs():
        try:
            token = (folder / ".token").read_text(encoding="utf-8").strip()
        except OSError:
            continue
        config = {}
        with contextlib.suppress(OSError, ValueError):
            config = json.loads((folder / ".config").read_text(encoding="utf-8"))
        base = str((config or {}).get("api_base_url") or "").rstrip("/")
        if token:
            out.append((f"the capture key in {folder}", token, base))
    for name, ctx in uninstall_plan.contexts().items():
        if ctx.get("ingest_token"):
            out.append((f"the capture key of account “{name}”", str(ctx["ingest_token"]),
                        uninstall_plan._base_url(ctx)))  # noqa: SLF001
    seen, unique = set(), []
    for item in out:
        if item[1] not in seen:
            seen.add(item[1])
            unique.append(item)
    return unique


def _dashboard_hint(base_url: str | None = None) -> str:
    from probe.sdk.links import dashboard_base_url

    try:
        base = dashboard_base_url(base_url)
    except Exception:  # noqa: BLE001
        base = None
    return f"{base}/settings" if base else "the dashboard's Settings › Connected clients"


def preflight_server(run: Run) -> None:
    """Right before the point of no return: is every context's server
    reachable? Not: refuse (nothing destroyed yet), unless --offline."""
    from probe.cli import uninstall_plan

    if run.options.offline or (run.plan.get("server") or {}).get("offline"):
        return
    try:
        uninstall_plan.server_ids()
    except uninstall_plan.Offline as exc:
        if run.resumed:
            raise Stop(EXIT_REFUSED, _offline_resumed(exc), Reason.OFFLINE, {"error": str(exc)}) from None
        raise Stop(EXIT_REFUSED, (
            f"probe uninstall: cannot reach Probe's server ({exc}). Nothing was revoked. Try again when online, "
            "or run `probe uninstall --offline` to remove Probe from this computer only."),
            Reason.OFFLINE, {"error": str(exc)}) from None


def _offline_resumed(exc: Exception) -> str:
    return (f"probe uninstall: cannot reach Probe's server ({exc}), so the uninstall cannot be finished yet: "
            "come back online, or run `probe uninstall --offline` to finish locally (then revoke this computer's "
            "keys yourself in the dashboard).")


def _phase_server(run: Run) -> list[str]:
    from probe.cli import capy_retire, uninstall_plan
    from probe.cli.capabilities import revoke_capture_token
    from probe.core import events

    lines = run.out
    server = run.plan.get("server") or {}
    if run.options.offline or server.get("offline"):
        hint = _dashboard_hint()
        lines.append(f"! offline: nothing was revoked on the server. Revoke this computer's keys in {hint}.")
        _step(events.Step.UNINSTALL_SERVER, events.Status.SKIPPED, f"offline: revoke this computer in {hint}")
        return lines
    transient: list[str] = []
    planned = server.get("contexts") or {}
    held = uninstall_plan.contexts()
    for name in sorted(set(planned) | set(held)):
        ctx = held.get(name) or {}
        base_url = (planned.get(name) or {}).get("base_url") or uninstall_plan._base_url(ctx)  # noqa: SLF001
        ids = list((planned.get(name) or {}).get("installation_ids") or [])
        delete_tokens = [str(t) for t in (ctx.get("companion_token"), ctx.get("token")) if t]
        if ids and delete_tokens:
            outcome, error = retire(ids, delete_tokens, base_url)
            if outcome is Released.REVOKED:
                lines.append(f"Retired this computer in account “{name}” ({base_url}).")
            elif outcome is Released.TRANSIENT:
                # Its keys stay: the rerun retires with them first.
                transient.append(f"retiring this computer in “{name}” ({error})")
                continue
            elif outcome in (Released.UNAUTHORIZED, Released.REFUSED):
                lines.append(f"! could not retire this computer in “{name}” ({error or 'its keys were refused'}); "
                             f"remove this computer under Settings > Connected clients ({_dashboard_hint(base_url)}).")
        for key, what in (("token", "API token"), ("mcp_token", "read-only MCP token"),
                          ("companion_token", "Probe daemon key")):
            token = ctx.get(key)
            if not token:
                continue
            outcome, others = release(str(token), base_url)
            label = f"the {what} of account “{name}”"
            if outcome is Released.REVOKED:
                lines.append(f"Revoked {label}.")
            elif outcome is Released.DETACHED:
                lines.append(f"Disconnected {label} from this computer; it stays in use on {len(others)} other "
                             f"device(s){': ' + ', '.join(others[:3]) if others else ''}.")
            elif outcome is Released.TRANSIENT:
                transient.append(f"revoking {label}")
            elif outcome is Released.REFUSED:
                lines.append(f"! could not revoke {label}; revoke it in {_dashboard_hint(base_url)}.")
    for what, token, base in _capture_tokens(run):
        answer = revoke_capture_token(token, base or uninstall_plan._base_url({}))  # noqa: SLF001
        if answer is None:
            transient.append(f"revoking {what}")
        elif answer:
            lines.append(f"Revoked {what}.")
    lines.extend(capy_retire.retire())
    from probe.cli.setup import _env_credential_warnings

    lines.extend(_env_credential_warnings())
    if transient:
        _step(events.Step.UNINSTALL_SERVER, events.Status.FAILED, "; ".join(transient))
        raise Stop(EXIT_PARTIAL, (
            "probe uninstall: Probe's server did not answer while " + "; ".join(transient) + ". Run "
            "`probe uninstall` again to finish (or `probe uninstall --offline` to finish locally and revoke the "
            f"rest in {_dashboard_hint()})."))
    _step(events.Step.UNINSTALL_SERVER, events.Status.DONE, "this computer retired, its keys revoked")
    return lines


# -- integrations (U-T7) -----------------------------------------------------------------------


def _phase_integrations(run: Run) -> list[str]:
    from probe.cli import uninstall_agents
    from probe.core import events
    from probe.harness import get_registry

    lines = run.out
    _set_killswitches(lines)  # past the point of no return: no session starts an uploader of its own
    registry = get_registry()
    agents = [edit.get("agent") for edit in run.plan.get("agent_edits", [])]
    agents += [a for a in uninstall_agents.all_traces() if a not in agents]
    failed = 0
    for agent in agents:
        harness = registry.find(agent)
        if harness is None:
            continue
        removed = uninstall_agents.remove(harness)
        left = {k: v for k, v in uninstall_agents.traces(harness).items() if k != "capture"}
        failed += bool(left)
        lines.append(f"{harness.label}:")
        lines.extend(f"  {line}" for line in removed)
        plugins = set(left.get("plugins", []))
        from probe.cli.capabilities import TAP_PLUGIN_NAME

        if run.options.embedded:
            continue
        events.agent_result(
            agent,
            requested={"tracking": False, "capture": False, "agent_rules": False},
            actual={
                "tracking": any(TAP_PLUGIN_NAME not in p for p in plugins) or bool(left.get("skills")),
                "capture": any(TAP_PLUGIN_NAME in p for p in plugins),
                "agent_rules": bool(left.get("rules")),
            },
            ok=not left,
            message="\n".join(line for line in removed if line.startswith("!")),
        )
    lines.extend(uninstall_agents.remove_hollow())  # what Probe's install left that now holds nothing
    _step(events.Step.UNINSTALL_INTEGRATIONS, events.Status.FAILED if failed else events.Status.DONE,
          f"{len(agents)} coding agent(s)" + (f", {failed} with something left" if failed else ""))
    if failed:
        raise Stop(EXIT_PARTIAL, (
            f"probe uninstall: Probe is still in {failed} coding agent(s) (the lines above say what and where). "
            "Fix that, then run `probe uninstall` again to finish."))
    return lines


# -- state (U-T8) --------------------------------------------------------------------------------


def _remove_path(path: Path) -> bool:
    """Remove one path, never through a symlink. True when it is gone."""
    if not os.path.lexists(path):
        return True
    try:
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)
    except FileNotFoundError:
        return True
    except OSError:
        return False
    return True


def standard_folders() -> set:
    """Folders an uninstall never removes, empty or not: HOME, its XDG and
    `~/.local` folders, and every coding agent's home."""
    home = Path.home()
    found = {home, home / ".config", home / ".cache", home / ".local", home / ".local" / "state",
             home / ".local" / "share", home / ".local" / "bin"}
    for name in ("XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_STATE_HOME", "XDG_DATA_HOME", "XDG_BIN_HOME"):
        if os.environ.get(name):
            found.add(Path(os.environ[name]))
    with contextlib.suppress(Exception):
        from probe.harness import get_registry

        found.update(h.home_dir() for h in get_registry().all() if h.home_dir() is not None)
    return found


def prune_empty_parents(path: Path, stop: Path | None = None) -> None:
    """rmdir `path`'s parents while they are empty: the folders Probe's files
    were the only reason for (`.../plugins/marketplaces/` around Probe's clone).
    Never a standard folder (`standard_folders`), never `stop`, never above
    HOME; a folder with anything in it stays."""
    keep = standard_folders()
    if stop is not None:
        keep.add(Path(stop))
    home = Path.home()
    for parent in Path(path).parents:
        if parent in keep or home not in parent.parents:
            return
        try:
            parent.rmdir()
        except OSError:
            return


def _clear_config(lines: list[str]) -> None:
    """Every saved account goes; the file too when it holds nothing else of
    the researcher's (and is not a dotfile manager's symlink)."""
    from probe.sdk import config as config_mod

    path = config_mod.config_path()
    try:
        raw = json.loads(Path(os.path.realpath(path)).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return
    except (OSError, ValueError) as exc:
        lines.append(f"! could not read {path} ({exc}); delete the saved Probe accounts in it by hand.")
        return
    probe_keys = {"version", "current_context", "contexts", *config_mod._CONTEXT_KEYS}  # noqa: SLF001
    others = {k: v for k, v in raw.items() if k not in probe_keys} if isinstance(raw, dict) else {}
    if not others and not path.is_symlink():
        _remove_path(path)
        prune_empty_parents(path)
        lines.append(f"Removed {path} (every saved Probe account).")
        return
    kept = {**others, "version": raw.get("version", config_mod.CONFIG_VERSION), "contexts": {}}
    try:
        config_mod.save_file(kept)
        lines.append(f"Removed every saved Probe account from {path}; kept the rest of the file.")
    except Exception as exc:  # noqa: BLE001
        lines.append(f"! could not clear {path} ({exc}); delete the saved Probe accounts in it by hand.")


def _runs_from_plan(plan: dict) -> bool:
    """Is this interpreter one of the env generations the finisher deletes?"""
    here = os.path.realpath(sys.prefix)
    if any(part in here.replace(os.sep, "/") for part in ("/.cache/uv/", "/Caches/uv/", "/uv/archive-")):
        return True  # `npx probe-research uninstall`'s throwaway env: uv's cache, uv's to clean
    for env in plan.get("env_generations", []):
        real = os.path.realpath(env)
        if here == real or here.startswith(real.rstrip(os.sep) + os.sep):
            return True
    return False


def _phase_state(run: Run) -> list[str]:
    from probe.cli import uninstall_plan
    from probe.core import events

    lines = run.out
    _recount_unsent(run)
    with contextlib.suppress(Exception):
        from probe.cli import uninstall_agents

        lines.extend(uninstall_agents.remove_hollow())  # again: a run resumed at "state" skipped integrations
    _telemetry_done(run)
    # Nothing in this process writes Probe's files again from here.
    os.environ["PROBE_TELEMETRY"] = "off"
    with contextlib.suppress(Exception):
        from probe.cli import import_jobs

        if import_jobs.clear_all():
            lines.append("Cleared Probe's import jobs.")
    _clear_config(lines)
    fresh = uninstall_plan.state_layout()
    planned = [p for p in run.plan.get("paths", []) if p.get("stage") == uninstall_plan.STAGE_STATE]
    by_path = {p["path"]: p for p in planned}
    for item in fresh["paths"]:
        by_path.setdefault(item["path"], item)
    from probe._shared import finisher

    left = []
    for item in finisher.ordered(list(by_path.values())):
        path = Path(item["path"])
        if item.get("empty_only"):
            with contextlib.suppress(OSError):
                path.rmdir()
                prune_empty_parents(path)
            continue
        if not _remove_path(path):
            left.append(str(path))
        else:
            prune_empty_parents(path)
    for line in fresh["kept"]:
        lines.append(f"Kept {line}.")
    if not _runs_from_plan(run.plan):
        lines.append(f"Kept the `probe` this runs from ({sys.prefix}): it is not Probe's managed install. Remove it "
                     "with what installed it (`pipx uninstall probe-research`, or `pip uninstall probe-research`).")
    for path in left:
        lines.append(f"! could not remove {path}")
    from probe.sdk.config import load_context

    try:
        signed_in = bool((load_context() or {}).get("token"))
    except Exception:  # noqa: BLE001 - an unreadable config holds no credential
        signed_in = False
    offline = run.options.offline or bool((run.plan.get("server") or {}).get("offline"))
    if not run.options.embedded:
        events.agent_result(None, requested={"signed_in": False}, actual={"signed_in": signed_in},
                            ok=not signed_in,
                            message=f"offline: revoke this computer's keys in {_dashboard_hint()}" if offline else "")
    _step(events.Step.UNINSTALL_STATE, events.Status.FAILED if left else events.Status.DONE,
          f"{len(left)} path(s) left" if left else "Probe's files for this user removed")
    if left:
        raise Stop(EXIT_PARTIAL, (
            f"probe uninstall: {len(left)} of Probe's files could not be removed (above). Fix that, then run "
            "`probe uninstall` again to finish."))
    return lines


# -- telemetry -----------------------------------------------------------------------------------


def _telemetry_start(run: Run) -> None:
    """`wizard.uninstall_started`, BEFORE the confirmation and before anything
    is torn down: what is being removed is unreadable after it."""
    try:
        from probe.cli import telemetry as telemetry_mod
        from probe.cli import uninstall_plan
        from probe.cli.capabilities import TAP_PLUGIN_NAME
        from probe.sdk.config import resolve

        run.telemetry = telemetry_mod.TelemetryContext.start(
            via=telemetry_mod.Via.WIZARD, interactive=run.options.interactive, base_url=resolve().base_url)
        traces = list(_all_traces().values())
        plugins = [p for found in traces for p in found.get("plugins", [])]
        run.telemetry.emit(
            telemetry_mod.EVENT_WIZARD_UNINSTALL_STARTED,
            agent_count=len(run.agents),
            tracking_installed=any(TAP_PLUGIN_NAME not in p for p in plugins),
            capture_installed=any(TAP_PLUGIN_NAME in p for p in plugins) or any("capture" in f for f in traces),
            agent_rules_installed=any("rules" in found for found in traces),
            was_signed_in=any(ctx.get("token") for ctx in uninstall_plan.contexts().values()),
            confirmed_via="prompt" if run.options.interactive else "flag",
        )
    except Exception:  # noqa: BLE001 - observability never stops the uninstall
        run.telemetry = None


def _all_traces() -> dict:
    from probe.cli import uninstall_agents

    return uninstall_agents.all_traces()


def _telemetry_pin(run: Run) -> None:
    """The person this removal is of, resolved while the credential that
    names them still exists (the server phase revokes it)."""
    with contextlib.suppress(Exception):
        if run.telemetry is not None:
            run.telemetry.pin_identity()


def _telemetry_declined(run: Run) -> None:
    with contextlib.suppress(Exception):
        if run.telemetry is not None:
            from probe.cli import telemetry as telemetry_mod

            run.telemetry.emit(telemetry_mod.EVENT_WIZARD_UNINSTALL_COMPLETED,
                               outcome=telemetry_mod.UninstallOutcome.DECLINED, agent_count=len(run.agents),
                               duration_seconds=round(time.monotonic() - run.started_at, 3))


def _telemetry_done(run: Run) -> None:
    if run.telemetry is None:
        return
    try:
        from probe._shared import telemetry as shared
        from probe.cli import telemetry as telemetry_mod

        run.telemetry.emit(telemetry_mod.EVENT_WIZARD_UNINSTALL_COMPLETED,
                           outcome=telemetry_mod.UninstallOutcome.REMOVED, agent_count=len(run.agents),
                           warnings=run.warnings, duration_seconds=round(time.monotonic() - run.started_at, 3))
        shared._ensure_sender().request_flush(2.0)  # noqa: SLF001 - before its files go
    except Exception:  # noqa: BLE001
        pass


# -- finishing (U-T9) ----------------------------------------------------------------------------


def _python_works(python: str) -> bool:
    """Does `python` start, isolated, as a Python >= 3.8 within 5 s? (macOS's
    /usr/bin/python3 without the developer tools is a stub that does not.)"""
    try:
        done = subprocess.run([python, "-I", "-S", "-c", "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 3)"],
                              capture_output=True, timeout=5, check=False, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError):
        return False
    return done.returncode == 0


def base_python(plan: dict) -> str | None:
    """The interpreter the finisher runs on, never one inside an env being
    deleted: this process's own (`realpath(sys.executable)`, which for a uv
    env is the uv-managed Python it was made from), else the first of the
    env's base (`pyvenv.cfg`'s home), `sys._base_executable`, `python3` on PATH
    and /usr/bin/python3 that passes `_python_works`. None: run it in-process."""
    from probe.service import lifeboat

    doomed = [Path(p) for p in plan.get("env_generations", [])]
    for path in plan.get("paths", []):
        if path.get("stage") == "finish" and path.get("kind") in ("dir", "link"):
            doomed.append(Path(path["path"]))

    def inside(candidate: str) -> bool:
        real = os.path.realpath(candidate)
        for root in doomed:
            for spelling in {str(root), os.path.realpath(root)}:
                prefix = spelling.rstrip(os.sep) + os.sep
                if candidate.startswith(prefix) or real.startswith(prefix):
                    return True
        return False

    own = os.path.realpath(sys.executable) if sys.executable else ""
    if own and os.path.isfile(own) and not inside(own):
        return own
    candidates = [lifeboat.base_python(Path(sys.prefix)), getattr(sys, "_base_executable", None),
                  shutil.which("python3"), "/usr/bin/python3"]
    for candidate in candidates:
        if isinstance(candidate, str) and os.path.isfile(candidate) and os.access(candidate, os.X_OK) \
                and not inside(candidate) and _python_works(candidate):
            return candidate
    return None


def _phase_finishing(run: Run) -> int:
    """Become the finisher. Returns only when that could not happen (then it
    runs in this process instead, and its exit status is returned)."""
    from probe._shared import finisher, handoff
    from probe.core import events
    from probe.service import paths

    if run.options.embedded:
        return _finish_here(run)
    folder = paths.uninstall_dir()
    plan_path = paths.uninstall_plan_path()
    copy = folder / FINISHER_NAME
    shutil.copyfile(finisher.__file__, copy)
    os.chmod(copy, 0o600)
    from probe.cli import tui

    tui.leave_window()  # the menu's window, when Uninstall came from it: nothing after this closes it
    json_mode = events.enabled()
    tail, events_fd = events.handover()
    if json_mode:
        # `resumed` for the finisher's own `reason` (exit 1): a finish of an earlier run.
        (folder / TAIL_NAME).write_text(json.dumps({**tail, "resumed": run.resumed}), encoding="utf-8")
    python = base_python(run.plan)
    argv = ["-I", "-S", str(copy), "--plan", str(plan_path), *(["--json"] if json_mode else [])]
    env = dict(os.environ)
    if run.lock_fd is not None:
        os.set_inheritable(run.lock_fd, True)
        env[handoff.LOCK_FD_ENV] = str(run.lock_fd)
    for stream in (sys.stdout, sys.stderr):
        with contextlib.suppress(Exception):
            stream.flush()
    if json_mode and events_fd is not None:
        os.dup2(events_fd, 1)  # the finisher ends the event stream on stdout
    if python is not None:
        try:
            os.execve(python, [python, *argv], env)
        except OSError:
            pass
    # No interpreter outside the env (or the exec failed): finish here. The
    # env's files go from under this process, which needs none of them again.
    os.environ.update({k: v for k, v in env.items() if k == handoff.LOCK_FD_ENV})
    code = finisher.run(str(plan_path), json_mode=json_mode)
    os._exit(code)  # the stream ended with the finisher's `done`: nothing more may be written


def _finish_here(run: Run) -> int:
    """The finisher in THIS process, for an installer that goes on after it:
    every planned path but the env this process runs from (the installer's
    own `prune` takes it once nothing runs from it)."""
    from probe._shared import finisher, handoff
    from probe.cli import uninstall_plan
    from probe.service import paths

    here = os.path.realpath(sys.prefix)

    def in_use(entry: dict) -> bool:
        real = os.path.realpath(entry.get("path") or "")
        return here == real or here.startswith(real.rstrip(os.sep) + os.sep)

    plan = dict(run.plan)
    plan["paths"] = [e for e in plan.get("paths", []) if not (e.get("kind") == "dir" and in_use(e))]
    uninstall_plan.write(plan)
    shutil.copyfile(finisher.__file__, paths.uninstall_dir() / FINISHER_NAME)
    held = run.lock_fd
    if held is None:
        held = handoff._held.get(str(handoff.lock_path(uninstall_plan.primary_versions_root())))  # noqa: SLF001
    previous = os.environ.get(handoff.LOCK_FD_ENV)
    if held is not None:
        os.environ[handoff.LOCK_FD_ENV] = str(held)
    try:
        return finisher.run(str(paths.uninstall_plan_path()))
    finally:
        if previous is None:
            os.environ.pop(handoff.LOCK_FD_ENV, None)
        else:
            os.environ[handoff.LOCK_FD_ENV] = previous


def halfway_notice() -> str | None:
    """The line `probe doctor` and `probe status` print FIRST while an
    uninstall that stopped halfway keeps Probe off (its barrier LIVE, its owner
    gone): nothing of Probe starts or updates until it is finished. None
    otherwise (no barrier, or an uninstall running right now). Never raises."""
    try:
        from probe._shared import uninstall_barrier as reader

        record = reader.read()
        if reader.state(record) != reader.State.LIVE or reader._owner_runs(record or {}):  # noqa: SLF001
            return None
        phase = (record or {}).get("phase")
    except Exception:  # noqa: BLE001 - a status line never breaks the command
        return None
    if phase in PHASES:
        return (f"An uninstall of Probe stopped halfway (phase {phase}). Run `probe repair` (or `npx "
                "probe-research`) to finish it and set Probe up again, or `probe uninstall` to finish removing it.")
    # How far it got is unknown: only `probe uninstall` itself runs it (`finish_interrupted`).
    return (f"An uninstall of Probe stopped halfway (phase {phase or 'unknown'}). Run `probe uninstall` to finish "
            "removing it; `npx probe-research` then sets Probe up again.")


class Interrupted(StrEnum):
    """What `finish_interrupted` found."""

    NONE = "none"  # no uninstall to finish (none, or a stale one: the installer clears it)
    RUNNING = "running"  # an uninstall runs right now: the installer refuses
    FINISHED = "finished"  # one had stopped halfway; it is finished now: install afresh
    FAILED = "failed"  # one had stopped halfway and could not be finished: refuse


def finish_interrupted() -> tuple[Interrupted, str]:
    """For every install entry, before it takes the install lock: an uninstall
    that stopped halfway (its barrier LIVE, its owner gone, past "draining" or
    unreadable) is finished first, as `probe uninstall` resumes it, and only
    then does the install go on: the owner chose a clean slate, and a person
    reinstalling wants Probe back. One line says so. An uninstall running right
    now (its owner alive) is never touched: RUNNING, with the reader's refusal.
    Returns (what, the line to print when the installer refuses)."""
    from probe._shared import uninstall_barrier as reader

    record = reader.read()
    if reader.state(record) != reader.State.LIVE:
        return Interrupted.NONE, ""
    record = record or {}
    if reader._owner_runs(record):  # noqa: SLF001 -- the one reader's own judgement of its owner
        return Interrupted.RUNNING, reader.refusal(record) or "an uninstall of Probe is running"
    phase = record.get("phase")
    if record.get("_unreadable") or phase not in PHASES:
        # How far it got is unknown (an unreadable record, "resuming", a
        # phase this release does not know): only `probe uninstall` itself,
        # which asks about what is unsent, may run it from the start.
        what = "its record cannot be read" if record.get("_unreadable") else f"phase {phase or 'unknown'}"
        return Interrupted.RUNNING, (f"an uninstall of Probe stopped halfway ({what}); finish it with "
                                     "`probe uninstall`, then install again")
    print(f"An uninstall stopped halfway (phase {phase}); finishing it first", file=sys.stderr, flush=True)
    telemetry = os.environ.get("PROBE_TELEMETRY")
    try:
        code = run(Options(yes=True, embedded=True))
    finally:
        # The state phase turns this process's telemetry off; the install goes on.
        if telemetry is None:
            os.environ.pop("PROBE_TELEMETRY", None)
        else:
            os.environ["PROBE_TELEMETRY"] = telemetry
    if code == EXIT_DONE and reader.state() != reader.State.LIVE:
        return Interrupted.FINISHED, ""
    return Interrupted.FAILED, (
        "the uninstall that stopped halfway could not be finished; run `probe uninstall` (or `probe uninstall "
        "--offline` without a network) to finish it, then install again")


# -- the run ---------------------------------------------------------------------------------


_PHASE_STEPS = {
    Phase.STOPPING: _phase_stopping,
    Phase.DRAINING: _phase_draining,
    Phase.SERVER: _phase_server,
    Phase.INTEGRATIONS: _phase_integrations,
    Phase.STATE: _phase_state,
}


def _resume_point(run: Run) -> Phase | None:
    """Where an earlier run stopped, when it must be finished; None to start
    afresh (none, or a stale one before the point of no return, cleared)."""
    from probe._shared import uninstall_barrier as reader
    from probe.cli import uninstall_plan

    record = reader.read()
    state = reader.state(record)
    if state == reader.State.ABSENT:
        return None
    if state == reader.State.STALE:
        return None  # cleared under the install lock (`_clear_stale_locked`): the reader's contract
    pid = record.get("pid") if isinstance(record, dict) else None
    if _owner_runs(record or {}) and not _is_self(record or {}):
        raise Stop(EXIT_REFUSED, f"probe uninstall: another uninstall is running (pid {pid}); let it finish.",
                   Reason.BUSY, {"pid": pid})
    phase = (record or {}).get("phase")
    if phase not in PHASES:
        # Unreadable, or a phase this release does not know: from the first
        # phase again (every phase can be run twice; what is gone stays gone).
        phase = Phase.STOPPING
    # From here this run finishes an earlier one: it never calls off.
    run.resumed = True
    run.at = Phase(phase)
    plan = uninstall_plan.read()
    if plan is None:
        # Its plan is gone: plan what is here now (the server's rows too,
        # while the server phase is still to run).
        due = PHASES.index(Phase(phase)) <= PHASES.index(Phase.SERVER)
        server = _server_ids(run) if due else {"device_ids": [], "installation_ids": [], "contexts": {}}
        plan = uninstall_plan.compute(server=server)
        uninstall_plan.write(plan)
    run.plan = plan
    return Phase(phase)


@contextlib.contextmanager
def _signals():
    """SIGTERM and SIGHUP end the run through its handlers (`Terminated`), as
    Ctrl-C does: before "server" everything is put back. A `--json` run's
    event session already turns them into SystemExit; it keeps its own."""
    from probe.core import events
    import signal
    import threading

    if events.enabled() or threading.current_thread() is not threading.main_thread():
        yield
        return

    def stop(signum, _frame):
        raise Terminated(signum)

    previous = {}
    for name in ("SIGTERM", "SIGHUP"):
        number = getattr(signal, name, None)
        if number is not None:
            with contextlib.suppress(OSError, ValueError):
                previous[number] = signal.signal(number, stop)
    try:
        yield
    finally:
        for number, handler in previous.items():
            with contextlib.suppress(OSError, ValueError):
                signal.signal(number, signal.SIG_DFL if handler is None else handler)


def _reversible(phase: object) -> bool:
    return phase in PHASES and PHASES.index(Phase(phase)) < PHASES.index(Phase.SERVER)


def _half_done(run: Run, stop: Stop) -> str:
    """A resumed run was refused: the barrier stays (LIVE), nothing is put
    back, and this says so. The way to finish: what the refusal said (the lock
    is held, the server is unreachable), else --discard-unsent only when
    something is unsent, else a rerun."""
    said = "This uninstall is half-done (an earlier run of it stopped partway), so Probe stays stopped until it is finished"
    if stop.reason in (Reason.BUSY, Reason.OFFLINE):
        return f"{said}."
    unsent = run.unsent
    if unsent is not None and unsent.total:
        online = ", or run `probe uninstall` again once online" if unsent.sendable else ""
        return (f"{said}: run `probe uninstall --backup-unsent` (or --discard-unsent) to finish it now"
                f"{online}.")
    return f"{said}: run `probe uninstall` again to finish it."


def _call_off(run: Run) -> str:
    """Before the point of no return, called off (a refusal, a cancel, a
    signal): the barrier goes, the service starts again the way `ensure`
    starts it (and with it the keeper and lifeboat), and what was stopped is
    said. Nothing else this run did lasts (the stop phase changes nothing on
    disk; what was sent stays sent). Returns the line to print."""
    _drop_barrier()
    said = "Nothing was removed."
    if run.stopped:
        said += f" Stopped meanwhile: {', '.join(run.stopped)}."
    if not run.options.embedded:
        with contextlib.suppress(Exception):
            from probe.service import client

            started = client.ensure()
            if started in (client.Ensured.SPAWNED, client.Ensured.STARTING, client.Ensured.RUNNING):
                said += " The Probe service is starting again."
    return said


def run(options: Options) -> int:
    """`probe uninstall`. Returns its exit code, or does not return (the
    finisher took over the process)."""
    from probe.core import events

    if not options.embedded:
        events.begin_result("uninstall", [None])
    state = Run(options=options)
    try:
        with _signals():
            try:
                return _run(state)
            except Stop as stop:
                return _stopped(state, stop)
            except (KeyboardInterrupt, Terminated, SystemExit) as exc:
                return _interrupted(state, exc)
    finally:
        if state.lock_fd is not None:
            from probe._shared import handoff

            handoff.release_lock(state.lock_fd)


def _stopped(state: Run, stop: Stop) -> int:
    from probe._shared import uninstall_barrier as reader
    from probe.core import events

    message = stop.message
    record = reader.read()
    if state.resumed:
        # Never called off: the earlier run's progress is unknown. The barrier
        # stays LIVE (RESUMING until "server").
        if stop.code == EXIT_REFUSED:
            message = f"{message} {_half_done(state, stop)}"
    elif record is None:
        if state.wrote_plan or state.wrote_barrier:
            _drop_barrier()  # stopped before it began: this run's plan goes too
    elif _owns_barrier(state, record) and _reversible(record.get("phase")):
        message = f"{message} {_call_off(state)}"
    print(message, file=sys.stderr if stop.code else sys.stdout)
    if not state.options.embedded:
        events.agent_result(None, requested={"signed_in": False}, actual=None, ok=False, message=message)
        events.set_reason(reason_record(state, stop.reason, stop.detail, stop.code))
    return stop.code


def reason_record(run: Run, reason: Reason | None, detail: dict | None, code: int) -> dict:
    """The `--json` result's `reason`: `{"code", "resumed", ...detail}`. A
    partial run says what finishes it (`resume`, `phase`). `resumed`: this run
    was finishing an earlier one, so a refusal leaves the uninstall half-done
    (nothing is put back)."""
    out = {"code": str(reason or (Reason.PARTIAL if code == EXIT_PARTIAL else Reason.CANCELLED)),
           "resumed": bool(run.resumed), **(detail or {})}
    if out["code"] == Reason.PARTIAL:
        out.setdefault("resume", "probe uninstall")
        out.setdefault("phase", str(run.at) if run.at else None)
    return out


def _interrupted(state: Run, exc: BaseException) -> int:
    """Ctrl-C, SIGTERM or SIGHUP: before "server" called off, as if it never
    began; after it, the barrier stays for `probe uninstall` to finish. Only
    this run's own barrier is called off; a resumed run's never is."""
    from probe._shared import uninstall_barrier as reader

    record = reader.read()
    if state.resumed:
        phase = state.at or "first"
        print(f"probe uninstall: interrupted at its '{phase}' step; run `probe uninstall` again to finish.",
              file=sys.stderr)
        code = EXIT_PARTIAL
    elif record is None or not _owns_barrier(state, record):
        if record is None and (state.wrote_plan or state.wrote_barrier):
            _drop_barrier()  # this run's plan, written before its barrier
        print("probe uninstall: interrupted; nothing was changed.", file=sys.stderr)
        code = EXIT_REFUSED
    elif _reversible(record.get("phase")):
        print(f"probe uninstall: interrupted. {_call_off(state)}", file=sys.stderr)
        code = EXIT_REFUSED
    else:
        print(f"probe uninstall: interrupted at its '{record.get('phase')}' step; run `probe uninstall` again "
              "to finish.", file=sys.stderr)
        code = EXIT_PARTIAL
    if not state.options.embedded:
        from probe.core import events

        events.set_reason(reason_record(state, Reason.PARTIAL if code == EXIT_PARTIAL else Reason.INTERRUPTED,
                                        None, code))
    if isinstance(exc, SystemExit):
        raise exc  # a `--json` run's event session ends it (`done`, interrupted)
    return code


def _clear_stale_locked(run: Run) -> None:
    """Under the install lock (which an uninstall takes before it writes its
    barrier): a STALE barrier left by an earlier run is cleared, and one that
    turned LIVE while this run was asking (another uninstall began, or one
    died past the point of no return) stops this one."""
    from probe._shared import uninstall_barrier as reader

    said = reader.clear_stale()
    if said:
        _say(f"probe uninstall: {said}; starting again.")
    record = reader.read()
    if reader.state(record) == reader.State.LIVE:
        pid = record.get("pid") if isinstance(record, dict) else None
        raise Stop(EXIT_REFUSED, "probe uninstall: another uninstall of Probe began meanwhile; nothing was changed. "
                                 "Run `probe uninstall` again when it ends.", Reason.BUSY, {"pid": pid})


def _run(run: Run) -> int:
    start = _resume_point(run)
    if start is None and run.options.embedded:
        return EXIT_DONE  # the barrier went meanwhile (another run finished it): never a fresh uninstall here
    if start is None:
        if not run.options.yes and not run.options.interactive:
            raise Stop(EXIT_REFUSED, "probe uninstall: nothing was changed: there is no terminal to confirm in. "
                                     "Pass --yes to confirm.", Reason.CONFIRM)
        _scope(run)
        run.agents = list(_all_traces())
        _telemetry_start(run)
        server = _server_ids(run)
        if run.options.interactive:
            _confirm(run)
        _telemetry_pin(run)
        _take_lock(run)
        _clear_stale_locked(run)
        _plan(run, server)
        run.at = Phase.PLANNED
        _write_barrier(run, Phase.PLANNED)
        start = Phase.STOPPING
        _say("Uninstalling Probe from this computer...")
    else:
        _take_lock(run)
        _say(f"Finishing the uninstall of Probe that stopped at its '{start}' step...")
    for phase in PHASES[PHASES.index(start):]:
        run.at = phase
        if phase is Phase.SERVER:
            # Reachable, right before the point of no return (a rerun too):
            # offline, a fresh run is called off and a resumed one waits.
            preflight_server(run)
        try:
            # A resumed run records RESUMING before "server": a barrier saying
            # "stopping" or "draining" would read STALE once it exits, and the
            # earlier run may have got further than that.
            _write_barrier(run, RESUMING if run.resumed and _reversible(phase) else phase)
        except OSError as exc:
            raise Stop(EXIT_PARTIAL, f"probe uninstall: could not record its progress ({exc}).") from None
        if phase is Phase.FINISHING:
            return _phase_finishing(run)
        step = _PHASE_STEPS.get(phase)
        if step is None:
            continue
        try:
            step(run)
        finally:
            run.warnings += sum(1 for line in run.out if str(line).lstrip().startswith("!"))
            _lines(run.out)
            run.out.clear()
    return EXIT_DONE
