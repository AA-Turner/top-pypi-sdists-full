"""Token usage helpers for the operator console projection."""

from __future__ import annotations

from collections.abc import Mapping
import json
import sqlite3
from typing import Any


def _json_loads(value: object, fallback: Any) -> Any:
    if value is None:
        return fallback
    try:
        return json.loads(str(value))
    except (TypeError, ValueError, json.JSONDecodeError):
        return fallback


def _table_exists(connection: sqlite3.Connection, table: str) -> bool:
    row = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone()
    return row is not None


def _query(
    connection: sqlite3.Connection,
    sql: str,
    params: tuple[object, ...] = (),
) -> list[dict[str, Any]]:
    try:
        rows = connection.execute(sql, params).fetchall()
    except sqlite3.Error:
        return []
    return [dict(row) for row in rows]


def _int_value(value: object) -> int:
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def _cache_hit_rate_label(cached_tokens: int, prompt_tokens: int) -> str:
    if prompt_tokens <= 0:
        return "n/a"
    return f"{(cached_tokens / prompt_tokens) * 100:.1f}%"


def _cache_summary(*, cached_tokens: int, prompt_tokens: int, creation_tokens: int) -> str:
    if prompt_tokens <= 0:
        return "No input token usage recorded for this query."
    label = _cache_hit_rate_label(cached_tokens, prompt_tokens)
    creation_note = f"; {creation_tokens} cache-write token(s)" if creation_tokens else ""
    return f"{label} cache hit ({cached_tokens}/{prompt_tokens} input token(s) cached{creation_note})."


def normalize_token_usage_row(row: Mapping[str, Any]) -> dict[str, Any]:
    record = dict(row)
    metadata_payload = _json_loads(record.pop("metadata_json", None), {})
    metadata = dict(metadata_payload) if isinstance(metadata_payload, Mapping) else {}
    prompt_tokens = _int_value(record.get("prompt_tokens"))
    cached_tokens = _int_value(
        metadata.get("cached_prompt_tokens")
        or metadata.get("cachedPromptTokens")
        or metadata.get("cache_read_input_tokens")
    )
    creation_tokens = _int_value(
        metadata.get("cache_creation_prompt_tokens")
        or metadata.get("cacheCreationPromptTokens")
        or metadata.get("cache_creation_input_tokens")
    )
    cache_usage_reported = bool(
        metadata.get("cache_usage_reported")
        or metadata.get("cacheUsageReported")
        or "cached_prompt_tokens" in metadata
        or "cachedPromptTokens" in metadata
        or "cache_read_input_tokens" in metadata
        or "cache_creation_prompt_tokens" in metadata
        or "cacheCreationPromptTokens" in metadata
        or "cache_creation_input_tokens" in metadata
    )
    record["metadata"] = metadata
    record["cached_prompt_tokens"] = cached_tokens
    record["cache_creation_prompt_tokens"] = creation_tokens
    record["cache_usage_reported"] = cache_usage_reported
    if cache_usage_reported:
        record["cache_hit_rate_label"] = _cache_hit_rate_label(cached_tokens, prompt_tokens)
        record["cache_summary"] = _cache_summary(
            cached_tokens=cached_tokens,
            prompt_tokens=prompt_tokens,
            creation_tokens=creation_tokens,
        )
    else:
        record["cache_hit_rate_label"] = "n/a"
        record["cache_summary"] = "Cache usage was not reported by the provider for this query."
    if cache_usage_reported and prompt_tokens > 0:
        record["cache_hit_rate"] = round(cached_tokens / prompt_tokens, 4)
    return record


def token_usage_rows_for_session(connection: sqlite3.Connection, session_id: object) -> list[dict[str, Any]]:
    if not _table_exists(connection, "token_usage_events"):
        return []
    rows = _query(
        connection,
        """
        SELECT usage_id, session_id, profile_id, run_id, source_event_id,
               provider_id, model_id, prompt_tokens, completion_tokens,
               total_tokens, unit, metadata_json, created_at
        FROM token_usage_events
        WHERE session_id = ?
        ORDER BY created_at ASC, usage_id ASC
        LIMIT 500
        """,
        (session_id,),
    )
    return [normalize_token_usage_row(row) for row in rows]


def summarize_token_usage(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not rows:
        return None
    prompt_tokens = sum(_int_value(row.get("prompt_tokens")) for row in rows)
    completion_tokens = sum(_int_value(row.get("completion_tokens")) for row in rows)
    total_tokens = sum(_int_value(row.get("total_tokens")) for row in rows)
    cached_tokens = sum(_int_value(row.get("cached_prompt_tokens")) for row in rows)
    creation_tokens = sum(_int_value(row.get("cache_creation_prompt_tokens")) for row in rows)
    cache_usage_reported = any(bool(row.get("cache_usage_reported")) for row in rows)
    summary = {
        "promptTokens": prompt_tokens,
        "completionTokens": completion_tokens,
        "totalTokens": total_tokens,
        "cachedPromptTokens": cached_tokens,
        "cacheCreationPromptTokens": creation_tokens,
        "cacheUsageReported": cache_usage_reported,
        "cacheHitRateLabel": _cache_hit_rate_label(cached_tokens, prompt_tokens) if cache_usage_reported else "n/a",
        "cacheSummary": (
            _cache_summary(
                cached_tokens=cached_tokens,
                prompt_tokens=prompt_tokens,
                creation_tokens=creation_tokens,
            )
            if cache_usage_reported
            else "Cache usage was not reported by the provider for this query."
        ),
    }
    if cache_usage_reported and prompt_tokens > 0:
        summary["cacheHitRate"] = round(cached_tokens / prompt_tokens, 4)
    latest = rows[-1]
    if latest.get("provider_id"):
        summary["providerId"] = latest["provider_id"]
    if latest.get("model_id"):
        summary["modelId"] = latest["model_id"]
    return summary


def cache_usage_fields(run: Mapping[str, Any]) -> dict[str, Any]:
    token_usage = run.get("tokenUsage")
    if not isinstance(token_usage, Mapping):
        return {}
    if not token_usage.get("cacheUsageReported"):
        return {}
    cache_summary = str(token_usage.get("cacheSummary") or "").strip()
    if not cache_summary:
        return {}
    fields: dict[str, Any] = {
        "cacheHitRateLabel": token_usage.get("cacheHitRateLabel") or "n/a",
        "cacheSummary": cache_summary,
        "promptTokens": token_usage.get("promptTokens"),
        "cachedPromptTokens": token_usage.get("cachedPromptTokens"),
        "cacheCreationPromptTokens": token_usage.get("cacheCreationPromptTokens"),
    }
    if token_usage.get("cacheHitRate") is not None:
        fields["cacheHitRate"] = token_usage.get("cacheHitRate")
    return fields
