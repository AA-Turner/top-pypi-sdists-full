"""Provider-side (built-in) tool use, read once from a settled UnifiedResponse.

A provider-hosted tool (Gemini Google Search grounding / URL context, OpenAI
web_search, Anthropic web_search) runs INSIDE the provider call, so it never
becomes a ToolCallUsage and ``chat.request.tool_calls_count`` reads 0 — a
grounded answer looked like "answered from memory". This module is the ONE
reader that turns each provider's own trace into a single shape that the
persisted request carries in ``metadata.builtin_tool_use``:

    {"web_search": {"count": n, "queries": [...], "sources_cited": n},
     "url_context": {"count": n, "urls": [...]}}

Pure and best-effort: it never raises and returns None when nothing ran.
"""

from __future__ import annotations

from typing import Any

_MAX_ITEMS = 50


def _get(obj: Any, *names: str) -> Any:
    for name in names:
        if isinstance(obj, dict):
            if obj.get(name) is not None:
                return obj[name]
        else:
            value = getattr(obj, name, None)
            if value is not None:
                return value
    return None


def _strs(values: Any) -> list[str]:
    if not isinstance(values, (list, tuple)):
        return []
    return [str(v) for v in values if isinstance(v, str) and v]


def _blocks(response: Any) -> list[Any]:
    out: list[Any] = []
    for msg in getattr(response, "messages", None) or []:
        content = getattr(msg, "content", None)
        if isinstance(content, list):
            out.extend(content)
    return out


def collect_builtin_tool_use(response: Any) -> dict[str, Any] | None:
    """Return the built-in tool use recorded on ``response``, or None."""
    try:
        queries: list[str] = []
        search_count = 0
        sources = 0
        urls: list[str] = []
        url_count = 0

        for block in _blocks(response):
            btype = getattr(block, "type", None)
            meta = getattr(block, "metadata", None)
            meta = meta if isinstance(meta, dict) else {}

            # Gemini: grounding + url_context ride the text part's metadata.
            grounding = meta.get("grounding_metadata")
            if grounding is not None:
                gq = _strs(_get(grounding, "web_search_queries", "webSearchQueries"))
                queries.extend(gq)
                search_count += len(gq)
                chunks = _get(grounding, "grounding_chunks", "groundingChunks")
                if isinstance(chunks, (list, tuple)):
                    sources += len(chunks)
            url_meta = meta.get("url_context_metadata")
            if url_meta is not None:
                entries = _get(url_meta, "url_metadata", "urlMetadata") or []
                for entry in entries if isinstance(entries, (list, tuple)) else []:
                    url_count += 1
                    url = _get(entry, "retrieved_url", "retrievedUrl")
                    if isinstance(url, str) and url:
                        urls.append(url)

            # OpenAI Responses web_search_call.
            if btype == "web_search_call":
                search_count += 1
                action = getattr(block, "action", None)
                q = _get(action, "query") if action is not None else None
                if isinstance(q, str) and q:
                    queries.append(q)
                queries.extend(_strs(_get(action, "queries")) if action is not None else [])

            # Anthropic hosted server_tool_use blocks.
            if btype == "hosted_tool":
                raw = getattr(block, "block", None) or {}
                if raw.get("type") == "server_tool_use":
                    name = raw.get("name")
                    inp = raw.get("input") or {}
                    if name == "web_search":
                        search_count += 1
                        q = inp.get("query") if isinstance(inp, dict) else None
                        if isinstance(q, str) and q:
                            queries.append(q)
                    elif name in ("web_fetch", "url_context"):
                        url_count += 1
                        u = inp.get("url") if isinstance(inp, dict) else None
                        if isinstance(u, str) and u:
                            urls.append(u)

        result: dict[str, Any] = {}
        if search_count or queries:
            result["web_search"] = {
                "count": search_count,
                "queries": queries[:_MAX_ITEMS],
                "sources_cited": sources,
            }
        if url_count or urls:
            result["url_context"] = {"count": url_count, "urls": urls[:_MAX_ITEMS]}
        return result or None
    except Exception:
        return None


