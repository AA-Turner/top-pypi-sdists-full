"""Trace projection and validation in Python; no JavaScript runtime is needed."""

from __future__ import annotations

import math
from typing import Any

from .trace_schema import Snapshot, Trace

TRACE_PROJECTION_SHA256 = (
    "22c666c6ace47d74d3f7dc477e68b27547257b319ba4014a4a32fbf977baac72"
)
MAX_PAYLOAD_CHARS = 16 * 1024


def trace_output(trace: dict[str, Any]) -> str | None:
    return trace["event"]["aiData"].get("output")


def trace_tool_calls(
    trace: dict[str, Any], name: str | None = None
) -> list[dict[str, Any]]:
    return [
        entry
        for entry in trace["entries"]
        if entry["type"] == "tool_call" and (name is None or entry["name"] == name)
    ]


def _slice(value: str, length: int) -> str:
    # JavaScript bounds strings by UTF-16 code units, including astral characters.
    return value.encode("utf-16-le", "surrogatepass")[: length * 2].decode(
        "utf-16-le", "surrogatepass"
    )


def _payload(raw: str | None) -> dict[str, Any]:
    size = (
        len(raw.encode("utf-16-le", "surrogatepass")) // 2 if raw is not None else None
    )
    return {
        "kind": "text" if raw else "empty",
        "raw": _slice(raw, MAX_PAYLOAD_CHARS) if raw is not None else None,
        "truncated": size is not None and size > MAX_PAYLOAD_CHARS,
        "sizeChars": size,
    }


def _milliseconds(value: int | float | str | None) -> int:
    if isinstance(value, (int, float)):
        return math.floor(value / 1000000 + 0.5)
    numerator = int(value or 0) + 500000
    return (1 if numerator >= 0 else -1) * (abs(numerator) // 1000000)


def project_workshop_trace(value: dict[str, Any]) -> dict[str, Any]:
    """Compatibility name for the shared pure trace projection; uses no Workshop service."""
    entries = []
    for index, span in enumerate(
        sorted(
            value["spans"],
            key=lambda s: (
                int(s["start_unix_ns"])
                if isinstance(s.get("start_unix_ns"), str)
                else s.get("start_unix_ns") or 0
            ),
        )
    ):
        span_id = span.get("span_id")
        kind = span.get("span_type") or "INTERNAL"
        entry = {
            "id": span_id or f"raw-step-{index}",
            "order": index,
            "startMs": None,
            "endMs": None,
            "source": {
                "adapter": "raw_spans",
                "confidence": "medium",
                "spanIds": [span_id] if span_id else [],
                "parentSpanIds": [],
                "attributeKeys": [],
            },
        }
        if kind == "TOOL_CALL":
            output = span.get("output_payload")
            entry.update(
                type="tool_call",
                callId=None,
                name=span.get("span_name") or "unknown",
                status={"ERROR": "error", "OK": "completed"}.get(
                    span.get("status"), "unknown"
                ),
                durationMs=_milliseconds(span.get("duration_ns")),
                input=_payload(span.get("input_payload") or None),
                output=_payload(output) if output else None,
                error=_payload(_slice(output, 500))
                if output and span.get("status") == "ERROR"
                else None,
            )
        else:
            entry.update(
                type="unknown_span",
                spanType=kind,
                name=span.get("span_name") or "unknown",
                hiddenByDefault=True,
            )
        entries.append(entry)
    return validate_trace(
        {"origin": value["origin"], "event": value["event"], "entries": entries}
    )


def normalize_reference_snapshot(value: dict[str, Any]) -> dict[str, Any]:
    return Snapshot.model_validate(value).wire()


def validate_trace(value: dict[str, Any]) -> dict[str, Any]:
    return Trace.model_validate(value).wire()


class TraceTools:
    get_output = staticmethod(trace_output)
    get_tool_calls = staticmethod(trace_tool_calls)


trace_tools = TraceTools()
