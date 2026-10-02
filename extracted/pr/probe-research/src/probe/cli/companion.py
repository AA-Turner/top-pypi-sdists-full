"""`probe companion`: the Probe daemon's key, and what it wrote.

    probe companion authorize          approve the daemon's own key (read + write; deletes go to the trash only)
    probe companion log [SESSION]      every decision: written, held (and why), failed
    probe companion report [SESSION]   who owned which part of the transcript, and the counts
    probe companion trace [CYCLE] [--session S]
                                       every cycle (id, range, outcome), or the exact request
                                       and answer of each model round in one
    probe companion feedback ID --wrong|--noise [--note TEXT]
                                       correct a write; the daemon reads it on its next cycle

The daemon itself is the tap plugin's worker (`tap/companion_worker.py`); this
module never imports it. It reads the worker's ledger file directly, which is
why the file carries a format version: a version this CLI does not know is
refused with "upgrade the CLI", never half-read. KNOWN_LEDGER_VERSIONS must
move with the tap's `companion_ledger.LEDGER_VERSION` --
`tests/test_companion_ledger_contract.py` holds the two together.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
import zlib
from pathlib import Path
from typing import Callable

import typer

#: Ledger formats this reader understands. See the module docstring.
KNOWN_LEDGER_VERSIONS = frozenset({1})
#: How long the worker keeps its traces (`companion_ledger.TRACE_KEEP_*`).
TRACE_KEEP_DAYS = 7
TRACE_KEEP_MB = 50

companion_app = typer.Typer(
    no_args_is_help=True,
    help="the Probe daemon (the `daemon` state): its key, and what it wrote",
)


def companion_dir() -> Path:
    xdg = os.environ.get("XDG_STATE_HOME")
    base = Path(xdg) if xdg else Path.home() / ".local" / "state"
    return base / "probe" / "companion"


def ledger_path(session_id: str) -> Path:
    return companion_dir() / f"{session_id}.sqlite"


class LedgerUnreadable(RuntimeError):
    pass


def open_ledger(session_id: str, *, write: bool = False) -> sqlite3.Connection:
    path = ledger_path(session_id)
    if not path.is_file():
        raise LedgerUnreadable(f"the Probe daemon has no record for session {session_id}")
    mode = "rw" if write else "ro"
    conn = sqlite3.connect(f"file:{path}?mode={mode}", uri=True, timeout=10.0)
    try:
        row = conn.execute("SELECT value FROM meta WHERE key = 'format_version'").fetchone()
        version = int(row[0]) if row else None
    except (sqlite3.Error, ValueError) as exc:
        conn.close()
        raise LedgerUnreadable(f"{path} is not a readable daemon ledger ({exc})") from None
    if version not in KNOWN_LEDGER_VERSIONS:
        conn.close()
        raise LedgerUnreadable(
            f"{path} is ledger format {version}, which this probe CLI cannot read; "
            "upgrade the CLI with the wizard's Update"
        )
    return conn


def tokens_today(now: float | None = None) -> int | None:
    """Model tokens this device's daemons spent today (UTC), or None if unreadable.

    The v2 daemon's counter (`<state>/probe/daemon/device.json`, a meter: no
    fuse reads it) plus what a v1 worker left in the tap's `device.sqlite`
    (companion_ledger.DeviceSpend; the ledger contract test pins that format).
    """
    from probe.daemon import store as daemon_store

    spent = daemon_store.device_tokens_today(now)
    path = companion_dir() / "device.sqlite"
    if not path.is_file():
        return spent
    day = time.strftime("%Y-%m-%d", time.gmtime(time.time() if now is None else now))
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        try:
            row = conn.execute("SELECT tokens FROM spend WHERE day = ?", (day,)).fetchone()
        finally:
            conn.close()
    except sqlite3.Error:
        return None
    return spent + (int(row[0]) if row else 0)


def read_daemon_log(session_id: str, *, status: str | None = None) -> list[dict] | None:
    """A v2 session's logbook (`probe.daemon.store`, table `writes`), read-only;
    None when the session has no v2 store."""
    from probe.daemon import store as daemon_store

    path = daemon_store.store_path(session_id)
    if not path.is_file():
        return None
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=10.0)
    except sqlite3.Error as exc:
        raise LedgerUnreadable(f"{path} is not a readable daemon store ({exc})") from None
    try:
        row = conn.execute("SELECT value FROM meta WHERE key = 'format_version'").fetchone()
        if row is None or int(row[0]) > daemon_store.FORMAT_VERSION:
            raise LedgerUnreadable(f"{path} is daemon store format {row and row[0]}, which this probe CLI "
                                   "cannot read; upgrade the CLI with the wizard's Update")
        query = "SELECT id, bite, at, argv, head, status, reason, exit_code, request FROM writes"
        params: tuple = ()
        if status:
            query += " WHERE status = ?"
            params = (status,)
        rows = conn.execute(query + " ORDER BY id", params).fetchall()
    except (sqlite3.Error, ValueError) as exc:
        raise LedgerUnreadable(f"{path} is not a readable daemon store ({exc})") from None
    finally:
        conn.close()
    return [
        {"id": r[0], "bite": r[1], "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(r[2])),
         "command": " ".join(json.loads(r[3])), "head": r[4], "status": r[5], "reason": r[6],
         "exit_code": r[7], "request": r[8]}
        for r in rows
    ]


def provision_daemon(base_url: str, *, open_browser: bool = True,
                     say: Callable[[str], None] | None = None, force: bool = False) -> list[str]:
    """Everything daemon mode needs on this machine: its own key (one browser
    approval) and its AI libraries (the `daemon` extra). The one path both
    `probe companion authorize` and the wizard's "Who records" row
    (`setup.apply_recorder`) take. Offline or a failed install leaves capture running: daemon mode reports
    itself unavailable (`probe daemon status`, `probe doctor`) and the agent records.

    Returns the report lines; `say` also gets each one as it is decided, so a
    terminal shows the key's line before the install's own output.
    """
    from . import setup as wizard
    from .daemon_cli import ai_libraries, daemon_install
    from .main import _authorize_companion

    lines: list[str] = []

    def emit(line: str) -> None:
        lines.append(line)
        if say is not None:
            say(line)

    # Each half only when it is missing (R12): a key already held is never
    # approved again -- unless `force`, for a key the server now refuses -- and
    # the libraries install without any approval.
    if force or not wizard.companion_token_held():
        for line in _authorize_companion(base_url, open_browser=open_browser):
            emit(line)
    if not wizard.companion_token_held() or ai_libraries():
        return lines
    try:
        daemon_install()
    except typer.Exit:
        emit("the daemon's AI libraries did not install; Enter on Who records in `probe wizard` "
             "retries once you are online")
    return lines


def _session(session: str | None) -> str:
    from .main import _resolve_agent_session

    return _resolve_agent_session(session)


def _fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise typer.Exit(1)


def read_log(conn: sqlite3.Connection, *, status: str | None = None) -> list[dict]:
    query = (
        "SELECT id, cycle, kind, target_type, target_id, payload, evidence, status, reason, "
        "attempts, created_at FROM proposals"
    )
    params: tuple = ()
    if status:
        query += " WHERE status = ?"
        params = (status,)
    rows = conn.execute(query + " ORDER BY id", params).fetchall()
    out = []
    for pid, cycle, kind, ttype, tid, payload, evidence, st, reason, attempts, created in rows:
        ev = json.loads(evidence) if evidence else {}
        ev.pop("_op", None)
        out.append(
            {
                "id": pid,
                "cycle": cycle,
                "kind": kind,
                "target": f"{ttype}:{tid}" if tid else None,
                "status": st,
                "reason": reason,
                "attempts": attempts,
                "payload": json.loads(payload),
                "evidence": ev,
                "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(created)),
            }
        )
    return out


def read_report(conn: sqlite3.Connection) -> dict:
    meta = dict(conn.execute("SELECT key, value FROM meta"))
    boundaries = [
        {"at": at, "offset": off, "from": frm, "to": to, "reason": reason}
        for at, off, frm, to, reason in conn.execute(
            "SELECT at, byte_offset, from_writer, to_writer, reason FROM boundaries ORDER BY id"
        )
    ]
    # Ownership segments: each handover starts a range the incoming writer owns.
    segments = []
    for i, b in enumerate(boundaries):
        end = boundaries[i + 1]["offset"] if i + 1 < len(boundaries) else None
        segments.append({"writer": b["to"], "from": b["offset"], "to": end, "reason": b["reason"]})
    counts = dict(conn.execute("SELECT status, COUNT(*) FROM proposals GROUP BY status"))
    by_kind = dict(
        conn.execute("SELECT kind, COUNT(*) FROM proposals WHERE status = 'published' GROUP BY kind")
    )
    cycles = conn.execute(
        "SELECT COUNT(*), COALESCE(SUM(input_tokens), 0), COALESCE(SUM(output_tokens), 0) FROM cycles"
    ).fetchone()
    directed = conn.execute("SELECT COUNT(*) FROM directed").fetchone()[0]
    return {
        "session_id": meta.get("session_id"),
        "writer_now": meta.get("writer"),
        "decided_through_offset": int(meta.get("watermark") or 0),
        "ownership": segments,
        "decisions": counts,
        "published_by_kind": by_kind,
        "directed_writes_seen": directed,
        "cycles": cycles[0],
        "tokens": {"input": cycles[1], "output": cycles[2]},
    }


@companion_app.command("authorize")
def authorize_cmd(
    no_browser: bool = typer.Option(False, "--no-browser", help="print the approval link only"),
) -> None:
    """Approve the Probe daemon's own key, and install the daemon's AI libraries.

    The daemon records a session only where `probe wizard` › Defaults › Who
    records names it (the switch then reads `on (daemon)`), and only with
    this key. It deletes only on a server with
    Probe's trash (restorable for 21 days); elsewhere deletes stay yours.
    Revoke it on its own under Settings › Connected clients; the agent then
    records again.
    """
    from probe.sdk.config import resolve

    from probe.sdk.config import load_context

    from .main import _conn

    # An explicit approval always mints a new key: this is the command a
    # revoked key's owner reaches for. Success is a NEW key, not any key: a
    # declined approval leaves the old one saved.
    before = (load_context() or {}).get("companion_token")
    provision_daemon(resolve(base_url=_conn.base_url).base_url, open_browser=not no_browser, say=print, force=True)
    after = (load_context() or {}).get("companion_token")
    if not after or after == before:
        raise typer.Exit(1)


@companion_app.command("log")
def log_cmd(
    session: str = typer.Argument(None, help="session id (defaults to this one)"),
    status: str = typer.Option(None, "--status", help="published | held | pending | failed"),
) -> None:
    """Every decision the daemon made in a session, and why."""
    from .main import _print_json

    resolved = _session(session)
    if not ledger_path(resolved).is_file():
        try:
            writes = read_daemon_log(resolved, status=status)
        except LedgerUnreadable as exc:
            _fail(str(exc))
        if writes is not None:
            _print_json({"session_id": resolved, "writes": writes})
            return
    try:
        conn = open_ledger(resolved)
    except LedgerUnreadable as exc:
        _fail(str(exc))
    try:
        _print_json({"session_id": resolved, "decisions": read_log(conn, status=status)})
    finally:
        conn.close()


def read_trace(conn: sqlite3.Connection, cycle: int) -> list[dict]:
    """The rounds of one cycle (none from a worker older than tap 0.8.0, whose
    ledger has no `traces` table)."""
    try:
        rows = conn.execute(
            "SELECT round, at, request, response, error FROM traces WHERE cycle = ? ORDER BY id", (cycle,)
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    return [
        {
            "round": r[0],
            "at": r[1],
            "request": json.loads(zlib.decompress(r[2])),
            "response": json.loads(zlib.decompress(r[3])) if r[3] is not None else None,
            "error": r[4],
        }
        for r in rows
    ]


def read_cycles(conn: sqlite3.Connection) -> list[dict]:
    """Every cycle, with how many traced rounds it kept."""
    try:
        traced = dict(conn.execute("SELECT cycle, COUNT(*) FROM traces GROUP BY cycle"))
    except sqlite3.OperationalError:
        traced = {}
    rows = conn.execute(
        "SELECT id, started_at, byte_start, byte_end, outcome, input_tokens, output_tokens FROM cycles ORDER BY id"
    ).fetchall()
    return [
        {"cycle": r[0], "started_at": r[1], "bytes": [r[2], r[3]], "outcome": r[4],
         "tokens": {"input": r[5] or 0, "output": r[6] or 0}, "traced_rounds": traced.get(r[0], 0)}
        for r in rows
    ]


@companion_app.command("trace")
def trace_cmd(
    cycle: int = typer.Argument(None, help="cycle id; without one, every cycle is listed"),
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Every cycle the daemon ran, or exactly what it sent the model in one and what came back."""
    from .main import _print_json

    resolved = _session(session)
    try:
        conn = open_ledger(resolved)
    except LedgerUnreadable as exc:
        _fail(str(exc))
    try:
        if cycle is None:
            _print_json({"session_id": resolved, "cycles": read_cycles(conn)})
            return
        rounds = read_trace(conn, cycle)
    finally:
        conn.close()
    if not rounds:
        _fail(f"no trace for cycle {cycle} (kept {TRACE_KEEP_DAYS} days / {TRACE_KEEP_MB} MB per session; "
              "a worker older than tap 0.8.0 keeps none)")
    _print_json({"session_id": resolved, "cycle": cycle, "rounds": rounds})


