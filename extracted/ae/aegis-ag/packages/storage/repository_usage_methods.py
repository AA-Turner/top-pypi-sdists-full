"""Token usage ledger methods for runtime storage."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import json
from uuid import uuid4

from .repository_support import _iso


def record_token_usage(
    self,
    *,
    session_id: str,
    profile_id: str,
    run_id: str | None = None,
    source_event_id: str | None = None,
    provider_id: str | None = None,
    model_id: str | None = None,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    total_tokens: int = 0,
    metadata: Mapping[str, object] | None = None,
    created_at: datetime | None = None,
) -> str:
    timestamp = _iso(created_at or datetime.now(timezone.utc))
    usage_id = f"usage:{session_id}:{uuid4().hex[:10]}"
    with self.connection() as connection:
        connection.execute(
            """
            INSERT INTO token_usage_events (
                usage_id, session_id, profile_id, run_id, source_event_id,
                provider_id, model_id, prompt_tokens, completion_tokens,
                total_tokens, unit, metadata_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                usage_id,
                session_id,
                profile_id,
                run_id,
                source_event_id,
                provider_id,
                model_id,
                max(0, int(prompt_tokens or 0)),
                max(0, int(completion_tokens or 0)),
                max(0, int(total_tokens or 0)),
                "tokens",
                json.dumps(dict(metadata or {}), sort_keys=True),
                timestamp,
            ),
        )
        connection.commit()
    return usage_id


def list_token_usage_events(
    self,
    *,
    session_id: str | None = None,
    limit: int = 500,
) -> list[dict[str, object]]:
    filters: list[str] = []
    parameters: list[object] = []
    if session_id is not None:
        filters.append("session_id = ?")
        parameters.append(session_id)
    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    parameters.append(max(1, int(limit)))
    with self.connection() as connection:
        rows = connection.execute(
            f"""
            SELECT usage_id, session_id, profile_id, run_id, source_event_id,
                   provider_id, model_id, prompt_tokens, completion_tokens,
                   total_tokens, unit, metadata_json, created_at
            FROM token_usage_events
            {where_clause}
            ORDER BY created_at DESC, usage_id ASC
            LIMIT ?
            """,
            tuple(parameters),
        ).fetchall()
    events: list[dict[str, object]] = []
    for row in rows:
        record = dict(row)
        try:
            record["metadata"] = json.loads(str(record.pop("metadata_json") or "{}"))
        except (TypeError, ValueError, json.JSONDecodeError):
            record["metadata"] = {}
        events.append(record)
    return events

