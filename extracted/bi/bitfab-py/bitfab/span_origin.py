from __future__ import annotations

from typing import Any, Literal

from bitfab.constants import __version__

SPAN_ORIGIN_NAME = "bitfab.sdk.python"
SPAN_ORIGIN_KEY = "span_origin"
SPAN_INSTRUMENTATIONS = (
    "span",
    "trace",
    "openai-agents",
    "langgraph",
    "claude-agent-sdk",
    "vercel-ai",
)
SpanInstrumentation = Literal[
    "span", "trace", "openai-agents", "langgraph", "claude-agent-sdk", "vercel-ai"
]
FRAMEWORK_INSTRUMENTATIONS = frozenset(
    {"openai-agents", "langgraph", "claude-agent-sdk", "vercel-ai"}
)


def make_span_origin(instrumentation: SpanInstrumentation) -> dict[str, Any]:
    return {
        "name": SPAN_ORIGIN_NAME,
        "version": __version__,
        "instrumentation": {"name": instrumentation},
    }


def span_origin_of(payload: dict[str, Any]) -> dict[str, Any] | None:
    raw_span = payload.get("rawSpan")
    if not isinstance(raw_span, dict):
        return None
    origin = raw_span.get(SPAN_ORIGIN_KEY)
    if not isinstance(origin, dict):
        return None
    instrumentation = origin.get("instrumentation")
    if not isinstance(instrumentation, dict):
        return None
    if (
        not isinstance(origin.get("name"), str)
        or not isinstance(origin.get("version"), str)
        or instrumentation.get("name") not in SPAN_INSTRUMENTATIONS
    ):
        return None
    return origin


def span_instrumentation_of(payload: dict[str, Any]) -> str | None:
    origin = span_origin_of(payload)
    return None if origin is None else origin["instrumentation"]["name"]


def recorded_by_framework(payload: dict[str, Any]) -> bool:
    return span_instrumentation_of(payload) in FRAMEWORK_INSTRUMENTATIONS