@companion_app.command("report")
def report_cmd(
    session: str = typer.Argument(None, help="session id (defaults to this one)"),
) -> None:
    """Who owned which part of the transcript, and what the daemon wrote."""
    from probe.sdk import session_marker

    from .main import _print_json

    resolved = _session(session)
    try:
        conn = open_ledger(resolved)
    except LedgerUnreadable as exc:
        _fail(str(exc))
    try:
        report = read_report(conn)
    finally:
        conn.close()
    status = session_marker.daemon_status(resolved)
    report["daemon"] = None if status is None else {"status": status[0], "reason": status[1]}
    _print_json(report)


@companion_app.command("feedback")
def feedback_cmd(
    decision: int = typer.Argument(..., help="decision id from `probe companion log`"),
    wrong: bool = typer.Option(False, "--wrong", help="it recorded something untrue"),
    noise: bool = typer.Option(False, "--noise", help="true, but not worth recording"),
    note: str = typer.Option(None, "--note", help="what it should have done"),
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Correct one of the daemon's decisions. It reads this on its next cycle.

    Nothing already written is changed here: fix or delete the record itself
    with the ordinary commands, and use this so the daemon does not repeat it.
    """
    if wrong == noise:
        _fail("pass exactly one of --wrong or --noise")
    resolved = _session(session)
    try:
        conn = open_ledger(resolved, write=True)
    except LedgerUnreadable as exc:
        _fail(str(exc))
    try:
        if conn.execute("SELECT 1 FROM proposals WHERE id = ?", (decision,)).fetchone() is None:
            _fail(f"no decision {decision} in session {resolved}")
        conn.execute(
            "INSERT INTO feedback(at, proposal_id, verdict, note) VALUES (?, ?, ?, ?)",
            (time.time(), decision, "wrong" if wrong else "noise", note),
        )
        conn.commit()
    finally:
        conn.close()
    print(f"recorded: decision {decision} is {'wrong' if wrong else 'noise'}")
