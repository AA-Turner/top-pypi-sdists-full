"""Directive, BlastRadiusGate, and DirectiveApplier (ADR 0001 §3.4).

Canonical home for the Directive dataclass.  reflex.py re-exports it for
backwards compatibility.
"""

from __future__ import annotations

import logging
import os
import secrets
import time
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Literal

import aigie.telemetry as _telemetry
from aigie.autonomous import adapters
from aigie.autonomous.adapters import ActionType, ApplyStatus, SpanContext
from aigie.autonomous.config import ConfigProvider
from aigie.autonomous.metrics import kytte_directives_applied_total
from aigie.autonomous.outcome import OutcomeReport, Status
from aigie.autonomous.reasons import (
    ADAPTER_RAISED,
    IN_STEP_ALREADY_HANDLED_INLINE,
    NO_ADAPTER,
    UNKNOWN_ACTION_TYPE,
    UNKNOWN_INTERVENTION_KIND,
)

logger = logging.getLogger(__name__)

tracer = _telemetry.get_tracer("aigie.autonomous")

# ---------------------------------------------------------------------------
# Tier ordering for ceiling comparison (lower = less blast radius)
# ---------------------------------------------------------------------------

_TIER_RANK: dict[str, int] = {
    "in_step": 1,
    "next_step": 2,
    "trajectory": 3,
}

# Maps max integer from config → tier name (ADR spec max values)
_MAX_INT_TO_TIER: dict[int, str] = {
    1: "in_step",
    2: "next_step",
    3: "trajectory",
}

# Maps ActionType → tier name
_ACTION_TIER: dict[ActionType, str] = {
    ActionType.IN_STEP_RETRY: "in_step",
    ActionType.IN_STEP_REWRITE_ARGS: "in_step",
    ActionType.NEXT_STEP_INJECT_MESSAGE: "next_step",
    ActionType.TRAJECTORY_REWRITE_OUTPUT: "trajectory",
    ActionType.TRAJECTORY_FORCE_FALLBACK: "trajectory",
    ActionType.TRAJECTORY_BREAK_LOOP: "trajectory",
}


# ---------------------------------------------------------------------------
# Helper — ULID-ish directive ID
# ---------------------------------------------------------------------------


def new_directive_id() -> str:
    """Return <ts_ms>_<8-byte-hex> identifier."""
    ms = int(time.time() * 1000)
    suffix = secrets.token_hex(8)
    return f"{ms}_{suffix}"


# ---------------------------------------------------------------------------
# Directive — canonical frozen dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Directive:
    """Locally synthesised or platform-pushed remediation directive.

    Source of truth for all downstream consumers (BlastRadiusGate, DirectiveApplier,
    OutcomeReport).  reflex.py re-exports this name for transitional compatibility.
    """

    directive_id: str
    rule_id: str  # empty for judge directives not yet tied to a rule
    remediation_plan_id: str  # empty when not tied to a plan
    plan_step_index: int  # -1 = not applicable
    trace_id: str
    span_id: str
    action_type: ActionType
    action_params: dict[str, Any]
    confidence: float
    expires_at_unix_ms: int
    source: Literal["reflex", "judge", "flow"]
    rule_cache_version: str
    context_url: str = ""
    # RemediationFlow linkage. Empty / -1 for directives not derived from
    # a flow (judge-pushed directives can carry this too).
    flow_id: str = ""
    step_index: int = -1
    total_steps: int = 0

    def is_expired(self, now_ms: int | None = None) -> bool:
        """Return True if the directive has passed its expiry timestamp."""
        ts = now_ms if now_ms is not None else int(time.time() * 1000)
        return ts >= self.expires_at_unix_ms


# ---------------------------------------------------------------------------
# PermitDecision + PermitResult
# ---------------------------------------------------------------------------


class PermitDecision(IntEnum):
    ALLOWED = 1
    DENIED = 2


@dataclass(frozen=True)
class PermitResult:
    decision: PermitDecision
    reason: str


# ---------------------------------------------------------------------------
# BlastRadiusGate
# ---------------------------------------------------------------------------