def merge_builtin_tool_use(parts: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Sum several per-call records (an iteration's retry attempts) into one."""
    merged: dict[str, Any] = {}
    for part in parts:
        for tool, rec in part.items():
            into = merged.setdefault(tool, {})
            for key, val in rec.items():
                if isinstance(val, list):
                    into[key] = (into.get(key, []) + val)[:_MAX_ITEMS]
                else:
                    into[key] = into.get(key, 0) + val
    return merged or None


#: What a person reads on the working block for each provider-side tool.
_BUILTIN_LABELS = {"web_search": "Searched the web", "url_context": "Read pages"}


#: The stored content-block type (and the assistant message's metadata key) that keeps a provider-side
#: tool's working card after a reload. DISPLAY ONLY: the DB-load funnel (``UnifiedMessage``
#: ``_reconstruct_stored_content`` / ``parse_content``) drops it, so it never reaches a provider.
PROVIDER_TOOL_ACTIVITY = "provider_tool_activity"


def builtin_tool_activity(builtin: dict[str, Any], *, call_key: str) -> list[dict[str, Any]]:
    """One record per provider-side tool: what the live frames say and what a reload draws (pure)."""
    records: list[dict[str, Any]] = []
    for tool, rec in builtin.items():
        if not isinstance(rec, dict):
            continue
        queries = _strs(rec.get("queries")) or _strs(rec.get("urls"))
        label = _BUILTIN_LABELS.get(tool, tool.replace("_", " ").capitalize())
        records.append({
            "call_id": f"builtin-{tool}-{call_key}",
            "name": f"provider_{tool}",
            "message": f"{label}: {', '.join(queries[:3])}" if queries else label,
            "arguments": {"queries": queries} if tool == "web_search" else {"urls": queries},
            "result": dict(rec),
        })
    return records


def builtin_tool_events(builtin: dict[str, Any], *, call_key: str) -> list[dict[str, Any]]:
    """The tool_started / tool_completed frames that put a provider-side tool on the working block.

    A built-in search runs inside the provider call, so no tool call event existed and the turn showed
    citations with no "Searched ..." card (feedback 017807f4). One started + completed pair per tool,
    under ``provider_<tool>`` (never our own ``web_search`` tool's name, whose card expects its result).
    Pure; the caller sends them.
    """
    frames: list[dict[str, Any]] = []
    for rec in builtin_tool_activity(builtin, call_key=call_key):
        base = {"call_id": rec["call_id"], "tool_name": rec["name"], "message": rec["message"], "show_spinner": False}
        frames.append({**base, "event": "tool_started", "data": {"arguments": rec["arguments"], "builtin": True}})
        frames.append({**base, "event": "tool_completed", "data": {"result": rec["result"], "builtin": True}})
    return frames


def provider_tool_activity_blocks(records: Any) -> list[dict[str, Any]]:
    """The stored content blocks for an assistant row's provider-side tool activity (pure)."""
    blocks: list[dict[str, Any]] = []
    for rec in records if isinstance(records, list) else []:
        if isinstance(rec, dict) and rec.get("call_id") and rec.get("name"):
            blocks.append({
                "type": PROVIDER_TOOL_ACTIVITY,
                "call_id": str(rec["call_id"]),
                "name": str(rec["name"]),
                "message": str(rec.get("message") or ""),
                "arguments": dict(rec.get("arguments") or {}),
                "result": dict(rec.get("result") or {}),
            })
    return blocks


def queue_provider_tool_activity_rows(
    blocks: list[dict[str, Any]],
    *,
    message_id: str,
    conversation_id: str,
    user_request_id: str | None,
    iteration: int,
    user_id: str | None,
) -> list[str]:
    """Queue one completed ``chat.tool_call`` per block, linked to the answer row, on the request's
    Coordinator (the same row shape every engine call stores). Never replayed: the rebuild consults
    tool_call rows only for role='tool' messages and tool_call blocks, and these have neither."""
    from datetime import UTC, datetime
    from uuid import uuid4

    from matrx_ai.persistence.queue_helpers import queue_tool_call_create
    from matrx_ai.tools.logger import build_tool_call_finished_fields, build_tool_call_started_row

    now = datetime.now(UTC)
    row_ids: list[str] = []
    for block in blocks:
        row_id = str(uuid4())
        row = build_tool_call_started_row(
            row_id=row_id,
            conversation_id=conversation_id,
            user_request_id=user_request_id,
            tool_name=block["name"],
            tool_type="provider",
            call_id=block["call_id"],
            arguments=block["arguments"],
            iteration=iteration,
            started_at=now,
            message_id=message_id,
            turn_actor_user_id=user_id,
            metadata={PROVIDER_TOOL_ACTIVITY: True},
        )
        row.update(build_tool_call_finished_fields(block["result"], is_error=False, completed_at=now, duration_ms=0))
        row.pop("id", None)
        row.pop("conversation_id", None)
        queue_tool_call_create(id=row_id, conversation_id=conversation_id, **row)
        row_ids.append(row_id)
    return row_ids


async def announce_builtin_tool_use(emitter: Any, builtin: dict[str, Any] | None, *, call_key: str) -> None:
    """Send the frames for one provider call. NEVER raises: the answer already exists; this narrates it."""
    if not builtin or emitter is None:
        return
    import logging

    for frame in builtin_tool_events(builtin, call_key=call_key):
        try:
            await emitter.send_tool_event(frame)
        except Exception:  # noqa: BLE001 - a display frame never fails the turn
            logging.getLogger(__name__).exception("could not stream the built-in tool frame %s", frame.get("call_id"))
            return
