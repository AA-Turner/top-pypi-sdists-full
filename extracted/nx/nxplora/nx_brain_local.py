"""
nx_brain_local.py — Local-first brain memory.

The brain writes to a SQLite database in ~/.nx/brain.db so memory always works,
regardless of the cloud session state. Cloud sync is a separate concern: if the
NX-scoped Supabase session is available, _brain_write_async also queues a cloud
write, but the local row is the source of truth.

This was added because the cloud bridge (Supabase edge function `nx-auth-bridge`
on the tiyoncvmleryjmoftdya project) currently rejects users who weren't
pre-provisioned in nx_memory — every brain write was silently failing.
"""
from __future__ import annotations

import json
import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path

_DB_PATH = Path.home() / ".nx" / "brain.db"
_LOCK = threading.Lock()
_INITIALIZED = False

# Brain schema version. Bump when columns change; add a step to _migrate.
BRAIN_SCHEMA_VERSION = 1


def _conn() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(_DB_PATH), timeout=5.0, isolation_level=None)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA synchronous=NORMAL")
    c.row_factory = sqlite3.Row
    return c


def _read_schema_version(c) -> int:
    """Read PRAGMA user_version. 0 means "fresh DB or pre-versioning"."""
    row = c.execute("PRAGMA user_version").fetchone()
    try:
        return int(row[0])
    except (TypeError, ValueError):
        return 0


def _migrate(c, from_version: int) -> int:
    """Forward-only migration ladder. Returns the new schema version."""
    v = from_version
    # v0 → v1: initial schema
    if v < 1:
        c.execute("""
            CREATE TABLE IF NOT EXISTS nx_memory (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     TEXT NOT NULL,
                label       TEXT,
                content     TEXT NOT NULL,
                world       TEXT,
                source      TEXT,
                metadata    TEXT,
                created_at  TEXT NOT NULL,
                synced_at   TEXT,
                sync_status TEXT DEFAULT 'pending'
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS nx_memory_user_idx ON nx_memory(user_id)")
        c.execute("CREATE INDEX IF NOT EXISTS nx_memory_label_idx ON nx_memory(user_id, label)")
        c.execute("CREATE INDEX IF NOT EXISTS nx_memory_unsynced_idx ON nx_memory(sync_status) WHERE sync_status='pending'")
        v = 1
    # Future migrations (v1 → v2 etc.) get added here.
    return v


def _ensure_schema():
    global _INITIALIZED
    if _INITIALIZED:
        return
    with _LOCK:
        if _INITIALIZED:
            return
        with _conn() as c:
            current = _read_schema_version(c)
            target = BRAIN_SCHEMA_VERSION
            if current > target:
                # Future-schema DB → refuse to migrate downward; clients on
                # older NX versions should leave it alone.
                raise RuntimeError(
                    f"brain.db is at schema v{current}; this NX expects ≤ v{target}. "
                    f"Upgrade NX with `pipx upgrade nxplora`."
                )
            new_v = _migrate(c, current)
            if new_v != current:
                c.execute(f"PRAGMA user_version = {int(new_v)}")
            try:
                os.chmod(_DB_PATH, 0o600)
            except OSError:
                pass
        _INITIALIZED = True


def schema_version() -> int:
    """Return the on-disk schema version, ensuring the schema is initialised."""
    _ensure_schema()
    with _conn() as c:
        return _read_schema_version(c)


def save(user_id: str, content: str, label: str = "", world: str = "",
         source: str = "nx_brain", metadata: dict | None = None) -> dict:
    """Insert a memory row locally. Returns the row dict."""
    _ensure_schema()
    if not user_id or not content:
        return {"error": "user_id and content are required"}
    now = datetime.now(timezone.utc).isoformat()
    md_json = json.dumps(metadata or {})
    with _LOCK, _conn() as c:
        cur = c.execute(
            """INSERT INTO nx_memory
               (user_id, label, content, world, source, metadata, created_at, sync_status)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')""",
            (user_id, label or "", content, world or "", source or "", md_json, now),
        )
        row_id = cur.lastrowid
    return {
        "success": True,
        "id": row_id,
        "user_id": user_id,
        "label": label,
        "content": content,
        "world": world,
        "source": source,
        "created_at": now,
    }


# ── flat→graph mapper (grail phase #2 STEP 2) ────────────────────────────────────────────────────────────────
# The UNIFIED brain (rckoht nx_brain_nodes) is a TYPED GRAPH; a CLI memory is a FLAT row. This maps one flat
# memory → the node body POST /api/brain/cli-write accepts, so a CLI memory becomes a real graph node in the ONE
# operator brain. PURE + deterministic. node_type inference is CONSERVATIVE (default 'concept'); the CLI's
# world/source ride in payload + sourceAttribution so context + provenance survive the lift. sourceWorld is left
# UNSET here so the route defaults source_world='cli' — CLI nodes stay identifiable for the compound proof.
VALID_NODE_TYPES = ("concept", "source", "returning_question", "decision", "contradiction", "current_edge", "pattern")


