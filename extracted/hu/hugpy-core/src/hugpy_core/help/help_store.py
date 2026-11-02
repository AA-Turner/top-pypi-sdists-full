"""Postgres-backed store for the console Help panel (help_routes.py).

LIFTED from legacy ``hugpy_server.app.help_agent`` — the ``HelpStore`` JSONL
transcript store (one ``$PROJECTS_HOME/help_sessions/<id>.jsonl`` per session)
and ``derive_status`` — re-homed onto the core DB (sql/017_help.sql). The record
shapes are kept verbatim so the console's ``helpModel.js`` parses them
unchanged; what changes is only WHERE they live (DB is truth, not a JSON file).

An LLM turn is never written here — the reply rides core's own /v1 relay so it
lands in hugpy_wrapper.call_log (help_routes._relay_chat). Only the transcript
scaffold (the operator's prompt, the reply text that landed, which backend
answered) is persisted, so the panel can re-open a conversation.
"""
from __future__ import annotations

import time
import uuid
from typing import Optional


ID_RX_PATTERN = r"^hs-[0-9a-f]{12}$"

import re as _re

ID_RX = _re.compile(ID_RX_PATTERN)

TICKET_STATUSES = ("pending", "acted", "sent", "dismissed")
_TICKET_COLS = ("id", "kind", "status", "created", "updated", "model_key",
                "worker_id", "worker_name", "title", "detail", "result", "occurrences")


def _db():
    import psycopg
    from psycopg.rows import dict_row
    from hugpy_core.imports.functions import core_dsn
    return psycopg.connect(core_dsn(), autocommit=True, connect_timeout=5,
                           row_factory=dict_row)


def new_id() -> str:
    return "hs-" + uuid.uuid4().hex[:12]


def valid_id(sid: str) -> bool:
    return bool(ID_RX.match(sid or ""))


