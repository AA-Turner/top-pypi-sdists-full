"""Proto <-> dataclass conversion seam — the ONLY module permitted to import _pb.

All wire format translations live here. Every other module works with frozen
dataclasses (Directive, OutcomeReport).

ADR §3.7 proto firewall: import-linter enforces this boundary.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from google.protobuf import timestamp_pb2

from aigie.autonomous.adapters import ActionType
from aigie.autonomous.control_plane._pb import (  # noqa: F401 (pb_grpc re-exported through codec to preserve the proto firewall)
    pb,
    pb_grpc,
)
from aigie.autonomous.directives import Directive, new_directive_id
from aigie.autonomous.outcome import OutcomeReport, Status

logger = logging.getLogger(__name__)

__all__ = [
    "CodecError",
    "RemediationContext",
    "proto_to_directive",
    "directive_to_proto",
    "proto_to_outcome",
    "outcome_to_proto",
    "proto_action_type_to_enum",
    "enum_to_proto_action_type",
    "proto_to_remediation_context",
    "parse_action_params",
    "build_action_proto",
    "pb",
    "pb_grpc",
]


# ---------------------------------------------------------------------------
# Error type
# ---------------------------------------------------------------------------


class CodecError(Exception):
    """Raised when a proto message cannot be decoded into an internal dataclass.

    Callers should catch CodecError and decide whether to skip or abort.
    Unknown enum values and missing required fields both raise this error.
    """


# ---------------------------------------------------------------------------
# RemediationContext dataclass (not in directives.py or outcome.py)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RemediationContext:
    """Rich context attached to a directive by the platform Judge tier."""

    directive_id: str
    evidence: tuple[str, ...]
    expected_outcome: str
    validation_hooks: tuple[str, ...]
    parent_directive_id: str
    applies_to_rules: tuple[str, ...]
    explanation_markdown: str


# ---------------------------------------------------------------------------
# ActionType helpers
# ---------------------------------------------------------------------------

# Map proto int values to our IntEnum
_PROTO_TO_ACTION_TYPE: dict[int, ActionType] = {
    1: ActionType.IN_STEP_RETRY,
    2: ActionType.IN_STEP_REWRITE_ARGS,
    3: ActionType.NEXT_STEP_INJECT_MESSAGE,
    4: ActionType.TRAJECTORY_REWRITE_OUTPUT,
    5: ActionType.TRAJECTORY_FORCE_FALLBACK,
    6: ActionType.TRAJECTORY_BREAK_LOOP,
}


def proto_action_type_to_enum(value: int) -> ActionType:
    """Map proto ActionType int to our ActionType IntEnum.

    Raises CodecError for unknown values (including ACTION_TYPE_UNSPECIFIED=0).
    """
    result = _PROTO_TO_ACTION_TYPE.get(value)
    if result is None:
        raise CodecError(f"Unknown proto ActionType value: {value!r}")
    return result


def enum_to_proto_action_type(value: ActionType) -> int:
    """Map our ActionType IntEnum to the proto int value."""
    return int(value)


# ---------------------------------------------------------------------------
# Action params helpers (oneof → dict and back)
# ---------------------------------------------------------------------------


def _extract_retry(a: Any) -> dict[str, Any]:
    p = a.in_step_retry
    return {"max_retries": p.max_retries, "backoff_ms": p.backoff_ms}


def _extract_rewrite_args(a: Any) -> dict[str, Any]:
    return {"args_overrides": dict(a.in_step_rewrite_args.args_overrides)}


def _extract_inject_msg(a: Any) -> dict[str, Any]:
    p = a.next_step_inject_message
    return {"role": p.role, "content": p.content}


def _extract_rewrite_output(a: Any) -> dict[str, Any]:
    return {"output": a.trajectory_rewrite_output.output}


def _extract_force_fallback(a: Any) -> dict[str, Any]:
    return {"model": a.trajectory_force_fallback.model}


def _extract_break_loop(a: Any) -> dict[str, Any]:
    return {"reason": a.trajectory_break_loop.reason}


_ONEOF_EXTRACTORS: dict[str, Any] = {
    "in_step_retry": _extract_retry,
    "in_step_rewrite_args": _extract_rewrite_args,
    "next_step_inject_message": _extract_inject_msg,
    "trajectory_rewrite_output": _extract_rewrite_output,
    "trajectory_force_fallback": _extract_force_fallback,
    "trajectory_break_loop": _extract_break_loop,
}


def parse_action_params(action: pb.Action) -> dict[str, Any]:  # type: ignore[name-defined]
    """Convert proto Action oneof to the params dict DirectiveApplier expects."""
    which = action.WhichOneof("params")
    if which is None:
        return {}
    extractor = _ONEOF_EXTRACTORS.get(which)
    if extractor is None:
        raise CodecError(f"Unknown Action oneof field: {which!r}")
    return extractor(action)


def build_action_proto(  # type: ignore[name-defined]
    action_type: ActionType, params: dict[str, Any]
) -> pb.Action:
    """Build a proto Action from our ActionType + params dict."""
    if action_type == ActionType.IN_STEP_RETRY:
        inner = pb.InStepRetry(
            max_retries=params.get("max_retries", 0),
            backoff_ms=params.get("backoff_ms", 0),
        )
        return pb.Action(in_step_retry=inner)
    if action_type == ActionType.IN_STEP_REWRITE_ARGS:
        inner = pb.InStepRewriteArgs(args_overrides=params.get("args_overrides", {}))
        return pb.Action(in_step_rewrite_args=inner)
    if action_type == ActionType.NEXT_STEP_INJECT_MESSAGE:
        inner = pb.NextStepInjectMessage(
            role=params.get("role", ""), content=params.get("content", "")
        )
        return pb.Action(next_step_inject_message=inner)
    if action_type == ActionType.TRAJECTORY_REWRITE_OUTPUT:
        inner = pb.TrajectoryRewriteOutput(output=params.get("output", ""))
        return pb.Action(trajectory_rewrite_output=inner)
    if action_type == ActionType.TRAJECTORY_FORCE_FALLBACK:
        inner = pb.TrajectoryForceFallback(model=params.get("model", ""))
        return pb.Action(trajectory_force_fallback=inner)
    if action_type == ActionType.TRAJECTORY_BREAK_LOOP:
        inner = pb.TrajectoryBreakLoop(reason=params.get("reason", ""))
        return pb.Action(trajectory_break_loop=inner)
    raise CodecError(f"Cannot build Action proto for action_type: {action_type!r}")


# ---------------------------------------------------------------------------
# Source field helpers
# ---------------------------------------------------------------------------

_PROTO_SOURCE_TO_STR: dict[int, str] = {
    0: "reflex",  # SOURCE_UNSPECIFIED → default to reflex
    1: "reflex",
    2: "judge",
}

_STR_TO_PROTO_SOURCE: dict[str, int] = {
    "reflex": 1,
    "judge": 2,
}


def _source_from_proto(value: int) -> str:
    result = _PROTO_SOURCE_TO_STR.get(value)
    if result is None:
        raise CodecError(f"Unknown RemediationDirective.Source value: {value!r}")
    return result


def _source_to_proto(source: str) -> int:
    result = _STR_TO_PROTO_SOURCE.get(source)
    if result is None:
        raise CodecError(f"Unknown source string: {source!r}")
    return result


# ---------------------------------------------------------------------------
# Timestamp helpers
# ---------------------------------------------------------------------------


def _ts_to_unix_ms(ts: timestamp_pb2.Timestamp) -> int:
    """Convert proto Timestamp → int Unix milliseconds."""
    return ts.seconds * 1000 + ts.nanos // 1_000_000


def _unix_ms_to_ts(unix_ms: int) -> timestamp_pb2.Timestamp:
    """Convert int Unix milliseconds → proto Timestamp."""
    seconds = unix_ms // 1000
    nanos = (unix_ms % 1000) * 1_000_000
    return timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)


# ---------------------------------------------------------------------------
# Outcome Status helpers
# ---------------------------------------------------------------------------

_PROTO_STATUS_TO_ENUM: dict[int, Status] = {
    1: Status.APPLIED,
    2: Status.FAILED,
    3: Status.REVERTED,
    4: Status.EXPIRED,
}

_STATUS_TO_PROTO: dict[Status, int] = {v: k for k, v in _PROTO_STATUS_TO_ENUM.items()}


def _status_from_proto(value: int) -> Status:
    result = _PROTO_STATUS_TO_ENUM.get(value)
    if result is None:
        raise CodecError(f"Unknown OutcomeReport.Status proto value: {value!r}")
    return result


# ---------------------------------------------------------------------------
# RemediationDirective
# ---------------------------------------------------------------------------


def proto_to_directive(  # type: ignore[name-defined]
    msg: pb.RemediationDirective,
) -> Directive:
    """Convert a proto RemediationDirective to our Directive dataclass.

    Raises CodecError on schema mismatch (unknown enum, missing required field).
    """
    action_type = proto_action_type_to_enum(msg.action)
    action_params = parse_action_params(msg.payload)
    source = _source_from_proto(msg.source)
    return Directive(
        directive_id=msg.directive_id or new_directive_id(),
        rule_id=msg.rule_id,
        remediation_plan_id=msg.remediation_plan_id,
        plan_step_index=msg.plan_step_index,
        trace_id=msg.trace_id,
        span_id=msg.span_id,
        action_type=action_type,
        action_params=action_params,
        confidence=msg.confidence,
        expires_at_unix_ms=msg.expires_at_unix_ms,
        source=source,  # type: ignore[arg-type]
        rule_cache_version="",  # not on wire; set by client after decode
        context_url=msg.context_url,
        flow_id=msg.flow_id,
        step_index=msg.step_index,
        total_steps=msg.total_steps,
    )


def directive_to_proto(d: Directive) -> pb.RemediationDirective:  # type: ignore[name-defined]
    """Convert our Directive to a proto RemediationDirective (used in stub tests)."""
    action_proto = build_action_proto(d.action_type, d.action_params)
    source_int = _source_to_proto(d.source)
    return pb.RemediationDirective(
        directive_id=d.directive_id,
        rule_id=d.rule_id,
        remediation_plan_id=d.remediation_plan_id,
        plan_step_index=d.plan_step_index,
        trace_id=d.trace_id,
        span_id=d.span_id,
        action=int(d.action_type),
        payload=action_proto,
        confidence=d.confidence,
        expires_at_unix_ms=d.expires_at_unix_ms,
        source=source_int,
        context_url=d.context_url,
        flow_id=d.flow_id,
        step_index=d.step_index,
        total_steps=d.total_steps,
    )


# ---------------------------------------------------------------------------
# OutcomeReport
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Span-context encoding in `reason` (v1 proto compatibility shim)
#
# The v1 proto OutcomeReport does not have trace_id / span_id fields. To let
# the platform side join an outcome to the span it concerns, we encode them
# as a JSON prefix on `reason`:
#
#   {"trace_id":"...","span_id":"..."}|<original-reason>
#
# Decoding is best-effort: outcomes without the prefix retain their reason
# verbatim and get empty trace_id / span_id.
# ---------------------------------------------------------------------------

import json as _json

_SPAN_PREFIX_SEP = "|"


def _encode_reason(trace_id: str, span_id: str, reason: str) -> str:
    if not trace_id and not span_id:
        return reason
    header = _json.dumps(
        {"trace_id": trace_id or "", "span_id": span_id or ""}, separators=(",", ":")
    )
    return f"{header}{_SPAN_PREFIX_SEP}{reason}"


def _decode_reason(raw: str) -> tuple[str, str, str]:
    """Return (trace_id, span_id, reason). Best-effort; never raises."""
    if not raw or not raw.startswith("{"):
        return "", "", raw
    sep_idx = raw.find(_SPAN_PREFIX_SEP)
    if sep_idx <= 0:
        return "", "", raw
    header = raw[:sep_idx]
    rest = raw[sep_idx + 1 :]
    try:
        parsed = _json.loads(header)
    except Exception:  # noqa: BLE001
        return "", "", raw
    if not isinstance(parsed, dict):
        return "", "", raw
    return str(parsed.get("trace_id") or ""), str(parsed.get("span_id") or ""), rest


def proto_to_outcome(msg: pb.OutcomeReport) -> OutcomeReport:  # type: ignore[name-defined]
    """Convert a proto OutcomeReport to our OutcomeReport dataclass."""
    status = _status_from_proto(msg.status)
    observed_ms = _ts_to_unix_ms(msg.observed_at)
    trace_id, span_id, reason = _decode_reason(msg.reason)
    return OutcomeReport(
        directive_id=msg.directive_id,
        rule_id=msg.rule_id,
        remediation_plan_id=msg.remediation_plan_id,
        plan_step_index=msg.plan_step_index,
        status=status,
        next_span_ok=msg.next_span_ok,
        observed_at_unix_ms=observed_ms,
        rule_cache_version=msg.rule_cache_version,
        reason=reason,
        trace_id=trace_id,
        span_id=span_id,
        flow_id=msg.flow_id,
        step_index=msg.step_index,
    )


def outcome_to_proto(o: OutcomeReport) -> pb.OutcomeReport:  # type: ignore[name-defined]
    """Convert our OutcomeReport to a proto OutcomeReport (hot send path).

    trace_id / span_id are encoded as a JSON prefix on `reason` because the
    v1 proto schema does not carry them as first-class fields. The platform
    ingest path decodes the prefix back into structured columns.
    """
    proto_status = _STATUS_TO_PROTO.get(o.status, 2)  # default FAILED
    ts = _unix_ms_to_ts(o.observed_at_unix_ms)
    encoded_reason = _encode_reason(o.trace_id, o.span_id, o.reason)
    return pb.OutcomeReport(
        directive_id=o.directive_id,
        rule_id=o.rule_id,
        remediation_plan_id=o.remediation_plan_id,
        plan_step_index=o.plan_step_index,
        status=proto_status,
        next_span_ok=o.next_span_ok,
        observed_at=ts,
        rule_cache_version=o.rule_cache_version,
        reason=encoded_reason,
        flow_id=o.flow_id,
        step_index=o.step_index,
    )


# ---------------------------------------------------------------------------
# RemediationContext
# ---------------------------------------------------------------------------


def proto_to_remediation_context(  # type: ignore[name-defined]
    msg: pb.RemediationContext,
) -> RemediationContext:
    """Convert a proto RemediationContext to our RemediationContext dataclass."""
    return RemediationContext(
        directive_id=msg.directive_id,
        evidence=tuple(msg.evidence),
        expected_outcome=msg.expected_outcome,
        validation_hooks=tuple(msg.validation_hooks),
        parent_directive_id=msg.parent_directive_id,
        applies_to_rules=tuple(msg.applies_to_rules),
        explanation_markdown=msg.explanation_markdown,
    )