def infer_node_type(label: str = "", content: str = "", source: str = "", metadata: dict | None = None) -> str:
    """Conservative node_type for a flat CLI memory. Default 'concept'. Upgrades ONLY on a clear flat signal:
    an external source/citation → 'source'; an open question → 'returning_question'; a stated decision →
    'decision'. Never guesses contradiction/pattern/current_edge — those need graph context a flat row lacks."""
    src = str(source or "").strip().lower()
    meta = metadata if isinstance(metadata, dict) else {}
    blob = f"{label} {content}".lower()
    if (src.startswith(("http://", "https://"))
            or src in ("web", "doc", "pdf", "article", "citation", "url", "link", "browser")
            or any(k in meta for k in ("url", "link", "citation", "source_url"))):
        return "source"
    if blob.rstrip().endswith("?") or any(k in blob for k in ("open question", "still unsure", "undecided", "to be decided")):
        return "returning_question"
    if any(k in blob for k in ("decided", "decision:", "we chose", "going with", "will ship", "the plan is", "chosen:")):
        return "decision"
    return "concept"


def flat_to_node(content: str = "", label: str = "", world: str = "", source: str = "",
                 metadata: dict | None = None) -> dict:
    """Map one flat CLI memory → the typed node body for POST /api/brain/cli-write. Pure + deterministic.
    Returns {nodeType, label, payload, sourceAttribution} — sourceWorld intentionally omitted (route → 'cli')."""
    content = str(content or "")
    label = str(label or "").strip()
    world = str(world or "").strip()
    source = str(source or "").strip()
    meta = metadata if isinstance(metadata, dict) else {}
    if not label:  # a node needs a human label; derive from the first content line when the flat row lacked one
        first = content.strip().splitlines()[0].strip() if content.strip() else ""
        label = first[:80] or "note"
    node_type = infer_node_type(label, content, source, meta)
    payload: dict = {}
    if content:
        payload["content"] = content
    if world:
        payload["world"] = world
    if meta:
        payload["meta"] = meta
    attribution: dict = {"sourceKind": "nx-cli"}
    if world:
        attribution["world"] = world
    if source:
        attribution["source"] = source
    return {"nodeType": node_type, "label": label[:200], "payload": payload, "sourceAttribution": attribution}


def search(user_id: str, query: str, limit: int = 5) -> list[dict]:
    """Return up to `limit` matching rows for this user, newest first."""
    _ensure_schema()
    if not user_id or not query:
        return []
    needle = f"%{query.lower()}%"
    with _conn() as c:
        rows = c.execute(
            """SELECT id, user_id, label, content, world, source, metadata, created_at
               FROM nx_memory
               WHERE user_id = ?
                 AND (lower(content) LIKE ? OR lower(label) LIKE ?)
               ORDER BY id DESC
               LIMIT ?""",
            (user_id, needle, needle, int(limit)),
        ).fetchall()
    return [dict(r) for r in rows]


def list_recent(user_id: str, limit: int = 20) -> list[dict]:
    _ensure_schema()
    with _conn() as c:
        rows = c.execute(
            """SELECT id, label, content, world, source, created_at
               FROM nx_memory
               WHERE user_id = ?
               ORDER BY id DESC
               LIMIT ?""",
            (user_id, int(limit)),
        ).fetchall()
    return [dict(r) for r in rows]


def count(user_id: str) -> int:
    _ensure_schema()
    with _conn() as c:
        row = c.execute(
            "SELECT COUNT(*) AS n FROM nx_memory WHERE user_id = ?", (user_id,)
        ).fetchone()
    return int(row["n"]) if row else 0


def delete_by_label(user_id: str, label: str) -> int:
    _ensure_schema()
    with _LOCK, _conn() as c:
        cur = c.execute(
            "DELETE FROM nx_memory WHERE user_id = ? AND label = ?",
            (user_id, label),
        )
        return cur.rowcount


def mark_synced(row_id: int) -> None:
    _ensure_schema()
    with _LOCK, _conn() as c:
        c.execute(
            "UPDATE nx_memory SET sync_status='synced', synced_at=? WHERE id=?",
            (datetime.now(timezone.utc).isoformat(), row_id),
        )


def pending_for_sync(user_id: str, limit: int = 50) -> list[dict]:
    """Return rows that haven't yet been pushed to cloud."""
    _ensure_schema()
    with _conn() as c:
        rows = c.execute(
            """SELECT id, user_id, label, content, world, source, metadata, created_at
               FROM nx_memory
               WHERE user_id = ? AND sync_status='pending'
               ORDER BY id ASC LIMIT ?""",
            (user_id, int(limit)),
        ).fetchall()
    return [dict(r) for r in rows]
