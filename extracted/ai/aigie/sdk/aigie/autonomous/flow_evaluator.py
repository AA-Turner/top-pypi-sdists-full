"""SDK port of the platform's flow-conditions DSL.

This module is intentionally narrow for Task 4 of the autonomous-v2 SDK
rewrite: it ports ``RemediationFlowExecutor.matches_conditions`` (see
``backend/src/monitor/remediation/flow_executor.py:60``) into the SDK and
provides the adapters needed to drive it from an OTel-derived ``SpanView``.

The full :class:`FlowEvaluator` (selector filtering, best-match selection,
pending-step lookup, directive synthesis) lands in a later task; what's
here is the predicate the evaluator will sit on top of.

Unsupported-key handling
------------------------
If a flow's ``conditions`` dict carries a key the SDK doesn't understand,
the flow is treated as **non-evaluable** and skipped. A single WARN is
emitted per ``flow.id`` to avoid log spam when the same misconfigured row
is matched against every error. The decision (vs. silently ignoring the
key) is deliberate: an unknown key likely means the platform shipped a
DSL extension the SDK hasn't been updated for, and matching anyway risks
firing a step for an error the author never intended.
"""

from __future__ import annotations

import contextlib
import logging
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import aigie.telemetry as _telemetry
from aigie.autonomous.actions import resolve_step
from aigie.autonomous.directives import Directive, new_directive_id
from aigie.autonomous.flows import Flow, FlowCache

logger = logging.getLogger(__name__)

tracer = _telemetry.get_tracer("aigie.autonomous")

# Pending-step lookup: given (flow_id, trace_id) return the next step index
# this trace should execute (defaults to 0 for a never-applied flow).
# The actual runtime tracker (TTL/eviction, increment on FAILED) is wired
# in a later task; FlowEvaluator only consumes the lookup interface here.
PendingStepLookup = Callable[[str, str], int]


def _zero_pending(_flow_id: str, _trace_id: str) -> int:
    return 0


# Directive TTL — how long a synthesised directive remains valid before the
# applier should treat it as expired.
_DIRECTIVE_TTL_MS = 60_000

# ---------------------------------------------------------------------------
# DSL key set — mirrors the keys handled in matches_conditions on platform.
# Keep this in lockstep with backend/src/monitor/remediation/flow_executor.py.
# ---------------------------------------------------------------------------

SUPPORTED_CONDITION_KEYS: frozenset[str] = frozenset(
    {
        "error_type",
        "error_types",
        "span_type",
        "tool_name",
        "error_message_contains",
        "error_message_contains_any",
        "excludes_error_message",
        "model_name",
    }
)

# flow_ids we've already warned about for unsupported keys — bounded to
# avoid unbounded growth in pathological deployments.
_WARNED_FLOW_IDS: set[str] = set()
_WARNED_FLOW_IDS_CAP = 1024


def _warn_once_unsupported(flow_id: str, unknown_keys: set[str]) -> None:
    if flow_id in _WARNED_FLOW_IDS:
        return
    if len(_WARNED_FLOW_IDS) >= _WARNED_FLOW_IDS_CAP:
        # Stop warning so the set can't grow unbounded; the operator already
        # has a sample of the misconfigured flows in their logs.
        return
    _WARNED_FLOW_IDS.add(flow_id)
    logger.warning(
        "flow %s has unsupported condition keys %s; treating flow as non-evaluable",
        flow_id,
        sorted(unknown_keys),
    )


def reset_warning_state() -> None:
    """Test hook: clear the warn-once memo."""
    _WARNED_FLOW_IDS.clear()


# ---------------------------------------------------------------------------
# SpanView — OTel normaliser
# ---------------------------------------------------------------------------

