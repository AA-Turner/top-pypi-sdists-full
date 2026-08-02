"""NX data client for the Supabase backend.

All functions are designed to fail gracefully: if Supabase is unreachable,
import fails, or any call errors, the CLI keeps working and the function
returns a safe default (usually None).

Writes that do not need to return data run in daemon threads so they never
block the REPL.
"""

import hashlib
import os
import threading
import uuid
from datetime import datetime, timezone

from nx_obfuscate import SB

try:
    from supabase import create_client

    _HAS_SUPABASE = True
except Exception:  # pragma: no cover
    create_client = None  # type: ignore[assignment]
    _HAS_SUPABASE = False


SUPABASE_URL = os.environ.get(
    "NX_SUPABASE_URL", SB["nx_url"]
)
SUPABASE_ANON_KEY = os.environ.get(
    "NX_SUPABASE_ANON_KEY",
    SB["anon_key"],
)
SUPABASE_SERVICE_KEY = os.environ.get("NX_SUPABASE_SERVICE_KEY")


def _now_utc():
    return datetime.now(timezone.utc).isoformat()


def _spawn(target, args=(), kwargs=None):
    """Run target in a daemon thread and return immediately."""
    if kwargs is None:
        kwargs = {}
    thread = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread


_JWT_MISMATCH_WARNED = False


def init_client(service_key=None, user_jwt=None):
    """Create and return a Supabase client, or None if unavailable.

    If a user JWT is supplied, create an anon client and authenticate the
    PostgREST session so RLS policies are enforced for reads and writes.
    Otherwise, fall back to the service_role key when available.
    """
    if not _HAS_SUPABASE:
        return None
    if not SUPABASE_URL:
        return None
    key = SUPABASE_ANON_KEY if user_jwt else (service_key or SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY)
    if not key:
        return None
    try:
        client = create_client(SUPABASE_URL, key)
        if user_jwt:
            client.postgrest.auth(user_jwt)
        return client
    except Exception:
        return None


def get_supabase_client(service_key=None, user_jwt=None):
    """Convenience alias for init_client."""
    return init_client(service_key=service_key, user_jwt=user_jwt)


def _content_hash(content):
    """Stable hash used for nx_memory deduplication."""
    return hashlib.sha256((content or "").encode("utf-8")).hexdigest()


def save_memory(client, user_id, content, label=None, world=None, source=None, metadata=None):
    """Insert a row into nx_memory, falling back to a minimal insert if the
    extended columns (label, source, world, metadata) do not yet exist.

    Returns the inserted row on success, or None on failure.
    """
    client = _client_or_none(client)
    if client is None or not user_id:
        return None

    full_row = {
        "user_id": user_id,
        "content": content or "",
        "content_hash": _content_hash(content),
    }
    if label is not None:
        full_row["label"] = label
    if world is not None:
        full_row["world"] = world
    if source is not None:
        full_row["source"] = source
    if metadata is not None:
        full_row["metadata"] = metadata

    try:
        result = client.table("nx_memory").insert(full_row).execute()
        return result.data[0] if result.data else None
    except Exception as exc:
        err = str(exc).lower()
        # Surface JWT/RLS rejection clearly in the log so on-call can
        # diagnose without staring at the silent-None return.
        if "pgrst301" in err or "no suitable key" in err or "wrong key type" in err:
            try:
                from pathlib import Path
                log = Path.home() / ".nx" / "logs" / "error.log"
                log.parent.mkdir(parents=True, exist_ok=True)
                with open(log, "a", encoding="utf-8") as f:
                    f.write(
                        "\nnx_memory JWT rejected — likely cross-project config mismatch "
                        "(user token from nexplora-v2 project, nx_memory expects its own "
                        "signing key). Server-side fix required.\n"
                    )
            except Exception:
                pass
            # Surface ONCE per process to the operator (not just the log) so a
            # silently-failing cloud brain is visible. Local-first memory keeps
            # working regardless.
            global _JWT_MISMATCH_WARNED
            if not _JWT_MISMATCH_WARNED:
                _JWT_MISMATCH_WARNED = True
                try:
                    import sys as _sys
                    _sys.stderr.write(
                        "  cloud memory sync is paused (session needs a refresh) — "
                        "local memory still active.\n"
                    )
                except Exception:
                    pass
            return None
        if "column" in err or "nx_memory" in err:
            try:
                minimal = {
                    "user_id": user_id,
                    "content": content or "",
                    "content_hash": _content_hash(content),
                }
                result = client.table("nx_memory").insert(minimal).execute()
                return result.data[0] if result.data else None
            except Exception:
                pass
        return None


