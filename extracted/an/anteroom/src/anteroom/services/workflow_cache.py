"""Response cache for workflow LLM steps (#988)."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any


def compute_cache_key(
    model: str,
    prompt: str,
    system_prompt: str,
    temperature: float | None,
    max_tokens: int | None,
    response_format: str | None,
) -> str:
    """SHA-256 hash of canonical JSON representation of LLM inputs."""
    canonical = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "system_prompt": system_prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "response_format": response_format,
        },
        sort_keys=True,
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def get_cached_response(
    db: Any,
    cache_key: str,
    space_id: str,
) -> dict[str, Any] | None:
    """Return cached response if found and not expired. Deletes expired on read."""
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "DELETE FROM workflow_llm_cache"
        " WHERE cache_key = ? AND space_id = ? AND expires_at IS NOT NULL AND expires_at < ?",
        (cache_key, space_id, now),
    )
    db.commit()
    row = db.execute(
        "SELECT response, prompt_tokens, completion_tokens, response_format, model"
        " FROM workflow_llm_cache WHERE cache_key = ? AND space_id = ?",
        (cache_key, space_id),
    ).fetchone()
    if not row:
        return None
    if hasattr(row, "keys"):
        return dict(row)
    return {
        "response": row[0],
        "prompt_tokens": row[1],
        "completion_tokens": row[2],
        "response_format": row[3],
        "model": row[4],
    }


def put_cached_response(
    db: Any,
    cache_key: str,
    space_id: str,
    workflow_id: str,
    model: str,
    response: str,
    prompt_tokens: int,
    completion_tokens: int,
    response_format: str | None,
    ttl_seconds: int,
) -> None:
    """Store a cached response with TTL."""
    now = datetime.now(timezone.utc)
    expires_at: str | None = None
    if ttl_seconds > 0:
        expires_at = (now + timedelta(seconds=ttl_seconds)).isoformat()
    db.execute(
        "INSERT OR REPLACE INTO workflow_llm_cache"
        " (cache_key, space_id, workflow_id, model, response, prompt_tokens,"
        " completion_tokens, response_format, created_at, expires_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            cache_key,
            space_id,
            workflow_id,
            model,
            response,
            prompt_tokens,
            completion_tokens,
            response_format,
            now.isoformat(),
            expires_at,
        ),
    )
    db.commit()


def invalidate_cache(db: Any, space_id: str | None = None) -> int:
    """Delete cache entries. Returns count of deleted rows."""
    if space_id is not None:
        cursor = db.execute("DELETE FROM workflow_llm_cache WHERE space_id = ?", (space_id,))
    else:
        cursor = db.execute("DELETE FROM workflow_llm_cache")
    db.commit()
    return cursor.rowcount
