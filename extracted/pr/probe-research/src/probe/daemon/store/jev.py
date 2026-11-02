"""list the shell commands Jev approved and the daemon ran, across session stores."""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass, field
from probe.daemon.store.store import FORMAT_VERSION, state_dir, store_path


#: How a shell write cut short is logged after who approved it (`tools._run_shell_write`).
CUT_SHORT = "the bite was cut short while it ran"
#: How a shell write that raised while it ran is logged after who approved it, with the error's type.
FAILED_WHILE_RUNNING = "failed while it ran"


@dataclass
class JevApproved:
    """`jev_approved`'s answer: the newest `rows`; how many matched in all
    (`total`, which can be more than the rows) and in each session
    (`by_session`, so a session none of whose rows is shown is still named);
    how many session stores could not be read (`unreadable`); and how many of
    its rows a store held in a shape no Jev yes is written in (`damaged`). The
    list is complete only when both of those are 0."""

    rows: list[dict]
    total: int
    unreadable: int
    damaged: int = 0
    by_session: dict[str, int] = field(default_factory=dict)


#: A Jev-approved command's logbook status, as `probe approvals` says it (`_run_shell_write`).
JEV_ENDINGS = {"ran": "ran", "cancelled": "cut short while it ran", "failed": "failed while it ran",
               "running": "still running, or the daemon stopped while it ran"}


def jev_approved(since: float, limit: int, *, session_id: str | None = None) -> JevApproved:
    """Shell commands Jev said yes to and the daemon ran without asking
    (`command_check`), logged at or after `since`, newest first: from every
    session's store on this machine, or `session_id`'s alone. Nobody is asked
    about these, so `probe approvals` lists them beside the questions (R2): the
    researcher sees what ran in their name.

    Only the rows `_run_shell_write` writes on a Jev yes count: a shell head, no
    question behind it, and a reason that is exactly Jev's, checked whole. The
    daemon's model writes the reason of its own `probe` writes (their `why`),
    so a prefix match would let the watched model fill the list and push a real
    one out of it. A command logged `running` started and has not been logged
    since: it still runs, or its worker died while it ran. Read-only; a store
    that cannot be read, or is a newer format, is counted in `unreadable`, and a
    row in another shape in `damaged`, never an error."""
    from probe.daemon.shell.command_check import AUTO_JEV, JEV_REASON

    # Exactly what `_run_shell_write` logs on a Jev yes, each status with its own reason.
    reason_of_jev = {
        "ran": re.compile(JEV_REASON.pattern), "running": re.compile(JEV_REASON.pattern),
        "cancelled": re.compile(JEV_REASON.pattern + "; " + re.escape(CUT_SHORT)),
        "failed": re.compile(JEV_REASON.pattern + "; " + re.escape(FAILED_WHILE_RUNNING) + r" \(\w+\)"),
    }
    paths = [store_path(session_id)] if session_id is not None else sorted(state_dir().glob("*.sqlite"))
    rows: list[dict] = []
    unreadable = damaged = 0
    for path in paths:
        # A row lands in the -wal file first: a store whose files are both older
        # wrote nothing since. The -wal first: a worker closing between the two
        # moves its rows into the main file, whose time is then read after it.
        try:
            touched = [path.with_name(path.name + "-wal").stat().st_mtime]
        except OSError:
            touched = []  # no -wal (closed cleanly): the main file holds every row
        try:
            touched.append(path.stat().st_mtime)
        except FileNotFoundError:
            if session_id is None:
                unreadable += 1  # listed a moment ago; a session with no store has nothing to list
            continue
        except OSError:
            unreadable += 1  # there, and not readable (permissions): never read as "nothing ran"
            continue
        if max(touched) < since:
            continue
        try:
            connection = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, timeout=2.0)
        except (OSError, sqlite3.Error):
            unreadable += 1
            continue
        try:
            row = connection.execute("SELECT value FROM meta WHERE key = 'format_version'").fetchone()
            if row is None or row[0] is None or int(row[0]) > FORMAT_VERSION:
                unreadable += 1
                continue
            # GLOB, not LIKE: it is case-sensitive, as the reason is. Every match is
            # read (a day's are few), so `total` counts exactly what is left out.
            found = connection.execute("SELECT at, argv, reason, exit_code, status FROM writes WHERE at >= ? "
                                 "AND head = 'shell' AND request IS NULL "
                                 "AND status IN ('ran', 'cancelled', 'failed', 'running') "
                                 "AND reason GLOB ?", (since, f"{AUTO_JEV} p=*")).fetchall()
        except (sqlite3.Error, ValueError, TypeError):
            unreadable += 1
            continue
        finally:
            connection.close()
        for at, argv, reason, exit_code, status in found:
            try:
                words = json.loads(argv)
            except (TypeError, ValueError):
                words = None
            jev = reason_of_jev[status].fullmatch(reason) if isinstance(reason, str) else None
            if (jev is None or not isinstance(at, (int, float)) or not isinstance(words, list) or len(words) != 3
                    or words[:2] not in (["sh", "-c"], ["bash", "-c"]) or not isinstance(words[2], str)
                    or not (exit_code is None or isinstance(exit_code, int))):
                damaged += 1  # the shape filter passed it: something wrote it another way
                continue
            rows.append({"session_id": path.stem, "at": float(at), "command": words[2], "lowest": jev.group(1),
                         "ended": status, "exit_code": exit_code})
    rows.sort(key=lambda r: r["at"], reverse=True)
    by_session: dict[str, int] = {}
    for r in rows:
        by_session[r["session_id"]] = by_session.get(r["session_id"], 0) + 1
    return JevApproved(rows=rows[:limit], total=len(rows), unreadable=unreadable, damaged=damaged,
                       by_session=by_session)
