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
