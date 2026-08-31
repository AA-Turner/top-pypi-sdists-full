"""Map the SDK's finalized-span shape to ``kytte.ingest.v1.Span``.

Input shape: the ``dict`` produced by ``Span.to_dict()`` in
``aigie.tracing.types``.
"""

import json
from datetime import datetime
from typing import Any  # noqa: TID251 — buffer payload is dict[str, Any] by contract.

from google.protobuf.timestamp_pb2 import Timestamp

from aigie._status import normalize_status
from aigie.ingest._pb.kytte.ingest.v1 import ingest_pb2 as _ingest_pb2

# Generated stubs ship without .pyi; alias as Any to silence attr-defined at
# every pb.X reference.
pb: Any = _ingest_pb2


def _set_ts(field: Timestamp, value: str | datetime | None) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        # datetime.fromisoformat on Python 3.10 rejects a trailing 'Z'.
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    field.FromDatetime(value)
    return True


def _json_or_empty(value: Any) -> str:
    """JSON-encode a value; empty string == proto3 default == "field unset"."""
    if value is None:
        return ""
    if isinstance(value, str):
        # The proto *_json fields must contain valid JSON. Empty string is
        # proto3's default ("unset"). If the string already parses as JSON,
        # pass it through (don't double-encode); otherwise it's opaque text
        # (e.g. an LLM prompt/completion) — encode it as a JSON string so the
        # gateway's json.loads() accepts it instead of rejecting the span.
        if not value:
            return ""
        try:
            json.loads(value)
        except ValueError:
            return json.dumps(value)
        return value
    if isinstance(value, (dict, list)) and not value:
        return ""
    return json.dumps(value, default=str)


def _fill_error(error_pb: pb.KytteError, error: dict[str, Any]) -> None:
    error_pb.type = str(error.get("type") or "error")
    error_pb.message = str(error.get("message") or "")
    error_pb.severity = str(error.get("severity") or "medium")
    error_pb.is_transient = bool(error.get("is_transient", False))
    error_pb.source = str(error.get("source") or "framework")
    raw = error.get("raw")
    if raw is not None:
        error_pb.raw = raw if isinstance(raw, str) else json.dumps(raw, default=str)


def _pick(metadata: dict[str, Any], payload: dict[str, Any], key: str) -> Any:
    """Read an LLM field from metadata first, then the top-level payload.

    Always pops from metadata so the promoted key is not re-serialized into
    metadata_json. Integrations historically disagreed on where the
    prompt/completion split lives (metadata vs top level); the mapper checked
    only one place and silently dropped the split for the other. Accepting both
    makes placement irrelevant to correctness.
    """
    value = metadata.pop(key, None)
    return value if value is not None else payload.get(key)


def _fill_llm_fields(span: pb.Span, metadata: dict[str, Any], payload: dict[str, Any]) -> None:
    """Promote LLM observability fields to typed proto fields (metadata or top level)."""
    if (m := _pick(metadata, payload, "model")) is not None:
        span.model = str(m)
    if (mp := metadata.pop("model_parameters", None)) is not None:
        span.model_parameters_json = _json_or_empty(mp)
    if (tt := _pick(metadata, payload, "total_tokens")) is not None:
        span.total_tokens = int(tt)
    if (pt := _pick(metadata, payload, "prompt_tokens")) is not None:
        span.prompt_tokens = int(pt)
    if (ct := _pick(metadata, payload, "completion_tokens")) is not None:
        span.completion_tokens = int(ct)
    if (ic := _pick(metadata, payload, "input_cost")) is not None:
        span.input_cost = float(ic)
    if (oc := _pick(metadata, payload, "output_cost")) is not None:
        span.output_cost = float(oc)
    if (tc := _pick(metadata, payload, "total_cost")) is not None:
        span.total_cost = float(tc)


def _build_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a mutable metadata dict that absorbs top-level error strings.

    Span.to_dict() emits error info as three top-level strings; we
    merge them in so they survive. The full KytteError envelope (a dict
    under metadata["error"]) takes priority.
    """
    metadata = dict(payload.get("metadata") or {})
    for key in ("error", "error_message", "error_type"):
        if (v := payload.get(key)) is not None and key not in metadata:
            metadata[key] = v
    return metadata


def span_to_proto(payload: dict[str, Any]) -> pb.Span:  # noqa: C901, PLR0915
    """Map a ``Span.to_dict()`` payload to a proto ``Span``."""
    span = pb.Span(
        span_id=str(payload.get("id", "")),
        trace_id=str(payload.get("trace_id", "")),
        parent_id=str(payload.get("parent_id") or ""),
        name=str(payload.get("name", "")),
        type=str(payload.get("type", "")),
    )
    _set_ts(span.start_time, payload.get("start_time"))
    _set_ts(span.end_time, payload.get("end_time"))
    if duration_ns := payload.get("duration_ns"):
        span.duration_ns = int(duration_ns)
    if (input_v := payload.get("input")) is not None:
        span.input_json = _json_or_empty(input_v)
    if (output_v := payload.get("output")) is not None:
        span.output_json = _json_or_empty(output_v)
    # Normalized here rather than at the emitter: this is the last code the span
    # passes through before the wire, and the gateway drops an undeclared status.
    if status := normalize_status(payload.get("status")):
        span.status = str(status)
    if tags := payload.get("tags"):
        span.tags.extend(str(t) for t in tags)

    metadata = _build_metadata(payload)
    error_envelope = metadata.get("error")
    if isinstance(error_envelope, dict) and error_envelope:
        metadata.pop("error")
        _fill_error(span.error, error_envelope)
    elif isinstance(error_envelope, str) and error_envelope:
        # Legacy emitters (e.g. the Strands hooks) carry a bare string under
        # metadata["error"]. Coerce it into the KytteError envelope so the
        # Determine selector sees the failure and the gateway (which rejects
        # a non-dict metadata.error) accepts the span.
        metadata.pop("error")
        envelope: dict[str, Any] = {"message": error_envelope}
        if (et := metadata.pop("error_type", None)) is not None:
            envelope["type"] = str(et)
        if (em := metadata.pop("error_message", None)) is not None and not envelope["message"]:
            envelope["message"] = str(em)
        _fill_error(span.error, envelope)
    _fill_llm_fields(span, metadata, payload)
    if metadata:
        span.metadata_json = _json_or_empty(metadata)
    return span