class BlastRadiusGate:
    """Enforces blast-radius policy before a directive reaches the applier."""

    def __init__(self, config_provider: ConfigProvider) -> None:
        self._cfg_provider = config_provider

    def permit(self, directive: Directive, framework: str | None) -> PermitResult:
        """Return ALLOWED or DENIED with a reason string."""
        cfg = self._cfg_provider.get().autonomous

        result = self._check_enabled(cfg)
        if result is not None:
            return result

        result = self._check_ceiling(directive, cfg)
        if result is not None:
            return result

        result = self._check_confidence(directive, cfg)
        if result is not None:
            return result

        result = self._check_trajectory_rule(directive)
        if result is not None:
            return result

        result = self._check_adapter(directive, framework)
        if result is not None:
            return result

        return PermitResult(decision=PermitDecision.ALLOWED, reason="ok")

    def _check_enabled(self, cfg: Any) -> PermitResult | None:
        """Deny if the env kill-switch is set or config.enabled is False."""
        if os.environ.get("AIGIE_AUTONOMOUS_DISABLE") == "1":
            return PermitResult(decision=PermitDecision.DENIED, reason="autonomous_disabled")
        if cfg is not None and not cfg.enabled:
            return PermitResult(decision=PermitDecision.DENIED, reason="autonomous_disabled")
        return None

    def _check_ceiling(self, directive: Directive, cfg: Any) -> PermitResult | None:
        """Deny if the action tier exceeds the configured blast-radius ceiling."""
        action_tier = _ACTION_TIER.get(directive.action_type, "trajectory")
        if cfg is None:
            return None
        max_int = cfg.blast_radius.max
        max_tier = _MAX_INT_TO_TIER.get(max_int, "trajectory")
        if _TIER_RANK[action_tier] > _TIER_RANK[max_tier]:
            return PermitResult(decision=PermitDecision.DENIED, reason="ceiling_exceeded")
        return None

    def _check_confidence(self, directive: Directive, cfg: Any) -> PermitResult | None:
        """Deny if confidence is below the tier-specific threshold."""
        if cfg is None:
            return None
        tier = _ACTION_TIER.get(directive.action_type, "trajectory")
        thresholds = cfg.blast_radius.thresholds
        if tier == "next_step":
            if directive.confidence < thresholds.next_step_min_confidence:
                return PermitResult(
                    decision=PermitDecision.DENIED, reason="confidence_below_threshold"
                )
        elif tier == "trajectory" and directive.confidence < thresholds.trajectory_min_confidence:
            return PermitResult(decision=PermitDecision.DENIED, reason="confidence_below_threshold")
        return None

    def _check_trajectory_rule(self, directive: Directive) -> PermitResult | None:
        """Deny trajectory directives that have no validated rule_id."""
        tier = _ACTION_TIER.get(directive.action_type, "trajectory")
        if tier != "trajectory":
            return None
        if not directive.rule_id:
            return PermitResult(
                decision=PermitDecision.DENIED, reason="trajectory_no_validated_rule"
            )
        # TODO: enrich with rule.prior_successes lookup
        return None

    def _check_adapter(self, directive: Directive, framework: str | None) -> PermitResult | None:
        """Deny if no adapter is available or action not in its capabilities."""
        if not framework:
            return PermitResult(decision=PermitDecision.DENIED, reason="no_framework_on_span")
        adapter = adapters.get(framework)
        if adapter is None:
            return PermitResult(
                decision=PermitDecision.DENIED,
                reason=NO_ADAPTER.format(framework=framework),
            )
        if directive.action_type not in adapter.capabilities():
            return PermitResult(
                decision=PermitDecision.DENIED, reason="unsupported_action_for_adapter"
            )
        return None


# ---------------------------------------------------------------------------
# DirectiveApplier
# ---------------------------------------------------------------------------


def _default_metrics_increment(result: str, source: str) -> None:
    kytte_directives_applied_total.labels(result=result, source=source).inc()