def _client_or_none(client):
    return client if client is not None else init_client()


def upsert_user(client, email):
    """Create or get an nx_users row and return its id."""
    client = _client_or_none(client)
    if client is None or not email:
        return None
    try:
        existing = (
            client.table("nx_users")
            .select("id")
            .eq("email", email)
            .limit(1)
            .execute()
        )
        if existing.data:
            return existing.data[0].get("id")

        inserted = (
            client.table("nx_users")
            .insert({"email": email})
            .execute()
        )
        if inserted.data:
            return inserted.data[0].get("id")
        return None
    except Exception:
        return None


def create_session(client, user_id, surface, project_id=None, model_primary=None):
    """Insert an nx_sessions row and return the session_id."""
    client = _client_or_none(client)
    if client is None or not user_id:
        return None
    try:
        session_id = str(uuid.uuid4())
        row = {
            "id": session_id,
            "user_id": user_id,
            "surface": surface,
            "started_at": _now_utc(),
            "message_count": 0,
            "total_tokens": 0,
        }
        if project_id is not None:
            row["project_id"] = project_id
        if model_primary is not None:
            row["model_primary"] = model_primary
        result = client.table("nx_sessions").insert(row).execute()
        if result.data:
            return result.data[0].get("id")
        return session_id
    except Exception:
        return None


def end_session(session_id, message_count=0, total_tokens=0, client=None):
    """Update nx_sessions with ended_at and counters (fire-and-forget)."""
    client = _client_or_none(client)
    if client is None or not session_id:
        return

    def _do():
        try:
            client.table("nx_sessions").update(
                {
                    "ended_at": _now_utc(),
                    "message_count": message_count,
                    "total_tokens": total_tokens,
                }
            ).eq("id", session_id).execute()
        except Exception:
            pass

    _spawn(_do)


def save_message(
    client,
    session_id,
    user_id,
    role,
    content,
    world=None,
    model=None,
    provider=None,
    tokens_in=0,
    tokens_out=0,
):
    """Insert an nx_messages row (fire-and-forget)."""
    client = _client_or_none(client)
    if client is None or not session_id or not user_id:
        return

    def _do():
        try:
            row = {
                "id": str(uuid.uuid4()),
                "session_id": session_id,
                "user_id": user_id,
                "role": role,
                "content": content or "",
                "tokens_in": tokens_in or 0,
                "tokens_out": tokens_out or 0,
                "created_at": _now_utc(),
            }
            if world is not None:
                row["world"] = world
            if model is not None:
                row["model_used"] = model
            if provider is not None:
                row["provider"] = provider
            client.table("nx_messages").insert(row).execute()
        except Exception:
            pass

    _spawn(_do)


def get_operation_context(user_id, world, project_id=None, client=None):
    """Fetch the nx_operation_context row for a user/world, or None."""
    client = _client_or_none(client)
    if client is None or not user_id or not world:
        return None
    try:
        query = (
            client.table("nx_operation_context")
            .select("*")
            .eq("user_id", user_id)
            .eq("world", world)
        )
        if project_id is not None:
            query = query.eq("project_id", project_id)
        result = query.limit(1).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None


def update_operation_context(
    user_id, world, summary, last_action, project_id=None, client=None
):
    """Upsert an nx_operation_context row (fire-and-forget)."""
    client = _client_or_none(client)
    if client is None or not user_id or not world:
        return

    def _do():
        try:
            now = _now_utc()
            existing_query = (
                client.table("nx_operation_context")
                .select("id")
                .eq("user_id", user_id)
                .eq("world", world)
            )
            if project_id is not None:
                existing_query = existing_query.eq("project_id", project_id)
            existing = existing_query.limit(1).execute()

            row = {
                "user_id": user_id,
                "world": world,
                "summary": summary or "",
                "last_action": last_action or "",
                "updated_at": now,
            }
            if project_id is not None:
                row["project_id"] = project_id

            if existing.data:
                ctx_id = existing.data[0].get("id")
                client.table("nx_operation_context").update(row).eq("id", ctx_id).execute()
            else:
                row["id"] = str(uuid.uuid4())
                client.table("nx_operation_context").insert(row).execute()
        except Exception:
            pass

    _spawn(_do)
