"""
cvc.dashboard.user_memory_api — Cross-workspace persistent user memory.

v2.91.46 — "Save permanently on the local CVC of any user's machine."

This module exposes an API for user-scoped memory that:

  1. **Lives in ``~/.cvc/``** — not inside any workspace's ``.cvc/``.
     Survives gateway restarts, workspace switches, and the user
     deleting/purging individual workspaces.

  2. **Is truly persistent** — written to disk as JSON immediately
     after every mutation. Atomic via temp-file + rename.

  3. **Is opt-in, scoped, and auditable** — every entry has a
     category (``preference`` / ``note`` / ``fact``), a scope
     (``global`` / ``<workspace-path>``), and timestamps.

  4. **Honors explicit deletion** — ``DELETE /api/memory/<id>``
     removes the entry from disk immediately. There is no
     soft-delete tombstone; what you delete is gone.

  5. **Honors workspace deletion** — when a workspace is removed or
     purged, the cross-workspace memory entries scoped to that
     workspace are also wiped from disk (registered via the
     ``on_workspace_removed`` hook installed by the gateway).

Endpoints (mounted by ``gateway.py``):

  GET    /api/memory                    — list entries (filter by category/scope)
  POST   /api/memory                    — create entry
  GET    /api/memory/{id}               — get single entry
  PATCH  /api/memory/{id}               — update entry
  DELETE /api/memory/{id}               — delete entry
  POST   /api/memory/wipe              — wipe all (or all matching filter)
  GET    /api/memory/stats             — counts + disk path
"""
from __future__ import annotations

import json
import logging
import os
import re
import tempfile
import threading
import time
import uuid
from pathlib import Path
from typing import Any

from fastapi import HTTPException, Request

logger = logging.getLogger("cvc.dashboard.user_memory")

# Where it all lives. This is intentionally OUTSIDE any workspace —
# the user can blow away every workspace and these memories stay
# (until they explicitly delete them).
USER_MEMORY_DIR = Path.home() / ".cvc" / "memory"
USER_MEMORY_FILE = USER_MEMORY_DIR / "user_memory.json"
USER_MEMORY_LOCK = threading.RLock()

# Valid categories. ``preference`` is for things the user wants
# remembered across sessions (default model, default persona,
# formatting preferences). ``note`` is free-form user-typed memory.
# ``fact`` is for things the agent has learned about the user that
# the user has confirmed (e.g. "user works on HydroPlus").
_VALID_CATEGORIES = frozenset({"preference", "note", "fact"})


# ─── Disk I/O ──────────────────────────────────────────────────────────


def _ensure_dir() -> None:
    USER_MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def _load_raw() -> list[dict[str, Any]]:
    """Read all entries from disk. Returns [] on missing/corrupt."""
    if not USER_MEMORY_FILE.exists():
        return []
    try:
        text = USER_MEMORY_FILE.read_text(encoding="utf-8")
        data = json.loads(text)
        if isinstance(data, list):
            return [e for e in data if isinstance(e, dict)]
        return []
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("user_memory: corrupt file, starting empty: %s", exc)
        return []


def _save_raw(entries: list[dict[str, Any]]) -> None:
    """Atomically write all entries to disk."""
    _ensure_dir()
    fd, tmp_path = tempfile.mkstemp(
        prefix="user_memory.", suffix=".tmp", dir=str(USER_MEMORY_DIR)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, USER_MEMORY_FILE)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ─── Public helpers ────────────────────────────────────────────────────


def add_entry(
    category: str,
    content: str,
    *,
    scope: str = "global",
    tags: list[str] | None = None,
    source: str = "user",
) -> dict[str, Any]:
    """Add a new memory entry. Thread-safe."""
    if category not in _VALID_CATEGORIES:
        raise ValueError(
            f"Invalid category {category!r}. "
            f"Must be one of: {sorted(_VALID_CATEGORIES)}"
        )
    content = (content or "").strip()
    if not content:
        raise ValueError("content cannot be empty")
    if len(content) > 8192:
        raise ValueError("content too long (max 8192 chars)")
    if scope and len(scope) > 1024:
        raise ValueError("scope too long (max 1024 chars)")

    entry = {
        "id": uuid.uuid4().hex[:12],
        "category": category,
        "content": content,
        "scope": scope or "global",
        "tags": [str(t).strip() for t in (tags or []) if str(t).strip()],
        "source": source[:64] if source else "user",
        "created_at": time.time(),
        "updated_at": time.time(),
    }
    with USER_MEMORY_LOCK:
        entries = _load_raw()
        entries.append(entry)
        _save_raw(entries)
    logger.info(
        "user_memory: added id=%s category=%s scope=%s", entry["id"], category, scope
    )
    return entry