# ── sessions + transcript records ────────────────────────────────────────────
def create_session(*, by: str, backend: Optional[str], backend_label: Optional[str],
                    tools: bool) -> str:
    sid = new_id()
    now = time.time()
    with _db() as c:
        c.execute("INSERT INTO help_sessions (id, created, updated, created_by, backend,"
                  " backend_label, tools) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                  (sid, now, now, by or "operator", backend, backend_label, bool(tools)))
    return sid


def exists(sid: str) -> bool:
    if not valid_id(sid):
        return False
    with _db() as c:
        return c.execute("SELECT 1 FROM help_sessions WHERE id=%s", (sid,)).fetchone() is not None


def append(sid: str, *records: dict) -> None:
    """Append one or more transcript records. Each record is {kind, ...rest}; the
    rest is stored as the payload jsonb, `t` stamped if absent."""
    from psycopg.types.json import Jsonb
    now = time.time()
    with _db() as c:
        for rec in records:
            rec = dict(rec)
            kind = rec.pop("kind")
            t = rec.pop("t", None) or now
            c.execute("INSERT INTO help_records (session_id, kind, payload, t)"
                      " VALUES (%s,%s,%s,%s)", (sid, kind, Jsonb(rec), float(t)))
        c.execute("UPDATE help_sessions SET updated=%s WHERE id=%s", (now, sid))


def read(sid: str) -> list:
    """All records for a session in append order, each merged back to
    {kind, **payload, t, i} with i = position (verbatim of legacy enumerate)."""
    with _db() as c:
        rows = c.execute("SELECT kind, payload, t FROM help_records WHERE session_id=%s"
                         " ORDER BY id", (sid,)).fetchall()
    out = []
    for i, r in enumerate(rows):
        rec = dict(r["payload"] or {})
        rec["kind"] = r["kind"]
        rec["t"] = r["t"]
        rec["i"] = i
        out.append(rec)
    return out


def derive_status(records: list) -> str:
    """idle | busy | error | stopped — from the transcript alone (verbatim of
    legacy help_agent.derive_status). busy while a sent user message id is not
    yet covered by a ``done`` event."""
    pending: set = set()
    last_done = None
    stopped = False
    for r in records:
        k = r.get("kind")
        if k == "user":
            pending.update(r.get("message_ids") or [])
            stopped = False
        elif k == "event" and r.get("type") == "done":
            pending.difference_update(r.get("message_ids") or [])
            last_done = r
        elif k == "stopped":
            stopped = True
        elif k == "error":
            last_done = {"error": r.get("error")}
            pending.clear()
    if stopped:
        return "stopped"
    if pending:
        return "busy"
    if last_done and (last_done.get("error") or (last_done.get("rc") not in (None, 0))):
        return "error"
    return "idle"


def _session_row(sid: str) -> Optional[dict]:
    with _db() as c:
        return c.execute("SELECT id, created, updated, created_by, backend, backend_label, tools"
                         " FROM help_sessions WHERE id=%s", (sid,)).fetchone()


def transcript(sid: str, *, since: int = 0) -> dict:
    """The panel's transcript shape. Raises KeyError when the session is absent."""
    row = _session_row(sid)
    if row is None:
        raise KeyError(sid)
    recs = read(sid)
    first_user = next((r.get("text", "") for r in recs if r.get("kind") == "user"), "")
    return {"id": sid, "backend": row["backend"], "backend_label": row["backend_label"],
            "tools": bool(row["tools"]), "by": row["created_by"], "created": row["created"],
            "title": first_user[:120], "status": derive_status(recs), "count": len(recs),
            "records": [r for r in recs if r["i"] >= int(since or 0)]}


def list_sessions(limit: int = 100) -> list:
    with _db() as c:
        rows = c.execute("SELECT id, created, updated, created_by, backend FROM help_sessions"
                         " ORDER BY updated DESC LIMIT %s", (int(limit),)).fetchall()
    out = []
    for row in rows:
        recs = read(row["id"])
        first_user = next((r.get("text", "") for r in recs if r.get("kind") == "user"), "")
        out.append({"id": row["id"], "created": row["created"], "updated": row["updated"],
                    "backend": row["backend"], "by": row["created_by"],
                    "title": first_user[:120], "status": derive_status(recs)})
    return out


def delete_session(sid: str) -> bool:
    """Remove an idle transcript and its records; never race a running turn."""
    if not valid_id(sid):
        return False
    with _db() as c:
        with c.transaction():
            row = c.execute("SELECT id FROM help_sessions WHERE id=%s FOR UPDATE", (sid,)).fetchone()
            if row is None:
                return False
            records = c.execute("SELECT kind,payload,t FROM help_records WHERE session_id=%s ORDER BY id", (sid,)).fetchall()
            view = [{"kind": r["kind"], **(r["payload"] or {}), "t": r["t"]} for r in records]
            if derive_status(view) in ("busy", "stopped"):
                raise ValueError("Wait for this help turn to finish before deleting it")
            c.execute("DELETE FROM help_sessions WHERE id=%s", (sid,))
    return True


# ── tickets (empty until a filer is lifted; shape 1:1 with legacy) ────────────
def list_tickets(status: Optional[str] = None, limit: int = 200) -> list:
    with _db() as c:
        cols = ", ".join(_TICKET_COLS)
        if status:
            rows = c.execute(f"SELECT {cols} FROM help_tickets WHERE status=%s"
                             " ORDER BY updated DESC LIMIT %s", (status, int(limit))).fetchall()
        else:
            rows = c.execute(f"SELECT {cols} FROM help_tickets ORDER BY updated DESC LIMIT %s",
                             (int(limit),)).fetchall()
    return [dict(r) for r in rows]


def pending_count() -> int:
    with _db() as c:
        return int(c.execute("SELECT count(*) AS n FROM help_tickets WHERE status='pending'")
                   .fetchone()["n"])


def get_ticket(tid: int) -> Optional[dict]:
    with _db() as c:
        cols = ", ".join(_TICKET_COLS)
        return c.execute(f"SELECT {cols} FROM help_tickets WHERE id=%s", (int(tid),)).fetchone()


def file_operator_ticket(description: str, proposed_action: str, context: str) -> int:
    """File a pending operator request; never execute the proposed action."""
    from psycopg.types.json import Jsonb
    now = time.time()
    with _db() as c:
        row = c.execute(
            "INSERT INTO help_tickets (kind,status,created,updated,title,detail,occurrences) "
            "VALUES ('operator-request','pending',%s,%s,%s,%s,1) RETURNING id",
            (now, now, description[:120], Jsonb({"description": description,
                "proposed_action": proposed_action, "context": context}))).fetchone()
    return int(row["id"])


def set_ticket_status(tid: int, status: str, result: Optional[dict] = None) -> Optional[dict]:
    if status not in TICKET_STATUSES:
        raise ValueError(f"status must be one of {TICKET_STATUSES}")
    from psycopg.types.json import Jsonb
    with _db() as c:
        cols = ", ".join(_TICKET_COLS)
        return c.execute(f"UPDATE help_tickets SET status=%s, result=%s, updated=%s WHERE id=%s"
                         f" RETURNING {cols}",
                         (status, Jsonb(result or {}), time.time(), int(tid))).fetchone()