# OTel semconv keys used by the Aigie autonomous pipeline.
_KEY_WORKFLOW_ID = "agent.workflow.id"
_KEY_CUSTOMER_ID = "agent.customer.id"
_KEY_USE_CASE = "agent.use_case"
_KEY_FRAMEWORK = "agent.framework"
_KEY_STATUS_CODE = "agent.status_code"
_KEY_ERROR_CLASS = "agent.error.class"
_KEY_DRIFT_SIGNATURE = "agent.drift.signature"
_KEY_TOOL_NAME = "agent.tool.name"
_KEY_MESSAGE_ROLE = "agent.message.role"
_KEY_STEP_KIND = "agent.step.kind"


@dataclass(frozen=True, slots=True)
class SpanView:
    """Read-only normaliser over an OTel-shaped span."""

    workflow_id: str | None
    customer_id: str | None
    use_case: str | None
    framework: str | None
    status_code: int | None
    error_class: str | None
    drift_signature: str | None
    tool_name: str | None
    message_role: str | None
    step_kind: str | None
    raw_attrs: dict[str, Any]

    @classmethod
    def from_otel_span(cls, span: Any) -> SpanView:
        """Build a SpanView from a duck-typed OTel-ish span.

        The span must expose a ``.attributes`` mapping. Missing keys return None.
        """
        attrs: Any = {}
        with contextlib.suppress(Exception):
            attrs = span.attributes or {}

        def _get(key: str) -> Any:
            with contextlib.suppress(Exception):
                return attrs.get(key)
            return None

        raw = dict(attrs) if attrs else {}

        status_raw = _get(_KEY_STATUS_CODE)
        status_code: int | None = None
        if status_raw is not None:
            with contextlib.suppress(TypeError, ValueError):
                status_code = int(status_raw)

        return cls(
            workflow_id=_get(_KEY_WORKFLOW_ID),
            customer_id=_get(_KEY_CUSTOMER_ID),
            use_case=_get(_KEY_USE_CASE),
            framework=_get(_KEY_FRAMEWORK),
            status_code=status_code,
            error_class=_get(_KEY_ERROR_CLASS),
            drift_signature=_get(_KEY_DRIFT_SIGNATURE),
            tool_name=_get(_KEY_TOOL_NAME),
            message_role=_get(_KEY_MESSAGE_ROLE),
            step_kind=_get(_KEY_STEP_KIND),
            raw_attrs=raw,
        )


# ---------------------------------------------------------------------------
# Condition matching — Python port of matches_conditions()
# ---------------------------------------------------------------------------


def _lower(v: Any) -> str:
    if v is None:
        return ""
    return str(v).lower()


def _match_error_type(conditions: dict[str, Any], error: dict[str, Any]) -> bool:
    if "error_type" not in conditions:
        return True
    return _lower(error.get("error_type")) == _lower(conditions.get("error_type"))


def _match_error_types(conditions: dict[str, Any], error: dict[str, Any]) -> bool:
    if "error_types" not in conditions:
        return True
    allowed = [_lower(t) for t in (conditions.get("error_types") or [])]
    return _lower(error.get("error_type")) in allowed


def _match_span_type(conditions: dict[str, Any], error: dict[str, Any]) -> bool:
    if "span_type" not in conditions:
        return True
    return _lower(error.get("span_type")) == _lower(conditions.get("span_type"))


def _match_tool_name(conditions: dict[str, Any], error: dict[str, Any]) -> bool:
    if "tool_name" not in conditions:
        return True
    return _lower(error.get("tool_name")) == _lower(conditions.get("tool_name"))


def _error_message(error: dict[str, Any]) -> str:
    return _lower(error.get("error_message") or error.get("message"))


def _match_message_contains(conditions: dict[str, Any], error: dict[str, Any]) -> bool:
    if "error_message_contains" not in conditions:
        return True
    pattern = _lower(conditions.get("error_message_contains"))
    if not pattern:
        return True
    return pattern in _error_message(error)


def _match_message_contains_any(conditions: dict[str, Any], error: dict[str, Any]) -> bool:
    if "error_message_contains_any" not in conditions:
        return True
    patterns = [_lower(p) for p in (conditions.get("error_message_contains_any") or [])]
    if not patterns:
        return True
    msg = _error_message(error)
    return any(p in msg for p in patterns if p)


