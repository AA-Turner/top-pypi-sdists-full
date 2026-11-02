"""draining: send every outbox, count what is still unsent, and decide (discard, back up, ask) before anything is deleted."""

from __future__ import annotations

import contextlib
import errno
import os
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
#: The drain's whole budget (plan: bounded, 60 s).
DRAIN_BUDGET_S = 60.0


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
    from probe.sdk.delivery.journal.journal import Journal

    try:
        return list(Journal.discover())
    except Exception:  # noqa: BLE001
        return []


def drain(deadline: float, lines: list[str]) -> None:
    """Send every outbox (the default root, its `rank-*` queues, the $TMPDIR
    fallback; each per-credential queue), within `deadline`."""
    from probe.sdk.delivery.journal.journal import Journal
    from probe.sdk.delivery.outbox.drain.drain import drain as drain_journal
    from probe.sdk.delivery.transport.deadlines import deadline_scope

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
        with contextlib.closing(sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=2)) as connection:
            row = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()  # noqa: S608 - a fixed table name
    except sqlite3.Error:
        return 0
    return int(row[0]) if row else 0


def _deleted_here(path: Path) -> bool:
    """Is `path` in what the uninstall deletes: Probe's state folders, or a
    `$TMPDIR` fallback outbox? (An outbox PROBE_OUTBOX_DIR names elsewhere is kept.)"""
    from probe.cli.install.uninstall import plan as uninstall_plan
    from probe.sdk.delivery.journal.paths import _fallback_roots

    path = Path(path)
    roots = [*uninstall_plan.state_roots(), *_fallback_roots()]
    return any(path == root or root in path.parents for root in roots)


def count_unsent() -> Unsent:
    """What is still on this computer, never reached the server, and would be
    deleted (`kept`: what an outbox outside Probe's folders keeps)."""
    from probe.cli.install.uninstall import agent_traces as uninstall_agents
    from probe.sdk.delivery import offline
    from probe.sdk.delivery.journal.journal import Journal
    from probe.sdk.delivery.journal.paths import _fallback_roots, default_root

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
        from probe.cli.install.uninstall import unsent_notes as uninstall_notes

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
    from probe.cli.wizard import terminal as tui

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
    from probe.cli.install.uninstall import unsent_notes as uninstall_notes

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
from probe.cli.install.uninstall.state import Reason, Run, Stop, UnsentChoice, _step  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.uninstall import EXIT_REFUSED, run  # noqa: E402 -- pieces need each other; the front door loads this one first