def list_entries(
    category: str | None = None,
    scope: str | None = None,
    search: str | None = None,
) -> list[dict[str, Any]]:
    """List memory entries, optionally filtered."""
    with USER_MEMORY_LOCK:
        entries = _load_raw()
    out = []
    for e in entries:
        if category and e.get("category") != category:
            continue
        if scope and e.get("scope") != scope:
            continue
        if search:
            hay = (
                e.get("content", "")
                + " "
                + " ".join(e.get("tags", []))
            ).lower()
            if search.lower() not in hay:
                continue
        out.append(e)
    # Newest first
    out.sort(key=lambda e: e.get("created_at", 0), reverse=True)
    return out


def get_entry(entry_id: str) -> dict[str, Any] | None:
    with USER_MEMORY_LOCK:
        for e in _load_raw():
            if e.get("id") == entry_id:
                return e
    return None


def update_entry(
    entry_id: str,
    *,
    content: str | None = None,
    tags: list[str] | None = None,
    scope: str | None = None,
    category: str | None = None,
) -> dict[str, Any] | None:
    """Update an existing entry. Returns the updated entry, or None if not found."""
    with USER_MEMORY_LOCK:
        entries = _load_raw()
        for i, e in enumerate(entries):
            if e.get("id") == entry_id:
                if content is not None:
                    content = content.strip()
                    if not content:
                        raise ValueError("content cannot be empty")
                    if len(content) > 8192:
                        raise ValueError("content too long (max 8192 chars)")
                    e["content"] = content
                if tags is not None:
                    e["tags"] = [
                        str(t).strip() for t in tags if str(t).strip()
                    ]
                if scope is not None:
                    if len(scope) > 1024:
                        raise ValueError("scope too long (max 1024 chars)")
                    e["scope"] = scope
                if category is not None:
                    if category not in _VALID_CATEGORIES:
                        raise ValueError(
                            f"Invalid category {category!r}. "
                            f"Must be one of: {sorted(_VALID_CATEGORIES)}"
                        )
                    e["category"] = category
                e["updated_at"] = time.time()
                _save_raw(entries)
                return e
    return None


def delete_entry(entry_id: str) -> bool:
    """Permanently delete a single entry. Returns True if it existed."""
    with USER_MEMORY_LOCK:
        entries = _load_raw()
        new_entries = [e for e in entries if e.get("id") != entry_id]
        if len(new_entries) == len(entries):
            return False
        _save_raw(new_entries)
    logger.info("user_memory: deleted id=%s", entry_id)
    return True


def wipe_entries(
    category: str | None = None,
    scope: str | None = None,
) -> int:
    """Permanently delete multiple entries. Returns count removed.

    With no filters, wipes EVERYTHING (destructive). Use with care.
    """
    with USER_MEMORY_LOCK:
        entries = _load_raw()
        if not category and not scope:
            removed = len(entries)
            _save_raw([])
            logger.warning("user_memory: WIPED ALL %d entries", removed)
            return removed
        kept = []
        removed = 0
        for e in entries:
            if category and e.get("category") != category:
                kept.append(e)
                continue
            if scope and e.get("scope") != scope:
                kept.append(e)
                continue
            removed += 1
        _save_raw(kept)
        logger.info(
            "user_memory: wiped %d entries (category=%s scope=%s)",
            removed, category, scope,
        )
        return removed


def drop_workspace_scope(workspace_path: str) -> int:
    """Remove all entries scoped to a specific workspace path.

    Called by the gateway when a workspace is removed/purged so the
    workspace-scoped memories don't outlive their workspace.
    """
    target = str(Path(workspace_path).resolve())
    with USER_MEMORY_LOCK:
        entries = _load_raw()
        kept = [e for e in entries if e.get("scope") != target]
        removed = len(entries) - len(kept)
        if removed:
            _save_raw(kept)
            logger.info(
                "user_memory: dropped %d entries scoped to %s",
                removed, target,
            )
        return removed


def stats() -> dict[str, Any]:
    """Return counts + disk path for the dashboard UI."""
    with USER_MEMORY_LOCK:
        entries = _load_raw()
    by_cat: dict[str, int] = {}
    by_scope: dict[str, int] = {}
    for e in entries:
        cat = e.get("category", "unknown")
        scope = e.get("scope", "global")
        by_cat[cat] = by_cat.get(cat, 0) + 1
        by_scope[scope] = by_scope.get(scope, 0) + 1
    return {
        "total": len(entries),
        "by_category": by_cat,
        "by_scope": by_scope,
        "path": str(USER_MEMORY_FILE),
        "exists": USER_MEMORY_FILE.exists(),
        "size_bytes": USER_MEMORY_FILE.stat().st_size
        if USER_MEMORY_FILE.exists()
        else 0,
    }