def _match_excludes_message(conditions: dict[str, Any], error: dict[str, Any]) -> bool:
    if "excludes_error_message" not in conditions:
        return True
    excludes = conditions.get("excludes_error_message") or []
    if isinstance(excludes, str):
        excludes = [excludes]
    msg = _error_message(error)
    return all(not (p and _lower(p) in msg) for p in excludes)


def _match_model_name(conditions: dict[str, Any], error: dict[str, Any]) -> bool:
    if "model_name" not in conditions:
        return True
    return _lower(error.get("model_name")) == _lower(conditions.get("model_name"))


_MATCHERS = (
    _match_error_type,
    _match_error_types,
    _match_span_type,
    _match_tool_name,
    _match_message_contains,
    _match_message_contains_any,
    _match_excludes_message,
    _match_model_name,
)


def matches_conditions(flow: Flow, error: dict[str, Any]) -> bool:
    """Return True iff *error* satisfies every key in *flow*'s conditions.

    Mirrors ``RemediationFlowExecutor.matches_conditions`` exactly:
      * all keys are AND'd
      * string comparisons are case-insensitive
      * an unrecognised key makes the flow non-evaluable (returns False
        and logs once per flow_id)
    """
    conditions = flow.conditions or {}
    unknown = set(conditions.keys()) - SUPPORTED_CONDITION_KEYS
    if unknown:
        _warn_once_unsupported(flow.id, unknown)
        return False
    return all(m(conditions, error) for m in _MATCHERS)


# ---------------------------------------------------------------------------
# SpanView → error-dict adapter
# ---------------------------------------------------------------------------

# OTel attribute keys read off SpanView.raw_attrs. Kept off the typed
# SpanView fields so the DSL vocabulary doesn't bleed into the normaliser.
_RAW_ATTR_ERROR_MESSAGE = "agent.error.message"
_RAW_ATTR_MODEL_NAME = "agent.model"
_RAW_ATTR_MODEL_NAME_ALT = "agent.llm.model"


def _raw(sv: Any, key: str) -> Any:
    raw = getattr(sv, "raw_attrs", None)
    if not isinstance(raw, dict):
        return None
    return raw.get(key)


def span_view_to_error_dict(sv: Any) -> dict[str, Any]:
    """Adapt a SpanView to the error-dict shape the DSL matchers consume.

    Mapping (explicit, intentionally simple):
      error_type     ← sv.error_class
      error_message  ← sv.raw_attrs["agent.error.message"]   (if present)
      span_type      ← sv.step_kind
      tool_name      ← sv.tool_name
      model_name     ← sv.raw_attrs["agent.model"] or "agent.llm.model"

    Unknown fields are simply omitted. Callers can also overlay additional
    keys on the returned dict (e.g. a framework adapter that already has a
    richer error payload).
    """
    model = _raw(sv, _RAW_ATTR_MODEL_NAME) or _raw(sv, _RAW_ATTR_MODEL_NAME_ALT)
    out: dict[str, Any] = {
        "error_type": getattr(sv, "error_class", None),
        "error_message": _raw(sv, _RAW_ATTR_ERROR_MESSAGE),
        "span_type": getattr(sv, "step_kind", None),
        "tool_name": getattr(sv, "tool_name", None),
        "model_name": model,
    }
    return {k: v for k, v in out.items() if v is not None}


# ---------------------------------------------------------------------------
# Selector filtering — read from flow.metadata.selector (see flows.py)
# ---------------------------------------------------------------------------


def _selector_matches(flow: Flow, sv: Any) -> bool:
    """True iff every non-None selector dimension equals the span_view field.

    A flow with no selector (or all-wildcard selector) matches any traffic.
    Matches case-insensitively, like the DSL itself, so authoring tools that
    normalise to lowercase don't fight runtime payloads.
    """
    sel = flow.selector
    for sel_val, sv_attr in (
        (sel.customer_id, "customer_id"),
        (sel.workflow_id, "workflow_id"),
        (sel.use_case, "use_case"),
    ):
        if sel_val is not None and _lower(getattr(sv, sv_attr, None)) != _lower(sel_val):
            return False
    return True


