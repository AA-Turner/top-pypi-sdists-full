"""Normalize and hash tool inventories for RegisterToolCatalog."""

from __future__ import annotations

import contextlib
import hashlib
import json
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aigie.client import Aigie


def _field(tool: Any, key: str) -> Any:
    """Read a key from either a dict or an object attribute."""
    if isinstance(tool, dict):
        return tool.get(key)
    return getattr(tool, key, None)


def _as_json_schema(schema: Any) -> dict[str, Any] | None:
    """Coerce a framework's schema carrier into a JSON-Schema dict."""
    if isinstance(schema, dict):
        return schema
    # LangChain/LangGraph expose input_schema as a pydantic model CLASS, so an
    # isinstance(dict) test silently drops every argument name — and a catalog
    # without arg names can't back a correct_tool_call arg_mapping.
    to_json_schema = getattr(schema, "model_json_schema", None)
    if callable(to_json_schema):
        with contextlib.suppress(Exception):
            produced = to_json_schema()
            if isinstance(produced, dict):
                return produced
    return None


def _normalize_one(tool: Any) -> dict[str, Any] | None:
    name = _field(tool, "name")
    if not name:
        return None
    schema = _as_json_schema(_field(tool, "input_schema"))
    if schema is None:
        schema = _as_json_schema(_field(tool, "parameters"))
    if schema is None:
        # LangChain's .args is already {arg: {type, title}} — the properties
        # block without the envelope, so rebuild the envelope around it.
        args = _field(tool, "args")
        if isinstance(args, dict) and args:
            schema = {"type": "object", "properties": args}
    return {
        "name": str(name),
        "description": str(_field(tool, "description") or ""),
        "input_schema": schema if isinstance(schema, dict) else {},
    }


def normalize_tools(tools: Iterable[Any] | None) -> list[dict[str, Any]]:
    """Return a sorted, deduped ``{name, description, input_schema}`` catalog."""
    if not tools:
        return []
    by_name: dict[str, dict[str, Any]] = {}
    for raw in tools:
        norm = _normalize_one(raw)
        if norm is not None and norm["name"] not in by_name:
            by_name[norm["name"]] = norm
    return [by_name[name] for name in sorted(by_name)]


def catalog_hash(catalog: list[dict[str, Any]]) -> str:
    """Return a stable SHA-256 digest for a normalized catalog."""
    canonical = json.dumps(catalog, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def find_tool(catalog: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    """Return the normalized catalog entry named ``name``, if present."""
    return next((tool for tool in catalog if tool.get("name") == name), None)


def required_args_for(tool: dict[str, Any]) -> tuple[str, ...]:
    """Return the ``input_schema.required`` arg names of a normalized catalog entry."""
    schema = tool.get("input_schema")
    required = schema.get("required") if isinstance(schema, dict) else None
    if not isinstance(required, list):
        return ()
    return tuple(str(name) for name in required)


def _active_aigie() -> Aigie | None:
    from aigie.client import get_aigie

    return get_aigie()


def register_catalog(tools: Iterable[Any] | None) -> str | None:
    """Register tools with the active Aigie client and return the catalog hash."""
    aigie = _active_aigie()
    if aigie is None:
        return None
    return aigie.register_tool_catalog(tools or [])


def bind_trace_hash(trace_id: str | None, tool_hash: str | None) -> None:
    """Bind a trace to its registered tool catalog hash on the active client."""
    if not trace_id or not tool_hash:
        return
    aigie = _active_aigie()
    if aigie is not None:
        aigie.bind_trace_tool_hash(trace_id, tool_hash)


def _span_tool_hash(span: Any) -> str | None:
    from aigie.decision.steps import span_metadata

    digest = span_metadata(span).get("tool_registry_hash")
    return digest if isinstance(digest, str) and digest else None


def catalog_for_span(span: Any, trace_id: str | None) -> list[dict[str, Any]] | None:
    """Resolve the run's retained tool catalog, if available."""
    aigie = _active_aigie()
    if aigie is None:
        return None
    digest = _span_tool_hash(span) or aigie.tool_hash_for_trace(trace_id)
    return aigie.tool_catalog_for_hash(digest)


def stamp_tool_registry_hash(
    tools: Iterable[Any] | None, metadata: dict[str, Any], trace_id: str | None = None
) -> str | None:
    """Register ``tools`` and stamp the resulting hash on metadata/trace state."""
    digest = register_catalog(tools)
    if digest:
        metadata["tool_registry_hash"] = digest
        bind_trace_hash(trace_id, digest)
    return digest