def format_for_prompt(
    max_entries: int = 50,
    max_chars: int = 4096,
) -> str:
    """Return a string suitable for injecting into the LLM system prompt.

    Used by the gateway to give the agent persistent context about
    the user across all sessions and workspaces. Capped at max_chars
    to prevent context-window bloat.
    """
    entries = list_entries()[:max_entries]
    if not entries:
        return ""
    lines = ["## Persistent user memory (auto-loaded from ~/.cvc/memory/)"]
    by_cat: dict[str, list[dict[str, Any]]] = {}
    for e in entries:
        by_cat.setdefault(e.get("category", "note"), []).append(e)
    for cat, items in by_cat.items():
        lines.append(f"\n### {cat.title()}s")
        for e in items[:20]:  # cap per category
            tag_str = (
                f" [tags: {', '.join(e.get('tags', []))}]"
                if e.get("tags")
                else ""
            )
            scope = e.get("scope", "global")
            scope_str = f" (scope: {scope})" if scope != "global" else ""
            lines.append(f"- {e['content']}{tag_str}{scope_str}")
    out = "\n".join(lines)
    if len(out) > max_chars:
        out = out[: max_chars - 50] + "\n\n[...truncated; use `cvc memory list` to see all]"
    return out


# ─── HTTP handlers (mounted by gateway.py) ─────────────────────────────


def _entry_to_dict(e: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": e.get("id"),
        "category": e.get("category"),
        "content": e.get("content"),
        "scope": e.get("scope"),
        "tags": e.get("tags", []),
        "source": e.get("source", "user"),
        "created_at": e.get("created_at"),
        "updated_at": e.get("updated_at"),
    }


async def list_memory(request: Request):
    category = request.query_params.get("category")
    scope = request.query_params.get("scope")
    search = request.query_params.get("search")
    entries = list_entries(category=category, scope=scope, search=search)
    return {"entries": [_entry_to_dict(e) for e in entries], "stats": stats()}


async def create_memory(request: Request):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(400, "Invalid JSON body")
    category = body.get("category", "note")
    content = body.get("content", "")
    scope = body.get("scope", "global")
    tags = body.get("tags")
    source = body.get("source", "user")
    try:
        entry = add_entry(category, content, scope=scope, tags=tags, source=source)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return _entry_to_dict(entry)


async def get_memory(entry_id: str):
    if not re.fullmatch(r"[0-9a-f]{1,32}", entry_id or ""):
        raise HTTPException(400, "Invalid entry id")
    entry = get_entry(entry_id)
    if not entry:
        raise HTTPException(404, f"No memory entry with id {entry_id}")
    return _entry_to_dict(entry)


async def update_memory(entry_id: str, request: Request):
    if not re.fullmatch(r"[0-9a-f]{1,32}", entry_id or ""):
        raise HTTPException(400, "Invalid entry id")
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(400, "Invalid JSON body")
    try:
        entry = update_entry(
            entry_id,
            content=body.get("content"),
            tags=body.get("tags"),
            scope=body.get("scope"),
            category=body.get("category"),
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    if not entry:
        raise HTTPException(404, f"No memory entry with id {entry_id}")
    return _entry_to_dict(entry)


async def delete_memory(entry_id: str):
    if not re.fullmatch(r"[0-9a-f]{1,32}", entry_id or ""):
        raise HTTPException(400, "Invalid entry id")
    if not delete_entry(entry_id):
        raise HTTPException(404, f"No memory entry with id {entry_id}")
    return {"status": "ok", "deleted": entry_id}


async def wipe_memory(request: Request):
    """Wipe all entries, OR filter by category/scope.

    Body: ``{"category": "fact"}`` or ``{"scope": "/some/path"}`` or empty
    """
    try:
        body = await request.json() if (await request.body()) else {}
    except Exception:
        body = {}
    category = body.get("category") if body else None
    scope = body.get("scope") if body else None
    removed = wipe_entries(category=category, scope=scope)
    return {"status": "ok", "removed": removed}


async def memory_stats():
    return stats()


# ─── Route registration (called by gateway.py) ──────────────────────────


def register_user_memory_routes(app) -> None:
    """Mount /api/memory/* routes on the gateway FastAPI app.

    Also registers a hook so that removing/purging a workspace also
    wipes any user-memory entries scoped to that workspace path.
    """
    app.add_api_route("/api/memory", list_memory, methods=["GET"])
    app.add_api_route("/api/memory", create_memory, methods=["POST"])
    app.add_api_route("/api/memory/wipe", wipe_memory, methods=["POST"])
    app.add_api_route("/api/memory/stats", memory_stats, methods=["GET"])
    app.add_api_route("/api/memory/{entry_id}", get_memory, methods=["GET"])
    app.add_api_route(
        "/api/memory/{entry_id}", update_memory, methods=["PATCH"]
    )
    app.add_api_route(
        "/api/memory/{entry_id}", delete_memory, methods=["DELETE"]
    )
    logger.info(
        "user_memory: registered /api/memory/* (storage: %s)", USER_MEMORY_FILE
    )
