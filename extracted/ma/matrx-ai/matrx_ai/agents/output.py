"""Parse an agent's textual output into structured data.

A thin convenience wrapper over ``extract_json``.  Accepts whatever shape the
caller has — a raw JSON Schema, an OpenAI ``response_format`` envelope, an
agent DB record, or an ``Agent`` / ``AgentConfig`` instance — and resolves the
inner JSON Schema before delegating.

The whole point of this module is that callers never write their own JSON
parsing again.  Improvements to ``extract_json`` (repair, multi-block disambig,
provider-native structured output) propagate to every consumer automatically.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.agents.response_parser import JsonExtraction, extract_json

__all__ = ["parse_agent_output", "resolve_output_schema"]


def resolve_output_schema(source: Any) -> dict | None:
    """Pull a JSON Schema dict out of any reasonable input shape.

    Recognized shapes (checked in order):
      * Already a JSON Schema: ``{"type": ..., ...}``
      * OpenAI ``response_format`` outer: ``{"type": "json_schema", "json_schema": {...}}``
      * Agent DB record / OpenAI ``json_schema`` inner: has ``"schema"`` key
      * Agent record: has ``"output_schema"`` key
      * Object with ``output_schema`` attribute (Agent / AgentConfig)
      * Object with ``config.response_format`` attribute

    Returns ``None`` if no JSON Schema can be located.  Never raises.
    """
    if source is None:
        return None

    try:
        if isinstance(source, dict):
            if "type" in source and (
                isinstance(source.get("properties"), dict)
                or isinstance(source.get("items"), dict)
                or "required" in source
            ):
                return source
            if "json_schema" in source and isinstance(source["json_schema"], dict):
                return resolve_output_schema(source["json_schema"])
            if "schema" in source and isinstance(source["schema"], dict):
                return resolve_output_schema(source["schema"])
            if "output_schema" in source:
                return resolve_output_schema(source["output_schema"])
            if "type" in source:
                return source
            return None

        for attr in ("output_schema",):
            value = getattr(source, attr, None)
            if value is not None:
                resolved = resolve_output_schema(value)
                if resolved is not None:
                    return resolved

        config = getattr(source, "config", None)
        if config is not None:
            rf = getattr(config, "response_format", None)
            if rf is not None:
                resolved = resolve_output_schema(rf)
                if resolved is not None:
                    return resolved

        rf = getattr(source, "response_format", None)
        if rf is not None:
            return resolve_output_schema(rf)
    except Exception:
        return None

    return None


def parse_agent_output(
    text: str,
    source: Any = None,
    *,
    return_all: bool = False,
    nth: int | None = None,
) -> JsonExtraction:
    """Parse an agent's response text into structured JSON.

    Args:
        text:       The agent's raw output (``agent_result.output``).
        source:     Optional — anything ``resolve_output_schema`` can interpret.
                    When provided, the matching candidate is selected and
                    normalized against the schema.
        return_all: Return every matching candidate in ``.data``.
        nth:        Return only the Nth matching candidate.

    Always returns a ``JsonExtraction`` — never raises, always has
    ``.success`` and ``.reason``.
    """
    schema = resolve_output_schema(source)
    return extract_json(
        text,
        schema=schema,
        return_all=return_all,
        nth=nth,
        detailed=True,
    )
