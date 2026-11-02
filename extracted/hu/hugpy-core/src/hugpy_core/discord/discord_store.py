"""The Discord bot's state over the hugpy_core DB.

The API of legacy central's ``functions.imports.utils.discord_bindings`` (a single
JSON file under fcntl lock), re-homed onto the core Postgres DB (DB is truth,
operator ruling). Every function here mirrors a method of the old
``DiscordBindingStore`` 1:1 — same arguments, same returned public shape — so
``discord_routes`` is a straight lift and the bot/console see no wire change.

Connection: the one core DSN (``modeldb._conn`` → ``HUGPY_CORE_DB``); no new env
name. ids are Discord snowflakes carried as strings; timestamps are epoch-second
floats so ``since``/``ts`` comparisons round-trip exactly.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

from hugpy_core.models.modeldb import _conn

_OUTBOX_KEEP = 200   # trim the outbox tail so the table can't grow unbounded
_MSGS_KEEP = 200     # cap transcript length per bridge

DEFER_MODES = ("auto", "defer", "directive")
BRAINS = ("model", "keeper")
LOG_MODES = ("open", "none")

_SESSION_TOKEN_BYTES = 32


def _norm_id(value: Any) -> Optional[str]:
    """A Discord snowflake as a non-empty string, or None."""
    if value is None:
        return None
    s = str(value).strip()
    return s or None


def _jsonb(value):
    from psycopg.types.json import Jsonb
    return Jsonb(value)


# ── bindings ────────────────────────────────────────────────────────────────
def _public_binding(r: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": r.get("id"),
        "model_key": r.get("model_key"),
        "channel_id": r.get("channel_id"),
        "user_id": r.get("user_id"),
        "label": r.get("label") or "",
        "enabled": r.get("enabled", True),
        "created_at": r.get("created_at"),
    }


def list_bindings() -> List[Dict[str, Any]]:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM discord_bindings ORDER BY created_at")
        return [_public_binding(r) for r in cur.fetchall()]


def add_binding(*, model_key: str, channel_id=None, user_id=None,
                label: Optional[str] = None) -> Dict[str, Any]:
    channel_id = _norm_id(channel_id)
    user_id = _norm_id(user_id)
    if channel_id is None and user_id is None:
        raise ValueError("a binding needs a channel_id and/or a user_id")
    row = {"id": uuid.uuid4().hex, "model_key": model_key, "channel_id": channel_id,
           "user_id": user_id, "label": (label or "").strip(), "enabled": True,
           "created_at": time.time()}
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO discord_bindings (id, model_key, channel_id, user_id, label, enabled, created_at)"
            " VALUES (%(id)s,%(model_key)s,%(channel_id)s,%(user_id)s,%(label)s,%(enabled)s,%(created_at)s)",
            row)
    return _public_binding(row)


def remove_binding(binding_id: str) -> bool:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM discord_bindings WHERE id=%s", (binding_id,))
        return cur.rowcount > 0


def resolve(channel_id=None, user_id=None) -> Optional[str]:
    """Most specific enabled binding wins: (channel AND user) > channel > user."""
    channel_id = _norm_id(channel_id)
    user_id = _norm_id(user_id)
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT model_key, channel_id, user_id FROM discord_bindings WHERE enabled")
        bindings = cur.fetchall()
    if channel_id and user_id:
        for b in bindings:
            if b["channel_id"] == channel_id and b["user_id"] == user_id:
                return b["model_key"]
    if channel_id:
        for b in bindings:
            if b["channel_id"] == channel_id and not b["user_id"]:
                return b["model_key"]
    if user_id:
        for b in bindings:
            if b["user_id"] == user_id and not b["channel_id"]:
                return b["model_key"]
    return None


# ── outbox (model -> channel push) ────────────────────────────────────────────
def _public_outbox(r: Dict[str, Any]) -> Dict[str, Any]:
    msg = {"id": r.get("id"), "binding_id": r.get("binding_id"),
           "channel_id": r.get("channel_id"), "user_id": r.get("user_id"),
           "content": r.get("content"), "created_at": r.get("created_at"),
           "delivered": r.get("delivered", False)}
    if r.get("delivered_at") is not None:
        msg["delivered_at"] = r["delivered_at"]
    if r.get("options"):
        msg["options"] = r["options"]
    return msg


def enqueue_outbound(*, content: str, channel_id=None, user_id=None,
                     binding_id: Optional[str] = None,
                     options: Optional[list] = None) -> Dict[str, Any]:
    channel_id = _norm_id(channel_id)
    user_id = _norm_id(user_id)
    with _conn() as conn, conn.cursor() as cur:
        if binding_id and channel_id is None and user_id is None:
            cur.execute("SELECT channel_id, user_id FROM discord_bindings WHERE id=%s", (binding_id,))
            b = cur.fetchone()
            if b:
                channel_id = b["channel_id"]
                user_id = b["user_id"]
        if channel_id is None and user_id is None:
            raise ValueError("outbound needs a channel_id, user_id, or a known binding_id")
        row = {"id": uuid.uuid4().hex, "binding_id": binding_id, "channel_id": channel_id,
               "user_id": user_id, "content": content, "created_at": time.time(),
               "delivered": False, "delivered_at": None,
               "options": list(options) if isinstance(options, list) and options else None}
        cur.execute(
            "INSERT INTO discord_outbox (id, binding_id, channel_id, user_id, content, options,"
            " created_at, delivered, delivered_at) VALUES (%(id)s,%(binding_id)s,%(channel_id)s,"
            "%(user_id)s,%(content)s,%(options)s,%(created_at)s,%(delivered)s,%(delivered_at)s)",
            {**row, "options": _jsonb(row["options"]) if row["options"] else None})
    return _public_outbox(row)


def drain_outbound(limit: int = 50) -> List[Dict[str, Any]]:
    """Hand out undelivered messages once (at-most-once) and mark them delivered."""
    now = time.time()
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE discord_outbox SET delivered=TRUE, delivered_at=%s WHERE id IN"
            " (SELECT id FROM discord_outbox WHERE NOT delivered ORDER BY created_at LIMIT %s)"
            " RETURNING *", (now, int(limit)))
        out = [_public_outbox(r) for r in cur.fetchall()]
        # trim the whole outbox to the most recent _OUTBOX_KEEP rows (delivered tail)
        cur.execute(
            "DELETE FROM discord_outbox WHERE id NOT IN"
            " (SELECT id FROM discord_outbox ORDER BY created_at DESC LIMIT %s)", (_OUTBOX_KEEP,))
    return out


# ── channel / user snapshots (the bot reports what it can see) ────────────────
def set_channels(channels: List[Dict[str, Any]]) -> Dict[str, Any]:
    now = time.time()
    clean: List[Dict[str, Any]] = []
    seen = set()
    for c in channels or []:
        cid = _norm_id(c.get("id"))
        if not cid or cid in seen:
            continue
        seen.add(cid)
        clean.append({"id": cid, "name": str(c.get("name") or "").strip() or cid,
                      "guild": str(c.get("guild") or "").strip(),
                      "guild_id": _norm_id(c.get("guild_id")), "reported_at": now})
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM discord_channels")
        if clean:
            cur.executemany(
                "INSERT INTO discord_channels (id, name, guild, guild_id, reported_at)"
                " VALUES (%(id)s,%(name)s,%(guild)s,%(guild_id)s,%(reported_at)s)", clean)
    return {"count": len(clean), "channels_at": now if clean else 0}


def get_channels() -> Dict[str, Any]:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name, guild, guild_id FROM discord_channels"
                    " ORDER BY lower(guild), lower(name)")
        rows = cur.fetchall()
        cur.execute("SELECT max(reported_at) AS at FROM discord_channels")
        at = (cur.fetchone() or {}).get("at") or 0
    return {"channels": rows, "channels_at": at}


def set_users(users: List[Dict[str, Any]]) -> Dict[str, Any]:
    now = time.time()
    clean: List[Dict[str, Any]] = []
    seen = set()
    for u in users or []:
        uid = _norm_id(u.get("id"))
        if not uid or uid in seen:
            continue
        seen.add(uid)
        clean.append({"id": uid, "name": str(u.get("name") or "").strip() or uid,
                      "guild": str(u.get("guild") or "").strip(), "reported_at": now})
    clean.sort(key=lambda u: u["name"].lower())
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM discord_users")
        if clean:
            cur.executemany(
                "INSERT INTO discord_users (id, name, guild, reported_at)"
                " VALUES (%(id)s,%(name)s,%(guild)s,%(reported_at)s)", clean)
    return {"count": len(clean), "users_at": now if clean else 0}


def get_users() -> Dict[str, Any]:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name, guild FROM discord_users ORDER BY lower(name)")
        rows = cur.fetchall()
        cur.execute("SELECT max(reported_at) AS at FROM discord_users")
        at = (cur.fetchone() or {}).get("at") or 0
    return {"users": rows, "users_at": at}


# ── bridges (a console session <-> a Discord channel) ─────────────────────────
def _public_bridge(r: Dict[str, Any]) -> Dict[str, Any]:
    return {"id": r.get("id"), "channel_id": r.get("channel_id"), "user_id": r.get("user_id"),
            "model_key": r.get("model_key"), "directive": r.get("directive") or "",
            "defer_mode": r.get("defer_mode"), "brain": r.get("brain"),
            "keeper_target": r.get("keeper_target"), "log_mode": r.get("log_mode"),
            "created_at": r.get("created_at")}


def add_bridge(*, channel_id, model_key=None, user_id=None, directive: str = "",
               defer_mode: str = "auto", brain: str = "model",
               keeper_target: Optional[str] = None, log_mode: str = "open") -> Dict[str, Any]:
    channel_id = _norm_id(channel_id)
    if channel_id is None:
        raise ValueError("a bridge needs a channel_id")
    if defer_mode not in DEFER_MODES:
        raise ValueError(f"defer_mode must be one of {DEFER_MODES}")
    if brain not in BRAINS:
        raise ValueError(f"brain must be one of {BRAINS}")
    if log_mode not in LOG_MODES:
        raise ValueError(f"log_mode must be one of {LOG_MODES}")
    if log_mode == "none" and (brain != "model" or defer_mode != "auto"):
        raise ValueError("no-logs is only allowed for a model bridge in auto mode — "
                         "keeper/defer/session bridges need a retained transcript to function")
    row = {"id": uuid.uuid4().hex, "channel_id": channel_id, "user_id": _norm_id(user_id),
           "model_key": model_key, "directive": (directive or "").strip(),
           "defer_mode": defer_mode, "brain": brain,
           "keeper_target": (keeper_target or "").strip() or None,
           "log_mode": log_mode, "created_at": time.time()}
    with _conn() as conn, conn.cursor() as cur:
        # one bridge per channel — replace any existing for this channel
        cur.execute("DELETE FROM discord_bridges WHERE channel_id=%s", (channel_id,))
        cur.execute(
            "INSERT INTO discord_bridges (id, channel_id, user_id, model_key, directive, defer_mode,"
            " brain, keeper_target, log_mode, created_at) VALUES (%(id)s,%(channel_id)s,%(user_id)s,"
            "%(model_key)s,%(directive)s,%(defer_mode)s,%(brain)s,%(keeper_target)s,%(log_mode)s,"
            "%(created_at)s)", row)
    return _public_bridge(row)


def list_bridges() -> List[Dict[str, Any]]:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM discord_bridges ORDER BY created_at")
        return [_public_bridge(r) for r in cur.fetchall()]


def get_bridge(bridge_id: str) -> Optional[Dict[str, Any]]:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM discord_bridges WHERE id=%s", (bridge_id,))
        r = cur.fetchone()
    return _public_bridge(r) if r else None


def remove_bridge(bridge_id: str) -> bool:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM discord_bridges WHERE id=%s", (bridge_id,))  # messages cascade
        return cur.rowcount > 0


def bridge_for_channel(channel_id) -> Optional[Dict[str, Any]]:
    channel_id = _norm_id(channel_id)
    if channel_id is None:
        return None
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM discord_bridges WHERE channel_id=%s", (channel_id,))
        r = cur.fetchone()
    return _public_bridge(r) if r else None


def bridged_channel_ids() -> List[str]:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT channel_id FROM discord_bridges WHERE channel_id IS NOT NULL")
        return [r["channel_id"] for r in cur.fetchall()]


def _public_message(r: Dict[str, Any]) -> Dict[str, Any]:
    msg = {"id": r.get("id"), "bridge_id": r.get("bridge_id"), "direction": r.get("direction"),
           "source": r.get("source"), "author": r.get("author") or "",
           "content": r.get("content"), "attachments": r.get("attachments") or [],
           "status": r.get("status"), "ts": r.get("ts")}
    if r.get("options"):
        msg["options"] = r["options"]
    return msg


def append_message(bridge_id: str, *, direction: str, source: str, content: str,
                   author: Optional[str] = None, status: str = "sent",
                   attachments: Optional[List[Dict[str, Any]]] = None,
                   options: Optional[list] = None) -> Optional[Dict[str, Any]]:
    row = {"id": uuid.uuid4().hex, "bridge_id": bridge_id, "direction": direction,
           "source": source, "author": author or "", "content": content,
           "attachments": attachments or [], "status": status,
           "options": list(options) if isinstance(options, list) and options else None,
           "ts": time.time()}
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT log_mode FROM discord_bridges WHERE id=%s", (bridge_id,))
        bridge = cur.fetchone()
        if bridge is None:
            return None
        if (bridge.get("log_mode") or "open") == "none":
            # Ephemeral bridge: the message transits (caller still gets it) but nothing is retained.
            return _public_message(row)
        cur.execute(
            "INSERT INTO discord_bridge_messages (id, bridge_id, direction, source, author, content,"
            " attachments, status, options, ts) VALUES (%(id)s,%(bridge_id)s,%(direction)s,%(source)s,"
            "%(author)s,%(content)s,%(attachments)s,%(status)s,%(options)s,%(ts)s)",
            {**row, "attachments": _jsonb(row["attachments"]),
             "options": _jsonb(row["options"]) if row["options"] else None})
        # cap the transcript per bridge
        cur.execute(
            "DELETE FROM discord_bridge_messages WHERE bridge_id=%s AND id NOT IN"
            " (SELECT id FROM discord_bridge_messages WHERE bridge_id=%s ORDER BY ts DESC LIMIT %s)",
            (bridge_id, bridge_id, _MSGS_KEEP))
    return _public_message(row)


def get_messages(bridge_id: str, since: float = 0.0) -> List[Dict[str, Any]]:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM discord_bridge_messages WHERE bridge_id=%s AND ts > %s ORDER BY ts",
                    (bridge_id, float(since or 0)))
        return [_public_message(r) for r in cur.fetchall()]


def update_message(bridge_id: str, msg_id: str, *, status: Optional[str] = None,
                   content: Optional[str] = None) -> Optional[Dict[str, Any]]:
    sets, params = [], {"bridge_id": bridge_id, "msg_id": msg_id}
    if status is not None:
        sets.append("status=%(status)s")
        params["status"] = status
    if content is not None:
        sets.append("content=%(content)s")
        params["content"] = content
    with _conn() as conn, conn.cursor() as cur:
        if sets:
            cur.execute(f"UPDATE discord_bridge_messages SET {', '.join(sets)}"
                        " WHERE bridge_id=%(bridge_id)s AND id=%(msg_id)s RETURNING *", params)
        else:
            cur.execute("SELECT * FROM discord_bridge_messages WHERE bridge_id=%s AND id=%s",
                        (bridge_id, msg_id))
        r = cur.fetchone()
    return _public_message(r) if r else None


def clear_messages(bridge_id: str) -> Optional[int]:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT 1 FROM discord_bridges WHERE id=%s", (bridge_id,))
        if cur.fetchone() is None:
            return None
        cur.execute("DELETE FROM discord_bridge_messages WHERE bridge_id=%s", (bridge_id,))
        return cur.rowcount or 0


# ── comms sessions (scoped bearer tokens for terminal agents) ─────────────────
def _public_session(r: Dict[str, Any]) -> Dict[str, Any]:
    return {"id": r.get("id"), "channel_id": r.get("channel_id"), "label": r.get("label") or "",
            "author": r.get("author"), "created_at": r.get("created_at"),
            "expires_at": r.get("expires_at"), "revoked": r.get("revoked", False),
            "last_used": r.get("last_used")}


def add_session(*, channel_id, label: str = "", ttl_hours: Optional[float] = None,
                author: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
    channel_id = _norm_id(channel_id)
    if channel_id is None:
        raise ValueError("a session needs a channel_id")
    token = secrets.token_urlsafe(_SESSION_TOKEN_BYTES)
    now = time.time()
    row = {"id": uuid.uuid4().hex, "channel_id": channel_id, "label": (label or "").strip(),
           "author": (author or "").strip() or None,
           "token_sha256": hashlib.sha256(token.encode("utf-8")).hexdigest(),
           "created_at": now,
           "expires_at": (now + float(ttl_hours) * 3600.0) if ttl_hours else None,
           "revoked": False, "last_used": None}
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO discord_sessions (id, channel_id, label, author, token_sha256, created_at,"
            " expires_at, revoked, last_used) VALUES (%(id)s,%(channel_id)s,%(label)s,%(author)s,"
            "%(token_sha256)s,%(created_at)s,%(expires_at)s,%(revoked)s,%(last_used)s)", row)
    return token, _public_session(row)


def list_sessions() -> List[Dict[str, Any]]:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM discord_sessions ORDER BY created_at")
        return [_public_session(r) for r in cur.fetchall()]


def revoke_session(session_id: str) -> bool:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE discord_sessions SET revoked=TRUE WHERE id=%s AND NOT revoked",
                    (session_id,))
        return cur.rowcount > 0


def delete_session(session_id: str) -> bool:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM discord_sessions WHERE id=%s", (session_id,))
        return cur.rowcount > 0


def prune_sessions() -> int:
    now = time.time()
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM discord_sessions WHERE revoked"
                    " OR (expires_at IS NOT NULL AND expires_at < %s)", (now,))
        return cur.rowcount or 0


def session_by_token(token: str) -> Optional[Dict[str, Any]]:
    """Presented bearer token -> live session dict, or None (bad/revoked/expired —
    indistinguishable, no oracle). last_used stamped at most once a minute."""
    if not token:
        return None
    digest = hashlib.sha256(str(token).encode("utf-8")).hexdigest()
    now = time.time()
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM discord_sessions WHERE token_sha256=%s", (digest,))
        for s in cur.fetchall():
            if not hmac.compare_digest(s.get("token_sha256") or "", digest):
                continue
            if s.get("revoked") or (s.get("expires_at") and now > s["expires_at"]):
                return None
            if (s.get("last_used") or 0) < now - 60.0:
                cur.execute("UPDATE discord_sessions SET last_used=%s WHERE id=%s", (now, s["id"]))
            return _public_session_internal(s)
    return None


def _public_session_internal(s: Dict[str, Any]) -> Dict[str, Any]:
    """Like _public_session but keeps channel_id for the session verbs (they need it)."""
    return _public_session(s)


# ── per-user prefs (Discord /model → the user's default model) ────────────────
def set_pref(user_id: str, patch: Dict[str, Any]) -> Dict[str, Any]:
    """Merge ``patch`` into the user's prefs value and return the merged value."""
    now = time.time()
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT value FROM discord_prefs WHERE user_id=%s", (user_id,))
        row = cur.fetchone()
        value = dict(row["value"]) if row and isinstance(row.get("value"), dict) else {}
        value.update(patch)
        cur.execute(
            "INSERT INTO discord_prefs (user_id, value, updated_at) VALUES (%s,%s,%s)"
            " ON CONFLICT (user_id) DO UPDATE SET value=EXCLUDED.value, updated_at=EXCLUDED.updated_at",
            (user_id, _jsonb(value), now))
    return value


def get_pref(user_id: str) -> Dict[str, Any]:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT value FROM discord_prefs WHERE user_id=%s", (user_id,))
        row = cur.fetchone()
    return dict(row["value"]) if row and isinstance(row.get("value"), dict) else {}
