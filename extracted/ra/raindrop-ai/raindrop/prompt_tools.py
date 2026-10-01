"""``ai.prompt.tools``: the tool list a model call was made with.

Raindrop records, on every model-call span, one JSON document per tool
(``{"type": "function", "name", "description", "inputSchema"}`` or
``{"type": "provider-defined", "id", "name", "args"}``) as an OTel string
array. An absent attribute means the SDK could not see the list; an empty
list means the model had no tools. Two sources feed it:

- implicit capture: the OpenLLMetry instrumentations write the request's
  tool list on model spans — ``gen_ai.tool.definitions`` (one JSON string,
  OpenLLMetry >= 0.54/0.55) or ``llm.request.functions.{i}.name`` /
  ``.description`` / ``.parameters`` (older releases) — rebuilt into the
  canonical shape at export;
- a manual override passed as ``tools=`` to ``begin()`` / ``prompt_tools()``,
  stamped on model spans started inside that scope.

A list a wrapper derives from a framework registry rather than the actual
request (an agent's tool catalog, which may overstate what one call received)
is marked with ``ai.prompt.tools.source`` (e.g. ``"agno.agent.tools"``) so
consumers can tell it from exact capture. Explicit overrides carry no source.

Both honour the ``TRACELOOP_TRACE_CONTENT`` content gate: with content
capture off, tool definitions are content too and are never recorded.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Mapping, Optional, Sequence, TypedDict

from opentelemetry import context as context_api

logger = logging.getLogger("raindrop.analytics")

PROMPT_TOOLS_ATTRIBUTE = "ai.prompt.tools"
PROMPT_TOOLS_SOURCE_ATTRIBUTE = "ai.prompt.tools.source"

# Any one of these on a span marks it as a model call. ``llm.request.type`` is
# set at span start by the OpenAI/Anthropic instrumentations; the model keys
# arrive later on instrumentations that populate the span after starting it.
# ``llm.model_name`` is the OpenInference marker (agno and the other
# openinference-instrumentation-* packages), also set after span start.
MODEL_SPAN_ATTRIBUTES = (
    "llm.request.type",
    "gen_ai.request.model",
    "llm.request.model",
    "llm.model_name",
)

FUNCTIONS_ATTRIBUTE_PREFIX = "llm.request.functions."

# ``GenAIAttributes.GEN_AI_TOOL_DEFINITIONS``: one JSON string holding the
# list of ``{"type", "name", "description", "parameters"}`` dicts. OpenLLMetry
# switched to it from ``llm.request.functions.*`` in 0.54.0 (anthropic) and
# 0.55.0 (openai, langchain).
TOOL_DEFINITIONS_ATTRIBUTE = "gen_ai.tool.definitions"


class ToolDefinition(TypedDict, total=False):
    """Canonical wire shape of one entry in ``ai.prompt.tools``."""

    type: str
    name: str
    description: str
    inputSchema: Mapping[str, object]
    id: str
    args: Mapping[str, object]


ToolsInput = Sequence[Mapping[str, object]]


def content_capture_enabled() -> bool:
    """Mirror of Traceloop's ``should_send_prompts`` content gate."""
    try:
        if (os.getenv("TRACELOOP_TRACE_CONTENT") or "true").lower() == "true":
            return True
        return bool(context_api.get_value("override_enable_content_tracing"))
    except Exception:
        return False


def is_model_span_attributes(attributes: Mapping[str, object] | None) -> bool:
    if not attributes:
        return False
    return any(key in attributes for key in MODEL_SPAN_ATTRIBUTES)


def _dumps(document: Mapping[str, object]) -> str:
    # Same bytes ``JSON.stringify`` produces for the JS SDKs: compact
    # separators, non-ASCII left as-is.
    return json.dumps(document, separators=(",", ":"), ensure_ascii=False)


_FUNCTION_KINDS = frozenset({"function", "dynamic", "custom"})


def _canonical_tool(tool: Mapping[str, object]) -> Optional[dict[str, object]]:
    """One tool in any accepted shape → canonical dict, or ``None`` to skip."""
    kind = tool.get("type")
    if kind == "provider-defined":
        name = tool.get("name")
        if not isinstance(name, str) or not name:
            return None
        result: dict[str, object] = {"type": "provider-defined"}
        identifier = tool.get("id")
        if isinstance(identifier, str):
            result["id"] = identifier
        result["name"] = name
        args = tool.get("args")
        if isinstance(args, Mapping):
            result["args"] = dict(args)
        return result

    # OpenAI: {"type": "function", "function": {"name", "description", "parameters"}}
    function = tool.get("function")
    if isinstance(function, Mapping):
        source: Mapping[str, object] = function
        schema = function.get("parameters")
    else:
        source = tool
        # Canonical carries ``inputSchema``; Anthropic carries ``input_schema``.
        schema = tool.get("inputSchema")
        if schema is None:
            schema = tool.get("input_schema")
        if schema is None:
            schema = tool.get("parameters")

    name = source.get("name")
    if function is None and isinstance(kind, str) and kind not in _FUNCTION_KINDS:
        # Provider-owned tools: OpenAI built-ins (``{"type": "web_search_preview"}``)
        # and Anthropic server tools (``{"type": "web_search_20250305", "name":
        # "web_search"}``) carry a type and no schema. Record them as
        # provider-defined rather than inventing a function declaration.
        if schema is None:
            label = name if isinstance(name, str) and name else kind
            return {"type": "provider-defined", "id": kind, "name": label}
    if not isinstance(name, str) or not name:
        return None
    result = {"type": "function", "name": name}
    description = source.get("description")
    if isinstance(description, str):
        result["description"] = description
    schema = _parse_schema(schema)
    if schema is not None:
        result["inputSchema"] = schema
    return result