class DirectiveApplier:
    """Routes a permitted Directive to the correct handler and records the outcome."""

    def __init__(
        self,
        metrics_increment: Callable[[str, str], None] | None = None,
    ) -> None:
        self._metrics_increment = metrics_increment or _default_metrics_increment

    def apply(
        self,
        directive: Directive,
        framework: str | None,
        span_ctx: SpanContext | None,
    ) -> OutcomeReport:
        """Apply the directive and return an OutcomeReport."""
        with tracer.start_as_current_span("directive.apply") as span:
            span.set_attribute("directive_id", directive.directive_id)
            span.set_attribute("rule_id", directive.rule_id)
            action_type_name = (
                directive.action_type.name
                if hasattr(directive.action_type, "name")
                else str(directive.action_type)
            )
            span.set_attribute("action_type", action_type_name)
            span.set_attribute("source", directive.source)
            span.set_attribute("framework", framework or "")
            return self._apply_inner(directive, framework, span_ctx, span)

    def _apply_inner(
        self,
        directive: Directive,
        framework: str | None,
        span_ctx: SpanContext | None,
        span: Any,
    ) -> OutcomeReport:
        logger.debug(
            "Directive APPLY: id=%s rule=%s action=%s source=%s framework=%s",
            directive.directive_id,
            directive.rule_id,
            directive.action_type,
            directive.source,
            framework,
        )

        if directive.is_expired():
            self._record_metric(Status.EXPIRED, directive.source)
            span.set_attribute("applied", False)
            span.set_attribute("reason", "expired_before_apply")
            return self._build_report(directive, Status.EXPIRED, "expired_before_apply")

        report = self._handle_adapter_action(directive, framework, span_ctx)
        span.set_attribute("applied", report.status == Status.APPLIED)
        span.set_attribute("reason", report.reason)
        return report

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _handle_adapter_action(
        self,
        directive: Directive,
        framework: str | None,
        span_ctx: SpanContext | None,
    ) -> OutcomeReport:
        """Resolve the directive into an Intervention and delegate to its adapter.

        Async arrivals (pushed Judge directives, post-span reflex) reach this
        method.  Call-domain directives are normally enacted inline by
        ``dispatch.py``; if one reaches here, it means inline dispatch already
        ran and we record a distinct status so it isn't double-counted.
        """
        # Local import to avoid circular dependency at module load.
        from aigie.autonomous.interventions import (
            CallIntervention,
            WorkflowIntervention,
        )
        from aigie.autonomous.interventions import (
            resolve as resolve_intervention,
        )

        intervention = resolve_intervention(directive)
        if intervention is None:
            self._record_metric(Status.FAILED, directive.source)
            return self._build_report(
                directive,
                Status.FAILED,
                UNKNOWN_ACTION_TYPE.format(action_type=int(directive.action_type)),
            )

        adapter = adapters.get(framework) if framework else None
        if adapter is None:
            self._record_metric(Status.FAILED, directive.source)
            return self._build_report(
                directive,
                Status.FAILED,
                NO_ADAPTER.format(framework=framework or ""),
            )

        if isinstance(intervention, CallIntervention):
            # Inline dispatch (chain hook) is the authoritative path for
            # call-domain directives.  An async arrival here means inline
            # already handled it — record without double-applying.
            self._record_metric(Status.APPLIED, directive.source)
            return self._build_report(directive, Status.APPLIED, IN_STEP_ALREADY_HANDLED_INLINE)

        if not isinstance(intervention, WorkflowIntervention):
            self._record_metric(Status.FAILED, directive.source)
            return self._build_report(directive, Status.FAILED, UNKNOWN_INTERVENTION_KIND)

        try:
            apply_result = adapter.apply(intervention, span_ctx)
        except Exception as exc:
            self._record_metric(Status.FAILED, directive.source)
            return self._build_report(directive, Status.FAILED, ADAPTER_RAISED.format(exc=exc))

        status = Status.APPLIED if apply_result.status == ApplyStatus.APPLIED else Status.FAILED
        self._record_metric(status, directive.source)
        return self._build_report(directive, status, apply_result.reason)

    def _record_metric(self, status: Status, source: str) -> None:
        self._metrics_increment(status.name.lower(), source)

    def _build_report(
        self,
        directive: Directive,
        status: Status,
        reason: str,
    ) -> OutcomeReport:
        return OutcomeReport(
            directive_id=directive.directive_id,
            rule_id=directive.rule_id,
            remediation_plan_id=directive.remediation_plan_id,
            plan_step_index=directive.plan_step_index,
            status=status,
            next_span_ok=False,
            observed_at_unix_ms=int(time.time() * 1000),
            rule_cache_version=directive.rule_cache_version,
            reason=reason,
            trace_id=directive.trace_id,
            span_id=directive.span_id,
            flow_id=directive.flow_id,
            step_index=directive.step_index,
        )