# ---------------------------------------------------------------------------
# FlowEvaluator
# ---------------------------------------------------------------------------


def _best_match(snap: tuple[Flow, ...], span_view: Any) -> Flow | None:
    """Return the highest-priority matching flow from *snap*, or None.

    Ordering: highest success_rate first, then most applications, then a
    stable id sort for deterministic tie-breaking.
    """
    if not snap:
        return None
    error = span_view_to_error_dict(span_view)
    candidates = [
        f for f in snap if _selector_matches(f, span_view) and matches_conditions(f, error)
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda f: (-f.success_rate, -f.application_count, f.id))
    return candidates[0]


class FlowEvaluator:
    """Picks the best matching flow for an error and synthesises a Directive.

    Pipeline on each call:
      1. snapshot the FlowCache
      2. keep flows whose selector matches the SpanView's customer/workflow/use_case
      3. keep flows whose conditions DSL matches the error dict
      4. sort survivors by (success_rate desc, application_count desc, id asc)
      5. take the top flow, look up its pending step index for this trace
      6. starting at that index, find the first locally-supported step
         (skipping refresh_credentials/validate_output, which stay on the
         platform-side manual queue)
      7. synthesise a Directive carrying flow_id / step_index / total_steps

    No-match (no surviving flow, all steps unsupported, or pending index past
    the end) → returns ``None``. The caller (runtime.evaluate_inline →
    dispatch.dispatch) is responsible for turning that into
    ``PostCallResult.allow()`` — see Gap 9 in the autonomous-v2 plan.
    """

    def __init__(self, flow_cache: FlowCache) -> None:
        self._cache = flow_cache

    def evaluate(
        self,
        span_view: Any,
        pending_step_lookup: PendingStepLookup | None = None,
    ) -> Directive | None:
        with tracer.start_as_current_span("flow_evaluator.evaluate") as span:
            return self._evaluate_inner(span_view, pending_step_lookup, span)

    def _evaluate_inner(
        self,
        span_view: Any,
        pending_step_lookup: PendingStepLookup | None,
        span: Any,
    ) -> Directive | None:
        snap = self._cache.snapshot()
        span.set_attribute("flow_count", len(snap))
        span.set_attribute("framework", getattr(span_view, "framework", None) or "")
        flow = _best_match(snap, span_view)
        if flow is None:
            span.set_attribute("result", "miss")
            return None
        trace_id = str(_raw(span_view, "trace_id") or "")
        lookup = pending_step_lookup or _zero_pending
        start = max(0, lookup(flow.id, trace_id))
        directive = self._build_directive(flow, span_view, trace_id, start)
        span.set_attribute("matched_flow_id", flow.id)
        if directive is None:
            # Matched a flow but every remaining step was unsupported.
            span.set_attribute("result", "miss")
            return None
        span.set_attribute("result", "hit")
        span.set_attribute("step_index", directive.step_index)
        return directive

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------

    def _build_directive(
        self,
        flow: Flow,
        span_view: Any,
        trace_id: str,
        start: int,
    ) -> Directive | None:
        total = flow.total_steps
        if start >= total:
            return None
        for k in range(start, total):
            mapping = resolve_step(flow.steps[k])
            if mapping is None:
                # Unsupported action (e.g. refresh_credentials) — try the
                # next step in the same flow rather than failing outright.
                continue
            now_ms = int(time.time() * 1000)
            return Directive(
                directive_id=new_directive_id(),
                rule_id="",
                remediation_plan_id="",
                plan_step_index=-1,
                trace_id=trace_id,
                span_id=str(_raw(span_view, "span_id") or ""),
                action_type=mapping.action_type,
                action_params=mapping.params,
                confidence=1.0,
                expires_at_unix_ms=now_ms + _DIRECTIVE_TTL_MS,
                source="flow",
                rule_cache_version=self._cache.version,
                flow_id=flow.id,
                step_index=k,
                total_steps=total,
            )
        return None