def _parse_schema(schema: object) -> Optional[dict[str, object]]:
    """A JSON Schema given as a mapping or a JSON string; ``None`` otherwise."""
    if isinstance(schema, Mapping):
        return dict(schema)
    if isinstance(schema, str):
        try:
            parsed = json.loads(schema)
        except ValueError:
            return None
        if isinstance(parsed, dict):
            return parsed
    return None


def normalize_tools(tools: ToolsInput) -> tuple[str, ...]:
    """Normalise a caller-supplied tool list to canonical JSON strings.

    Accepts the canonical shape, OpenAI's ``{"type": "function", "function":
    {...}}`` and Anthropic's ``{"name", "description", "input_schema"}``.
    Entries that are not mappings or carry no name are skipped, never raised
    on: a malformed tool must not take the caller's request down.
    """
    result: list[str] = []
    for tool in tools:
        try:
            if not isinstance(tool, Mapping):
                continue
            canonical = _canonical_tool(tool)
            if canonical is None:
                continue
            result.append(_dumps(canonical))
        except Exception as exc:
            logger.debug("[raindrop] skipping unserialisable tool: %s", exc)
    return tuple(result)


def rebuild_from_functions(
    attributes: Mapping[str, object],
) -> Optional[tuple[str, ...]]:
    """Rebuild ``ai.prompt.tools`` from ``llm.request.functions.{i}.*``.

    Returns ``None`` when the span carries no such attributes (the SDK could
    not see the list). Tools come out in index order; entries without a name
    are skipped and a ``parameters`` value that is not valid JSON drops only
    that tool's ``inputSchema``.
    """
    by_index: dict[int, dict[str, object]] = {}
    for key, value in attributes.items():
        if not isinstance(key, str) or not key.startswith(FUNCTIONS_ATTRIBUTE_PREFIX):
            continue
        rest = key[len(FUNCTIONS_ATTRIBUTE_PREFIX) :]
        index_text, separator, field = rest.partition(".")
        if not separator or not index_text.isdigit():
            continue
        by_index.setdefault(int(index_text), {})[field] = value
    if not by_index:
        return None

    result: list[str] = []
    for index in sorted(by_index):
        fields = by_index[index]
        name = fields.get("name")
        if not isinstance(name, str) or not name:
            continue
        tool: dict[str, object] = {"type": "function", "name": name}
        description = fields.get("description")
        if isinstance(description, str):
            tool["description"] = description
        schema = _parse_schema(fields.get("parameters"))
        if schema is not None:
            tool["inputSchema"] = schema
        result.append(_dumps(tool))
    return tuple(result)


def rebuild_from_tool_definitions(
    attributes: Mapping[str, object],
) -> Optional[tuple[str, ...]]:
    """Rebuild ``ai.prompt.tools`` from ``gen_ai.tool.definitions``.

    The attribute is a JSON string (an already-parsed list is accepted too)
    of ``{"type", "name", "description", "parameters"}`` entries, kept in
    order with each ``parameters`` schema verbatim; OpenAI-wrapped
    ``{"type": "function", "function": {...}}`` and Anthropic ``input_schema``
    entries are normalised the same way. Returns ``None`` when the attribute
    is absent, is not valid JSON, is not a list, or names no tool at all:
    recording nothing beats recording a wrong list.
    """
    raw = attributes.get(TOOL_DEFINITIONS_ATTRIBUTE)
    if raw is None:
        return None
    if isinstance(raw, str):
        try:
            definitions: object = json.loads(raw)
        except ValueError:
            return None
    else:
        definitions = raw
    if isinstance(definitions, (str, bytes, Mapping)) or not isinstance(
        definitions, Sequence
    ):
        return None
    result: list[str] = []
    for entry in definitions:
        if not isinstance(entry, Mapping):
            continue
        canonical = _canonical_tool(entry)
        if canonical is not None:
            result.append(_dumps(canonical))
    if definitions and not result:
        return None
    return tuple(result)


def rebuild_implicit(
    attributes: Mapping[str, object],
) -> Optional[tuple[str, ...]]:
    """``ai.prompt.tools`` from whichever instrumentation attribute is present.

    ``llm.request.functions.*`` is consulted first, then
    ``gen_ai.tool.definitions``; ``None`` when neither yields a list.
    """
    tools = rebuild_from_functions(attributes)
    if tools is None:
        tools = rebuild_from_tool_definitions(attributes)
    return tools
